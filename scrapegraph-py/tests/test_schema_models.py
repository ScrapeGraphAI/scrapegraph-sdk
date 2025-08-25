"""
Test cases for schema generation models in isolation
"""

import json
from uuid import uuid4

import pytest
from pydantic import ValidationError

from scrapegraph_py.models.schema import (
    GenerateSchemaRequest,
    GetSchemaStatusRequest,
    SchemaGenerationResponse,
)


class TestGenerateSchemaRequest:
    """Test cases for GenerateSchemaRequest model"""

    def test_valid_request_without_existing_schema(self):
        """Test valid request creation without existing schema"""
        request = GenerateSchemaRequest(
            user_prompt="Find laptops with brand and price"
        )
        assert request.user_prompt == "Find laptops with brand and price"
        assert request.existing_schema is None

    def test_valid_request_with_existing_schema(self):
        """Test valid request creation with existing schema"""
        existing_schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "price": {"type": "number"},
            },
        }
        
        request = GenerateSchemaRequest(
            user_prompt="Add rating field",
            existing_schema=existing_schema
        )
        assert request.user_prompt == "Add rating field"
        assert request.existing_schema == existing_schema

    def test_request_with_complex_existing_schema(self):
        """Test request with complex nested existing schema"""
        complex_schema = {
            "$defs": {
                "ProductSchema": {
                    "title": "ProductSchema",
                    "type": "object",
                    "properties": {
                        "name": {"title": "Name", "type": "string"},
                        "price": {"title": "Price", "type": "number"},
                        "specifications": {
                            "type": "object",
                            "properties": {
                                "brand": {"type": "string"},
                                "model": {"type": "string"},
                            },
                        },
                    },
                }
            },
            "title": "ProductList",
            "type": "object",
            "properties": {
                "products": {
                    "title": "Products",
                    "type": "array",
                    "items": {"$ref": "#/$defs/ProductSchema"},
                }
            },
        }
        
        request = GenerateSchemaRequest(
            user_prompt="Add warranty and color fields",
            existing_schema=complex_schema
        )
        assert request.user_prompt == "Add warranty and color fields"
        assert request.existing_schema == complex_schema

    def test_empty_user_prompt(self):
        """Test request with empty user prompt"""
        with pytest.raises(ValueError, match="user_prompt cannot be empty"):
            GenerateSchemaRequest(user_prompt="")

    def test_whitespace_only_user_prompt(self):
        """Test request with whitespace-only user prompt"""
        with pytest.raises(ValueError, match="user_prompt cannot be empty"):
            GenerateSchemaRequest(user_prompt="   ")

    def test_none_user_prompt(self):
        """Test request with None user prompt"""
        with pytest.raises(ValidationError):
            GenerateSchemaRequest(user_prompt=None)

    def test_user_prompt_trimming(self):
        """Test that user prompt is properly trimmed"""
        request = GenerateSchemaRequest(user_prompt="  Find laptops  ")
        assert request.user_prompt == "Find laptops"

    def test_model_serialization(self):
        """Test model serialization to dict"""
        request = GenerateSchemaRequest(
            user_prompt="Test prompt",
            existing_schema={"type": "object"}
        )
        
        serialized = request.model_dump()
        assert serialized["user_prompt"] == "Test prompt"
        assert serialized["existing_schema"] == {"type": "object"}

    def test_model_json_serialization(self):
        """Test model JSON serialization"""
        request = GenerateSchemaRequest(
            user_prompt="Test prompt",
            existing_schema={"type": "object"}
        )
        
        json_str = request.model_dump_json()
        parsed = json.loads(json_str)
        assert parsed["user_prompt"] == "Test prompt"
        assert parsed["existing_schema"] == {"type": "object"}

    def test_model_with_none_existing_schema_serialization(self):
        """Test model serialization when existing_schema is None"""
        request = GenerateSchemaRequest(user_prompt="Test prompt")
        
        serialized = request.model_dump()
        assert "existing_schema" not in serialized  # Should be excluded when None


