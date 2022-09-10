APPLICATION_NAME = bot

format:  ##@Code Reformat code with isort and black
	poetry run python3 -m isort $(CODE)
	poetry run python3 -m black $(CODE)

run:  ##@Application Run application server
	poetry run python3 -m $(APPLICATION_NAME)

