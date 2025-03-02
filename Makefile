install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

lint:
	pylint -d=C,E src/*.py

format:
	black src/*.py

run:
	python src/train.py