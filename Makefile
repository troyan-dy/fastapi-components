clean:
	@rm -rf build dist .eggs *.egg-info
	@rm -rf .benchmarks .coverage coverage.xml htmlcov report.xml .tox
	@find . -type d -name '.mypy_cache' -exec rm -rf {} +
	@find . -type d -name '__pycache__' -exec rm -rf {} +
	@find . -type d -name '*pytest_cache*' -exec rm -rf {} +
	@find . -type f -name "*.py[co]" -exec rm -rf {} +

lint:
	@poetry run mypy fastapi_components/
	@poetry run flake8 fastapi_components/

format:
	@poetry run black fastapi_components/ tests/
	@poetry run isort fastapi_components/ tests/

setup:
	@poetry install --no-root --no-dev -E all

test:
	@poetry run pytest tests/

build:
	@poetry build

publish:
	@poetry publish -r zvuk
