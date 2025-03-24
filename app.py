import streamlit as st
from src.databricks_client import DatabricksGenieClient
from src.chat_interface import ChatInterface
import config

def main():
    # Set page config
    st.set_page_config(
        page_title="Clinical Chatbot",
        page_icon="🏥",
        layout="wide"
    )
    
    # Initialize session state for chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # App header
    st.title("Clinical Chatbot")
    st.markdown("Ask medical questions and get responses powered by Databricks Genie")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("Configuration")
        api_key = st.text_input("Databricks API Key", type="password", 
                               value=st.session_state.get("api_key", ""))
        if api_key:
            st.session_state.api_key = api_key
        
        st.divider()
        st.markdown("### About")
        st.markdown("""
        This clinical chatbot uses Databricks Genie API to provide 
        clinically relevant information. Always consult with a healthcare 
        professional for medical advice.
        """)
    
    # Initialize the Databricks client
    try:
        # Use API key from session state or config
        api_key_to_use = api_key or config.DATABRICKS_API_KEY
        client = DatabricksGenieClient(api_key=api_key_to_use)
        chat_interface = ChatInterface(client)
    except Exception as e:
        st.error(f"Error initializing Databricks client: {str(e)}")
        st.warning("Please check your API key and configuration.")
        return
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Input field for new messages
    if prompt := st.chat_input("Ask a clinical question..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get response from Databricks Genie API
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = chat_interface.get_response(prompt)
                st.markdown(response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()