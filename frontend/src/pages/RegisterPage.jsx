import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const INITIAL_FORM = {
  email: '',
  full_name: '',
  password: '',
  role: 'student',
};

export default function RegisterPage() {
  const { register } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState(INITIAL_FORM);

  const updateField = (field, value) => setForm((current) => ({ ...current, [field]: value }));

  const submit = async (event) => {
    event.preventDefault();
    await register(form);
    navigate('/');
  };

  return (
    <div className="grid min-h-screen place-items-center p-4">
      <form onSubmit={submit} className="glass w-full max-w-md rounded-3xl p-8">
        <h1 className="mb-6 text-3xl font-bold">Create account</h1>
        <input className="input mb-3" placeholder="Full name" onChange={(event) => updateField('full_name', event.target.value)} />
        <input className="input mb-3" placeholder="Email" onChange={(event) => updateField('email', event.target.value)} />
        <input
          className="input mb-3"
          type="password"
          placeholder="Password"
          onChange={(event) => updateField('password', event.target.value)}
        />
        <select className="input mb-4" onChange={(event) => updateField('role', event.target.value)}>
          <option value="student">Student</option>
          <option value="admin">Admin</option>
        </select>
        <button className="btn w-full">Register</button>
        <p className="mt-4 text-sm">
          <Link className="text-indigo-500" to="/login">
            Back to login
          </Link>
        </p>
      </form>
    </div>
  );
}
