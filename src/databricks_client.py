import requests
import json
import logging
from typing import Dict, Any, Optional
import config

# Configure logging
logging.basicConfig(level=getattr(logging, config.LOG_LEVEL))
logger = logging.getLogger(__name__)

class DatabricksGenieClient:
    """Client for interacting with the Databricks Genie API."""
    
    def __init__(self, 
                 api_key: Optional[str] = None, 
                 workspace_url: Optional[str] = None,
                 endpoint: Optional[str] = None):
        """
        Initialize the Databricks Genie client.
        
        Args:
            api_key: Databricks API key
            workspace_url: Databricks workspace URL
            endpoint: Genie API endpoint
        """
        self.api_key = api_key or config.DATABRICKS_API_KEY
        self.workspace_url = workspace_url or config.DATABRICKS_WORKSPACE_URL
        self.endpoint = endpoint or config.DATABRICKS_GENIE_ENDPOINT
        
        if not self.api_key:
            raise ValueError("Databricks API key is required")
        
        self.base_url = f"{self.workspace_url.rstrip('/')}/{self.endpoint.lstrip('/')}";
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def generate_completion(self, 
                           prompt: str, 
                           model: Optional[str] = None,
                           max_tokens: Optional[int] = None,
                           temperature: Optional[float] = None) -> Dict[str, Any]:
        """
        Generate a completion using the Databricks Genie API.
        
        Args:
            prompt: The input text prompt
            model: The model to use for completion
            max_tokens: Maximum number of tokens to generate
            temperature: Sampling temperature
            
        Returns:
            The API response as a dictionary
        """
        model = model or config.MODEL_NAME
        max_tokens = max_tokens or config.MAX_TOKENS
        temperature = temperature or config.TEMPERATURE
        
        payload = {
            "model": model,
            "prompt": self._format_clinical_prompt(prompt),
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        if config.DEBUG_MODE:
            logger.debug(f"Request payload: {json.dumps(payload, indent=2)}")
        
        try:
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()
            result = response.json()
            
            if config.DEBUG_MODE:
                logger.debug(f"Response: {json.dumps(result, indent=2)}")
                
            return result
        
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Response status: {e.response.status_code}")
                logger.error(f"Response body: {e.response.text}")
            
            raise Exception(f"Failed to get response from Databricks API: {str(e)}")
    
    def _format_clinical_prompt(self, prompt: str) -> str:
        """
        Format the prompt for clinical context.
        
        Args:
            prompt: The user's input prompt
            
        Returns:
            Formatted prompt with clinical context
        """
        return f"""
You are a clinical assistant providing information based on medical knowledge.
Always indicate when information is uncertain and recommend consulting healthcare professionals.

QUESTION: {prompt}

ANSWER:
"""

    def extract_response_text(self, api_response: Dict[str, Any]) -> str:
        """
        Extract the generated text from the API response.
        
        Args:
            api_response: The raw API response
            
        Returns:
            The extracted generated text
        """
        try:
            # This may need to be adjusted based on the actual Databricks Genie API response format
            if "choices" in api_response and len(api_response["choices"]) > 0:
                return api_response["choices"][0]["text"].strip()
            elif "result" in api_response:
                return api_response["result"].strip()
            else:
                logger.warning(f"Unexpected API response format: {api_response}")
                return "Sorry, I couldn't process that request. Please try again."
        
        except (KeyError, IndexError, AttributeError) as e:
            logger.error(f"Error extracting response text: {str(e)}")
            return "Sorry, there was an error processing the response."