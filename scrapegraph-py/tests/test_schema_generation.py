"""
Test cases for schema generation functionality
"""

from uuid import uuid4

import pytest
import responses
from pydantic import ValidationError

from scrapegraph_py.models.schema import (
    GenerateSchemaRequest,
    GetSchemaStatusRequest,
    SchemaGenerationResponse,
)
from scrapegraph_py.client import Client
from scrapegraph_py.async_client import AsyncClient
from tests.utils import generate_mock_api_key


@pytest.fixture
def mock_api_key():
    return generate_mock_api_key()


@pytest.fixture
def mock_uuid():
    return str(uuid4())


@pytest.fixture
def sample_schema():
    return {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "price": {"type": "number"},
        },
        "required": ["name", "price"],
    }


class TestSchemaModels:
    """Test cases for schema generation models"""

    def test_generate_schema_request_valid(self):
        """Test valid GenerateSchemaRequest creation"""
        request = GenerateSchemaRequest(
            user_prompt="Find laptops with brand and price"
        )
        assert request.user_prompt == "Find laptops with brand and price"
        assert request.existing_schema is None

    def test_generate_schema_request_with_existing_schema(self, sample_schema):
        """Test GenerateSchemaRequest with existing schema"""
        request = GenerateSchemaRequest(
            user_prompt="Add rating field",
            existing_schema=sample_schema
        )
        assert request.user_prompt == "Add rating field"
        assert request.existing_schema == sample_schema

    def test_generate_schema_request_empty_prompt(self):
        """Test GenerateSchemaRequest with empty prompt"""
        with pytest.raises(ValueError, match="user_prompt cannot be empty"):
            GenerateSchemaRequest(user_prompt="")

    def test_generate_schema_request_whitespace_prompt(self):
        """Test GenerateSchemaRequest with whitespace-only prompt"""
        with pytest.raises(ValueError, match="user_prompt cannot be empty"):
            GenerateSchemaRequest(user_prompt="   ")

    def test_get_schema_status_request_valid(self, mock_uuid):
        """Test valid GetSchemaStatusRequest creation"""
        request = GetSchemaStatusRequest(request_id=mock_uuid)
        assert request.request_id == mock_uuid

    def test_get_schema_status_request_invalid_uuid(self):
        """Test GetSchemaStatusRequest with invalid UUID"""
        with pytest.raises(ValueError, match="request_id must be a valid UUID"):
            GetSchemaStatusRequest(request_id="invalid-uuid")

    def test_schema_generation_response_valid(self, mock_uuid):
        """Test valid SchemaGenerationResponse creation"""
        response_data = {
            "request_id": mock_uuid,
            "status": "completed",
            "user_prompt": "Find laptops",
            "refined_prompt": "Find laptops with specifications",
            "generated_schema": {
                "type": "object",
                "properties": {
                    "laptops": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "brand": {"type": "string"},
                                "price": {"type": "number"},
                            },
                        },
                    },
                },
            },
        }
        
        response = SchemaGenerationResponse(**response_data)
        assert response.request_id == mock_uuid
        assert response.status == "completed"
        assert response.user_prompt == "Find laptops"
        assert response.refined_prompt == "Find laptops with specifications"
        assert response.generated_schema is not None

    def test_schema_generation_response_model_dump(self, mock_uuid):
        """Test SchemaGenerationResponse model_dump method"""
        response = SchemaGenerationResponse(
            request_id=mock_uuid,
            status="completed",
            user_prompt="Test prompt"
        )
        
        dumped = response.model_dump()
        assert "request_id" in dumped
        assert "status" in dumped
        assert "user_prompt" in dumped
        assert "generated_schema" not in dumped  # Should be excluded when None


