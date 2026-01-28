import pytest
import os
import sys
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent.parent))

from session_manager import RedisSessionManager
from models import SessionHistory, ChatMessage


@pytest.fixture
def session_manager():
    with patch.dict(os.environ, {
        "REDIS_HOST": "localhost",
        "REDIS_PORT": "6379",
        "REDIS_DB": "0",
        "CUSTOMER_ID": "test_cust_02",
        "SESSION_ID": "test-session-456"
    }):
        manager = RedisSessionManager()
        yield manager
        manager.clear_session()
        manager.close()


def test_save_statement(session_manager: RedisSessionManager) -> None:
    statement = "I love Python programming"
    session_manager.save_message(statement)
    
    history = session_manager.get_session_history()
    assert history is not None
    assert len(history.messages) == 1
    assert history.messages[0].content == statement


def test_save_mixed_messages(session_manager: RedisSessionManager) -> None:
    messages = [
        "What is Python?",
        "I like coding",
        "How do I learn Redis?",
        "This is interesting"
    ]
    
    for content in messages:
        session_manager.save_message(content)
    
    history = session_manager.get_session_history()
    assert history is not None
    assert len(history.messages) == len(messages)
    
    for i, content in enumerate(messages):
        assert history.messages[i].content == content


def test_multiple_messages_stored(session_manager: RedisSessionManager) -> None:
    session_manager.save_message("What is Redis?")
    session_manager.save_message("I am learning Python")
    session_manager.save_message("How does it work?")
    
    history = session_manager.get_session_history()
    assert history is not None
    assert len(history.messages) == 3
    
    assert history.messages[0].content == "What is Redis?"
    assert history.messages[1].content == "I am learning Python"
    assert history.messages[2].content == "How does it work?"
