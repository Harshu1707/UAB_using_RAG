import { motion } from 'framer-motion';
import ReactMarkdown from 'react-markdown';

export default function ChatMessage({ role, content, sources = [] }) {
  const isUser = role === 'user';

  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}
    >
      <div className={`max-w-3xl rounded-2xl p-4 ${isUser ? 'bg-indigo-600 text-white' : 'glass'}`}>
        <ReactMarkdown>{content}</ReactMarkdown>
        {sources.length > 0 && (
          <div className="mt-3 border-t pt-2 text-xs opacity-80">
            Sources:{' '}
            {sources.map((source, index) => (
              <a className="mr-2 underline" key={index} href={source.link || '#'}>
                {source.source || source.title || 'source'}
                {source.page ? ` p.${source.page}` : ''}
              </a>
            ))}
          </div>
        )}
      </div>
    </motion.div>
  );
}
