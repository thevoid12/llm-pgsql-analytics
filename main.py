import streamlit as st
from session_manager import RedisSessionManager
from llm import check_question_or_statement, generate_statement_response

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
        response = "This is a hardcoded response. I'm here to help you!"
    
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
