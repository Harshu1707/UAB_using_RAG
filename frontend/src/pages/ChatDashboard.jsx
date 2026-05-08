import { useState } from 'react';
import ChatInput from '../components/ChatInput';
import ChatMessage from '../components/ChatMessage';
import Loader from '../components/Loader';
import { sendChat } from '../services/api';

const WELCOME_MESSAGE = {
  role: 'assistant',
  content: 'Hi! Ask me about course PDFs, student analytics, or latest scholarships and internships.',
};

export default function ChatDashboard() {
  const [messages, setMessages] = useState([WELCOME_MESSAGE]);
  const [loading, setLoading] = useState(false);

  const onSend = async (text) => {
    setMessages((current) => [...current, { role: 'user', content: text }]);
    setLoading(true);

    try {
      const { data } = await sendChat(text);
      setMessages((current) => [
        ...current,
        {
          role: 'assistant',
          content: `**Intent:** ${data.intent}\n\n${data.answer}`,
          sources: data.sources,
        },
      ]);
    } catch {
      setMessages((current) => [
        ...current,
        { role: 'assistant', content: 'Sorry, the advisor API returned an error.' },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="flex flex-1 flex-col p-4">
      <div className="mb-4 flex-1 space-y-4 overflow-y-auto rounded-3xl p-2">
        {messages.map((message, index) => (
          <ChatMessage key={`${message.role}-${index}`} {...message} />
        ))}
        {loading && (
          <div className="glass inline-block rounded-2xl p-4">
            <Loader />
          </div>
        )}
      </div>
      <ChatInput onSend={onSend} loading={loading} />
    </section>
  );
}
