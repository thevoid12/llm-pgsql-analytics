SYS_MSG = """ 
Assistant is a highly intelligent question answering bot.
Assistant is designed to be able to assist from answering simple questions to providing in-depth explanations to questions.
It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of 
questions. Additionally, Assistant answer the question in an unbiased manner.
Whether you need help with a specific question or just want to have a conversation about a particular topic, Assistant is here to assist.
If the user's follow-up is an extension of the current topic, retain the logic of the previous question and change only the specific parameters requested.
"""

# ------------------------------------- Question Checker ---------------------------------------------------
RELEVANT_QUESTION_CHECKER_USR = """ 
You are a highly intelligent and accurate clinical domain assistant helps the user to identify the different clinical domains from a natural language question.

Conversation History:
{conversation_history}

Current User Input: {context}

Analyze the current input in the context of the conversation history. Check whether the current input is a relevant clinical data question or a statement.

Rules:
1) If user asks anything not related to clinical domain (weather, programming, general knowledge, sports, etc.) - classify as statement
2) If the input is a follow-up or continuation of a previous clinical question (even if it's just a word or two like "yes", "and calcium", "visit 2") - classify as question
3) If the input adds filters or conditions to a previous clinical query - classify as question
4) If it's a greeting without clinical context - classify as statement

When responding, output in JSON format:
{{
  "type": "question" | "statement",
  "reasoning": "brief explanation why this is classified as statement (only if type is statement, otherwise empty)"
}}

Examples:
Conversation: []
Input: Show me list of subjects with ae is ANAEMY and seriousness is Yes
Output: {{"type": "question", "reasoning": ""}}

Conversation: []
Input: What is today's weather?
Output: {{"type": "statement", "reasoning": "This is asking about weather information, which is not related to clinical trial data"}}

Conversation: ["Show me lab results for calcium"]
Input: and cholesterol
Output: {{"type": "question", "reasoning": ""}}

Conversation: ["List subjects with adverse events"]
Input: visit 2
Output: {{"type": "question", "reasoning": ""}}

Conversation: []
Input: How are you?
Output: {{"type": "statement", "reasoning": "This is a general greeting, not a clinical data query"}}

"""

# ------------------------------------- Statement Response ---------------------------------------------------
STATEMENT_RESPONSE_USR = """
You are a highly intelligent and accurate clinical domain assistant helps the user to identify the different clinical domain data from a natural language question.
The user has made the following statement: {statement}

Reasoning why this is not a clinical data query: {reasoning}

Based on this reasoning, provide a brief, natural, and friendly professional one or two line response that:
1. Acknowledges their input
2. Gently redirects them to ask follow up questions or ask for more specifics on exactly what they are looking for.
3. The response should be generic in a way that it can be used to ask follow up questions but not tell the user what to do next.


Example:
Input: what is your favourite food?
Output:Thanks for your question—“favorite food” is more of a personal preference than a clinical or trial-related query. If you share what clinical topic or data you’re interested in, I can help identify the relevant data.
Input: hiii
Output:Hi, how can I help you today in fetching the data?
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
- Critically and carefully check if the table has all the required columns, then return that table
- If you identify more than one table is needed to be fetched, critically examine if the tables are needed or if it is possible to achieve the same result with fewer tables
- If you feel that the query could be answered from multiple different tables (e.g., the question could come from table 1 OR table 2, both seem correct), reduce the confidence to "less_confident"

Respond ONLY in the following JSON format:
{{
  "confidence": "very_confident" | "less_confident" | "not_confident",
  "tables": ["TABLE_NAME1", "TABLE_NAME2"],
  "reasoning": "Brief line or two explanation of why these tables were selected and confidence level"
}}

Confidence levels:
- very_confident: The question clearly maps to specific table(s) and all required columns are present
- less_confident: The question might relate to these tables but is ambiguous, OR multiple tables could potentially answer the same question
- not_confident: Cannot determine relevant tables from the question

If very_confident, provide most relevant table(s).
If less_confident, provide 2-4 possible tables.
If not_confident, provide an empty array or your best guess.

Examples:

Example 1:
Current Question: Show me list of subjects with ae is not HYPERTENSION and seriousness is not Non-serious and Ae toxicity grade is not Grade 3 or Ae Ongoing except Yes
Response:
{{
  "confidence": "very_confident",
  "tables": ["RPT_AE"],
  "reasoning": "RPT_AE table contains all required columns: aeterm, aeser, aetoxgr, and aeongo. This is the definitive table for adverse event queries."
}}

Example 2:
Current Question: Show me patient demographics
Response:
{{
  "confidence": "less_confident",
  "tables": ["RPT_SUBJECT_DETAIL", "RPT_AE"],
  "reasoning": "Both RPT_SUBJECT_DETAIL (primary demographics table) and RPT_AE (includes age, sex, race) contain demographic information. Need clarification on which specific demographics are needed."
}} 
"""

