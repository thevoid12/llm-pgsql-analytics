import streamlit as st
from session_manager import RedisSessionManager
from llm import check_question_or_statement, generate_statement_response, identify_tables, generate_follow_up_question, identify_entities_and_columns, generate_sql_query
from models import ConfidenceLevel, MessageRole
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "data"))
from database_data import format_tables_for_llm,format_table_columns_for_llm

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
        conversation_history = st.session_state.session_manager.get_user_messages()
        conversation_history_with_sql = st.session_state.session_manager.get_conversation_history_with_sql()
        print(f"conversation_history_with_sql: {conversation_history_with_sql}") 
        print("*********************")
        input_classification = check_question_or_statement(prompt, conversation_history)
        print(f"input_classification: {input_classification}")
        print("*********************")
        
        st.session_state.session_manager.save_message(prompt, MessageRole.USER)
        
        if input_classification.type == "statement":
            response = generate_statement_response(prompt, input_classification.reasoning)
        else:
            tables_info = format_tables_for_llm()
            table_result = identify_tables(prompt, tables_info, conversation_history)
            
            if table_result.confidence == ConfidenceLevel.VERY_CONFIDENT:
                table_columns_info = format_table_columns_for_llm(table_result.tables)
                
                entity_column_result = identify_entities_and_columns(
                    user_question=prompt,
                    table_columns_info=table_columns_info,
                    conversation_history=conversation_history_with_sql
                )
                tables_from_entity_result = [tc.table for tc in entity_column_result]
                print(f"tables from entity result: {tables_from_entity_result}")
                print("*********************")
                full_table_schema = format_table_columns_for_llm(tables_from_entity_result)
                print(full_table_schema)
                sql_query = generate_sql_query(
                    user_question=prompt,
                    table_column_results=entity_column_result,
                    full_table_schema=full_table_schema,
                    conversation_history=conversation_history_with_sql
                )
                
                response_parts = [f"**Identified tables:** {', '.join(table_result.tables)}"]
                response_parts.append("\n**Columns and entities detected:**")
                
                for table_col in entity_column_result:
                    response_parts.append(f"\n`{table_col.table}`:")
                    for col_mapping in table_col.columns:
                        if col_mapping.entity_value:
                            response_parts.append(f"  - {col_mapping.column} = '{col_mapping.entity_value}'")
                        else:
                            response_parts.append(f"  - {col_mapping.column}")
                
                response_parts.append("\n\n**Generated SQL Query:**")
                response_parts.append(f"```sql\n{sql_query}\n```")
                
                response = "\n".join(response_parts)
                st.session_state.session_manager.save_message(response, MessageRole.AGENT, sql_content=sql_query)
            else:
                response = generate_follow_up_question(
                    user_question=prompt,
                    confidence=table_result.confidence.value,
                    possible_tables=table_result.tables,
                    reasoning=table_result.reasoning
                )
                st.session_state.session_manager.save_message(response, MessageRole.AGENT)
    
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
