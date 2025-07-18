"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt
from sqlalchemy import select



api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)

bcrypt = Bcrypt()

@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200


@api.route("/user", methods=["GET"])
@jwt_required()
def get_user():
    current_user_id = int(get_jwt_identity())
    user = db.session.execute(select(User).where(User.id == current_user_id)).scalar_one_or_none()
    if user is None:
        return jsonify({"msg": "Usuario no encontrado"}), 404
    return jsonify({
        "id": user.id,
        "email": user.email
    }), 200



@api.route('/signup', methods=['POST'])
def handle_signup():
    data = request.get_json()
    email= data.get("email")
    password= data.get("password")

    if not email or not password:
        return jsonify({'msg':'el email o password son obligatorios'}),400

    if User.query.filter_by(email=email).first():
        return jsonify({'msg': 'el usuario ya existe'}), 409

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

    new_user = User(email=email, password=hashed_password, is_active=True)
    
   

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'msg':'nuevo usuario creado'}), 200



@api.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if 'email' not in data or 'password' not in data:
        return jsonify({'msg':'debes rellenar todos los campos'})
    
    user = User.query.filter_by(email=email).first()

    if user is None:
        return jsonify({"msg": "El usuario no existe"}), 401
    
    token = create_access_token(identity=str(user.id))

    return jsonify(token=token), 200


@api.route("/private", methods=['GET'])
@jwt_required()
def private():
    current_user_id = int(get_jwt_identity())

    user = db.session.execute(select(User).where(User.id == current_user_id)).scalar_one_or_none()

    if not user:
        return jsonify({"msg": "Usuario no encontrado"}), 404
    
    return jsonify({"message": "Acceso concedido", "user": {"id": user.id, "email": user.email}}), 200