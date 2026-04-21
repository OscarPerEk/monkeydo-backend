.PHONY: start install

start:
	poetry run uvicorn app.main:app --reload

install:
	poetry install