class TestSchemaGenerationClient:
    """Test cases for schema generation using sync client"""

    @responses.activate
    def test_generate_schema_success(self, mock_api_key):
        """Test successful schema generation"""
        mock_response = {
            "request_id": str(uuid4()),
            "status": "pending",
            "user_prompt": "Find laptops with brand and price",
        }
        
        responses.add(
            responses.POST,
            "https://api.scrapegraphai.com/v1/generate_schema",
            json=mock_response,
            status=200,
        )

        with Client(api_key=mock_api_key) as client:
            response = client.generate_schema("Find laptops with brand and price")
            assert response["status"] == "pending"
            assert response["request_id"] is not None

    @responses.activate
    def test_generate_schema_with_existing_schema(self, mock_api_key, sample_schema):
        """Test schema generation with existing schema"""
        mock_response = {
            "request_id": str(uuid4()),
            "status": "pending",
            "user_prompt": "Add rating field",
        }
        
        responses.add(
            responses.POST,
            "https://api.scrapegraphai.com/v1/generate_schema",
            json=mock_response,
            status=200,
        )

        with Client(api_key=mock_api_key) as client:
            response = client.generate_schema(
                "Add rating field", 
                existing_schema=sample_schema
            )
            assert response["status"] == "pending"

    @responses.activate
    def test_generate_schema_api_error(self, mock_api_key):
        """Test schema generation with API error"""
        responses.add(
            responses.POST,
            "https://api.scrapegraphai.com/v1/generate_schema",
            json={"error": "Invalid API key"},
            status=401,
        )

        with Client(api_key=mock_api_key) as client:
            response = client.generate_schema("Find laptops")
            assert "error" in response

    @responses.activate
    def test_get_schema_status_success(self, mock_api_key, mock_uuid):
        """Test successful schema status retrieval"""
        mock_response = {
            "request_id": mock_uuid,
            "status": "completed",
            "user_prompt": "Find laptops",
            "generated_schema": {
                "type": "object",
                "properties": {
                    "laptops": {
                        "type": "array",
                        "items": {"type": "object"},
                    },
                },
            },
        }
        
        responses.add(
            responses.GET,
            f"https://api.scrapegraphai.com/v1/generate_schema/{mock_uuid}",
            json=mock_response,
            status=200,
        )

        with Client(api_key=mock_api_key) as client:
            response = client.get_schema_status(mock_uuid)
            assert response["status"] == "completed"
            assert response["generated_schema"] is not None

    @responses.activate
    def test_get_schema_status_not_found(self, mock_api_key, mock_uuid):
        """Test schema status retrieval for non-existent request"""
        responses.add(
            responses.GET,
            f"https://api.scrapegraphai.com/v1/generate_schema/{mock_uuid}",
            json={"error": "Request not found"},
            status=404,
        )

        with Client(api_key=mock_api_key) as client:
            response = client.get_schema_status(mock_uuid)
            assert "error" in response


class TestSchemaGenerationAsyncClient:
    """Test cases for schema generation using async client"""

    @pytest.mark.asyncio
    @responses.activate
    async def test_generate_schema_async_success(self, mock_api_key):
        """Test successful async schema generation"""
        mock_response = {
            "request_id": str(uuid4()),
            "status": "pending",
            "user_prompt": "Find laptops with brand and price",
        }
        
        responses.add(
            responses.POST,
            "https://api.scrapegraphai.com/v1/generate_schema",
            json=mock_response,
            status=200,
        )

        async with AsyncClient(api_key=mock_api_key) as client:
            response = await client.generate_schema("Find laptops with brand and price")
            assert response["status"] == "pending"
            assert response["request_id"] is not None

    @pytest.mark.asyncio
    @responses.activate
    async def test_generate_schema_async_with_existing_schema(self, mock_api_key, sample_schema):
        """Test async schema generation with existing schema"""
        mock_response = {
            "request_id": str(uuid4()),
            "status": "pending",
            "user_prompt": "Add rating field",
        }
        
        responses.add(
            responses.POST,
            "https://api.scrapegraphai.com/v1/generate_schema",
            json=mock_response,
            status=200,
        )

        async with AsyncClient(api_key=mock_api_key) as client:
            response = await client.generate_schema(
                "Add rating field", 
                existing_schema=sample_schema
            )
            assert response["status"] == "pending"

    @pytest.mark.asyncio
    @responses.activate
    async def test_get_schema_status_async_success(self, mock_api_key, mock_uuid):
        """Test successful async schema status retrieval"""
        mock_response = {
            "request_id": mock_uuid,
            "status": "completed",
            "user_prompt": "Find laptops",
            "generated_schema": {
                "type": "object",
                "properties": {
                    "laptops": {
                        "type": "array",
                        "items": {"type": "object"},
                    },
                },
            },
        }
        
        responses.add(
            responses.GET,
            f"https://api.scrapegraphai.com/v1/generate_schema/{mock_uuid}",
            json=mock_response,
            status=200,
        )

        async with AsyncClient(api_key=mock_api_key) as client:
            response = await client.get_schema_status(mock_uuid)
            assert response["status"] == "completed"
            assert response["generated_schema"] is not None


