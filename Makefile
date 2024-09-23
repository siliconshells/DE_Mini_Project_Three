install:
	pip install --upgrade pip && pip install -r requirements.txt

format:
	black *.py

lint:
	pylint --disable=R,C --ignore-patterns=test_.*?py *.py

test:
	python -m pytest -cov=main test_main.py

generate_and_push:
	# Create the markdown file
	python convert_to_markdown.py

	# Add, commit, and push the generated files to GitHub
	git config --local user.email "action@github.com"; \
	git config --local user.name "GitHub Action"; \
	git add .; \
	git commit -m "Add generated plots and markdown"; \
	git push; \

all: install format lint test generate_and_push