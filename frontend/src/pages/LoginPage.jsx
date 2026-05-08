import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function LoginPage() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState('student@uab.edu');
  const [password, setPassword] = useState('student123');
  const [error, setError] = useState('');

  const submit = async (event) => {
    event.preventDefault();
    setError('');

    try {
      await login(email, password);
      navigate('/');
    } catch {
      setError('Login failed. Check your credentials and try again.');
    }
  };

  return (
    <div className="grid min-h-screen place-items-center p-4">
      <form onSubmit={submit} className="glass w-full max-w-md rounded-3xl p-8">
        <h1 className="text-3xl font-bold">Welcome to UAB</h1>
        <p className="mb-6 opacity-70">AI-powered academic advising.</p>
        {error && <p className="mb-3 text-red-500">{error}</p>}
        <input className="input mb-3" value={email} onChange={(event) => setEmail(event.target.value)} placeholder="Email" />
        <input
          className="input mb-4"
          type="password"
          value={password}
          onChange={(event) => setPassword(event.target.value)}
          placeholder="Password"
        />
        <button className="btn w-full">Login</button>
        <p className="mt-4 text-sm">
          No account?{' '}
          <Link className="text-indigo-500" to="/register">
            Register
          </Link>
        </p>
        <p className="mt-4 text-xs opacity-70">Demo admin: admin@uab.edu / admin123</p>
      </form>
    </div>
  );
}
