import streamlit as st
from session_manager import RedisSessionManager
from llm import check_question_or_statement, generate_statement_response, identify_tables, generate_follow_up_question
from models import ConfidenceLevel
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
    
    with st.spinner("Processing your request..."):
        input_classification = check_question_or_statement(prompt)
        print(f"input_classification: {input_classification}")
        st.session_state.session_manager.save_message(prompt)
        
        if input_classification.type == "statement":
            response = generate_statement_response(prompt, input_classification.reasoning)
        else:
            session_history = st.session_state.session_manager.get_session_history()
            conversation_history = []
            if session_history and session_history.messages:
                conversation_history = [msg.content for msg in session_history.messages[-5:]]
            
            tables_info = format_tables_for_llm()
            table_result = identify_tables(prompt, tables_info, conversation_history)
            
            if table_result.confidence == ConfidenceLevel.VERY_CONFIDENT:
                response = f"Identified tables: {', '.join(table_result.tables)}\n\nThis is a placeholder response. Full query implementation coming next!"
            else:
                response = generate_follow_up_question(
                    user_question=prompt,
                    confidence=table_result.confidence.value,
                    possible_tables=table_result.tables
                )
        
        st.session_state.session_manager.save_message(response)
    
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
