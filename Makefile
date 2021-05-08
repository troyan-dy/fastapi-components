clean:
	@rm -rf build dist .eggs *.egg-info
	@rm -rf .benchmarks .coverage coverage.xml htmlcov report.xml .tox
	@find . -type d -name '.mypy_cache' -exec rm -rf {} +
	@find . -type d -name '__pycache__' -exec rm -rf {} +
	@find . -type d -name '*pytest_cache*' -exec rm -rf {} +
	@find . -type f -name "*.py[co]" -exec rm -rf {} +

lint:
	@poetry run mypy zvuk_service_lib/
	@poetry run flake8 zvuk_service_lib/

format:
	@poetry run black zvuk_service_lib/ tests/
	@poetry run isort zvuk_service_lib/ tests/

setup:
	@poetry install --no-root --no-dev -E all

test:
	@poetry run pytest tests/

build:
	@poetry build

publish:
	@poetry publish -r zvuk

