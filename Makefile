.PHONY: test-docker

lint-docker:
	docker compose -f docker-compose.lint.yml down && docker compose -f docker-compose.lint.yml up --force-recreate --build --abort-on-container-exit

test-docker:
	echo "No test docker"