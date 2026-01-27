import pytest
import redis
from typing import Generator


@pytest.fixture
def redis_client() -> Generator[redis.Redis, None, None]:
    """Create a Redis client for testing."""
    client = redis.Redis(
        host="localhost",
        port=6379,
        db=0,
        decode_responses=True,
        socket_connect_timeout=5,
    )
    yield client
    client.close()


def test_redis_connection(redis_client: redis.Redis) -> None:
    """Test basic Redis connection."""
    assert redis_client.ping() is True


def test_redis_set_get(redis_client: redis.Redis) -> None:
    """Test Redis SET and GET operations."""
    key = "test_key"
    value = "test_value"
    
    redis_client.set(key, value)
    result = redis_client.get(key)
    
    assert result == value
    
    redis_client.delete(key)


def test_redis_incr(redis_client: redis.Redis) -> None:
    """Test Redis INCR operation."""
    key = "test_counter"
    
    redis_client.set(key, 0)
    redis_client.incr(key)
    result = redis_client.get(key)
    
    assert result == "1"
    
    redis_client.delete(key)


def test_redis_hash_operations(redis_client: redis.Redis) -> None:
    """Test Redis hash operations."""
    key = "test_hash"
    field = "field1"
    value = "value1"
    
    redis_client.hset(key, field, value)
    result = redis_client.hget(key, field)
    
    assert result == value
    
    redis_client.delete(key)


def test_redis_list_operations(redis_client: redis.Redis) -> None:
    """Test Redis list operations."""
    key = "test_list"
    values = ["item1", "item2", "item3"]
    
    for value in values:
        redis_client.rpush(key, value)
    
    length = redis_client.llen(key)
    assert length == len(values)
    
    result = redis_client.lrange(key, 0, -1)
    assert result == values
    
    redis_client.delete(key)
