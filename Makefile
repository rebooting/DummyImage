.PHONEY: restore build-docker

VENV := venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
restore:
	@echo "Restoring virtual environment..."
	@python3 -m venv $(VENV)
	@$(PIP) install --upgrade pip
	@$(PIP) install -r requirements.txt
	@echo "Virtual environment restored."
	@echo "To activate the virtual environment, run 'source $(VENV)/bin/activate'."
	@echo "To deactivate the virtual environment, run 'deactivate'."


build-docker:
	@echo "Building Docker image..."
	docker build -t test/helloworld .
	@echo "Docker image built and tagged as test/helloworld."

run-docker:
	@echo "Running Docker container..."
	docker run --rm -it -p 7010:7010 test/helloworld
	@echo "Docker container stopped."
