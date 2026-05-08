import { Moon, Sun } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';

export default function Navbar() {
  const { user, logout } = useAuth();
  const { dark, setDark } = useTheme();

  return (
    <nav className="glass flex items-center justify-between p-4">
      <div>
        <b>{user?.full_name}</b>
        <span className="ml-2 rounded-full bg-indigo-100 px-2 py-1 text-xs text-indigo-700">
          {user?.role}
        </span>
      </div>
      <div className="flex gap-2">
        <button
          onClick={() => setDark(!dark)}
          className="rounded-xl p-2 hover:bg-slate-100 dark:hover:bg-slate-800"
          type="button"
        >
          {dark ? <Sun /> : <Moon />}
        </button>
        <button onClick={logout} className="btn" type="button">
          Logout
        </button>
      </div>
    </nav>
  );
}
