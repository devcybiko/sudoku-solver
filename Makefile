install:
	pip install -r requirements.txt

coverage:
	rm -rf .covarage htmlcov
	coverage run --source ./ -m unittest tests/TestPuzzle.py

report:
	coverage report -m
	coverage html
	open htmlcov/index.html
