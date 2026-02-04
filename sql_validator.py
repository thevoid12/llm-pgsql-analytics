import json
import re
from typing import Tuple, List
import sqlglot
from data.database_data import PROHIBITED_KEYWORDS


def load_config() -> dict:
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"max_sql_validation_loops": 3}


def validate_sql_syntax(sql_query: str) -> Tuple[bool, str]:
    try:
        sqlglot.parse_one(sql_query, read='postgres')
        return True, ""
    except Exception as e:
        return False, f"SQL syntax error: {str(e)}"


def check_prohibited_keywords(sql_query: str) -> Tuple[bool, List[str]]:
    sql_lower = sql_query.lower()
    found_keywords = []
    
    for keyword in PROHIBITED_KEYWORDS:
        pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
        if re.search(pattern, sql_lower):
            found_keywords.append(keyword)
    
    if found_keywords:
        return False, found_keywords
    return True, []

# todo add many more security issues whenever we identify something
def check_security_issues(sql_query: str) -> Tuple[bool, List[str]]:
    issues = []
    sql_lower = sql_query.lower()
    
    if ';' in sql_query and sql_query.count(';') > 1:
        issues.append("Multiple statements detected (potential SQL injection)")
    
    if '--' in sql_query:
        issues.append("SQL comments detected (potential security risk)")
    
    if '/*' in sql_query and '*/' in sql_query:
        issues.append("Block comments detected (potential security risk)")
    
    if 'select' not in sql_lower:
        issues.append("Query must be a SELECT statement")
    
    if issues:
        return False, issues
    return True, []


def validate_sql(sql_query: str) -> Tuple[bool, str]:
    is_valid_syntax, syntax_error = validate_sql_syntax(sql_query)
    if not is_valid_syntax:
        return False, syntax_error
    
    is_keyword_safe, prohibited_found = check_prohibited_keywords(sql_query)
    if not is_keyword_safe:
        keywords_str = ", ".join(prohibited_found)
        return False, f"Prohibited keywords found: {keywords_str}"
    
    is_secure, security_issues = check_security_issues(sql_query)
    if not is_secure:
        issues_str = "; ".join(security_issues)
        return False, f"Security issues detected: {issues_str}"
    
    return True, "SQL query is valid and secure"
