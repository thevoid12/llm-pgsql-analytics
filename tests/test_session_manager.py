import pytest
import os
import sys
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent.parent))

from session_manager import RedisSessionManager
from models import SessionHistory, UserQuestion


@pytest.fixture
def session_manager():
    with patch.dict(os.environ, {
        "REDIS_HOST": "localhost",
        "REDIS_PORT": "6379",
        "REDIS_DB": "0",
        "CUSTOMER_ID": "test_cust_01",
        "SESSION_ID": "test-session-123"
    }):
        manager = RedisSessionManager()
        yield manager
        manager.clear_session()
        manager.close()


def test_redis_key_generation(session_manager: RedisSessionManager) -> None:
    expected_key = "test_cust_01_test-session-123"
    assert session_manager._get_redis_key() == expected_key


def test_save_question(session_manager: RedisSessionManager) -> None:
    question = "What is the weather today?"
    session_manager.save_question(question)
    
    history = session_manager.get_session_history()
    assert history is not None
    assert len(history.questions) == 1
    assert history.questions[0].question == question
    assert history.customer_id == "test_cust_01"
    assert history.session_id == "test-session-123"


def test_save_multiple_questions(session_manager: RedisSessionManager) -> None:
    questions = [
        "What is the weather today?",
        "Tell me about Python",
        "How do I use Redis?"
    ]
    
    for question in questions:
        session_manager.save_question(question)
    
    history = session_manager.get_session_history()
    assert history is not None
    assert len(history.questions) == len(questions)
    
    for i, question in enumerate(questions):
        assert history.questions[i].question == question
        assert history.questions[i].timestamp is not None


def test_get_session_history_empty(session_manager: RedisSessionManager) -> None:
    history = session_manager.get_session_history()
    assert history is None


def test_clear_session(session_manager: RedisSessionManager) -> None:
    session_manager.save_question("Test question")
    
    history = session_manager.get_session_history()
    assert history is not None
    
    session_manager.clear_session()
    
    history = session_manager.get_session_history()
    assert history is None


def test_question_timestamps_are_ordered(session_manager: RedisSessionManager) -> None:
    session_manager.save_question("First question")
    session_manager.save_question("Second question")
    
    history = session_manager.get_session_history()
    assert history is not None
    assert len(history.questions) == 2
    assert history.questions[0].timestamp <= history.questions[1].timestamp
