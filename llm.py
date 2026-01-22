import os
from openai import AzureOpenAI
from dotenv import load_dotenv

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
