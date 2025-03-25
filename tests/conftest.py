import sys
import os
import pytest
from unittest.mock import patch
from datetime import datetime

# Add the project root directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Mock the openai module for tests
@pytest.fixture(autouse=True)
def mock_openai():
    with patch('openai.chat.completions.create') as mock_create:
        mock_create.return_value.choices = [
            type('obj', (object,), {
                'message': type('obj', (object,), {
                    'content': 'This is a test response from the mocked OpenAI API.'
                })
            })
        ]
        mock_create.return_value.usage = type('obj', (object,), {
            'total_tokens': 50
        })
        yield mock_create