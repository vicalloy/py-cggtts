platform ?= $(shell uname -m)
base_images ?= rust
py-version ?= 3.10
app-name ?= cggtts

ifeq ($(platform), armv7l)
  platform := armv7
endif

ifeq ($(platform), armv7l)
  base_images ?= arm32v7/rust
endif


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


docker-start-builder:
	docker run \
		-it \
		-d \
	    --name $(app-name)-$(platform)-builder \
		-v `pwd`:/app \
		-v ${HOME}/.ssh:/root/.ssh \
		$(base_images):bullseye bash || true
	docker start $(app-name)-$(platform)-builder

docker-start-builder-bash: docker-start-builder
	docker exec -it $(app-name)-$(platform)-builder bash

init-builder:
	docker exec -it $(app-name)-$(platform)-builder bash -c "\
		apt update && \
		apt install python3-pip \
		pip3 install -i https://mirrors.aliyun.com/pypi/simple/ maturin && \
		cd /app/;maturin build --release  --interpreter python3.10 --strip"

release:
		maturin build --release --strip

docker-release:
	docker exec -it $(app-name)-$(platform)-builder bash -c "\
		cd /app/;maturin build --release  --interpreter python3.10 --strip"
