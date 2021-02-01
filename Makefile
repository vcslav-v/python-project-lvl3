FILE_VSCODE_SETTINGS = .vscode/settings.json

define VSCODE_SETTINGS
echo "{" >> $(FILE_VSCODE_SETTINGS)
echo "\"python.pythonPath\": \".venv/bin/python\"," >> $(FILE_VSCODE_SETTINGS)
echo "\"python.linting.pylintEnabled\": false," >> $(FILE_VSCODE_SETTINGS)
echo "\"python.linting.flake8Enabled\": true," >> $(FILE_VSCODE_SETTINGS)
echo "\"python.linting.mypyEnabled\": true," >> $(FILE_VSCODE_SETTINGS)
echo "\"python.linting.enabled\": true," >> $(FILE_VSCODE_SETTINGS)
echo "\"python.testing.pytestArgs\": [" >> $(FILE_VSCODE_SETTINGS)
echo "\"tests\"" >> $(FILE_VSCODE_SETTINGS)
echo "]," >> $(FILE_VSCODE_SETTINGS)
echo "\"python.testing.unittestEnabled\": false," >> $(FILE_VSCODE_SETTINGS)
echo "\"python.testing.nosetestsEnabled\": false," >> $(FILE_VSCODE_SETTINGS)
echo "\"python.testing.pytestEnabled\": true" >> $(FILE_VSCODE_SETTINGS)
echo "}" >> $(FILE_VSCODE_SETTINGS)

endef

FILE_GITIGNORE = .gitignore

define GITIGNORE
echo ".venv" >> $(FILE_GITIGNORE)
echo ".vscode" >> $(FILE_GITIGNORE)
echo "*_cache" >> $(FILE_GITIGNORE)
echo "__pycache__" >> $(FILE_GITIGNORE)
echo ".python-version" >> $(FILE_GITIGNORE)

endef


init:
	pyenv local 3.8.3
	poetry init -n
	poetry add --dev flake8
	poetry add --dev mypy
	poetry add --dev pytest
	mkdir .vscode
	touch $(FILE_VSCODE_SETTINGS)
	$(VSCODE_SETTINGS)
	touch $(FILE_GITIGNORE)
	$(GITIGNORE)
	mkdir app
	touch app/__init__.py
	mkdir tests
	touch tests/__init__.py
	touch tests/test_app.py
	poetry shell

lint:
	poetry run flake8 page_loader
	poetry run mypy page_loader

install:
	poetry install

test:
	poetry run pytest tests/
coverage:
	poetry run pytest --cov=page_loader --cov-report xml tests/
