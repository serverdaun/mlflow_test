install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

lint:
	pylint -d=C,E src/*.py

format:
	black src/*.py

train:
	python src/train.py

run:
	python src/fastapi_app.py