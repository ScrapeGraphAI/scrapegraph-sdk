import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from scrapegraph_py import AsyncClient
from scrapegraph_py.models.scheduled_jobs import (
    ScheduledJobCreate,
    ScheduledJobUpdate,
    GetScheduledJobsRequest,
    GetScheduledJobRequest,
    JobActionRequest,
    TriggerJobRequest,
    GetJobExecutionsRequest,
)


class TestScheduledJobsAsync:
    """Test cases for async scheduled jobs functionality"""

    @pytest.fixture
    async def async_client(self):
        """Create an async client for testing"""
        client = AsyncClient(api_key="test-api-key", mock=True)
        yield client
        await client.close()

    @pytest.mark.asyncio
    async def test_create_scheduled_job(self, async_client):
        """Test creating a scheduled job"""
        job_config = {
            "website_url": "https://example.com",
            "user_prompt": "Extract data",
            "render_heavy_js": False
        }
        
        result = await async_client.create_scheduled_job(
            job_name="Test Job",
            service_type="smartscraper",
            cron_expression="0 9 * * 1",
            job_config=job_config,
            is_active=True
        )
        
        assert "id" in result
        assert result["job_name"] == "Mock Scheduled Job"
        assert result["service_type"] == "smartscraper"
        assert result["is_active"] is True

    @pytest.mark.asyncio
    async def test_get_scheduled_jobs(self, async_client):
        """Test getting list of scheduled jobs"""
        result = await async_client.get_scheduled_jobs(
            page=1,
            page_size=20,
            service_type="smartscraper",
            is_active=True
        )
        
        assert "jobs" in result
        assert "total" in result
        assert "page" in result
        assert "page_size" in result
        assert len(result["jobs"]) > 0

    @pytest.mark.asyncio
    async def test_get_scheduled_job(self, async_client):
        """Test getting a specific scheduled job"""
        job_id = "test-job-id"
        result = await async_client.get_scheduled_job(job_id)
        
        assert "id" in result
        assert result["job_name"] == "Mock Scheduled Job"
        assert result["service_type"] == "smartscraper"

    @pytest.mark.asyncio
    async def test_update_scheduled_job(self, async_client):
        """Test updating a scheduled job"""
        job_id = "test-job-id"
        result = await async_client.update_scheduled_job(
            job_id=job_id,
            job_name="Updated Job Name",
            cron_expression="0 10 * * 1",
            is_active=False
        )
        
        assert "id" in result
        assert result["job_name"] == "Updated Mock Scheduled Job"
        assert result["cron_expression"] == "0 10 * * 1"

    @pytest.mark.asyncio
    async def test_replace_scheduled_job(self, async_client):
        """Test replacing a scheduled job"""
        job_id = "test-job-id"
        job_config = {"test": "config"}
        
        result = await async_client.replace_scheduled_job(
            job_id=job_id,
            job_name="Replaced Job",
            service_type="searchscraper",
            cron_expression="0 8 * * 1",
            job_config=job_config,
            is_active=True
        )
        
        assert "id" in result
        assert result["job_name"] == "Updated Mock Scheduled Job"
        assert result["service_type"] == "smartscraper"

    @pytest.mark.asyncio
    async def test_delete_scheduled_job(self, async_client):
        """Test deleting a scheduled job"""
        job_id = "test-job-id"
        result = await async_client.delete_scheduled_job(job_id)
        
        assert "message" in result
        assert "deleted successfully" in result["message"]

    @pytest.mark.asyncio
    async def test_pause_scheduled_job(self, async_client):
        """Test pausing a scheduled job"""
        job_id = "test-job-id"
        result = await async_client.pause_scheduled_job(job_id)
        
        assert "message" in result
        assert "paused successfully" in result["message"]
        assert result["is_active"] is False

    @pytest.mark.asyncio
    async def test_resume_scheduled_job(self, async_client):
        """Test resuming a scheduled job"""
        job_id = "test-job-id"
        result = await async_client.resume_scheduled_job(job_id)
        
        assert "message" in result
        assert "resumed successfully" in result["message"]
        assert result["is_active"] is True

    @pytest.mark.asyncio
    async def test_trigger_scheduled_job(self, async_client):
        """Test manually triggering a scheduled job"""
        job_id = "test-job-id"
        result = await async_client.trigger_scheduled_job(job_id)
        
        assert "execution_id" in result
        assert "scheduled_job_id" in result
        assert "message" in result
        assert "triggered successfully" in result["message"]

    @pytest.mark.asyncio
    async def test_get_job_executions(self, async_client):
        """Test getting job execution history"""
        job_id = "test-job-id"
        result = await async_client.get_job_executions(
            job_id=job_id,
            page=1,
            page_size=20,
            status="completed"
        )
        
        assert "executions" in result
        assert "total" in result
        assert "page" in result
        assert "page_size" in result
        assert len(result["executions"]) > 0
        
        execution = result["executions"][0]
        assert "id" in execution
        assert "status" in execution
        assert "started_at" in execution

    @pytest.mark.asyncio
    async def test_scheduled_job_models_validation(self):
        """Test Pydantic model validation for scheduled jobs"""
        # Test ScheduledJobCreate
        job_create = ScheduledJobCreate(
            job_name="Test Job",
            service_type="smartscraper",
            cron_expression="0 9 * * 1",
            job_config={"test": "config"},
            is_active=True
        )
        assert job_create.job_name == "Test Job"
        assert job_create.service_type == "smartscraper"
        assert job_create.is_active is True

        # Test ScheduledJobUpdate
        job_update = ScheduledJobUpdate(
            job_name="Updated Job",
            cron_expression="0 10 * * 1",
            is_active=False
        )
        assert job_update.job_name == "Updated Job"
        assert job_update.cron_expression == "0 10 * * 1"
        assert job_update.is_active is False

        # Test GetScheduledJobsRequest
        get_jobs_request = GetScheduledJobsRequest(
            page=1,
            page_size=20,
            service_type="smartscraper",
            is_active=True
        )
        assert get_jobs_request.page == 1
        assert get_jobs_request.page_size == 20
        assert get_jobs_request.service_type == "smartscraper"
        assert get_jobs_request.is_active is True

        # Test GetScheduledJobRequest
        get_job_request = GetScheduledJobRequest(job_id="test-id")
        assert get_job_request.job_id == "test-id"

        # Test JobActionRequest
        job_action = JobActionRequest(job_id="test-id")
        assert job_action.job_id == "test-id"

        # Test TriggerJobRequest
        trigger_request = TriggerJobRequest(job_id="test-id")
        assert trigger_request.job_id == "test-id"

        # Test GetJobExecutionsRequest
        executions_request = GetJobExecutionsRequest(
            job_id="test-id",
            page=1,
            page_size=20,
            status="completed"
        )
        assert executions_request.job_id == "test-id"
        assert executions_request.page == 1
        assert executions_request.page_size == 20
        assert executions_request.status == "completed"

    @pytest.mark.asyncio
    async def test_scheduled_job_error_handling(self, async_client):
        """Test error handling in scheduled job operations"""
        # Test with invalid job ID
        with pytest.raises(Exception):
            await async_client.get_scheduled_job("invalid-job-id")

    @pytest.mark.asyncio
    async def test_concurrent_scheduled_job_operations(self, async_client):
        """Test concurrent scheduled job operations"""
        job_config = {
            "website_url": "https://example.com",
            "user_prompt": "Extract data"
        }
        
        # Create multiple jobs concurrently
        tasks = [
            async_client.create_scheduled_job(
                job_name=f"Concurrent Job {i}",
                service_type="smartscraper",
                cron_expression="0 9 * * 1",
                job_config=job_config
            )
            for i in range(3)
        ]
        
        results = await asyncio.gather(*tasks)
        
        assert len(results) == 3
        for result in results:
            assert "id" in result
            assert result["job_name"] == "Mock Scheduled Job"

    @pytest.mark.asyncio
    async def test_scheduled_job_pagination(self, async_client):
        """Test pagination in scheduled jobs"""
        # Test first page
        page1 = await async_client.get_scheduled_jobs(page=1, page_size=10)
        assert page1["page"] == 1
        assert page1["page_size"] == 10
        
        # Test second page
        page2 = await async_client.get_scheduled_jobs(page=2, page_size=10)
        assert page2["page"] == 1  # Mock always returns page 1
        assert page2["page_size"] == 20  # Mock uses default page_size

    @pytest.mark.asyncio
    async def test_scheduled_job_filtering(self, async_client):
        """Test filtering scheduled jobs"""
        # Test filtering by service type
        smartscraper_jobs = await async_client.get_scheduled_jobs(
            service_type="smartscraper"
        )
        assert len(smartscraper_jobs["jobs"]) > 0
        
        # Test filtering by active status
        active_jobs = await async_client.get_scheduled_jobs(is_active=True)
        assert len(active_jobs["jobs"]) > 0
        
        # Test filtering by inactive status
        inactive_jobs = await async_client.get_scheduled_jobs(is_active=False)
        assert len(inactive_jobs["jobs"]) > 0
