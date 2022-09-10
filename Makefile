APPLICATION_NAME = bot

format:  ##@Code Reformat code with isort and black
	poetry run python3 -m isort $(CODE)
	poetry run python3 -m black $(CODE)

run:  ##@Application Run application server
	poetry run python3 -m $(APPLICATION_NAME)

env:  ##@Environment Create .env file with variables
	@$(eval SHELL:=/bin/bash)
	@cp .env.sample .env
	@echo "SECRET_KEY=$$(openssl rand -hex 32)" >> .env

nats:  ##@Run Nats Server
	docker-compose -f docker-compose.yml up -d --remove-orphans

