import openai
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional
from app.core.config import settings
from app.models.schema import MedicalQueryRequest, MedicalQueryResponse, Message, Role
from loguru import logger

class OpenAIService:
    """Service for handling interactions with the OpenAI API.
    
    This service encapsulates all interactions with the OpenAI API for medical queries,
    including formatting patient information, preparing message payloads, and processing
    responses. It ensures consistent handling of medical disclaimers and response formatting.
    
    Attributes:
        _disclaimer (str): Medical disclaimer text to be included with all responses.
    
    Examples:
        >>> service = OpenAIService()
        >>> request = MedicalQueryRequest(patient_info=PatientInfo(age=45), query="What causes hypertension?")
        >>> response = await service.process_medical_query(request)
    """
    
    def __init__(self):
        """Initialize the OpenAI service with default settings.
        
        Sets up the medical disclaimer text that will be included with all responses.
        """
        self._disclaimer = """
MEDICAL DISCLAIMER: For informational purposes only. Not a substitute for professional medical advice, diagnosis, or treatment. Consult qualified healthcare professionals for medical concerns.
"""

    def _create_system_prompt(self) -> str:
        """Create the system prompt for the OpenAI model.
        
        Returns:
            str: A system prompt that defines the AI assistant's behavior and response guidelines
                for medical queries.
        
        Note:
            The system prompt establishes guidelines for the AI to follow when generating
            responses to medical queries, emphasizing evidence-based information and caution.
        """
        return """You are an emergency room physician responding to a consult. 
Your responses should be:
1. Concise and direct (10-12 sentences maximum)
2. Evidence-based with facts and numbers when applicable
3. Focused on most likely diagnoses and immediate next steps
4. Organized in a logical sequence like an ER assessment
5. Free of bullet points or extensive formatting

RESPONSE GUIDELINES:
- Start with your immediate assessment of the most likely diagnosis/condition
- Provide specific reasoning based on patient data (labs, vitals, symptoms)
- Include brief differential diagnosis only for key competing possibilities
- Recommend specific next steps with clear priorities
- Be direct - avoid hedging language and unnecessary qualifiers
- Use complete sentences, not fragmentary bullet points
- Include dosing where appropriate (e.g., "Start 325mg ASA now")
- Avoid lengthy educational explanations - focus on the case at hand

STYLE EXAMPLES:
- Too wordy: "The patient could potentially have several possible conditions including..."
- Better: "This is acute coronary syndrome based on chest pain, ST depression, and elevated troponin."

- Too vague: "Consider starting appropriate cardiac medications."
- Better: "Start aspirin 325mg, sublingual nitroglycerin 0.4mg, and IV metoprolol 5mg."

- Too educational: "Asthma exacerbations are characterized by bronchospasm which occurs when..."
- Better: "Moderate asthma exacerbation requiring albuterol 2.5mg + ipratropium 0.5mg via nebulizer."

DO NOT provide definitive guarantees about outcomes. 
DO NOT use first person plural ("we recommend").
DO NOT include long explanations of pathophysiology.
DO NOT add disclaimers at the end of your response.
"""

    def _format_patient_info(self, patient_info: Dict[str, Any]) -> str:
        """Format patient information into a readable string.
        
        Args:
            patient_info (Dict[str, Any]): Dictionary containing patient information fields.
                Expected keys include 'age', 'gender', 'medical_history', 'current_medications',
                'symptoms', and 'vitals'.
        
        Returns:
            str: Formatted string containing all provided patient information.
            
        Examples:
            >>> patient_info = {
            ...     "age": 45,
            ...     "gender": "male",
            ...     "medical_history": ["hypertension", "type 2 diabetes"],
            ...     "current_medications": ["metformin", "lisinopril"],
            ... }
            >>> formatted = service._format_patient_info(patient_info)
            >>> print(formatted)
            PATIENT INFORMATION:
            Age: 45
            Gender: male
            Medical History:
            - hypertension
            - type 2 diabetes
            Current Medications:
            - metformin
            - lisinopril
        """
        formatted = "PATIENT INFORMATION:\n"
        
        if patient_info.get("age"):
            formatted += f"Age: {patient_info['age']}\n"
        
        if patient_info.get("gender"):
            formatted += f"Gender: {patient_info['gender']}\n"
        
        if patient_info.get("medical_history"):
            formatted += "Medical History:\n"
            for item in patient_info["medical_history"]:
                formatted += f"- {item}\n"
        
        if patient_info.get("current_medications"):
            formatted += "Current Medications:\n"
            for med in patient_info["current_medications"]:
                formatted += f"- {med}\n"
        
        if patient_info.get("symptoms"):
            formatted += "Current Symptoms:\n"
            for symptom in patient_info["symptoms"]:
                formatted += f"- {symptom}\n"
        
        if patient_info.get("vitals"):
            formatted += "Vitals:\n"
            for key, value in patient_info["vitals"].items():
                formatted += f"- {key}: {value}\n"
        
        return formatted
    
    def _prepare_messages(self, query_request: MedicalQueryRequest) -> List[Dict[str, str]]:
        """Prepare messages for the OpenAI API from a medical query request.
        
        Args:
            query_request (MedicalQueryRequest): The medical query request object containing
                patient information, query, and optional conversation history.
                
        Returns:
            List[Dict[str, str]]: A list of message dictionaries formatted for the OpenAI API,
                with 'role' and 'content' keys.
                
        Note:
            The returned messages include:
            1. A system message with guidelines for the AI
            2. Any previous conversation history messages
            3. A user message with formatted patient information and the current query
            
        Examples:
            >>> request = MedicalQueryRequest(
            ...     patient_info=PatientInfo(age=65, gender="female"),
            ...     query="What are the risks of statins for elderly patients?",
            ...     conversation_history=[]
            ... )
            >>> messages = service._prepare_messages(request)
            >>> len(messages) # System message + user query
            2
        """
        messages = [{"role": "system", "content": self._create_system_prompt()}]
        
        # Add conversation history if it exists
        if query_request.conversation_history:
            for msg in query_request.conversation_history:
                messages.append({"role": msg.role.value, "content": msg.content})
        
        # Format patient info and query
        patient_info = self._format_patient_info(query_request.patient_info.model_dump(exclude_none=True))
        
        query_content = f"{patient_info}\n\nMEDICAL QUERY: {query_request.query}"
        
        if query_request.additional_context:
            query_content += f"\n\nADDITIONAL CONTEXT: {query_request.additional_context}"
        
        messages.append({"role": "user", "content": query_content})
        
        return messages
    
    async def process_medical_query(self, query_request: MedicalQueryRequest) -> MedicalQueryResponse:
        """Process a medical query and return an AI-generated response.
        
        This method is the main interface for medical query processing. It takes a structured
        request, formats it appropriately, sends it to the OpenAI API, and processes the response
        into a standardized MedicalQueryResponse object.
        
        Args:
            query_request (MedicalQueryRequest): A medical query request object containing patient
                information, the query, and optional additional context.
                
        Returns:
            MedicalQueryResponse: A structured response containing the AI-generated medical advice,
                a disclaimer, model information, and usage statistics.
                
        Raises:
            Exception: Any exceptions encountered during API communication or response processing
                are logged and re-raised.
                
        Examples:
            >>> request = MedicalQueryRequest(
            ...     patient_info=PatientInfo(
            ...         age=42,
            ...         gender="male",
            ...         medical_history=["asthma"],
            ...         symptoms=["shortness of breath", "chest tightness"]
            ...     ),
            ...     query="Could these symptoms indicate a COVID-19 infection?"
            ... )
            >>> response = await service.process_medical_query(request)
            >>> print(f"Model used: {response.model_used}")
            Model used: gpt-4o-mini
            >>> print(f"Response ID: {response.response_id}")
            Response ID: 3fa85f64-5717-4562-b3fc-2c963f66afa6
        """
        try:
            messages = self._prepare_messages(query_request)
            model = query_request.model or settings.OPENAI_MODEL
            
            logger.info(f"Sending request to OpenAI using model: {model}")
            
            # Import the async OpenAI client
            from openai import AsyncOpenAI
            
            # Create an async client instance
            client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
            
            # Use the async client to create chat completions
            response = await client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.3,  # Lower temperature for more conservative medical responses
                max_tokens=1000,
            )
            
            # Extract response content
            response_content = response.choices[0].message.content
            tokens_used = response.usage.total_tokens if hasattr(response, 'usage') else None
            
            # Create response with disclaimer
            medical_response = MedicalQueryResponse(
                response_id=str(uuid.uuid4()),
                response=response_content,
                disclaimer=self._disclaimer.strip(),
                model_used=model,
                created_at=datetime.utcnow(),
                tokens_used=tokens_used
            )
            
            return medical_response
        
        except Exception as e:
            logger.error(f"Error processing medical query: {str(e)}")
            raise