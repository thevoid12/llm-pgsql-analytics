# ------------------------------------- Question Checker ---------------------------------------------------
QUESTION_CHECKER_USR = """ 
Given the context below, check wheather context is a question or a statement.
Context: {context}

When responding, please output a response in one of two below options and nothing else:
1) question.
2) statement.

"""

# ------------------------------------- Statement Response ---------------------------------------------------
STATEMENT_RESPONSE_USR = """
The user has made the following statement: {statement}

Please provide a brief, natural, and friendly one or two line response acknowledging their statement.

"""
