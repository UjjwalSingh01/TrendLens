import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

interface ProtectedRouteProps {
  children: React.ReactElement;
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children }) => {
  const { currentUser, loading } = useAuth();

  if (loading) return <div>Loading...</div>;
  
  if (!currentUser) {
    return <Navigate to="/login" replace />;
  }

  return children;
};

export default ProtectedRoute;