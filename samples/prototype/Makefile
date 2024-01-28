SRC=$(shell git ls-files '*.py')

.PHONY: run
run:
	python -m pygate

.PHONY: fmt
fmt: ruff-format-isort ruff-format ruff-fix

.PHONY: ruff-format-isort
ruff-format-isort:
	@ruff check --select I --fix --preview . ${SRC}

.PHONY: ruff-format
ruff-format:
	@ruff format --force-exclude --preview ${SRC}

.PHONY: ruff-fix
ruff-fix:
	@ruff check . --fix --force-exclude --preview ${SRC}

.PHONY: check
check: ruff mypy vulture

.PHONY: ruff
ruff:
	@ruff check --force-exclude --preview ${SRC}

.PHONY: mypy
mypy:
	@mypy ${SRC}

.PHONY: vulture
vulture:
	@vulture ${SRC}
