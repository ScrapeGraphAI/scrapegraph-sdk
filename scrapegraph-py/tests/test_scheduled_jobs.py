"""
Tests for scheduled jobs functionality
"""
from uuid import uuid4

import pytest
from pydantic import ValidationError

from scrapegraph_py.client import Client
from scrapegraph_py.models.scheduled_jobs import (
    ServiceType,
    ScheduledJobCreate,
    ScheduledJobUpdate,
    GetScheduledJobsRequest,
    GetJobExecutionsRequest,
    TriggerJobRequest,
    JobActionRequest
)
from tests.utils import generate_mock_api_key


@pytest.fixture
def mock_api_key():
    return generate_mock_api_key()


@pytest.fixture
def mock_job_id():
    return str(uuid4())


@pytest.fixture
def mock_job_response():
    return {
        "id": str(uuid4()),
        "job_name": "Test Job",
        "service_type": "SMARTSCRAPER",
        "cron_expression": "0 9 * * *",
        "job_config": {
            "website_url": "https://example.com",
            "user_prompt": "test"
        },
        "is_active": True,
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z",
        "next_run_at": "2024-01-02T09:00:00Z"
    }


@pytest.fixture
def mock_jobs_list_response():
    return {
        "jobs": [
            {
                "id": str(uuid4()),
                "job_name": "Job 1",
                "service_type": "SMARTSCRAPER",
                "cron_expression": "0 9 * * *",
                "is_active": True,
                "created_at": "2024-01-01T00:00:00Z",
                "next_run_at": "2024-01-02T09:00:00Z"
            },
            {
                "id": str(uuid4()),
                "job_name": "Job 2", 
                "service_type": "MARKDOWNIFY",
                "cron_expression": "0 10 * * *",
                "is_active": False,
                "created_at": "2024-01-01T00:00:00Z",
                "next_run_at": None
            }
        ],
        "total": 2,
        "page": 1,
        "per_page": 10
    }


@pytest.fixture
def mock_executions_response():
    return {
        "executions": [
            {
                "id": str(uuid4()),
                "job_id": str(uuid4()),
                "status": "completed",
                "started_at": "2024-01-01T09:00:00Z",
                "completed_at": "2024-01-01T09:05:00Z",
                "result": {"status": "success"}
            }
        ],
        "total": 1,
        "page": 1,
        "per_page": 10
    }


# Note: API endpoint tests would require 'responses' library
# For now, focusing on mock mode and validation tests


class TestScheduledJobsValidation:
    """Test Pydantic model validation for scheduled jobs"""

    def test_valid_scheduled_job_create(self):
        """Test valid scheduled job creation model"""
        job = ScheduledJobCreate(
            job_name="Test Job",
            service_type=ServiceType.SMARTSCRAPER,
            cron_expression="0 9 * * *",
            job_config={
                "website_url": "https://example.com",
                "user_prompt": "test"
            }
        )
        
        assert job.job_name == "Test Job"
        assert job.service_type == ServiceType.SMARTSCRAPER
        assert job.cron_expression == "0 9 * * *"
        assert job.is_active is True  # Default value

    def test_invalid_cron_expression(self):
        """Test validation of invalid cron expressions"""
        with pytest.raises(ValidationError) as exc_info:
            ScheduledJobCreate(
                job_name="Test Job",
                service_type=ServiceType.SMARTSCRAPER,
                cron_expression="invalid cron",  # Invalid format
                job_config={"website_url": "https://example.com", "user_prompt": "test"}
            )
        
        assert "Cron expression must have exactly 5 fields" in str(exc_info.value)

    def test_empty_job_name(self):
        """Test validation of empty job name"""
        with pytest.raises(ValidationError) as exc_info:
            ScheduledJobCreate(
                job_name="",  # Empty name
                service_type=ServiceType.SMARTSCRAPER,
                cron_expression="0 9 * * *",
                job_config={"website_url": "https://example.com", "user_prompt": "test"}
            )
        
        assert "String should have at least 1 character" in str(exc_info.value)

    def test_valid_service_types(self):
        """Test all valid service types"""
        for service_type in ServiceType:
            job = ScheduledJobCreate(
                job_name="Test Job",
                service_type=service_type,
                cron_expression="0 9 * * *",
                job_config={"website_url": "https://example.com", "user_prompt": "test"}
            )
            assert job.service_type == service_type

    def test_scheduled_job_update_partial(self):
        """Test partial update model"""
        update = ScheduledJobUpdate(job_name="Updated Name")
        assert update.job_name == "Updated Name"
        assert update.cron_expression is None
        assert update.job_config is None
        assert update.is_active is None

    def test_get_scheduled_jobs_request_validation(self):
        """Test query parameters validation"""
        request = GetScheduledJobsRequest(page=1, page_size=50, is_active=True)
        assert request.page == 1
        assert request.page_size == 50
        assert request.is_active is True

    def test_get_job_executions_request_validation(self):
        """Test job executions query parameters"""
        request = GetJobExecutionsRequest(
            job_id="test-job-id",
            page=2,
            page_size=25,
            status="completed"
        )
        assert request.job_id == "test-job-id"
        assert request.page == 2
        assert request.page_size == 25
        assert request.status == "completed"


