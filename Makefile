# Define variables
PROTO_DIR = ./app/proto
PROTO_FILES = $(wildcard $(PROTO_DIR)/*.proto)
PYTHON_OUT = $(PROTO_DIR)
APP_ENTRY = ./app/main.py
VENV_DIR = venv
PYTHON_BIN = $(VENV_DIR)/bin/python
PIP_BIN = $(VENV_DIR)/bin/pip

.PHONY: all ensure_venv proto proto-dev run clean test

# Default target: compile protobuf and run the app
all: run

# Ensure virtual environment exists and activate it
ensure_venv:
	@if [ ! -d "$(VENV_DIR)" ]; then \
		echo "Virtual environment not found. Creating one..."; \
		python3 -m venv $(VENV_DIR); \
	fi
	@if [ "$(VIRTUAL_ENV)" = "" ]; then \
		echo "Activating virtual environment..."; \
		. $(VENV_DIR)/bin/activate; \
	fi
	@echo "Ensuring dependencies are installed..."
	$(PIP_BIN) install -r requirements.txt

# Compile protobuf files (without .pyi)
proto: ensure_venv
	$(PYTHON_BIN) -m grpc_tools.protoc -I$(PROTO_DIR) \
		--python_out=$(PYTHON_OUT) \
		$(PROTO_FILES)

# Compile protobuf files with .pyi for development
proto-dev: ensure_venv
	$(PYTHON_BIN) -m grpc_tools.protoc -I$(PROTO_DIR) \
		--python_out=$(PYTHON_OUT) \
		--mypy_out=$(PYTHON_OUT) \
		$(PROTO_FILES)

# Run the application
run: ensure_venv proto
	$(PYTHON_BIN) -m app.main

# Run tests
test: ensure_venv proto-dev
	pytest

# Clean up generated protobuf files and cache
clean:
	rm -f $(PYTHON_OUT)/*_pb2.py $(PYTHON_OUT)/*_pb2.pyi
	find . -name '__pycache__' -exec rm -rf {} +
