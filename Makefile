.PHONY: init install run activate redis-build redis-start redis-stop redis-logs redis-clean test-redis run_clean app-build build-all pod-up pod-down pod-restart pod-logs pod-logs-redis

init:
	uv init

install:
	uv add streamlit sqlglot

run:
	uv run streamlit run main.py

activate:
	source .venv/bin/activate

# --- Redis container (standalone) ---

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
	@echo "Clearing all session data for customer..."
	@podman exec chat-poc-redis sh -c "redis-cli KEYS '$$(grep CUSTOMER_ID .env | sed "s/^export //" | cut -d "=" -f2)_*' | xargs -r redis-cli DEL" || echo "No sessions found or already cleared"
	@echo "Sessions cleared. Starting application..."
	uv run streamlit run main.py

# --- App container ---

app-build:
	podman build -t chat-poc-app -f Dockerfile .

# --- Full stack (podman pod) ---

build-all: redis-build app-build

pod-up:
	podman pod create --name chat-poc-pod -p 8501:8501
	podman run -d --pod chat-poc-pod --name chat-poc-redis chat-poc-redis
	@sed 's/^export //' .env > .env.podman
	podman run -d --pod chat-poc-pod --name chat-poc-app --env-file .env.podman chat-poc-app
	@rm -f .env.podman
	@echo "Pod is up — app at http://localhost:8501"

pod-down:
	podman pod stop chat-poc-pod || true
	podman pod rm chat-poc-pod || true

pod-restart: pod-down pod-up

pod-logs:
	podman logs -f chat-poc-app

pod-logs-redis:
	podman logs -f chat-poc-redis
