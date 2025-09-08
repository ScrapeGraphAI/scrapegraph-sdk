from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class ScheduledJobCreate(BaseModel):
    """Model for creating a new scheduled job"""
    job_name: str = Field(..., description="Name of the scheduled job")
    service_type: str = Field(..., description="Type of service (smartscraper, searchscraper, etc.)")
    cron_expression: str = Field(..., description="Cron expression for scheduling")
    job_config: Dict[str, Any] = Field(..., description="Configuration for the job")
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