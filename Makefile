# Makefile for eddiedunn.terminal collection development

.PHONY: all reset clean build install reinstall verify

all: reinstall verify

reset:
	@echo "[Makefile] Resetting local environment..."
	./scripts/reset_local_terminal_env.sh
	@echo "[Makefile] Removing installed collection(s)..."
	rm -rf ~/.ansible/collections/ansible_collections/eddiedunn/terminal
	rm -rf /usr/share/ansible/collections/ansible_collections/eddiedunn/terminal || true
	@echo "[Makefile] Removing collection tarballs..."
	rm -f eddiedunn-terminal-*.tar.gz
	@echo "[Makefile] Reset complete. Please restart your shell if necessary."

clean:
	@echo "[Makefile] Cleaning build artifacts..."
	rm -f eddiedunn-terminal-*.tar.gz

build:
	@echo "[Makefile] Building collection artifact..."
	ansible-galaxy collection build --force

install: build
	@echo "[Makefile] Installing collection artifact..."
	ansible-galaxy collection install --force ./eddiedunn-terminal-*.tar.gz

reinstall: clean reset install

verify:
	@echo "[Makefile] Verifying environment..."
	./scripts/verify_local_terminal_env.sh

reset_shell:
	@echo "[Makefile] Resetting shell environment..."
	./scripts/reset_local_terminal_env.sh
