import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.openai_service import OpenAIService
from unittest.mock import patch, AsyncMock

# Create a test client
client = TestClient(app)

# Test health check endpoint
def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

# Test root endpoint
def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "name" in response.json()
    assert "docs" in response.json()

# Test authentication
def test_login():
    response = client.post(
        "/api/v1/auth/token",
        data={
            "username": "testuser",
            "password": "testpassword"
        }
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

# Test login with wrong credentials
def test_login_wrong_credentials():
    response = client.post(
        "/api/v1/auth/token",
        data={
            "username": "testuser",
            "password": "wrongpassword"
        }
    )
    assert response.status_code == 401

# Test medical query endpoint with mocked OpenAI service
@pytest.mark.asyncio
async def test_medical_query():
    # Get token
    token_response = client.post(
        "/api/v1/auth/token",
        data={
            "username": "testuser",
            "password": "testpassword"
        }
    )
    token = token_response.json()["access_token"]
    
    # Test medical query
    with patch.object(OpenAIService, "process_medical_query", autospec=True) as mock_process:
        from datetime import datetime
        import uuid
        from app.models.schema import MedicalQueryResponse
        
        mock_response_id = str(uuid.uuid4())
        mock_response = MedicalQueryResponse(
            response_id=mock_response_id,
            response="This is a test response from the mocked OpenAI API.",
            disclaimer="MEDICAL DISCLAIMER: This is a test disclaimer.",
            model_used="gpt-4o",
            created_at=datetime.utcnow(),
            tokens_used=50
        )
        mock_process.return_value = mock_response
        
        response = client.post(
            "/api/v1/medical/query",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "patient_info": {
                    "age": 30,
                    "gender": "male",
                    "medical_history": ["hypertension"],
                    "current_medications": ["lisinopril"],
                    "symptoms": ["headache", "dizziness"]
                },
                "query": "What could be causing these symptoms?"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "response_id" in data
        assert "response" in data
        assert "disclaimer" in data
        assert "model_used" in data