.PHONY: init install run activate

init:
	uv init

install:
	uv add streamlit

run:
	uv run streamlit run main.py

activate:
	source .venv/bin/activate