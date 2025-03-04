import asyncio
from typing import Any, Optional, Dict, Callable, Awaitable, TypeVar, Generic
from enum import Enum
from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4

from aiohttp import ClientSession, ClientTimeout, TCPConnector
from aiohttp.client_exceptions import ClientError
from pydantic import BaseModel

from scrapegraph_py.config import API_BASE_URL, DEFAULT_HEADERS
from scrapegraph_py.exceptions import APIError
from scrapegraph_py.logger import sgai_logger as logger
from scrapegraph_py.models.feedback import FeedbackRequest
from scrapegraph_py.models.markdownify import GetMarkdownifyRequest, MarkdownifyRequest
from scrapegraph_py.models.searchscraper import (
    GetSearchScraperRequest,
    SearchScraperRequest,
)
from scrapegraph_py.models.smartscraper import (
    GetSmartScraperRequest,
    SmartScraperRequest,
)
from scrapegraph_py.utils.helpers import handle_async_response, validate_api_key

T = TypeVar('T')

class JobStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class Job(Generic[T]):
    id: str
    status: JobStatus
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Optional[T] = None
    error: Optional[Exception] = None
    task: Optional[Callable[..., Awaitable[T]]] = None
    args: tuple = ()
    kwargs: dict = None

class AsyncClient:
    @classmethod
    def from_env(
        cls,
        verify_ssl: bool = True,
        timeout: Optional[float] = None,
        max_retries: int = 3,
        retry_delay: float = 1.0,
    ):
        """Initialize AsyncClient using API key from environment variable.

        Args:
            verify_ssl: Whether to verify SSL certificates
            timeout: Request timeout in seconds. None means no timeout (infinite)
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

    def __init__(
        self,
        api_key: str = None,
        verify_ssl: bool = True,
        timeout: Optional[float] = None,
        max_retries: int = 3,
        retry_delay: float = 1.0,
        max_queue_size: int = 1000,
    ):
        """Initialize AsyncClient with configurable parameters.

        Args:
            api_key: API key for authentication. If None, will try to load from environment
            verify_ssl: Whether to verify SSL certificates
            timeout: Request timeout in seconds. None means no timeout (infinite)
            max_retries: Maximum number of retry attempts
            retry_delay: Delay between retries in seconds
            max_queue_size: Maximum number of jobs in the queue
        """
        logger.info("🔑 Initializing AsyncClient")

        # Try to get API key from environment if not provided
        if api_key is None:
            from os import getenv

            api_key = getenv("SGAI_API_KEY")
            if not api_key:
                raise ValueError(
                    "SGAI_API_KEY not provided and not found in environment"
                )

        validate_api_key(api_key)
        logger.debug(
            f"🛠️ Configuration: verify_ssl={verify_ssl}, timeout={timeout}, max_retries={max_retries}"
        )
        self.api_key = api_key
        self.headers = {**DEFAULT_HEADERS, "SGAI-APIKEY": api_key}
        self.max_retries = max_retries
        self.retry_delay = retry_delay

        ssl = None if verify_ssl else False
        self.timeout = ClientTimeout(total=timeout) if timeout is not None else None

        self.session = ClientSession(
            headers=self.headers, connector=TCPConnector(ssl=ssl), timeout=self.timeout
        )

        # Initialize job queue
        self.job_queue: asyncio.Queue[Job] = asyncio.Queue(maxsize=max_queue_size)
        self.jobs: Dict[str, Job] = {}
        self._queue_processor_task = None

        logger.info("✅ AsyncClient initialized successfully")

    async def start_queue_processor(self):
        """Start the background job queue processor."""
        if self._queue_processor_task is None:
            self._queue_processor_task = asyncio.create_task(self._process_queue())
            logger.info("🚀 Job queue processor started")

    async def stop_queue_processor(self):
        """Stop the background job queue processor."""
        if self._queue_processor_task is not None:
            self._queue_processor_task.cancel()
            try:
                await self._queue_processor_task
            except asyncio.CancelledError:
                pass
            self._queue_processor_task = None
            logger.info("⏹️ Job queue processor stopped")

    async def _process_queue(self):
        """Process jobs from the queue."""
        while True:
            try:
                job = await self.job_queue.get()
                job.status = JobStatus.RUNNING
                job.started_at = datetime.now()

                try:
                    if job.task:
                        job.result = await job.task(*job.args, **(job.kwargs or {}))
                        job.status = JobStatus.COMPLETED
                except Exception as e:
                    job.error = e
                    job.status = JobStatus.FAILED
                    logger.error(f"❌ Job {job.id} failed: {str(e)}")
                finally:
                    job.completed_at = datetime.now()
                    self.job_queue.task_done()

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ Queue processor error: {str(e)}")

    async def submit_job(self, task: Callable[..., Awaitable[T]], *args, **kwargs) -> str:
        """Submit a new job to the queue.
        
        Args:
            task: Async function to execute
            *args: Positional arguments for the task
            **kwargs: Keyword arguments for the task
            
        Returns:
            str: Job ID
        """
        job_id = str(uuid4())
        job = Job(
            id=job_id,
            status=JobStatus.PENDING,
            created_at=datetime.now(),
            task=task,
            args=args,
            kwargs=kwargs
        )
        
        self.jobs[job_id] = job
        await self.job_queue.put(job)
        logger.info(f"📋 Job {job_id} submitted to queue")
        
        # Ensure queue processor is running
        if self._queue_processor_task is None:
            await self.start_queue_processor()
            
        return job_id

    async def get_job_status(self, job_id: str) -> Dict[str, Any]:
        """Get the status of a job.
        
        Args:
            job_id: The ID of the job to check
            
        Returns:
            Dict containing job status information
        """
        if job_id not in self.jobs:
            raise ValueError(f"Job {job_id} not found")
            
        job = self.jobs[job_id]
        return {
            "id": job.id,
            "status": job.status.value,
            "created_at": job.created_at,
            "started_at": job.started_at,
            "completed_at": job.completed_at,
            "result": job.result,
            "error": str(job.error) if job.error else None
        }

    async def wait_for_job(self, job_id: str, timeout: Optional[float] = None) -> Any:
        """Wait for a job to complete and return its result.
        
        Args:
            job_id: The ID of the job to wait for
            timeout: Maximum time to wait in seconds
            
        Returns:
            The result of the job
        """
        if job_id not in self.jobs:
            raise ValueError(f"Job {job_id} not found")
            
        job = self.jobs[job_id]
        
        while job.status in (JobStatus.PENDING, JobStatus.RUNNING):
            await asyncio.sleep(0.1)
            
        if job.error:
            raise job.error
            
        return job.result

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

    async def markdownify(
        self, website_url: str, headers: Optional[dict[str, str]] = None
    ):
        """Send a markdownify request"""
        logger.info(f"🔍 Starting markdownify request for {website_url}")
        if headers:
            logger.debug("🔧 Using custom headers")

        request = MarkdownifyRequest(website_url=website_url, headers=headers)
        logger.debug("✅ Request validation passed")

        result = await self._make_request(
            "POST", f"{API_BASE_URL}/markdownify", json=request.model_dump()
        )
        logger.info("✨ Markdownify request completed successfully")
        return result

    async def get_markdownify(self, request_id: str):
        """Get the result of a previous markdownify request"""
        logger.info(f"🔍 Fetching markdownify result for request {request_id}")

        # Validate input using Pydantic model
        GetMarkdownifyRequest(request_id=request_id)
        logger.debug("✅ Request ID validation passed")

        result = await self._make_request(
            "GET", f"{API_BASE_URL}/markdownify/{request_id}"
        )
        logger.info(f"✨ Successfully retrieved result for request {request_id}")
        return result

    async def smartscraper(
        self,
        user_prompt: str,
        website_url: Optional[str] = None,
        website_html: Optional[str] = None,
        headers: Optional[dict[str, str]] = None,
        output_schema: Optional[BaseModel] = None,
    ):
        """Send a smartscraper request"""
        logger.info("🔍 Starting smartscraper request")
        if website_url:
            logger.debug(f"🌐 URL: {website_url}")
        if website_html:
            logger.debug("📄 Using provided HTML content")
        if headers:
            logger.debug("🔧 Using custom headers")
        logger.debug(f"📝 Prompt: {user_prompt}")

        request = SmartScraperRequest(
            website_url=website_url,
            website_html=website_html,
            headers=headers,
            user_prompt=user_prompt,
            output_schema=output_schema,
        )
        logger.debug("✅ Request validation passed")

        result = await self._make_request(
            "POST", f"{API_BASE_URL}/smartscraper", json=request.model_dump()
        )
        logger.info("✨ Smartscraper request completed successfully")
        return result

    async def get_smartscraper(self, request_id: str):
        """Get the result of a previous smartscraper request"""
        logger.info(f"🔍 Fetching smartscraper result for request {request_id}")

        # Validate input using Pydantic model
        GetSmartScraperRequest(request_id=request_id)
        logger.debug("✅ Request ID validation passed")

        result = await self._make_request(
            "GET", f"{API_BASE_URL}/smartscraper/{request_id}"
        )
        logger.info(f"✨ Successfully retrieved result for request {request_id}")
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

        result = await self._make_request(
            "POST", f"{API_BASE_URL}/feedback", json=feedback.model_dump()
        )
        logger.info("✨ Feedback submitted successfully")
        return result

    async def get_credits(self):
        """Get credits information"""
        logger.info("💳 Fetching credits information")

        result = await self._make_request(
            "GET",
            f"{API_BASE_URL}/credits",
        )
        logger.info(
            f"✨ Credits info retrieved: {result.get('remaining_credits')} credits remaining"
        )
        return result

    async def searchscraper(
        self,
        user_prompt: str,
        headers: Optional[dict[str, str]] = None,
        output_schema: Optional[BaseModel] = None,
    ):
        """Send a searchscraper request"""
        logger.info("🔍 Starting searchscraper request")
        logger.debug(f"📝 Prompt: {user_prompt}")
        if headers:
            logger.debug("🔧 Using custom headers")

        request = SearchScraperRequest(
            user_prompt=user_prompt,
            headers=headers,
            output_schema=output_schema,
        )
        logger.debug("✅ Request validation passed")

        result = await self._make_request(
            "POST", f"{API_BASE_URL}/searchscraper", json=request.model_dump()
        )
        logger.info("✨ Searchscraper request completed successfully")
        return result

    async def get_searchscraper(self, request_id: str):
        """Get the result of a previous searchscraper request"""
        logger.info(f"🔍 Fetching searchscraper result for request {request_id}")

        # Validate input using Pydantic model
        GetSearchScraperRequest(request_id=request_id)
        logger.debug("✅ Request ID validation passed")

        result = await self._make_request(
            "GET", f"{API_BASE_URL}/searchscraper/{request_id}"
        )
        logger.info(f"✨ Successfully retrieved result for request {request_id}")
        return result

    async def close(self):
        """Close the session and stop the queue processor."""
        logger.info("🔒 Closing AsyncClient session")
        await self.stop_queue_processor()
        await self.session.close()
        logger.debug("✅ Session closed successfully")

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
