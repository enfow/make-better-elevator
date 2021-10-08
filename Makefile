format:
	black .
	isort .

lint:
	pytest --pylint src/