class TestGetSchemaStatusRequest:
    """Test cases for GetSchemaStatusRequest model"""

    def test_valid_request_id(self):
        """Test valid UUID request ID"""
        valid_uuid = str(uuid4())
        request = GetSchemaStatusRequest(request_id=valid_uuid)
        assert request.request_id == valid_uuid

    def test_invalid_uuid_format(self):
        """Test invalid UUID format"""
        invalid_uuids = [
            "invalid-uuid",
            "123e4567-e89b-12d3-a456-42661417400",  # too short
            "123e4567-e89b-12d3-a456-4266141740000",  # too long
            "123e4567-e89b-12d3-a456-42661417400g",  # invalid character
            "123e4567-e89b-12d3-a456-42661417400G",  # invalid character
            "123e4567-e89b-12d3-a456-42661417400x",  # invalid character
        ]
        
        for invalid_uuid in invalid_uuids:
            with pytest.raises(ValueError, match="request_id must be a valid UUID"):
                GetSchemaStatusRequest(request_id=invalid_uuid)

    def test_empty_request_id(self):
        """Test empty request ID"""
        with pytest.raises(ValueError, match="request_id must be a valid UUID"):
            GetSchemaStatusRequest(request_id="")

    def test_whitespace_request_id(self):
        """Test whitespace-only request ID"""
        with pytest.raises(ValueError, match="request_id must be a valid UUID"):
            GetSchemaStatusRequest(request_id="   ")

    def test_none_request_id(self):
        """Test None request ID"""
        with pytest.raises(ValidationError):
            GetSchemaStatusRequest(request_id=None)

    def test_request_id_trimming(self):
        """Test that request ID is properly trimmed"""
        valid_uuid = str(uuid4())
        request = GetSchemaStatusRequest(request_id=f"  {valid_uuid}  ")
        assert request.request_id == valid_uuid

    def test_model_serialization(self):
        """Test model serialization to dict"""
        valid_uuid = str(uuid4())
        request = GetSchemaStatusRequest(request_id=valid_uuid)
        
        serialized = request.model_dump()
        assert serialized["request_id"] == valid_uuid

    def test_model_json_serialization(self):
        """Test model JSON serialization"""
        valid_uuid = str(uuid4())
        request = GetSchemaStatusRequest(request_id=valid_uuid)
        
        json_str = request.model_dump_json()
        parsed = json.loads(json_str)
        assert parsed["request_id"] == valid_uuid


