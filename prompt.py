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

# ------------------------------------- Identify Table ---------------------------------------------------
IDENTIFY_TABLE_USR = """
You are a clinical trial database expert. Given the user's conversation history and their current question, identify which database table(s) they are most likely asking about.

Available Tables:
{tables_info}

Conversation History:
{conversation_history}

Current Question: {current_question}

Analyze the question and determine which table(s) are most relevant. Consider:
- Keywords related to adverse events, lab results, ECG, vital signs, demographics, etc.
- Context from previous questions in the conversation
- Specific medical or clinical terminology

Respond ONLY in the following JSON format:
{{
  "confidence": "very_confident" | "less_confident" | "not_confident",
  "tables": ["TABLE_NAME1", "TABLE_NAME2"]
}}

Confidence levels:
- very_confident: The question clearly maps to specific table(s)
- less_confident: The question might relate to these tables but is ambiguous
- not_confident: Cannot determine relevant tables from the question

If very_confident, provide 1-3 most relevant tables.
If less_confident, provide 2-4 possible tables.
If not_confident, provide an empty array or your best guess.

"""
