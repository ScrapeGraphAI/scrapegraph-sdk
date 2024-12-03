import asyncio
from typing import Any, Optional

import aiohttp
from aiohttp import ClientSession, ClientTimeout, TCPConnector
from aiohttp.client_exceptions import ClientError
from pydantic import BaseModel

from scrapegraph_py.config import API_BASE_URL, DEFAULT_HEADERS
from scrapegraph_py.exceptions import APIError
from scrapegraph_py.logger import sgai_logger as logger
from scrapegraph_py.models.feedback import FeedbackRequest
from scrapegraph_py.models.smartscraper import (
    GetSmartScraperRequest,
    SmartScraperRequest,
)
from scrapegraph_py.utils.helpers import handle_async_response, validate_api_key


class AsyncClient:
    def __init__(
        self,
        api_key: str,
        verify_ssl: bool = True,
        timeout: float = 120,
        max_retries: int = 3,
        retry_delay: float = 1.0,
    ):
        """Initialize AsyncClient with configurable parameters.

        Args:
            api_key: API key for authentication
            verify_ssl: Whether to verify SSL certificates
            timeout: Request timeout in seconds
            max_retries: Maximum number of retry attempts
            retry_delay: Delay between retries in seconds
        """
        logger.info("🔑 Initializing AsyncClient")
        validate_api_key(api_key)
        logger.debug(
            f"🛠️ Configuration: verify_ssl={verify_ssl}, timeout={timeout}, max_retries={max_retries}"
        )
        self.api_key = api_key
        self.headers = {**DEFAULT_HEADERS, "SGAI-APIKEY": api_key}
        self.max_retries = max_retries
        self.retry_delay = retry_delay

        ssl = None if verify_ssl else False
        self.timeout = ClientTimeout(total=timeout)

        self.session = ClientSession(
            headers=self.headers, connector=TCPConnector(ssl=ssl), timeout=self.timeout
        )

        logger.info("✅ AsyncClient initialized successfully")

    @classmethod
    def from_env(
        cls,
        verify_ssl: bool = True,
        timeout: float = 120,
        max_retries: int = 3,
        retry_delay: float = 1.0,
    ):
        """Initialize AsyncClient using API key from environment variable.

        Args:
            verify_ssl: Whether to verify SSL certificates
            timeout: Request timeout in seconds
            max_retries: Maximum number of retry attempts
            retry_delay: Delay between retries in seconds
        """
        from os import getenv
        api_key = getenv("SGAI_API_KEY")
        if not api_key:
            raise ValueError("SGAI_API_KEY environment variable not set")
        return cls(
            api_key=api_key,
            verify_ssl=verify_ssl,
            timeout=timeout,
            max_retries=max_retries,
            retry_delay=retry_delay,
        )

    async def _make_request(self, method: str, url: str, **kwargs) -> Any:
        """Make HTTP request with retry logic."""
        for attempt in range(self.max_retries):
            try:
                logger.info(
                    f"🚀 Making {method} request to {url} (Attempt {attempt + 1}/{self.max_retries})"
                )
                logger.debug(f"🔍 Request parameters: {kwargs}")

                async with self.session.request(method, url, **kwargs) as response:
                    logger.debug(f"📥 Response status: {response.status}")
                    result = await handle_async_response(response)
                    logger.info(f"✅ Request completed successfully: {method} {url}")
                    return result

            except ClientError as e:
                logger.warning(f"⚠️ Request attempt {attempt + 1} failed: {str(e)}")
                if hasattr(e, "status") and e.status is not None:
                    try:
                        error_data = await e.response.json()
                        error_msg = error_data.get("error", str(e))
                        logger.error(f"🔴 API Error: {error_msg}")
                        raise APIError(error_msg, status_code=e.status)
                    except ValueError:
                        logger.error("🔴 Could not parse error response")
                        raise APIError(
                            str(e),
                            status_code=e.status if hasattr(e, "status") else None,
                        )

                if attempt == self.max_retries - 1:
                    logger.error(f"❌ All retry attempts failed for {method} {url}")
                    raise ConnectionError(f"Failed to connect to API: {str(e)}")

                retry_delay = self.retry_delay * (attempt + 1)
                logger.info(f"⏳ Waiting {retry_delay}s before retry {attempt + 2}")
                await asyncio.sleep(retry_delay)

    async def smartscraper(
        self,
        website_url: str,
        user_prompt: str,
        output_schema: Optional[BaseModel] = None,
    ):
        """Send a smartscraper request"""
        logger.info(f"🔍 Starting smartscraper request for {website_url}")
        logger.debug(f"📝 Prompt: {user_prompt}")

        request = SmartScraperRequest(
            website_url=website_url,
            user_prompt=user_prompt,
            output_schema=output_schema,
        )
        logger.debug("✅ Request validation passed")

        try:
            async with self.session.post(
                f"{API_BASE_URL}/smartscraper", json=request.model_dump()
            ) as response:
                response.raise_for_status()
                result = await handle_async_response(response)
                logger.info("✨ Smartscraper request completed successfully")
                return result
        except aiohttp.ClientError as e:
            logger.error(f"❌ Smartscraper request failed: {str(e)}")
            raise ConnectionError(f"Failed to connect to API: {str(e)}")

    async def get_smartscraper(self, request_id: str):
        """Get the result of a previous smartscraper request"""
        logger.info(f"🔍 Fetching smartscraper result for request {request_id}")

        # Validate input using Pydantic model
        GetSmartScraperRequest(request_id=request_id)
        logger.debug("✅ Request ID validation passed")

        async with self.session.get(
            f"{API_BASE_URL}/smartscraper/{request_id}"
        ) as response:
            result = await handle_async_response(response)
            logger.info(f"✨ Successfully retrieved result for request {request_id}")
            return result

    async def get_credits(self):
        """Get credits information"""
        logger.info("💳 Fetching credits information")

        async with self.session.get(
            f"{API_BASE_URL}/credits",
        ) as response:
            result = await handle_async_response(response)
            logger.info(
                f"✨ Credits info retrieved: {result.get('remaining_credits')} credits remaining"
            )
            return result

    async def submit_feedback(
        self, request_id: str, rating: int, feedback_text: Optional[str] = None
    ):
        """Submit feedback for a request"""
        logger.info(f"📝 Submitting feedback for request {request_id}")
        logger.debug(f"⭐ Rating: {rating}, Feedback: {feedback_text}")

        feedback = FeedbackRequest(
            request_id=request_id, rating=rating, feedback_text=feedback_text
        )
        logger.debug("✅ Feedback validation passed")

        async with self.session.post(
            f"{API_BASE_URL}/feedback", json=feedback.model_dump()
        ) as response:
            result = await handle_async_response(response)
            logger.info("✨ Feedback submitted successfully")
            return result

    async def close(self):
        """Close the session to free up resources"""
        logger.info("🔒 Closing AsyncClient session")
        await self.session.close()
        logger.debug("✅ Session closed successfully")

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
