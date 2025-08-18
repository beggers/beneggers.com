# Prod stuff

.PHONY: full
full: clean test content gen-tf deploy clear-caches

.PHONY: clean
clean:
	rm -rf public/*

.PHONY: test
test:
	pytest

.PHONY: content
content: clean
	python3 -m beneggerscom.ssg.main

.PHONY: gen-tf
gen-tf:
	python3 -m beneggerscom.gen_tf.main

.PHONY: deploy
deploy: gen-tf
	terraform -chdir=terraform init && terraform -chdir=terraform apply

.PHONY: clear-caches
clear-caches:
	./scripts/invalidate_caches.sh

# Dev stuff

.PHONY: js-dev
js-dev:
	cd web && OUT_DIR=../public_dev ./node_modules/.bin/vite build --watch

.PHONY: js-prod
js-prod:
	cd web && npm run build

.PHONY: continuous-test
continuous-test:
	find . | grep -v public | grep -v -e "^\./\." | entr -d pytest

.PHONY: dev-clean
dev-clean:
	rm -rf public_dev/*

.PHONY: dev-content
dev-content: dev-clean
	python3 -m beneggerscom.ssg.main --dev

.PHONY: dev-js-once
dev-js-once:
	cd web && OUT_DIR=../public_dev ./node_modules/.bin/vite build

.PHONY: server
server: dev-content dev-js-once
	python3 -m beneggerscom.dev_server.main

.PHONY: only-server
only-server:
	find . | grep -v public | grep -v -e "^\./\." | entr -drz python3 -m beneggerscom.dev_server.main

# Reloads everything on any file changes, including content.
.PHONY: dev
dev:
	find . | grep -v public | grep -v -e "^\./\." | entr -drz make server

# Scripts and local stuff

.PHONY: post
post:
	python3 -m beneggerscom.new_post.main

.PHONY: output
output:
	terraform -chdir=terraform output