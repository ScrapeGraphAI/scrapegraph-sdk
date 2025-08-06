"""
Utility functions for tests
"""
import uuid


def generate_mock_api_key() -> str:
    """Generate a mock API key for testing purposes"""
    # Generate a realistic looking API key format: sgai-{uuid}
    mock_uuid = str(uuid.uuid4()).replace('-', '')
    return f"sgai-{mock_uuid}"