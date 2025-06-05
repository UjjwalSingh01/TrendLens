import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';

const SignIn: React.FC = () => {
  const [email, setEmail] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [error, setError] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const { login } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    try {
      setError('');
      setLoading(true);
      await login(email, password);
    } catch (err) {
      setError(`Login failed: ${(err as Error).message}`);
    }
    setLoading(false);
  };

  return (
    <div>
      <h2>Login</h2>
      {error && <div className="error">{error}</div>}
      <form onSubmit={handleSubmit}>
        <input 
          type="email" 
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Email"
          required
        />
        <input 
          type="password" 
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password"
          required
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Logging In...' : 'Login'}
        </button>
      </form>
    </div>
  );
};

export default SignIn;