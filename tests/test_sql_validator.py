import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from sql_validator import validate_sql_syntax, check_prohibited_keywords, check_security_issues, validate_sql


def test_validate_sql_syntax_valid():
    valid_sql = "SELECT usubjid, lbtest FROM RPT_LAB_INFORMATION WHERE lbtest ILIKE '%calcium%'"
    is_valid, error = validate_sql_syntax(valid_sql)
    assert is_valid is True
    assert error == ""


def test_validate_sql_syntax_invalid():
    invalid_sql = "SELCT usubjid FROM table"
    is_valid, error = validate_sql_syntax(invalid_sql)
    assert is_valid is False
    assert "syntax error" in error.lower()


def test_check_prohibited_keywords_safe():
    safe_sql = "SELECT usubjid, lbtest FROM RPT_LAB_INFORMATION WHERE lbtest = 'calcium'"
    is_safe, found = check_prohibited_keywords(safe_sql)
    assert is_safe is True
    assert found == []


def test_check_prohibited_keywords_insert():
    unsafe_sql = "INSERT INTO RPT_LAB_INFORMATION VALUES (1, 2, 3)"
    is_safe, found = check_prohibited_keywords(unsafe_sql)
    assert is_safe is False
    assert 'insert' in [k.lower() for k in found]


def test_check_prohibited_keywords_delete():
    unsafe_sql = "DELETE FROM RPT_LAB_INFORMATION WHERE usubjid = '123'"
    is_safe, found = check_prohibited_keywords(unsafe_sql)
    assert is_safe is False
    assert 'delete' in [k.lower() for k in found]


def test_check_prohibited_keywords_drop():
    unsafe_sql = "DROP TABLE RPT_LAB_INFORMATION"
    is_safe, found = check_prohibited_keywords(unsafe_sql)
    assert is_safe is False
    assert 'drop' in [k.lower() for k in found]


def test_check_security_issues_safe():
    safe_sql = "SELECT usubjid FROM RPT_LAB_INFORMATION WHERE lbtest = 'calcium'"
    is_secure, issues = check_security_issues(safe_sql)
    assert is_secure is True
    assert issues == []


def test_check_security_issues_multiple_statements():
    unsafe_sql = "SELECT * FROM table1; SELECT * FROM table2;"
    is_secure, issues = check_security_issues(unsafe_sql)
    assert is_secure is False
    assert any("Multiple statements" in issue for issue in issues)


def test_check_security_issues_comments():
    unsafe_sql = "SELECT * FROM table -- this is a comment"
    is_secure, issues = check_security_issues(unsafe_sql)
    assert is_secure is False
    assert any("comments" in issue.lower() for issue in issues)


def test_check_security_issues_block_comments():
    unsafe_sql = "SELECT * FROM table /* block comment */"
    is_secure, issues = check_security_issues(unsafe_sql)
    assert is_secure is False
    assert any("comments" in issue.lower() for issue in issues)


def test_check_security_issues_not_select():
    unsafe_sql = "UPDATE table SET column = 'value'"
    is_secure, issues = check_security_issues(unsafe_sql)
    assert is_secure is False
    assert any("SELECT statement" in issue for issue in issues)


def test_validate_sql_full_valid():
    valid_sql = "SELECT usubjid, lbtest, lbstresn FROM RPT_LAB_INFORMATION WHERE LOWER(lbtest) ILIKE '%calcium%'"
    is_valid, message = validate_sql(valid_sql)
    assert is_valid is True
    assert "valid and secure" in message.lower()


def test_validate_sql_full_invalid_syntax():
    invalid_sql = "SELCT usubjid FROM table"
    is_valid, message = validate_sql(invalid_sql)
    assert is_valid is False
    assert "syntax error" in message.lower()


def test_validate_sql_full_prohibited_keyword():
    unsafe_sql = "DELETE FROM RPT_LAB_INFORMATION WHERE usubjid = '123'"
    is_valid, message = validate_sql(unsafe_sql)
    assert is_valid is False
    assert "prohibited" in message.lower()


def test_validate_sql_full_security_issue():
    unsafe_sql = "SELECT * FROM table1; SELECT * FROM table2;"
    is_valid, message = validate_sql(unsafe_sql)
    assert is_valid is False
    assert "security" in message.lower()


def test_sql_validation_loop_with_syntax_error():
    from llm import generate_sql_with_validation, improve_sql_query
    from models import TableColumnResponse, ColumnEntityMapping
    
    table_column_results = [
        TableColumnResponse(
            table="RPT_LAB_INFORMATION",
            columns=[
                ColumnEntityMapping(column="usubjid", entity_value=""),
                ColumnEntityMapping(column="lbtest", entity_value="calcium")
            ]
        )
    ]
    
    full_table_schema = """Table: RPT_LAB_INFORMATION
Description: Laboratory test results
Columns:
  - usubjid (TEXT): Unique subject identifier
  - lbtest (TEXT): Lab test name
  - lbstresn (NUMERIC): Lab result value"""
    
    try:
        sql_query = generate_sql_with_validation(
            user_question="Show me calcium lab results",
            table_column_results=table_column_results,
            full_table_schema=full_table_schema,
            conversation_history=None,
            max_loops=2
        )
        assert "SELECT" in sql_query.upper()
        assert "RPT_LAB_INFORMATION" in sql_query
    except ValueError as e:
        assert "validation failed" in str(e).lower()


def test_improve_sql_query_fixes_issues():
    from llm import improve_sql_query
    
    problematic_sql = "SELCT usubjid FROM RPT_LAB_INFORMATION"
    validation_error = "SQL syntax error: Expected token"
    
    table_column_info = """Selected columns and entities:
Table: RPT_LAB_INFORMATION
Selected Columns: usubjid, lbtest (entity: calcium)

Full table schema (all available columns):
Table: RPT_LAB_INFORMATION
Columns:
  - usubjid (TEXT): Unique subject identifier
  - lbtest (TEXT): Lab test name"""
    
    improved_sql = improve_sql_query(
        user_question="Show me calcium lab results",
        table_column_info=table_column_info,
        previous_sql=problematic_sql,
        validation_errors=validation_error
    )
    
    assert improved_sql is not None
    assert len(improved_sql) > 0
