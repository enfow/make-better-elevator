format:
	black .
	isort .

lint:
	pytest --pylint src/

utest:
	pytest src/