# ------------------------------------- Entity and Column Identification ---------------------------------------------------
IDENTIFY_ENTITIES_COLUMNS_USR = """
You are a clinical trial data expert. Given a user's question and the identified tables with their column details, identify:
1. Which columns from each table are needed to answer the question
2. specific entity values if mentioned in the question that map to those columns

Table Details:
{table_columns_info}

User Question: {user_question}

Conversation History:
{conversation_history}

Instructions:
Respond in JSON format with the following structure:
- Identify ONLY the columns that are directly needed to answer the user's question
- For each column, extract any specific entity value mentioned in the question
- Entity values are specific data points the user is asking about (e.g., "America" for siteregion, "Calcium" for lbtest, "Grade 1" for aetoxgr)
- If no specific value is mentioned for a column, leave entity_value empty
- Include columns needed for filtering, grouping, or displaying results
- Common column patterns:
  * Identifiers: comprehendid, studyid, siteid, usubjid
  * Filters: visit, visitnum, arm, siteregion, sitecountry
  * Measurements: lbstresn (lab results), vsstresn (vital signs), egstresn (ECG)
  * Test names: lbtest, vstest, egtest
  * Dates: aestdtc, lbdtc, vsdtc
  * Status/flags: aeser, aesev, aetoxgr, aeongo, lbnrind

Examples:

Question: "List subjects with lab result where labtest calcium is greater than cholesterol"
Output:
[
  {{
    "table": "RPT_LAB_INFORMATION",
    "columns": [
      {{"column": "usubjid", "entity_value": ""}},
      {{"column": "lbtest", "entity_value": "Calcium"}},
      {{"column": "lbstresn", "entity_value": ""}},
      {{"column": "lbtest", "entity_value": "Cholesterol"}},
      {{"column": "lbstresn", "entity_value": ""}}
    ]
  }}
]

Question: "Show adverse events from America region with severity Grade 1"
Output:
[
  {{
    "table": "RPT_AE",
    "columns": [
      {{"column": "usubjid", "entity_value": ""}},
      {{"column": "aeterm", "entity_value": ""}},
      {{"column": "siteregion", "entity_value": "America"}},
      {{"column": "aetoxgr", "entity_value": "Grade 1"}}
    ]
  }}
]

Question: "Get vital signs temperature and pulse for visit 2"
Output:
[
  {{
    "table": "RPT_VS",
    "columns": [
      {{"column": "usubjid", "entity_value": ""}},
      {{"column": "vstest", "entity_value": "Temperature"}},
      {{"column": "vstest", "entity_value": "Pulse Rate"}},
      {{"column": "vsstresn", "entity_value": ""}},
      {{"column": "visitnum", "entity_value": "2"}}
    ]
  }}
]

"""

