from typing import Any, Dict, List
from fastapi import APIRouter, Depends, HTTPException, status
from loguru import logger

from app.models.schema import MedicalQueryRequest, MedicalQueryResponse, FeedbackRequest, User
from app.services.openai_service import OpenAIService
from app.core.security import get_current_active_user

router = APIRouter()
openai_service = OpenAIService()

@router.post("/query", response_model=MedicalQueryResponse)
async def process_medical_query(
    query: MedicalQueryRequest,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Process a medical query using the OpenAI service.
    
    This endpoint accepts a medical query with patient information and returns an AI-generated
    response. It requires authentication and all requests are logged.
    
    Args:
        query (MedicalQueryRequest): The medical query containing patient information and the question.
        current_user (User): The authenticated user making the request (automatically provided by dependency).
        
    Returns:
        MedicalQueryResponse: A structured response containing the AI-generated medical advice,
            a disclaimer, model information, and usage statistics.
            
    Raises:
        HTTPException: 500 error if there's an issue processing the query.
        
    Examples:
        ```
        # Request
        POST /api/v1/medical/query
        
        {
          "patient_info": {
            "age": 42,
            "gender": "male",
            "medical_history": ["hypertension"],
            "current_medications": ["lisinopril 10mg daily"],
            "symptoms": ["headache", "dizziness"]
          },
          "query": "Could these symptoms be related to blood pressure medication?",
          "additional_context": "Patient reports symptoms occur about 1 hour after taking medication"
        }
        
        # Response
        {
          "response_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
          "response": "Yes, headache and dizziness can be side effects of lisinopril...",
          "disclaimer": "MEDICAL DISCLAIMER: This information is provided by an AI assistant...",
          "model_used": "gpt-4o-mini",
          "created_at": "2025-03-24T18:25:43.511Z",
          "tokens_used": 450
        }
        ```
    """
    try:
        logger.info(f"Medical query received from user: {current_user.username}")
        response = await openai_service.process_medical_query(query)
        logger.info(f"Medical query processed successfully, response ID: {response.response_id}")
        return response
    except Exception as e:
        logger.error(f"Error processing medical query: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing medical query: {str(e)}",
        )

@router.post("/query_demo", response_model=MedicalQueryResponse)
async def process_medical_query_demo(query: MedicalQueryRequest) -> Any:
    """
    Process a medical query without authentication (FOR TESTING ONLY).
    
    This endpoint accepts a medical query with patient information and returns an AI-generated
    response. It does NOT require authentication and should only be used for testing purposes.
    
    WARNING: This endpoint should be disabled in production environments as it bypasses 
    authentication and could lead to unauthorized API usage.
    
    Args:
        query (MedicalQueryRequest): The medical query containing patient information and the question.
        
    Returns:
        MedicalQueryResponse: A structured response containing the AI-generated medical advice,
            a disclaimer, model information, and usage statistics.
            
    Raises:
        HTTPException: 500 error if there's an issue processing the query.
    """
    try:
        logger.warning("Demo endpoint (no auth) used for medical query - FOR TESTING ONLY")
        response = await openai_service.process_medical_query(query)
        logger.info(f"Demo medical query processed successfully, response ID: {response.response_id}")
        return response
    except Exception as e:
        logger.error(f"Error processing demo medical query: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing medical query: {str(e)}",
        )

@router.get("/test", response_model=Dict[str, str])
async def test_medical_api() -> Dict[str, str]:
    """
    Simple test endpoint to check if the medical API is running.
    This endpoint doesn't require authentication and is useful for checking API connectivity.
    """
    return {"status": "ok", "message": "Medical API is running"}

@router.post("/feedback", status_code=status.HTTP_201_CREATED)
async def submit_response_feedback(
    feedback: FeedbackRequest,
    current_user: User = Depends(get_current_active_user)
) -> Dict[str, str]:
    """
    Submit feedback for a medical response.
    
    This endpoint allows users to provide feedback on AI-generated medical responses.
    Feedback helps improve the quality and safety of the AI system. Harmful feedback
    is logged with higher urgency for immediate review.
    
    Args:
        feedback (FeedbackRequest): The feedback information, including response ID, feedback type,
            optional rating, and optional comments.
        current_user (User): The authenticated user submitting the feedback (automatically provided by dependency).
        
    Returns:
        Dict[str, str]: A confirmation message with the status and response ID.
        
    Raises:
        HTTPException: 500 error if there's an issue submitting the feedback.
        
    Examples:
        ```
        # Request
        POST /api/v1/medical/feedback
        
        {
          "response_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
          "feedback_type": "helpful",
          "rating": 5,
          "comment": "Provided clear information on medication side effects"
        }
        
        # Response
        {
          "status": "Feedback submitted successfully",
          "response_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
        }
        ```
    """
    try:
        # In a real implementation, this would store the feedback in a database
        logger.info(
            f"Feedback received from user {current_user.username} for response {feedback.response_id}: "
            f"Type: {feedback.feedback_type}, Rating: {feedback.rating}"
        )
        
        # Process harmful feedback with higher urgency
        if feedback.feedback_type == "harmful":
            logger.warning(
                f"HARMFUL FEEDBACK reported for response {feedback.response_id}. "
                f"Comment: {feedback.comment}"
            )
        
        return {"status": "Feedback submitted successfully", "response_id": feedback.response_id}
    except Exception as e:
        logger.error(f"Error submitting feedback: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error submitting feedback: {str(e)}",
        )