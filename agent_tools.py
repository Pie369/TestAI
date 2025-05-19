import httpx
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

async def search_brave(
    query: str,
    api_key: str,
    subscription_token: str,
    limit: int = 10,
    offset: int = 0,
    market: str = "en-US"
) -> list[dict]:
    url = "https://api.search.brave.com/res/v1/web/search"
    headers = {
        "x-api-key": api_key,
        "x-subscription-token": subscription_token,
        "Accept": "application/json"
    }
    params = {
        "q": query,
        "limit": limit,
        "offset": offset,
        "market": market
    }

    async with httpx.AsyncClient() as client:
        try:
            logger.debug(f"Sending request to Brave Search API: url={url}, params={params}, headers={headers}")
            response = await client.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            logger.debug(f"Response data keys: {list(data.keys())}")
        except httpx.HTTPStatusError as http_err:
            content = await response.aread()
            text = content.decode('utf-8') if content else ''
            logger.error(f"HTTP error occurred: {http_err}\nResponse content: {text}")
            raise RuntimeError(f"Search API HTTP error: {http_err} - Response: {text}")
        except Exception as exc:
            logger.error(f"Unexpected error calling Brave Search API: {exc}")
            raise RuntimeError(f"Search API call failed: {exc}")

    web_results = data.get("web", {}).get("results", [])
    if not web_results:
        logger.warning("No search results found in web.results")
        raise RuntimeError("No search results found")

    results = []
    for item in web_results:
        results.append({
            "title": item.get("title"),
            "link": item.get("url"),
            "snippet": item.get("description") or item.get("body", "")
        })

    return results
