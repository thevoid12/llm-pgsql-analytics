import os
from openai import AzureOpenAI
from dotenv import load_dotenv
from prompt import RELEVANT_QUESTION_CHECKER_USR, STATEMENT_RESPONSE_USR, IDENTIFY_TABLE_USR, FOLLOW_UP_TABLE_USR, IDENTIFY_ENTITIES_COLUMNS_USR
from models import TableIdentificationResponse, ConfidenceLevel, InputClassification, TableColumnResponse, EntityColumnDetectionResponse
from typing import List

load_dotenv()

def get_llm_client():
    client = AzureOpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        api_version=os.getenv("OPENAI_API_VERSION"),
        azure_endpoint=os.getenv("OPENAI_API_BASE")
    )
    return client

def hello_check():
    client = get_llm_client()
    model = os.getenv("MODEL")
    
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": "Say hello!"}
        ]
    )
    
    return response.choices[0].message.content

def check_question_or_statement(user_input: str, conversation_history: List[str] = None) -> InputClassification:
    client = get_llm_client()
    model = os.getenv("MODEL")
    
    if conversation_history is None:
        conversation_history = []
    
    history_text = str(conversation_history) if conversation_history else "[]"
    
    prompt = RELEVANT_QUESTION_CHECKER_USR.format(
        context=user_input,
        conversation_history=history_text
    )
    
    try:
        completion = client.beta.chat.completions.parse(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            response_format=InputClassification
        )
        
        return completion.choices[0].message.parsed
    except Exception as e:
        return InputClassification(type="statement", reasoning="Unable to classify input")

def generate_statement_response(statement: str, reasoning: str = "") -> str:
    client = get_llm_client()
    model = os.getenv("MODEL")
    prompt = STATEMENT_RESPONSE_USR.format(statement=statement, reasoning=reasoning)
    
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    
    return response.choices[0].message.content.strip()

def identify_tables(
    current_question: str,
    tables_info: str,
    conversation_history: List[str]
) -> TableIdentificationResponse:
    client = get_llm_client()
    model = os.getenv("MODEL")
    
    history_text = "\n".join([f"- {msg}" for msg in conversation_history]) if conversation_history else "No previous conversation"
    
    #TODO: in future we need to check for tokens and compress the history to prevent limit. not now but a good optimization
    prompt = IDENTIFY_TABLE_USR.format(
        tables_info=tables_info,
        conversation_history=history_text,
        current_question=current_question
    )
    
    try:
        completion = client.beta.chat.completions.parse(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            response_format=TableIdentificationResponse
        )
        
        return completion.choices[0].message.parsed
    except Exception as e:
        return TableIdentificationResponse(
            confidence=ConfidenceLevel.NOT_CONFIDENT,
            tables=[]
        )

def generate_follow_up_question(
    user_question: str,
    confidence: str,
    possible_tables: List[str]
) -> str:
    client = get_llm_client()
    model = os.getenv("MODEL")
    
    tables_list = "\n".join([f"- {table}" for table in possible_tables])
    
    prompt = FOLLOW_UP_TABLE_USR.format(
        user_question=user_question,
        confidence=confidence,
        possible_tables=tables_list
    )
    
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    
    return response.choices[0].message.content.strip()


def identify_entities_and_columns(
    user_question: str,
    table_columns_info: str,
    conversation_history: List[str]
) -> List[TableColumnResponse]:
    client = get_llm_client()
    model = os.getenv("MODEL")
    
    history_text = str(conversation_history) if conversation_history else "[]"
    
    prompt = IDENTIFY_ENTITIES_COLUMNS_USR.format(
        table_columns_info=table_columns_info,
        user_question=user_question,
        conversation_history=history_text
    )
    
    try:
        completion = client.beta.chat.completions.parse(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            response_format=EntityColumnDetectionResponse
        )
        
        return completion.choices[0].message.parsed.tables
    except Exception as e:
        print(f"Error in identify_entities_and_columns: {e}")
        return []
