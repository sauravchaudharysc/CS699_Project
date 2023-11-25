VENV_NAME := venv
VENV_ACTIVATE := $(VENV_NAME)/bin/activate

.PHONY: venv runserver

venv: $(VENV_ACTIVATE)

$(VENV_ACTIVATE): requirements.txt
	@. $(VENV_ACTIVATE) && pip install -r requirements.txt

runserver: venv
	. $(VENV_ACTIVATE) && python3 manage.py runserver
