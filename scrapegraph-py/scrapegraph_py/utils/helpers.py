# Utility functions go here

from typing import Any, Dict
from uuid import UUID

import aiohttp
from requests import Response

from scrapegraph_py.exceptions import APIError


def validate_api_key(api_key: str) -> bool:
    if not api_key.startswith("sgai-"):
        raise ValueError("Invalid API key format. API key must start with 'sgai-'")
    uuid_part = api_key[5:]  # Strip out 'sgai-'
    try:
        UUID(uuid_part)
    except ValueError:
        raise ValueError(
            "Invalid API key format. API key must be 'sgai-' followed by a valid UUID. You can get one at https://dashboard.scrapegraphai.com/"
        )
    return True


def handle_sync_response(response: Response) -> Dict[str, Any]:
    try:
        data = response.json()
    except ValueError:
        # If response is not JSON, use the raw text
        data = {"error": response.text}

    if response.status_code >= 400:
        error_msg = data.get("error", data.get("detail", f"HTTP {response.status_code}: {response.text}"))
        raise APIError(error_msg, status_code=response.status_code)

    return data


async def handle_async_response(response: aiohttp.ClientResponse) -> Dict[str, Any]:
    try:
        data = await response.json()
        text = None
    except ValueError:
        # If response is not JSON, use the raw text
        text = await response.text()
        data = {"error": text}

    if response.status >= 400:
        if text is None:
            text = await response.text()
        error_msg = data.get("error", data.get("detail", f"HTTP {response.status}: {text}"))
        raise APIError(error_msg, status_code=response.status)

    return data
