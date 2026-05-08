import { BarChart3, MessageSquare, Upload } from 'lucide-react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function Sidebar() {
  const { user } = useAuth();

  return (
    <aside className="hidden w-72 flex-col gap-3 border-r border-slate-200 p-4 dark:border-slate-800 md:flex">
      <h1 className="text-xl font-bold">UAB Advisor</h1>
      <Link className="glass flex items-center gap-2 rounded-xl p-3" to="/">
        <MessageSquare /> Chat Dashboard
      </Link>
      <Link className="glass flex items-center gap-2 rounded-xl p-3" to="/analytics">
        <BarChart3 /> Analytics
      </Link>
      {user?.role === 'admin' && (
        <Link className="glass flex items-center gap-2 rounded-xl p-3" to="/admin">
          <Upload /> Admin Upload
        </Link>
      )}
      <div className="mt-4 text-sm opacity-70">
        Conversation history appears as saved chat cards in future expansions.
      </div>
    </aside>
  );
}
