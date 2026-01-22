import streamlit as st
from llm import hello_check


def main():
    st.title("Chat POC")
    st.write("Hello from chat-poc!")
    
    if st.button("Test LLM Connection"):
        with st.spinner("Getting response from LLM..."):
            try:
                response = hello_check()
                st.success("LLM Response:")
                st.write(response)
            except Exception as e:
                st.error(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
