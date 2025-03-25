# Leo Medical Assistant API

A secure and compliant API for integrating OpenAI's large language models into healthcare applications.

## Project Overview

The Leo Medical Assistant API helps healthcare providers quickly access AI-generated medical insights for patient care. It serves as an interface between healthcare applications and OpenAI's large language models, processing patient information to generate medically relevant responses while maintaining data privacy and regulatory compliance.

## Features

- **Secure Authentication**: OAuth2 with JWT tokens
- **Comprehensive Logging**: Detailed logging for audit trails and debugging
- **Rate Limiting**: Prevent API abuse
- **Medical Context Handling**: Process patient information and format prompts appropriately
- **Response Validation**: Ensuring appropriate medical disclaimers and content filtering
- **Feedback System**: Allow providers to rate and report responses

## Tech Stack

- **Framework**: FastAPI
- **Validation**: Pydantic
- **Documentation**: OpenAPI/Swagger
- **Authentication**: OAuth2 with JWT
- **LLM Provider**: OpenAI API
- **Logging**: Loguru

## Getting Started

### Prerequisites

- Python 3.9+
- OpenAI API key

### Installation

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the project root with the following variables:
   ```
   OPENAI_API_KEY=your_openai_api_key
   SECRET_KEY=your_secret_key
   OPENAI_MODEL=gpt-4o-mini (example)
   LOG_LEVEL=WARNING
   ```

### Running the API

```
python run.py
```

The API will be available at http://localhost:8000

API documentation can be accessed at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Authentication

- `POST /api/v1/auth/token` - Get access token

### Medical Queries

- `POST /api/v1/medical/query` - Process a medical query
- `POST /api/v1/medical/feedback` - Submit feedback for a response

### Utilities

- `GET /health` - Health check endpoint
- `GET /` - API information

## Testing

Run tests with:

```
pytest
```

## Security Considerations

- All medical data is processed in memory and not stored
- Sensitive information is filtered from logs
- Access is controlled via JWT tokens
- Medical disclaimers are included with all responses

## License

[MIT License](LICENSE)