class TestSchemaGenerationIntegration:
    """Integration test cases for schema generation workflow"""

    @responses.activate
    def test_complete_schema_generation_workflow(self, mock_api_key):
        """Test complete schema generation workflow"""
        request_id = str(uuid4())
        
        # Mock initial schema generation request
        responses.add(
            responses.POST,
            "https://api.scrapegraphai.com/v1/generate_schema",
            json={
                "request_id": request_id,
                "status": "pending",
                "user_prompt": "Find laptops with brand and price",
            },
            status=200,
        )
        
        # Mock status check (still processing)
        responses.add(
            responses.GET,
            f"https://api.scrapegraphai.com/v1/generate_schema/{request_id}",
            json={
                "request_id": request_id,
                "status": "processing",
                "user_prompt": "Find laptops with brand and price",
            },
            status=200,
        )
        
        # Mock final status check (completed)
        responses.add(
            responses.GET,
            f"https://api.scrapegraphai.com/v1/generate_schema/{request_id}",
            json={
                "request_id": request_id,
                "status": "completed",
                "user_prompt": "Find laptops with brand and price",
                "generated_schema": {
                    "type": "object",
                    "properties": {
                        "laptops": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "brand": {"type": "string"},
                                    "price": {"type": "number"},
                                },
                            },
                        },
                    },
                },
            },
            status=200,
        )

        with Client(api_key=mock_api_key) as client:
            # Step 1: Generate schema
            response = client.generate_schema("Find laptops with brand and price")
            assert response["status"] == "pending"
            assert response["request_id"] == request_id
            
            # Step 2: Check status (processing)
            status_response = client.get_schema_status(request_id)
            assert status_response["status"] == "processing"
            
            # Step 3: Check status (completed)
            final_response = client.get_schema_status(request_id)
            assert final_response["status"] == "completed"
            assert final_response["generated_schema"] is not None

    @responses.activate
    def test_schema_modification_workflow(self, mock_api_key, sample_schema):
        """Test schema modification workflow"""
        request_id = str(uuid4())
        
        responses.add(
            responses.POST,
            "https://api.scrapegraphai.com/v1/generate_schema",
            json={
                "request_id": request_id,
                "status": "completed",
                "user_prompt": "Add rating field",
                "generated_schema": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "price": {"type": "number"},
                        "rating": {"type": "number"},
                    },
                    "required": ["name", "price", "rating"],
                },
            },
            status=200,
        )

        with Client(api_key=mock_api_key) as client:
            response = client.generate_schema(
                "Add rating field", 
                existing_schema=sample_schema
            )
            assert response["status"] == "completed"
            assert "rating" in response["generated_schema"]["properties"]


class TestSchemaGenerationEdgeCases:
    """Test cases for edge cases and error conditions"""

    @responses.activate
    def test_generate_schema_network_error(self, mock_api_key):
        """Test schema generation with network error"""
        responses.add(
            responses.POST,
            "https://api.scrapegraphai.com/v1/generate_schema",
            body=Exception("Network error"),
            status=500,
        )

        with Client(api_key=mock_api_key) as client:
            response = client.generate_schema("Find laptops")
            assert "error" in response

    @responses.activate
    def test_generate_schema_malformed_response(self, mock_api_key):
        """Test schema generation with malformed API response"""
        responses.add(
            responses.POST,
            "https://api.scrapegraphai.com/v1/generate_schema",
            body="Invalid JSON",
            status=200,
        )

        with Client(api_key=mock_api_key) as client:
            response = client.generate_schema("Find laptops")
            assert "error" in response

    def test_generate_schema_invalid_input_types(self, mock_api_key):
        """Test schema generation with invalid input types"""
        with Client(api_key=mock_api_key) as client:
            # Test with non-string prompt
            with pytest.raises(Exception):
                client.generate_schema(123)
            
            # Test with non-dict existing schema
            with pytest.raises(Exception):
                client.generate_schema("Test", existing_schema="invalid")

    def test_get_schema_status_invalid_uuid_format(self, mock_api_key):
        """Test get schema status with invalid UUID format"""
        with Client(api_key=mock_api_key) as client:
            with pytest.raises(ValueError, match="request_id must be a valid UUID"):
                client.get_schema_status("invalid-uuid-format")


class TestSchemaGenerationValidation:
    """Test cases for input validation"""

    def test_generate_schema_request_validation(self):
        """Test GenerateSchemaRequest validation rules"""
        # Valid cases
        GenerateSchemaRequest(user_prompt="Valid prompt")
        GenerateSchemaRequest(
            user_prompt="Valid prompt",
            existing_schema={"type": "object"}
        )
        
        # Invalid cases
        with pytest.raises(ValueError):
            GenerateSchemaRequest(user_prompt="")
        
        with pytest.raises(ValueError):
            GenerateSchemaRequest(user_prompt="   ")

    def test_get_schema_status_request_validation(self):
        """Test GetSchemaStatusRequest validation rules"""
        valid_uuid = str(uuid4())
        
        # Valid case
        GetSchemaStatusRequest(request_id=valid_uuid)
        
        # Invalid cases
        with pytest.raises(ValueError):
            GetSchemaStatusRequest(request_id="invalid-uuid")
        
        with pytest.raises(ValueError):
            GetSchemaStatusRequest(request_id="")
        
        with pytest.raises(ValueError):
            GetSchemaStatusRequest(request_id="123")

    def test_schema_generation_response_validation(self):
        """Test SchemaGenerationResponse validation rules"""
        valid_uuid = str(uuid4())
        
        # Valid case
        SchemaGenerationResponse(
            request_id=valid_uuid,
            status="completed",
            user_prompt="Test prompt"
        )
        
        # Test with all optional fields
        SchemaGenerationResponse(
            request_id=valid_uuid,
            status="completed",
            user_prompt="Test prompt",
            refined_prompt="Refined test prompt",
            generated_schema={"type": "object"},
            created_at="2024-01-01T00:00:00Z",
            updated_at="2024-01-01T00:00:00Z"
        )

