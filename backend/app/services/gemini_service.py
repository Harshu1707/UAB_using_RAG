import google.generativeai as genai
from app.core.config import get_settings

class GeminiService:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.enabled = bool(self.settings.gemini_api_key)
        if self.enabled:
            genai.configure(api_key=self.settings.gemini_api_key)
            self.model = genai.GenerativeModel("gemini-1.5-flash")
        else:
            self.model = None

    async def generate(self, prompt: str) -> str:
        if not self.enabled or self.model is None:
            return "Gemini API key is not configured. I can still route requests and return local analytics/search context."
        response = await self.model.generate_content_async(prompt)
        return response.text or "I could not generate a response."

    async def classify_intent(self, message: str) -> str:
        lower = message.lower()
        if any(w in lower for w in ["topper", "cgpa", "attendance", "at-risk", "risk", "pass", "rank", "student"]):
            return "SQL"
        if any(w in lower for w in ["scholarship", "internship", "latest", "conference", "event", "opportunity"]):
            return "WEB"
        if any(w in lower for w in ["syllabus", "elective", "pdf", "course", "semester", "module", "unit"]):
            return "RAG"
        if self.enabled:
            prompt = "Classify this query as exactly one of RAG, SQL, WEB, GENERAL_CHAT: " + message
            result = (await self.generate(prompt)).strip().upper()
            for intent in ["RAG", "SQL", "WEB", "GENERAL_CHAT"]:
                if intent in result:
                    return intent
        return "GENERAL_CHAT"

gemini_service = GeminiService()
