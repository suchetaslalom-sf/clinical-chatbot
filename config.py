import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Databricks API configuration
DATABRICKS_API_KEY = os.getenv("DATABRICKS_API_KEY", "")
DATABRICKS_WORKSPACE_URL = os.getenv("DATABRICKS_WORKSPACE_URL", "https://dbc-xxxxxxxx-xxxx.cloud.databricks.com")
DATABRICKS_GENIE_ENDPOINT = os.getenv("DATABRICKS_GENIE_ENDPOINT", "/api/2.0/genie/completions")

# Model configuration
MODEL_NAME = os.getenv("MODEL_NAME", "genie-1-mistral")
MAX_TOKENS = int(os.getenv("MAX_TOKENS", 2000))
TEMPERATURE = float(os.getenv("TEMPERATURE", 0.3))

# Application settings
DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() == "true"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")