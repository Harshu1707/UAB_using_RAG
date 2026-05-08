from pathlib import Path
from typing import Any
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.core.config import get_settings
from app.services.gemini_service import gemini_service

class RAGService:
    def __init__(self) -> None:
        self.settings = get_settings()
        Path(self.settings.upload_dir).mkdir(exist_ok=True)
        Path(self.settings.vectorstore_dir).mkdir(exist_ok=True)
        self.index_path = Path(self.settings.vectorstore_dir) / "faiss_index"
        self._embeddings = None

    @property
    def embeddings(self):
        if self._embeddings is None:
            self._embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        return self._embeddings

    def _load_store(self):
        if self.index_path.exists():
            return FAISS.load_local(str(self.index_path), self.embeddings, allow_dangerous_deserialization=True)
        return None

    def index_pdf(self, path: str) -> dict[str, Any]:
        loader = PyPDFLoader(path)
        docs = loader.load()
        splitter = RecursiveCharacterTextSplitter(chunk_size=900, chunk_overlap=150)
        chunks = splitter.split_documents(docs)
        for doc in chunks:
            doc.metadata["source"] = Path(path).name
        store = self._load_store()
        if store:
            store.add_documents(chunks)
        else:
            store = FAISS.from_documents(chunks, self.embeddings)
        store.save_local(str(self.index_path))
        return {"pages": len(docs), "chunks": len(chunks)}

    async def answer(self, question: str) -> tuple[str, list[dict]]:
        store = self._load_store()
        if not store:
            return "No PDFs are indexed yet. Ask an admin to upload syllabus or course PDFs first.", []
        docs = store.similarity_search(question, k=4)
        context = "\n\n".join(f"Source: {d.metadata.get('source')} page {d.metadata.get('page', 0) + 1}\n{d.page_content}" for d in docs)
        prompt = f"Answer using only the context. Include concise citations by file and page.\nContext:\n{context}\nQuestion: {question}"
        answer = await gemini_service.generate(prompt)
        sources = [{"source": d.metadata.get("source"), "page": d.metadata.get("page", 0) + 1} for d in docs]
        return answer, sources

rag_service = RAGService()
