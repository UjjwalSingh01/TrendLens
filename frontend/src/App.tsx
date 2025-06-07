import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import ProtectedRoute from './components/ProtectedRoute';
import { AuthProvider } from './context/AuthContext';
import SignUp from './pages/SignUp';
import SignIn from './pages/SignIn';
import ImageUploadPortal from './pages/ImageUploadPortal';


function App() {
  return (
    <Router>
      <AuthProvider>
        <Routes>
          <Route path="/signup" element={<SignUp />} />
          <Route path="/login" element={<SignIn />} />
          <Route path="/imageUploadPortal" element={<ImageUploadPortal />} />
          {/* <Route 
            path="/" 
            element={
              <ProtectedRoute>
                <ImageUploadPortal />
              </ProtectedRoute>
            } 
          /> */}
          <Route path="*" element={<SignIn />} />
        </Routes>
      </AuthProvider>
    </Router>
  );
}

export default App;