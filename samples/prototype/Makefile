SRC=$(shell git ls-files '*.py')

.PHONY: run
run:
	python -m pygate

.PHONY: format
format:
	@ruff format --preview --quiet .
	@ruff check . --fix --force-exclude --preview ${SRC}
	@ruff format --preview --quiet .

.PHONY: fmt
fmt: format

.PHONY: check
check:
	@ruff check --force-exclude --preview ${SRC}
	@mypy ${SRC}
	@vulture ${SRC}
