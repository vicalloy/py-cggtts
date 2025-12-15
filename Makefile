dev:
	maturin develop 

.PHONY: build
build:
	maturin build

.PHONY: test
test:
	. .venv/bin/activate && python -m pytest tests/ -v

init-venv:
	uv venv -p 3.10
	uv sync
	make shell

.PHONY: shell
shell:
	@echo "copy and paste the following command to activate the virtual environment"
	@echo "source .venv/bin/activate"