import streamlit as st
from session_manager import RedisSessionManager
from llm import check_question_or_statement, generate_statement_response, identify_tables
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "data"))
from database_data import format_tables_for_llm

st.title("Chat POC")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_manager" not in st.session_state:
    st.session_state.session_manager = RedisSessionManager()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What would you like to know?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    input_type = check_question_or_statement(prompt)
    
    st.session_state.session_manager.save_message(prompt)
    
    if "statement" in input_type:
        response = generate_statement_response(prompt)
    else:
        session_history = st.session_state.session_manager.get_session_history()
        conversation_history = []
        if session_history and session_history.messages:
            conversation_history = [msg.content for msg in session_history.messages[-5:]]
        
        tables_info = format_tables_for_llm()
        table_result = identify_tables(prompt, tables_info, conversation_history)
        
        response = f"Identified tables with {table_result.confidence.value} confidence: {', '.join(table_result.tables) if table_result.tables else 'None'}\n\nThis is a placeholder response. Full query implementation coming next!"
    
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
