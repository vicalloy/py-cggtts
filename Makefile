platform ?= armv7
docker_platform_option ?= linux/$(platform)
docker_platform_option ?= linux/$(platform)
py-version ?= 3.10
app-name ?= cggtts

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


docker-start-armv7-builder:
	docker run \
		-it \
		-d \
	    --name $(app-name)-$(platform)-builder \
		-v `pwd`:/app \
		-v ${HOME}/.ssh:/root/.ssh \
		arm32v7/rust:bullseye bash || true
	docker start $(app-name)-$(platform)-builder || true

docker-start-builder-bash: docker-start-armv7-builder
	docker exec -it $(app-name)-$(platform)-builder bash

init-builder:
	docker exec -it $(app-name)-$(platform)-builder bash -c "\
		apt update && \
		apt install python3-pip \
		pip3 install -i https://mirrors.aliyun.com/pypi/simple/ maturin && \
		cd /app/;maturin build --release  --interpreter python3.10 --strip
	"

release:
		maturin build --release --strip

release-armv7: init-builder
	docker exec -it $(app-name)-$(platform)-builder bash -c "\
		cd /app/;maturin build --release  --interpreter python3.10 --strip
	"
