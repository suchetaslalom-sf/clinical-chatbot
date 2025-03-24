import pytest
from unittest.mock import patch, MagicMock
import json
from src.databricks_client import DatabricksGenieClient

class TestDatabricksGenieClient:
    """Test cases for the DatabricksGenieClient class."""
    
    def test_init_raises_error_without_api_key(self):
        """Test that initialization raises an error without an API key."""
        with patch('config.DATABRICKS_API_KEY', ''):
            with pytest.raises(ValueError, match="Databricks API key is required"):
                DatabricksGenieClient()
    
    def test_init_with_api_key(self):
        """Test successful initialization with an API key."""
        client = DatabricksGenieClient(api_key="test_key")
        assert client.api_key == "test_key"
        assert "Authorization" in client.headers
        assert client.headers["Authorization"] == "Bearer test_key"
    
    @patch('requests.post')
    def test_generate_completion_success(self, mock_post):
        """Test successful API call to generate completion."""
        # Mock a successful API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [
                {
                    "text": "This is a test response"
                }
            ]
        }
        mock_post.return_value = mock_response
        
        client = DatabricksGenieClient(api_key="test_key")
        result = client.generate_completion("Test prompt")
        
        # Verify API was called with correct arguments
        mock_post.assert_called_once()
        assert result["choices"][0]["text"] == "This is a test response"
    
    @patch('requests.post')
    def test_generate_completion_error(self, mock_post):
        """Test error handling in generate_completion."""
        # Mock a failed API response
        mock_post.side_effect = Exception("API error")
        
        client = DatabricksGenieClient(api_key="test_key")
        with pytest.raises(Exception, match="Failed to get response from Databricks API"):
            client.generate_completion("Test prompt")
    
    def test_format_clinical_prompt(self):
        """Test clinical prompt formatting."""
        client = DatabricksGenieClient(api_key="test_key")
        prompt = "What are the symptoms of diabetes?"
        formatted = client._format_clinical_prompt(prompt)
        
        assert "QUESTION: What are the symptoms of diabetes?" in formatted
        assert "ANSWER:" in formatted
    
    def test_extract_response_text_with_choices(self):
        """Test extracting text from response with choices format."""
        client = DatabricksGenieClient(api_key="test_key")
        api_response = {
            "choices": [
                {
                    "text": "  Response with whitespace  "
                }
            ]
        }
        
        text = client.extract_response_text(api_response)
        assert text == "Response with whitespace"
    
    def test_extract_response_text_with_result(self):
        """Test extracting text from response with result format."""
        client = DatabricksGenieClient(api_key="test_key")
        api_response = {
            "result": "  Response with result key  "
        }
        
        text = client.extract_response_text(api_response)
        assert text == "Response with result key"
    
    def test_extract_response_text_unknown_format(self):
        """Test extracting text from unknown response format."""
        client = DatabricksGenieClient(api_key="test_key")
        api_response = {
            "unknown_key": "value"
        }
        
        text = client.extract_response_text(api_response)
        assert "Sorry, I couldn't process that request" in text