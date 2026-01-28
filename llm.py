import os
from openai import AzureOpenAI
from dotenv import load_dotenv
from prompt import QUESTION_CHECKER_USR, STATEMENT_RESPONSE_USR

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

def check_question_or_statement(user_input: str) -> str:
    client = get_llm_client()
    model = os.getenv("MODEL")
    
    prompt = QUESTION_CHECKER_USR.format(context=user_input)
    
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )
    
    result = response.choices[0].message.content.strip().lower()
    return result

def generate_statement_response(statement: str) -> str:
    client = get_llm_client()
    model = os.getenv("MODEL")
    
    prompt = STATEMENT_RESPONSE_USR.format(statement=statement)
    
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    
    return response.choices[0].message.content.strip()
