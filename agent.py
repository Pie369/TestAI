from __future__ import annotations as _annotations
import os
from typing import Any, Optional
from pydantic_ai import Agent, RunContext
from agent_tools import search_brave
from agent_prompts import SYSTEM_PROMPT

class Deps:
    def __init__(self, api_key: Optional[str] = None, subscription_token: Optional[str] = None):
        self.api_key = api_key
        self.subscription_token = subscription_token

greeting_agent = Agent(
    model='openai:gpt-4o-mini',
    system_prompt=SYSTEM_PROMPT,
    deps_type=Deps,
)

@greeting_agent.tool
async def brave_search(ctx: RunContext[Deps], query: str) -> list[dict[str, Any]]:
    if ctx.deps.api_key is None:
        raise RuntimeError("API key for Brave Search not configured.")
    if ctx.deps.subscription_token is None:
        raise RuntimeError("Subscription token for Brave Search not configured.")
    return await search_brave(
        query=query,
        api_key=ctx.deps.api_key,
        subscription_token=ctx.deps.subscription_token,
    )
