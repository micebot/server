# Run unit tests and collect the code coverage.
poetry run coverage run -m unittest discover -s test/unit -v
poetry run coverage report