class TestSchemaGenerationResponse:
    """Test cases for SchemaGenerationResponse model"""

    def test_minimal_response(self):
        """Test response with minimal required fields"""
        valid_uuid = str(uuid4())
        response = SchemaGenerationResponse(
            request_id=valid_uuid,
            status="completed",
            user_prompt="Test prompt"
        )
        
        assert response.request_id == valid_uuid
        assert response.status == "completed"
        assert response.user_prompt == "Test prompt"
        assert response.refined_prompt is None
        assert response.generated_schema is None
        assert response.error is None

    def test_full_response(self):
        """Test response with all fields populated"""
        valid_uuid = str(uuid4())
        generated_schema = {
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
        }
        
        response = SchemaGenerationResponse(
            request_id=valid_uuid,
            status="completed",
            user_prompt="Find laptops",
            refined_prompt="Find laptops with specifications",
            generated_schema=generated_schema,
            error=None,
            created_at="2024-01-01T00:00:00Z",
            updated_at="2024-01-01T00:00:00Z"
        )
        
        assert response.request_id == valid_uuid
        assert response.status == "completed"
        assert response.user_prompt == "Find laptops"
        assert response.refined_prompt == "Find laptops with specifications"
        assert response.generated_schema == generated_schema
        assert response.error is None
        assert response.created_at == "2024-01-01T00:00:00Z"
        assert response.updated_at == "2024-01-01T00:00:00Z"

    def test_response_with_error(self):
        """Test response with error field"""
        valid_uuid = str(uuid4())
        response = SchemaGenerationResponse(
            request_id=valid_uuid,
            status="failed",
            user_prompt="Test prompt",
            error="API rate limit exceeded"
        )
        
        assert response.status == "failed"
        assert response.error == "API rate limit exceeded"

    def test_response_status_values(self):
        """Test different status values"""
        valid_uuid = str(uuid4())
        valid_statuses = ["pending", "processing", "completed", "failed"]
        
        for status in valid_statuses:
            response = SchemaGenerationResponse(
                request_id=valid_uuid,
                status=status,
                user_prompt="Test prompt"
            )
            assert response.status == status

    def test_model_dump_excludes_none(self):
        """Test that model_dump excludes None values"""
        valid_uuid = str(uuid4())
        response = SchemaGenerationResponse(
            request_id=valid_uuid,
            status="completed",
            user_prompt="Test prompt"
        )
        
        dumped = response.model_dump()
        assert "request_id" in dumped
        assert "status" in dumped
        assert "user_prompt" in dumped
        assert "refined_prompt" not in dumped  # Should be excluded when None
        assert "generated_schema" not in dumped  # Should be excluded when None
        assert "error" not in dumped  # Should be excluded when None

    def test_model_dump_includes_non_none(self):
        """Test that model_dump includes non-None values"""
        valid_uuid = str(uuid4())
        response = SchemaGenerationResponse(
            request_id=valid_uuid,
            status="completed",
            user_prompt="Test prompt",
            refined_prompt="Refined prompt",
            generated_schema={"type": "object"}
        )
        
        dumped = response.model_dump()
        assert "refined_prompt" in dumped
        assert "generated_schema" in dumped

    def test_model_json_serialization(self):
        """Test model JSON serialization"""
        valid_uuid = str(uuid4())
        response = SchemaGenerationResponse(
            request_id=valid_uuid,
            status="completed",
            user_prompt="Test prompt",
            generated_schema={"type": "object"}
        )
        
        json_str = response.model_dump_json()
        parsed = json.loads(json_str)
        assert parsed["request_id"] == valid_uuid
        assert parsed["status"] == "completed"
        assert parsed["user_prompt"] == "Test prompt"
        assert parsed["generated_schema"] == {"type": "object"}

    def test_complex_generated_schema(self):
        """Test response with complex generated schema"""
        valid_uuid = str(uuid4())
        complex_schema = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "title": "Company Directory",
            "type": "object",
            "properties": {
                "company": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "industry": {"type": "string"},
                        "founded": {"type": "integer", "format": "year"},
                    },
                    "required": ["name", "industry"]
                },
                "departments": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "employees": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "name": {"type": "string"},
                                        "position": {"type": "string"},
                                        "email": {"type": "string", "format": "email"},
                                        "projects": {
                                            "type": "array",
                                            "items": {"type": "string"}
                                        }
                                    },
                                    "required": ["name", "position"]
                                }
                            }
                        },
                        "required": ["name", "employees"]
                    }
                }
            },
            "required": ["company", "departments"]
        }
        
        response = SchemaGenerationResponse(
            request_id=valid_uuid,
            status="completed",
            user_prompt="Create a company directory schema",
            generated_schema=complex_schema
        )
        
        assert response.generated_schema == complex_schema
        assert response.generated_schema["$schema"] == "http://json-schema.org/draft-07/schema#"
        assert "company" in response.generated_schema["properties"]
        assert "departments" in response.generated_schema["properties"]


class TestSchemaModelsIntegration:
    """Integration tests for schema models"""

    def test_workflow_with_models(self):
        """Test complete workflow using all models"""
        # Step 1: Create a schema generation request
        request = GenerateSchemaRequest(
            user_prompt="Find laptops with brand and price"
        )
        
        # Step 2: Simulate API response
        response = SchemaGenerationResponse(
            request_id=str(uuid4()),
            status="completed",
            user_prompt=request.user_prompt,
            generated_schema={
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
            }
        )
        
        # Step 3: Check status using the request ID
        status_request = GetSchemaStatusRequest(request_id=response.request_id)
        
        # Verify all models work together
        assert request.user_prompt == "Find laptops with brand and price"
        assert response.request_id == status_request.request_id
        assert response.status == "completed"
        assert response.generated_schema is not None

    def test_model_validation_chain(self):
        """Test validation chain across models"""
        # This should work without errors
        request = GenerateSchemaRequest(
            user_prompt="Test prompt",
            existing_schema={"type": "object"}
        )
        
        response = SchemaGenerationResponse(
            request_id=str(uuid4()),
            status="completed",
            user_prompt=request.user_prompt,
            generated_schema=request.existing_schema
        )
        
        status_request = GetSchemaStatusRequest(request_id=response.request_id)
        
        # All models should be valid
        assert request.user_prompt == "Test prompt"
        assert response.user_prompt == request.user_prompt
        assert status_request.request_id == response.request_id

