import pytest
from unittest.mock import patch, MagicMock
from src.chat_interface import ChatInterface
from src.databricks_client import DatabricksGenieClient

class TestChatInterface:
    """Test cases for the ChatInterface class."""
    
    @pytest.fixture
    def mock_client(self):
        """Create a mock Databricks client for testing."""
        client = MagicMock(spec=DatabricksGenieClient)
        client.generate_completion.return_value = {
            "choices": [
                {
                    "text": "Test response"
                }
            ]
        }
        client.extract_response_text.return_value = "Test response"
        return client
    
    def test_init(self, mock_client):
        """Test initialization of ChatInterface."""
        interface = ChatInterface(mock_client)
        assert interface.client == mock_client
        assert interface.history == []
    
    def test_get_response_success(self, mock_client):
        """Test successful response generation."""
        interface = ChatInterface(mock_client)
        response = interface.get_response("Test question")
        
        # Verify client methods were called
        mock_client.generate_completion.assert_called_once()
        mock_client.extract_response_text.assert_called_once()
        
        # Verify response and history update
        assert response == "Test response"
        assert len(interface.history) == 2
        assert interface.history[0]["role"] == "user"
        assert interface.history[0]["content"] == "Test question"
        assert interface.history[1]["role"] == "assistant"
        assert interface.history[1]["content"] == "Test response"
    
    def test_get_response_error(self, mock_client):
        """Test error handling in get_response."""
        mock_client.generate_completion.side_effect = Exception("Test error")
        
        interface = ChatInterface(mock_client)
        response = interface.get_response("Test question")
        
        # Verify error handling and history update
        assert "I'm sorry, I encountered an error" in response
        assert len(interface.history) == 2
        assert interface.history[0]["role"] == "user"
        assert interface.history[1]["role"] == "assistant"
        assert "I'm sorry, I encountered an error" in interface.history[1]["content"]
    
    def test_create_context(self, mock_client):
        """Test context creation with conversation history."""
        interface = ChatInterface(mock_client)
        
        # Add some messages to history
        interface.history = [
            {"role": "user", "content": "Question 1"},
            {"role": "assistant", "content": "Answer 1"},
            {"role": "user", "content": "Question 2"}
        ]
        
        context = interface._create_context()
        
        # Verify context format
        assert "The following is a conversation with a clinical assistant" in context
        assert "User: Question 1" in context
        assert "Assistant: Answer 1" in context
        assert "User: Question 2" in context
    
    def test_clear_history(self, mock_client):
        """Test history clearing."""
        interface = ChatInterface(mock_client)
        
        # Add some messages to history
        interface.history = [
            {"role": "user", "content": "Test"},
            {"role": "assistant", "content": "Response"}
        ]
        
        interface.clear_history()
        assert interface.history == []