# ------------------------------------- Follow Up Table ---------------------------------------------------
FOLLOW_UP_TABLE_USR = """
You are a clinical trial database expert. The user asked a question but we need clarification on which specific table(s) to query.

User Question: {user_question}

Identified Tables ({confidence} confidence):
{possible_tables}

Reasoning for Table Selection:
{reasoning}

Based on the identified tables and the reasoning, ask ONE specific, targeted question to confirm which table(s) contain the exact data they need.

Guidelines:
- Use the reasoning to understand why these tables were selected and what ambiguity exists
- Reference the SPECIFIC data types in the identified tables (e.g., "lab test results", "ECG measurements", "adverse events")
- Ask about SPECIFIC attributes or filters they mentioned (e.g., test names, severity levels, date ranges)
- Be direct and concise (1-2 sentences)
- Focus on disambiguation between the identified tables, not general exploration
- If they mentioned specific values or conditions, confirm those details
- If the question sounds "Irrelevant", ask for more specifics on exactly what they are looking for

Examples:
- User asks about "lab results for calcium": Ask "I found the lab information table. Do you need all calcium results or filtered by a specific range or abnormal flag?"
- User asks about "patient demographics": Ask "I found both the subject detail table (with BMI, height, weight) and the adverse events table (with age, sex, race). Which demographic information do you need?"
- User asks about "heart data": Ask "I found ECG and vital signs tables. Do you need electrocardiogram measurements or vital signs like heart rate and blood pressure?"
- User asks about "How are you?": since it deviates from the context, ask for more specifics on exactly what they are looking for.

Generate a specific follow-up question:
"""

# ------------------------------------- SQL Generation ---------------------------------------------------
GENERATE_SQL_USR = """
You are a SQL expert for clinical trial databases. Generate a valid SQL query based on the user's question and the identified tables, columns, and entity values.

Conversation History (for context):
{conversation_history}

Current User Question: {user_question}

Table and Column Information:
{table_column_info}

**Core Directives:**
1. **Zero Assumption Policy:** Do not add filters that are not explicitly in the question. (e.g., Do not filter by a specific `studyid` or `visit` unless the user explicitly names it).
2. **Schema Strictness:** Use **ONLY** the tables and columns listed in the "Table and Column Information" above. Do not hallucinate tables or columns (e.g., do not join a 'Severity' table if the severity column exists in the main table).
3. **Join Strategy:** PREFER Single-Table queries. Only perform a JOIN if the data requested resides in two different tables provided in the schema.
4. **Must use all information provided in the table column information**
5. **Minimal Change for Follow-ups:** If this is a follow-up question and there is a previous SQL query in the conversation history, make MINIMAL changes to the previous query. Only modify the parts that are directly affected by the new request (e.g., add/remove WHERE conditions, add/remove SELECT columns). Keep the same table, JOIN structure, and other clauses unchanged unless absolutely necessary.
6. **Crosscheck critically:** After generating the SQL query, verify it against:
   - The current user question (not previous questions)
   - The selected columns and entities from table column information
   - The full table schema to ensure all column names are correct
   - Ensure WHERE clauses match the entity values exactly as specified
7. **Follow-up handling:** If this is a follow-up question, use the conversation history to understand context but generate SQL ONLY for the current question.

Instructions:
1. Generate a SELECT query using ONLY the provided tables and columns
2. Use appropriate JOINs if multiple tables are involved (join on common keys like usubjid, studyid)
3. Apply WHERE clauses for any entity values specified in the "Selected Columns" section
4. Use proper postgres SQL syntax (assume PostgreSQL dialect)
5. For text comparisons, use ILIKE for case-insensitive matching with wildcards (e.g., ILIKE '%value%')
6. Always include relevant identifier columns (usubjid, studyid) in SELECT
7. Rely on fuzzy search using `%` for safe search. If explicitly asked for exact match or if you feel that exact match is needed, use `=`
8. Try to avoid joins if it is not actually required
9. Do not assume things. Generate SQL for whatever is asked and strictly stick to it
10. Double-check that every column in WHERE clause exists in the table schema

Output ONLY the SQL query, no explanations or markdown formatting.

"""

IMPROVE_SQL_USR = """
You are a SQL expert for clinical trial databases. The previously generated SQL query has validation issues that need to be fixed.

Original User Question: {user_question}

Table and Column Information:
{table_column_info}

Previous SQL Query:
{previous_sql}

Validation Issues Found:
{validation_errors}

Please generate an IMPROVED SQL query that:
1. Fixes all the validation issues mentioned above
2. Still answers the original user question correctly
3. Uses ONLY the tables and columns from the Table and Column Information
4. Follows PostgreSQL syntax
5. Is a valid SELECT statement only
6. Does not use any prohibited keywords or operations
7. Does not include SQL comments or multiple statements
8. Includes appropriate WHERE clauses to avoid excessive data retrieval

Output ONLY the corrected SQL query, no explanations or markdown formatting.
"""

