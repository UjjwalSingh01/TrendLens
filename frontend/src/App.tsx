import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import ProtectedRoute from './components/ProtectedRoute';
import { AuthProvider, useAuth } from './context/AuthContext';
import SignUp from './pages/SignUp';
import SignIn from './pages/SignIn';

const Dashboard: React.FC = () => {
  const { currentUser, logout } = useAuth();

  return (
    <div>
      <h2>Dashboard</h2>
      <p>Welcome, {currentUser?.email}</p>
      <button onClick={logout}>Log Out</button>
    </div>
  );
};

function App() {
  return (
    <Router>
      <AuthProvider>
        <Routes>
          <Route path="/signup" element={<SignUp />} />
          <Route path="/login" element={<SignIn />} />
          <Route 
            path="/" 
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            } 
          />
          <Route path="*" element={<SignIn />} />
        </Routes>
      </AuthProvider>
    </Router>
  );
}

export default App;