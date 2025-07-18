import React, { useEffect } from "react"
import rigoImageUrl from "../assets/img/rigo-baby.jpg";
import useGlobalReducer from "../hooks/useGlobalReducer.jsx";
import { Signup } from "./Signup.jsx";

export const Home = () => {

	

	return (
		<div className="text-center mt-5">
			<Signup/>
		</div>
	);
}; 