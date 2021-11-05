.PHONY: test docs

# Lint all Python code in the project.
lint:
	black .

# Run unit tests.
test:
	py.test

# Generate HTML docs.
docs:
	cd docs && make html
