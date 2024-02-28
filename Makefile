up:
	@docker-compose up -d
	@docker images -q -f dangling=true | xargs docker rmi -f

up-build:
	@docker-compose up -d --build
	@docker images -q -f dangling=true | xargs docker rmi -f

down:
	@docker-compose down

down-v:
	@docker-compose down


# If the first argument is "test"...
ifeq (test,$(firstword $(MAKECMDGOALS)))
  # use the rest as arguments for "test"
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # ...and turn them into do-nothing targets
  $(eval $(RUN_ARGS):;@:)
endif
test:
	@docker-compose run -e PYTHONDONTWRITEBYTECODE=1 --rm web pytest -p no:cacheprovider $(RUN_ARGS) -s -vv --create-db

ps:
	@docker-compose ps

sh:
	@docker-compose exec web sh

bash:
	@docker-compose exec web bash

# If the first argument is "logs"...
ifeq (logs,$(firstword $(MAKECMDGOALS)))
  # use the rest as arguments for "logs"
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # ...and turn them into do-nothing targets
  $(eval $(RUN_ARGS):;@:)
endif
logs:
	@docker-compose logs -f $(RUN_ARGS)
