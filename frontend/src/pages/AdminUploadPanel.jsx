import { useState } from 'react';
import { uploadPdf } from '../services/api';

export default function AdminUploadPanel() {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState('');

  const submit = async (event) => {
    event.preventDefault();
    if (!file) return;

    setMessage('Indexing PDF...');
    try {
      const { data } = await uploadPdf(file);
      setMessage(`Indexed ${data.filename}: ${data.pages} pages, ${data.chunks} chunks.`);
    } catch {
      setMessage('Upload failed. Ensure you are admin and selected a PDF.');
    }
  };

  return (
    <div className="p-6">
      <div className="glass max-w-2xl rounded-3xl p-8">
        <h2 className="text-2xl font-bold">Admin PDF Upload</h2>
        <p className="mb-6 opacity-70">
          Upload syllabus/course PDFs to incrementally update the FAISS vector store.
        </p>
        <form onSubmit={submit} className="rounded-2xl border-2 border-dashed p-8 text-center">
          <input type="file" accept="application/pdf" onChange={(event) => setFile(event.target.files[0])} />
          <button className="btn mt-4">Upload & Index</button>
        </form>
        {message && <p className="mt-4">{message}</p>}
      </div>
    </div>
  );
}
