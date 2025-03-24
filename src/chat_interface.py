import logging
from typing import List, Dict, Any, Optional
from src.databricks_client import DatabricksGenieClient
import config

# Configure logging
logging.basicConfig(level=getattr(logging, config.LOG_LEVEL))
logger = logging.getLogger(__name__)

class ChatInterface:
    """Handles chat interaction logic and message history management."""
    
    def __init__(self, databricks_client: DatabricksGenieClient):
        """
        Initialize the chat interface.
        
        Args:
            databricks_client: An initialized Databricks Genie client
        """
        self.client = databricks_client
        self.history: List[Dict[str, str]] = []
    
    def get_response(self, user_message: str) -> str:
        """
        Get a response from the Databricks Genie API for the user message.
        
        Args:
            user_message: The user's input message
            
        Returns:
            The model's response text
        """
        # Add the user message to history
        self.history.append({"role": "user", "content": user_message})
        
        try:
            # Create context with recent conversation history
            context = self._create_context()
            
            # Get response from the model
            response = self.client.generate_completion(context)
            response_text = self.client.extract_response_text(response)
            
            # Add the assistant's response to history
            self.history.append({"role": "assistant", "content": response_text})
            
            return response_text
        
        except Exception as e:
            logger.error(f"Error getting response: {str(e)}")
            error_msg = "I'm sorry, I encountered an error processing your request. Please try again."
            self.history.append({"role": "assistant", "content": error_msg})
            return error_msg
    
    def _create_context(self, max_history: int = 5) -> str:
        """
        Create a prompt context incorporating recent conversation history.
        
        Args:
            max_history: Maximum number of recent messages to include
            
        Returns:
            A formatted prompt string with conversation context
        """
        # Get recent history (limited to max_history messages)
        recent_history = self.history[-max_history*2:] if len(self.history) > 0 else []
        
        # Format the context with conversation history
        context = "The following is a conversation with a clinical assistant.\n\n"
        
        for message in recent_history:
            role = "User" if message["role"] == "user" else "Assistant"
            context += f"{role}: {message['content']}\n\n"
        
        # If the last message was from the user, we don't need to add anything else
        # If the last message was from the assistant, we need to add a user message placeholder
        if len(recent_history) > 0 and recent_history[-1]["role"] == "assistant":
            context += "User: "
        
        return context
    
    def clear_history(self) -> None:
        """Clear the conversation history."""
        self.history = []