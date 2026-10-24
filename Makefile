clean:
	@rm -rf build dist .eggs *.egg-info
	@rm -rf .benchmarks .coverage coverage.xml htmlcov report.xml .tox
	@find . -type d -name '.mypy_cache' -exec rm -rf {} +
	@find . -type d -name '__pycache__' -exec rm -rf {} +
	@find . -type d -name '*pytest_cache*' -exec rm -rf {} +
	@find . -type f -name "*.py[co]" -exec rm -rf {} +

lint:
	@poetry run mypy fastapi_components/
	@# flake8 silently skips the WPS codes from `select` if the plugin is missing
	@poetry run python -c "import wemake_python_styleguide" 2>/dev/null \
		|| (echo "wemake-python-styleguide is not installed, run: poetry install" >&2; exit 1)
	@poetry run flake8 fastapi_components/

format:
	@poetry run black fastapi_components/ examples/
	@poetry run isort fastapi_components/ examples/

setup:
	@poetry install --no-root --without dev -E all

test:
	@poetry run pytest tests/

build:
	@poetry build

publish:
	@poetry publish -r zvuk
