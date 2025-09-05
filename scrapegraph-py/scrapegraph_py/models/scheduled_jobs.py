# Models for scheduled jobs endpoints

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field, model_validator


class ServiceType(str, Enum):
    SMARTSCRAPER = "smartscraper"
    SEARCHSCRAPER = "searchscraper"
    MARKDOWNIFY = "markdownify"
    SMARTCRAWLER = "smartcrawler"
    AGENTICSCRAPPER = "agenticscrapper"


class ScheduledJobCreate(BaseModel):
    job_name: str = Field(..., min_length=1, max_length=255)
    service_type: ServiceType = Field(...)
    cron_expression: str = Field(...)
    job_config: Dict[str, Any] = Field(...)
    is_active: bool = Field(default=True)

    @model_validator(mode="after")
    def validate_cron_expression(self) -> "ScheduledJobCreate":
        if not self.cron_expression or not isinstance(self.cron_expression, str):
            raise ValueError("Cron expression must be a non-empty string")
        
        parts = self.cron_expression.strip().split()
        if len(parts) != 5:
            raise ValueError("Cron expression must have exactly 5 fields")
        
        self.cron_expression = self.cron_expression.strip()
        return self


class ScheduledJobUpdate(BaseModel):
    job_name: Optional[str] = Field(None, min_length=1, max_length=255)
    cron_expression: Optional[str] = Field(None)
    job_config: Optional[Dict[str, Any]] = Field(None)
    is_active: Optional[bool] = Field(None)

    @model_validator(mode="after")
    def validate_cron_expression(self) -> "ScheduledJobUpdate":
        if self.cron_expression is not None:
            if not isinstance(self.cron_expression, str):
                raise ValueError("Cron expression must be a string")
            
            parts = self.cron_expression.strip().split()
            if len(parts) != 5:
                raise ValueError("Cron expression must have exactly 5 fields")
            
            self.cron_expression = self.cron_expression.strip()
        return self


class ScheduledJobResponse(BaseModel):
    id: str = Field(...)
    user_id: str = Field(...)
    job_name: str = Field(...)
    service_type: ServiceType = Field(...)
    cron_expression: str = Field(...)
    job_config: Dict[str, Any] = Field(...)
    is_active: bool = Field(...)
    created_at: datetime = Field(...)
    updated_at: datetime = Field(...)
    last_run_at: Optional[datetime] = Field(None)
    next_run_at: Optional[datetime] = Field(None)


class ScheduledJobListResponse(BaseModel):
    jobs: List[ScheduledJobResponse] = Field(...)
    total: int = Field(...)
    page: int = Field(...)
    page_size: int = Field(...)


class JobExecutionResponse(BaseModel):
    id: str = Field(...)
    scheduled_job_id: str = Field(...)
    execution_id: str = Field(...)
    status: str = Field(...)
    started_at: datetime = Field(...)
    completed_at: Optional[datetime] = Field(None)
    result: Optional[Dict[str, Any]] = Field(None)
    error_message: Optional[str] = Field(None)
    credits_used: int = Field(default=0)


class JobExecutionListResponse(BaseModel):
    executions: List[JobExecutionResponse] = Field(...)
    total: int = Field(...)
    page: int = Field(...)
    page_size: int = Field(...)


class JobTriggerResponse(BaseModel):
    execution_id: str = Field(...)
    scheduled_job_id: str = Field(...)
    triggered_at: datetime = Field(...)
    message: str = Field(...)


class JobActionResponse(BaseModel):
    message: str = Field(...)
    job_id: str = Field(...)
    is_active: bool = Field(...)
    next_run_at: Optional[datetime] = Field(None)


class GetScheduledJobsRequest(BaseModel):
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)
    service_type: Optional[ServiceType] = Field(None)
    is_active: Optional[bool] = Field(None)


class GetJobExecutionsRequest(BaseModel):
    job_id: str = Field(...)
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)
    status: Optional[str] = Field(None)


class GetScheduledJobRequest(BaseModel):
    job_id: str = Field(...)

    @model_validator(mode="after")
    def validate_job_id(self) -> "GetScheduledJobRequest":
        if not self.job_id or not isinstance(self.job_id, str):
            raise ValueError("Job ID must be a non-empty string")
        self.job_id = self.job_id.strip()
        return self


class TriggerJobRequest(BaseModel):
    job_id: str = Field(...)

    @model_validator(mode="after")
    def validate_job_id(self) -> "TriggerJobRequest":
        if not self.job_id or not isinstance(self.job_id, str):
            raise ValueError("Job ID must be a non-empty string")
        self.job_id = self.job_id.strip()
        return self


class JobActionRequest(BaseModel):
    job_id: str = Field(...)

    @model_validator(mode="after")
    def validate_job_id(self) -> "JobActionRequest":
        if not self.job_id or not isinstance(self.job_id, str):
            raise ValueError("Job ID must be a non-empty string")
        self.job_id = self.job_id.strip()
        return self
