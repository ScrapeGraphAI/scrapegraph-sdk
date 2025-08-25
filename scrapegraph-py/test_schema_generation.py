#!/usr/bin/env python3
"""
Simple test for schema generation functionality.

This script tests the basic schema generation models and client methods.
"""

import json
from scrapegraph_py.models.schema import (
    GenerateSchemaRequest,
    GetSchemaStatusRequest,
    SchemaGenerationResponse,
)


def test_schema_models():
    """Test the schema generation models"""
    print("🧪 Testing Schema Generation Models...")
    
    # Test GenerateSchemaRequest
    print("\n1. Testing GenerateSchemaRequest...")
    try:
        request = GenerateSchemaRequest(
            user_prompt="Find laptops with brand, processor, and RAM"
        )
        print("✅ GenerateSchemaRequest created successfully")
        print(f"   User prompt: {request.user_prompt}")
        print(f"   Existing schema: {request.existing_schema}")
        
        # Test with existing schema
        existing_schema = {"type": "object", "properties": {"name": {"type": "string"}}}
        request_with_schema = GenerateSchemaRequest(
            user_prompt="Add price field",
            existing_schema=existing_schema
        )
        print("✅ GenerateSchemaRequest with existing schema created successfully")
        
    except Exception as e:
        print(f"❌ Error creating GenerateSchemaRequest: {e}")
        return False

    # Test GetSchemaStatusRequest
    print("\n2. Testing GetSchemaStatusRequest...")
    try:
        status_request = GetSchemaStatusRequest(
            request_id="123e4567-e89b-12d3-a456-426614174000"
        )
        print("✅ GetSchemaStatusRequest created successfully")
        print(f"   Request ID: {status_request.request_id}")
        
    except Exception as e:
        print(f"❌ Error creating GetSchemaStatusRequest: {e}")
        return False

    # Test SchemaGenerationResponse
    print("\n3. Testing SchemaGenerationResponse...")
    try:
        response_data = {
            "request_id": "123e4567-e89b-12d3-a456-426614174000",
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
                                "processor": {"type": "string"},
                                "ram": {"type": "string"}
                            }
                        }
                    }
                }
            }
        }
        
        response = SchemaGenerationResponse(**response_data)
        print("✅ SchemaGenerationResponse created successfully")
        print(f"   Request ID: {response.request_id}")
        print(f"   Status: {response.status}")
        print(f"   Has generated schema: {response.generated_schema is not None}")
        
        # Test model_dump
        dumped = response.model_dump()
        print("✅ model_dump() works correctly")
        print(f"   Dumped keys: {list(dumped.keys())}")
        
    except Exception as e:
        print(f"❌ Error creating SchemaGenerationResponse: {e}")
        return False

    print("\n🎉 All schema model tests passed!")
    return True


def test_schema_validation():
    """Test schema validation rules"""
    print("\n🧪 Testing Schema Validation Rules...")
    
    # Test empty user_prompt
    print("\n1. Testing empty user_prompt validation...")
    try:
        GenerateSchemaRequest(user_prompt="")
        print("❌ Should have failed with empty user_prompt")
        return False
    except ValueError as e:
        print(f"✅ Correctly caught empty user_prompt: {e}")
    
    # Test invalid UUID in GetSchemaStatusRequest
    print("\n2. Testing invalid UUID validation...")
    try:
        GetSchemaStatusRequest(request_id="invalid-uuid")
        print("❌ Should have failed with invalid UUID")
        return False
    except ValueError as e:
        print(f"✅ Correctly caught invalid UUID: {e}")
    
    print("\n🎉 All validation tests passed!")
    return True


def main():
    """Run all tests"""
    print("🚀 Schema Generation Test Suite")
    print("=" * 50)
    
    # Test models
    if not test_schema_models():
        print("\n❌ Model tests failed!")
        return
    
    # Test validation
    if not test_schema_validation():
        print("\n❌ Validation tests failed!")
        return
    
    print("\n🎉 All tests passed successfully!")
    print("\n📋 Summary:")
    print("   ✅ GenerateSchemaRequest model works")
    print("   ✅ GetSchemaStatusRequest model works")
    print("   ✅ SchemaGenerationResponse model works")
    print("   ✅ Validation rules work correctly")
    print("   ✅ Model serialization works")


if __name__ == "__main__":
    main()
