format:
	black .
	isort .

lint:
	pytest src/ --pylint --mypy

utest:
	PYTHONPATH=src/ pytest test/unittest
