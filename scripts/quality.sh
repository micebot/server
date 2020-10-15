# Remove unsed variables and imports.
poetry run autoflake \
    --remove-all-unused-imports \
    --recursive \
    --remove-unused-variables \
    --in-place server \
    --exclude=__init__.py

# Sort imports from app and unit tests.
# There's a configuration on 'pyproject.toml' to make isort compatible with black.
# See: https://black.readthedocs.io/en/stable/compatible_configs.html#isort
poetry run isort server test/unit

# Audit python files on app and unit tests.
poetry run pylama server test/unit

# Pydocstyle:
#   - D101: Missing docstring in public class.
#   - D102: Missing docstring in public method.
#   - D103: Missing docstring in public function.
pydocstyle --select=D101,D102,D103 server

# Run black formatter for verify errors, do not fix them (--check flag).
poetry run black --check server