"""
Pydantic models for the Scheduled Jobs API endpoints.

This module defines request and response models for managing scheduled jobs,
which allow you to automate recurring scraping tasks using cron expressions.

Scheduled Jobs support:
- Creating recurring scraping jobs
- Managing job lifecycle (pause, resume, delete)
- Manually triggering jobs on demand
- Viewing execution history
- Filtering and pagination
"""

from typing import Any, Dict, Optional
from enum import Enum
from pydantic import BaseModel, Field


class ServiceType(str, Enum):
    """
    Enum defining available service types for scheduled jobs.

    Available services:
        SMART_SCRAPER: AI-powered web scraping
        SEARCH_SCRAPER: Web research across multiple sources
        AGENTIC_SCRAPER: Automated browser interactions
    """
    SMART_SCRAPER = "smartscraper"
    SEARCH_SCRAPER = "searchscraper"
    AGENTIC_SCRAPER = "agenticscraper"


class ScheduledJobCreate(BaseModel):
    """Model for creating a new scheduled job"""
    job_name: str = Field(..., description="Name of the scheduled job")
    service_type: str = Field(..., description="Type of service (smartscraper, searchscraper, etc.)")
    cron_expression: str = Field(..., description="Cron expression for scheduling")
    job_config: Dict[str, Any] = Field(
        ..., 
        example={
            "website_url": "https://example.com",
            "user_prompt": "Extract company information",
            "headers": {
                "User-Agent": "scrapegraph-py",
                "Cookie": "session=abc123"
            }
        },
        description="Configuration for the job"
    )
    is_active: bool = Field(default=True, description="Whether the job is active")


class ScheduledJobUpdate(BaseModel):
    """Model for updating a scheduled job (partial update)"""
    job_name: Optional[str] = Field(None, description="Name of the scheduled job")
    cron_expression: Optional[str] = Field(None, description="Cron expression for scheduling")
    job_config: Optional[Dict[str, Any]] = Field(None, description="Configuration for the job")
    is_active: Optional[bool] = Field(None, description="Whether the job is active")


class GetScheduledJobsRequest(BaseModel):
    """Model for getting list of scheduled jobs"""
    page: int = Field(default=1, ge=1, description="Page number")
    page_size: int = Field(default=20, ge=1, le=100, description="Number of jobs per page")
    service_type: Optional[str] = Field(None, description="Filter by service type")
    is_active: Optional[bool] = Field(None, description="Filter by active status")


class GetScheduledJobRequest(BaseModel):
    """Model for getting a specific scheduled job"""
    job_id: str = Field(..., description="ID of the scheduled job")


class JobActionRequest(BaseModel):
    """Model for job actions (pause, resume, delete)"""
    job_id: str = Field(..., description="ID of the scheduled job")


class TriggerJobRequest(BaseModel):
    """Model for manually triggering a job"""
    job_id: str = Field(..., description="ID of the scheduled job")


class GetJobExecutionsRequest(BaseModel):
    """Model for getting job execution history"""
    job_id: str = Field(..., description="ID of the scheduled job")
    page: int = Field(default=1, ge=1, description="Page number")
    page_size: int = Field(default=20, ge=1, le=100, description="Number of executions per page")
    status: Optional[str] = Field(None, description="Filter by execution status")


class JobActionResponse(BaseModel):
    """Response model for job actions"""
    success: bool = Field(..., description="Whether the action was successful")
    message: str = Field(..., description="Response message")
    job_id: str = Field(..., description="ID of the scheduled job")


class JobExecutionListResponse(BaseModel):
    """Response model for job execution list"""
    executions: list = Field(..., description="List of job executions")
    total_count: int = Field(..., description="Total number of executions")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Number of executions per page")


class JobTriggerResponse(BaseModel):
    """Response model for job trigger"""
    success: bool = Field(..., description="Whether the job was triggered successfully")
    message: str = Field(..., description="Response message")
    job_id: str = Field(..., description="ID of the scheduled job")
    execution_id: Optional[str] = Field(None, description="ID of the triggered execution")


class ScheduledJobListResponse(BaseModel):
    """Response model for scheduled job list"""
    jobs: list = Field(..., description="List of scheduled jobs")
    total_count: int = Field(..., description="Total number of jobs")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Number of jobs per page")


class JobExecutionResponse(BaseModel):
    """Response model for a single job execution"""
    execution_id: str = Field(..., description="ID of the job execution")
    job_id: str = Field(..., description="ID of the scheduled job")
    status: str = Field(..., description="Execution status")
    started_at: Optional[str] = Field(None, description="Execution start timestamp")
    completed_at: Optional[str] = Field(None, description="Execution completion timestamp")
    result: Optional[Dict[str, Any]] = Field(None, description="Execution result data")
    error_message: Optional[str] = Field(None, description="Error message if execution failed")


class ScheduledJobResponse(BaseModel):
    """Response model for a single scheduled job"""
    job_id: str = Field(..., description="ID of the scheduled job")
    job_name: str = Field(..., description="Name of the scheduled job")
    service_type: str = Field(..., description="Type of service")
    cron_expression: str = Field(..., description="Cron expression for scheduling")
    job_config: Dict[str, Any] = Field(..., description="Configuration for the job")
    is_active: bool = Field(..., description="Whether the job is active")
    created_at: Optional[str] = Field(None, description="Job creation timestamp")
    updated_at: Optional[str] = Field(None, description="Job last update timestamp")