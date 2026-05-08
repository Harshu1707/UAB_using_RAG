from serpapi import GoogleSearch
from app.core.config import get_settings
from app.services.gemini_service import gemini_service

async def web_search(query: str) -> dict:
    settings = get_settings()
    if not settings.serpapi_api_key:
        return {"summary": "SerpAPI key is not configured.", "results": []}
    search = GoogleSearch({"q": query, "api_key": settings.serpapi_api_key, "engine": "google", "num": 5})
    data = search.get_dict()
    results = [{"title": r.get("title"), "link": r.get("link"), "snippet": r.get("snippet")} for r in data.get("organic_results", [])[:5]]
    prompt = "Summarize these student academic opportunity results with links:\n" + str(results)
    summary = await gemini_service.generate(prompt)
    return {"summary": summary, "results": results}
