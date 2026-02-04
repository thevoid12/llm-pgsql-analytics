.PHONY: init install run activate redis-build redis-start redis-stop redis-logs redis-clean test-redis run_clean

init:
	uv init

install:
	uv add streamlit sqlglot

run:
	uv run streamlit run main.py

activate:
	source .venv/bin/activate

redis-build:
	podman build -t chat-poc-redis -f Dockerfile.redis .

redis-start:
	podman run -d --name chat-poc-redis -p 6379:6379 chat-poc-redis

redis-stop:
	podman stop chat-poc-redis || true
	podman rm chat-poc-redis || true

redis-logs:
	podman logs -f chat-poc-redis

redis-clean: redis-stop
	podman rmi chat-poc-redis || true

test-redis:
	uv run pytest tests/test_redis.py -v

run_clean:
	@echo "Clearing Redis session data..."
	@podman exec chat-poc-redis redis-cli DEL "$$(grep CUSTOMER_ID .env | cut -d '=' -f2)_$$(grep SESSION_ID .env | cut -d '=' -f2)" || echo "Redis key not found or already cleared"
	@echo "Session cleared. Starting application..."
	uv run streamlit run main.py