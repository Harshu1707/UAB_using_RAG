import { Mic, Send } from 'lucide-react';
import { useState } from 'react';

export default function ChatInput({ onSend, loading }) {
  const [text, setText] = useState('');

  const submit = (event) => {
    event.preventDefault();
    const trimmed = text.trim();
    if (!trimmed) return;
    onSend(trimmed);
    setText('');
  };

  return (
    <form onSubmit={submit} className="glass flex gap-2 rounded-2xl p-2">
      <button
        type="button"
        className="rounded-xl p-3 hover:bg-slate-100 dark:hover:bg-slate-800"
        title="Voice input UI"
      >
        <Mic size={20} />
      </button>
      <input
        className="flex-1 bg-transparent outline-none"
        placeholder="Ask about syllabus, CGPA, scholarships..."
        value={text}
        onChange={(event) => setText(event.target.value)}
      />
      <button className="btn" disabled={loading}>
        <Send size={18} />
      </button>
    </form>
  );
}