class TestScheduledJobsMockMode:
    """Test scheduled jobs in mock mode"""

    def test_mock_create_scheduled_job(self, mock_api_key):
        """Test creating scheduled job in mock mode"""
        client = Client(api_key=mock_api_key, mock=True)
        
        job = client.create_scheduled_job(
            job_name="Mock Test Job",
            service_type=ServiceType.SMARTSCRAPER,
            cron_expression="0 9 * * *",
            job_config={
                "website_url": "https://example.com",
                "user_prompt": "test"
            }
        )
        
        assert job["job_name"] == "Mock Scheduled Job"  # Mock response uses fixed name
        assert job["service_type"] == "smartscraper"  # Mock response uses lowercase
        assert "id" in job
        assert job["id"].startswith("mock-job-")

    def test_mock_get_scheduled_jobs(self, mock_api_key):
        """Test listing scheduled jobs in mock mode"""
        client = Client(api_key=mock_api_key, mock=True)
        
        jobs = client.get_scheduled_jobs()
        
        assert "jobs" in jobs
        assert "total" in jobs
        assert isinstance(jobs["jobs"], list)
        assert jobs["total"] >= 0

    def test_mock_job_operations(self, mock_api_key):
        """Test various job operations in mock mode"""
        client = Client(api_key=mock_api_key, mock=True)
        
        # Create a job first
        job = client.create_scheduled_job(
            job_name="Mock Job",
            service_type=ServiceType.SMARTSCRAPER,
            cron_expression="0 9 * * *",
            job_config={"website_url": "https://example.com", "user_prompt": "test"}
        )
        job_id = job["id"]
        
        # Test get single job
        job_details = client.get_scheduled_job(job_id)
        assert "job_name" in job_details
        
        # Test update
        updated_job = client.update_scheduled_job(job_id, job_name="Updated Mock Job")
        assert "job_name" in updated_job
        
        # Test pause
        pause_result = client.pause_scheduled_job(job_id)
        assert "message" in pause_result
        
        # Test resume
        resume_result = client.resume_scheduled_job(job_id)
        assert "message" in resume_result
        
        # Test trigger
        trigger_result = client.trigger_scheduled_job(job_id)
        assert "message" in trigger_result
        
        # Test get executions
        executions = client.get_job_executions(job_id)
        assert "executions" in executions
        assert "total" in executions
        
        # Test delete
        delete_result = client.delete_scheduled_job(job_id)
        assert "message" in delete_result

    def test_mock_error_handling(self, mock_api_key):
        """Test error handling in mock mode"""
        client = Client(api_key=mock_api_key, mock=True)
        
        # Test invalid cron expression
        with pytest.raises(ValidationError):
            client.create_scheduled_job(
                job_name="Invalid Job",
                service_type=ServiceType.SMARTSCRAPER,
                cron_expression="invalid",  # Invalid cron
                job_config={"website_url": "https://example.com", "user_prompt": "test"}
            )
        
        # Test empty job name
        with pytest.raises(ValidationError):
            client.create_scheduled_job(
                job_name="",  # Empty name
                service_type=ServiceType.SMARTSCRAPER,
                cron_expression="0 9 * * *",
                job_config={"website_url": "https://example.com", "user_prompt": "test"}
            )
