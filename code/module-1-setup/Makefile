.PHONY: help run test lint lint-openapi verify init-db clean

help:
	@echo "Course 4: API & Agent Development"
	@echo ""
	@echo "Targets:"
	@echo "  run           Start Flask development server"
	@echo "  test          Run pytest test suite"
	@echo "  lint          Run ruff linter"
	@echo "  lint-openapi  Validate OpenAPI spec"
	@echo "  verify        Run all checks"
	@echo "  init-db       Initialize SQLite database"
	@echo "  clean         Remove generated files"

run:
	FLASK_APP=src.app:create_app FLASK_DEBUG=1 flask run --port=5000

test:
	pytest tests/ -v --tb=short

lint:
	ruff check src/ tests/ --fix
	ruff format src/ tests/

lint-openapi:
	openapi-spec-validator openapi/api-spec.yaml

verify: lint lint-openapi test
	@echo "✅ All checks passed!"

init-db:
	python -c "from src.database.db import init_db; init_db()"

clean:
	rm -rf data/*.db __pycache__ .pytest_cache .ruff_cache cdk.out
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
