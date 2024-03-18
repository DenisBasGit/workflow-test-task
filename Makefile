up:
	@docker-compose -f local.yml up -d
	@docker images -q -f dangling=true | xargs docker rmi -f

up-build:
	@docker-compose -f local.yml up -d --build
	@docker images -q -f dangling=true | xargs docker rmi -f

down:
	@docker-compose -f local.yml down

down-v:
	@docker-compose -f local.yml down -v


ps:
	@docker-compose -f local.yml ps

sh:
	@docker-compose -f local.yml exec web sh

bash:
	@docker-compose -f local.yml exec web bash

# If the first argument is "logs"...
ifeq (logs,$(firstword $(MAKECMDGOALS)))
  # use the rest as arguments for "logs"
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # ...and turn them into do-nothing targets
  $(eval $(RUN_ARGS):;@:)
endif
logs:
	@docker-compose -f local.yml logs -f $(RUN_ARGS)

validate:
	@docker-compose -f local.yml run -e PRE_COMMIT_HOME=/tmp --rm web pre-commit run --all-files -c .pre-commit-config.yaml

test:
	@docker-compose -f local.yml exec web pytest
