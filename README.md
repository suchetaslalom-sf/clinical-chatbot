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

## Project Structure

```
clinical-chatbot/
├── README.md
├── requirements.txt
├── .gitignore
├── app.py
├── config.py
├── src/
│   ├── __init__.py
│   ├── databricks_client.py
│   ├── chat_interface.py
│   └── utils.py
└── tests/
    ├── __init__.py
    ├── test_databricks_client.py
    └── test_chat_interface.py
```

## Development

### Running Tests

```bash
pytest
```

### Adding New Features

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This application is for informational purposes only and is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.