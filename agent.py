from __future__ import annotations as _annotations
from typing import Any
from pydantic_ai import Agent, RunContext
from agent_tools import search_brave
from agent_prompts import SYSTEM_PROMPT

class Deps:
    api_key: str | None = None

greeting_agent = Agent(
    model='openai:gpt-4o-mini',
    system_prompt=SYSTEM_PROMPT,
    deps_type=Deps,
)

@greeting_agent.tool
async def brave_search(ctx: RunContext[Deps], query: str) -> list[dict[str, Any]]:
    if ctx.deps.api_key is None:
        raise RuntimeError("API key for Brave Search (SerpAPI) not configured.")
    return await search_brave(query=query, api_key=ctx.deps.api_key)
