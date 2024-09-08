.DEFAULT_GOAL := help

.TESTS_DIR := tests
.REPORTS_DIR := reports
.PACKAGE_NAME := waldiez

.PHONY: help
help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Default target: help"
	@echo ""
	@echo "Targets:"
	@echo " help             Show this message and exit"
	@echo " format           Format the code"
	@echo " lint             Lint the code"
	@echo " forlint          Alias for 'make format && make lint'"
	@echo " export           Export *.waldiez files in ./examples to {.py,.ipynb}"
	@echo " requirements	 Generate requirements/*.txt files"
	@echo " test             Run the tests"
	@echo " test_stream      Run tests on the 'stream' directory"
	@echo " test_models      Run tests on the 'models' directory"
	@echo " test_exporting   Run tests on the 'exporting' directory"
	@echo " docs             Generate the documentation"
	@echo " docs-live        Generate the documentation in 'live' mode"
	@echo " clean            Remove unneeded files (__pycache__, .mypy_cache, etc.)"
	@echo " build            Build the python package"
	@echo " dev              Generate (and install) requirements, lint, test, build, docs, and export"
	@echo " install          Install the python package"
	@echo " publish          Publish the python package to PyPI"
	@echo ""

.PHONY: format
format:
	isort .
	autoflake --remove-all-unused-imports --remove-unused-variables --in-place .
	black --config pyproject.toml .
	ruff format --config pyproject.toml .

.PHONY: lint
lint:
	isort --check-only .
	black --check --config pyproject.toml .
	mypy --config pyproject.toml .
	flake8 --config=.flake8
	pydocstyle --config pyproject.toml .
	bandit -r -c pyproject.toml .
	yamllint -c .yamllint.yaml .
	ruff check --config pyproject.toml .
	pylint --rcfile=pyproject.toml .

.PHONY: forlint
forlint: format lint

.PHONY: clean
clean:
	python scripts/clean.py

.PHONY: export
export:
	python scripts/export.py

.PHONY: requirements
requirements:
	python scripts/requirements.py

.PHONY: .before_test
.before_test:
	python -c 'import os; os.makedirs("${.REPORTS_DIR}", exist_ok=True)'
	python -c \
		'import subprocess, sys; subprocess.run(\
		[sys.executable, "-m", "pip", "uninstall", "-y", "${.PACKAGE_NAME}"], \
		stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)'

.PHONY: test
test: .before_test
	python -m pytest \
		-c pyproject.toml \
		--cov=${.PACKAGE_NAME} \
		--cov-report=term-missing:skip-covered \
		--cov-report html:${.REPORTS_DIR}/html \
		--cov-report xml:${.REPORTS_DIR}/coverage.xml \
		--junitxml=${.REPORTS_DIR}/xunit.xml \
		${.TESTS_DIR}/

.PHONY: test_stream
test_stream: .before_test
	python -m pytest \
		-c pyproject.toml -vv \
		--cov-report=term-missing:skip-covered \
		--cov=${.PACKAGE_NAME}/stream \
		${.TESTS_DIR}/stream

.PHONY: test_models
test_models: .before_test
	python -m pytest \
		-c pyproject.toml -vv \
		--cov-report=term-missing:skip-covered \
		--cov=${.PACKAGE_NAME}/models \
		${.TESTS_DIR}/models

.PHONY: test_exporting
test_exporting: .before_test
	python -m pytest \
		-c pyproject.toml -vv \
		--cov-report=term-missing:skip-covered \
		--cov=${.PACKAGE_NAME}/exporting \
		${.TESTS_DIR}/exporting

.PHONY: docs
docs:
	python -m mkdocs build -d site
	@echo "open:   file://`pwd`/site/index.html"
	@echo "or use: \`python -m http.server --directory site\`"

.PHONY: docs-live
docs-live:
	python -m pip install -r requirements/docs.txt
	python -m mkdocs serve --watch mkdocs.yml --watch docs --watch waldiez

.PHONY: build
build:
	python -c 'import os; os.makedirs("dist", exist_ok=True); os.makedirs("build", exist_ok=True)'
	python -c 'import shutil; shutil.rmtree("dist", ignore_errors=True); shutil.rmtree("build", ignore_errors=True)'
	python -m pip install --upgrade pip wheel
	python -m pip install -r requirements/main.txt
	python -m pip install build twine
	python -m build --sdist --wheel --outdir dist/
	python -m twine check dist/*.whl
	python -c 'import shutil; shutil.rmtree("build", ignore_errors=True)'

.PHONY: dev
dev: clean requirements
	python -m pip install -r requirements/all.txt
	make forlint
	make test
	make build
	make docs
	make export

.PHONY: install
install: build
	python -m pip uninstall -y waldiez
	python -c 'import subprocess, glob, sys; sys.exit(subprocess.run([sys.executable, "-m", "pip", "install", glob.glob("dist/*.whl")[0]]).returncode)'

.PHONY: publish
publish: build
	python -m pip install --upgrade pip twine
	python -m twine upload dist/*
