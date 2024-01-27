.PHONY: fmt
fmt: ruff-format-isort ruff-format ruff-fix

.PHONY: ruff-format-isort
ruff-format-isort:
	ruff check --select I --fix .

.PHONY: ruff-format
ruff-format:
	ruff format --force-exclude

.PHONY: ruff-fix
ruff-fix:
	ruff check . --fix --force-exclude

.PHONY: check
check: ruff mypy vulture

.PHONY: ruff
ruff:
	ruff check --force-exclude

.PHONY: mypy
mypy:
	mypy

.PHONY: vulture
vulture:
	vulture
