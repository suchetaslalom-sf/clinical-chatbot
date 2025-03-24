# Clinical Chatbot

A Streamlit-based chatbot application that connects to Databricks Genie API to provide clinically relevant information.

## Features

- Interactive chat interface for asking clinical questions
- Integration with Databricks Genie API for medical AI responses
- Secure API key management
- Conversation history management
- Markdown formatting for responses

## Prerequisites

- Python 3.8+
- Databricks Workspace with Genie API access
- Databricks API key

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/clinical-chatbot.git
   cd clinical-chatbot
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file with your Databricks credentials:
   ```
   DATABRICKS_API_KEY=your_api_key_here
   DATABRICKS_WORKSPACE_URL=https://dbc-xxxxxxxx-xxxx.cloud.databricks.com
   DATABRICKS_GENIE_ENDPOINT=/api/2.0/genie/completions
   MODEL_NAME=genie-1-mistral
   MAX_TOKENS=2000
   TEMPERATURE=0.3
   DEBUG_MODE=False
   LOG_LEVEL=INFO
   ```

## Usage

Run the Streamlit application:

```bash
streamlit run app.py
```

Then open your browser and navigate to `http://localhost:8501`.
