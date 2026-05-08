from sqlalchemy.orm import Session

from app.models.models import Conversation, User
from app.rag.rag_service import rag_service
from app.services.analytics_service import answer_sql_question
from app.services.gemini_service import gemini_service
from app.services.search_service import web_search


async def handle_chat(db: Session, user: User, message: str) -> dict:
    intent = await gemini_service.classify_intent(message)
    sources = []

    if intent == "RAG":
        answer, sources = await rag_service.answer(message)
    elif intent == "SQL":
        answer = answer_sql_question(db, message)
    elif intent == "WEB":
        result = await web_search(message)
        answer = result["summary"]
        sources = result["results"]
    else:
        answer = await gemini_service.generate(
            f"You are a helpful university academic advisor. Answer conversationally: {message}"
        )

    db.add(
        Conversation(
            user_id=user.id,
            title=message[:80],
            user_message=message,
            assistant_message=answer,
            intent=intent,
        )
    )
    db.commit()
    return {"answer": answer, "intent": intent, "sources": sources}
