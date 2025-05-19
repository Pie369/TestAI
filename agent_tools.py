import httpx
import logging

logger = logging.getLogger(__name__)

async def search_brave(query: str, api_key: str) -> list[dict]:
    url = 'https://serpapi.com/search.json'
    params = {
        'engine': 'brave',
        'q': query,
        'api_key': api_key,
        'brave_domain': 'brave.com',
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
        except Exception as exc:
            logger.error("Error calling Brave Search API: %s", exc)
            raise RuntimeError(f"Search API call failed: {exc}")

    results = []
    organic_results = data.get('organic_results', [])
    for item in organic_results:
        results.append({
            'title': item.get('title'),
            'link': item.get('link'),
            'snippet': item.get('snippet'),
        })

    if not results:
        raise RuntimeError("No search results found")

    return results
