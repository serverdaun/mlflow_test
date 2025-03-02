install:
	pip install --upgrade pip
	pip install -r requirements.txt

lint:
	pylint src/*.py

format:
	black src/*.py