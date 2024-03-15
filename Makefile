up:
	@docker-compose up -d
	@docker images -q -f dangling=true | xargs docker rmi -f

up-build:
	@docker-compose up -d --build
	@docker images -q -f dangling=true | xargs docker rmi -f

down:
	@docker-compose down

down-v:
	@docker-compose down -v


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

validate:
	@docker-compose run -e PRE_COMMIT_HOME=/tmp --rm web pre-commit run --all-files -c .pre-commit-config.yaml

test:
	@docker-compose exec web pytest
