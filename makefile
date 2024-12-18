PYTHON = python3
VENV_DIR = .venv
SCRIPT = main.py
REQUIREMENTS = requirements.txt
LOGFILE = /var/log/ticket_monitoring.log

.PHONY: all
all: setup run

.PHONY: venv
venv:
	$(PYTHON) -m venv $(VENV_DIR)

.PHONY: setup
setup: venv
	$(VENV_DIR)/bin/pip install -r $(REQUIREMENTS)
	$(VENV_DIR)/bin/playwright install

.PHONY: run
run:
	$(VENV_DIR)/bin/$(PYTHON) $(SCRIPT)

.PHONY: clean
clean:
	rm -rf $(VENV_DIR) __pycache__ *.log

.PHONY: cron
cron:
	@echo "Running cron job: $(SCRIPT)"
	$(VENV_DIR)/bin/$(PYTHON) $(SCRIPT) >> $(LOGFILE) 2>&1