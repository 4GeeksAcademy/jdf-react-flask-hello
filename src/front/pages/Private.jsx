import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

export const Private = () => {
  const [data, setData] = useState(null);
  const [message, setMessage] = useState('');
  const navigate = useNavigate();
  useEffect(() => {
    const fetchData = async () => {
      const token = localStorage.getItem('token');
      if (!token) {
        navigate('/login');
        return;
      }

      try {
        const response = await fetch('https://opulent-fiesta-pjwpjx767vw5296wj-3001.app.github.dev/api/private', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
          },
        });
        const data = await response.json();
        if (response.ok) {
          setData(data);
        } else {
          setMessage(data.msg || 'Error al acceder a la ruta protegida');
        }
      } catch (error) {
        setMessage('Error al conectar con el servidor');
      }
    };

    fetchData();
  }, [navigate]);

  return (
    <div>
      <h2>Página Privada</h2>
      {data && <p>{data.message}</p>}
      {message && <p>{message}</p>}
      {data && <p>{data.user.email}</p>}
    </div>
  );
};

