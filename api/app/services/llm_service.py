import os
import httpx
import numpy as np
from typing import List, Dict, Any, Optional
from loguru import logger
from app.core.config import settings


async def openai_complete_if_cache(
    model: str,
    prompt: str,
    system_prompt: Optional[str] = None,
    history_messages: List[Dict[str, str]] = [],
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
    **kwargs,
) -> str:
    """
    Make a completion request to an OpenAI-compatible API with optional caching.
    """
    try:
        headers = {
            "Authorization": f"Bearer {api_key or settings.MODEL_API_KEY}",
            "Content-Type": "application/json",
        }

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        for msg in history_messages:
            messages.append(msg)

        messages.append({"role": "user", "content": prompt})

        async with httpx.AsyncClient(timeout=30.0) as client:
            # print(f"Prompt: {prompt}")
            response = await client.post(
                f"{base_url or settings.MODEL_BASE_URL}/chat/completions",
                headers=headers,
                json={"model": model, "messages": messages, **kwargs},
            )

            if response.status_code != 200:
                logger.error(f"API request failed: {response.text}")
                raise Exception(
                    f"API request failed with status {response.status_code}"
                )
            result = response.json()
            return result["choices"][0]["message"]["content"]

    except Exception as e:
        logger.error(f"Error in openai_complete_if_cache: {str(e)}")
        raise


async def openai_embed(
    texts: List[str],
    model: str,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
) -> np.ndarray:
    """
    Get embeddings from an OpenAI-compatible API.
    """
    try:
        headers = {
            "Authorization": f"Bearer {api_key or settings.EMBEDDING_MODEL_API_KEY}",
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{base_url or settings.EMBEDDING_MODEL_BASE_URL}/embeddings",
                headers=headers,
                json={"model": model, "input": texts, "encoding_format": "float"},
            )

            if response.status_code != 200:
                logger.error(f"API request failed: {response.text}")
                raise Exception(
                    f"API request failed with status {response.status_code}"
                )

            result = response.json()
            embeddings = [item["embedding"] for item in result["data"]]
            return np.array(embeddings)

    except Exception as e:
        logger.error(f"Error in openai_embed: {str(e)}")
        raise
