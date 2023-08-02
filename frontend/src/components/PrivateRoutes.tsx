import React from "react";
import { Outlet, Navigate } from "react-router-dom";

const PrivateRoutes = () => {
  const user = localStorage.getItem("user");
  return user ? <Outlet /> : <Navigate to="/signin" />;
};

export default PrivateRoutes;
