# Remove unsed variables and imports.
if poetry run autoflake \
    --remove-all-unused-imports \
    --recursive \
    --remove-unused-variables \
    --in-place server \
    --exclude=__init__.py
then
    echo Removed unused imports.
else
    echo Failed to remove unused imports.
fi

# Sort imports from app and unit tests.
# There's a configuration on 'pyproject.toml' to make isort compatible with black.
# See: https://black.readthedocs.io/en/stable/compatible_configs.html#isort
if poetry run isort server test/unit
then
    echo Fixed imports order.
else
    echo Failed to fix the imports order.
    exit 1
fi

# Audit python files on app and unit tests.
if poetry run pylama server test/unit
then
    echo Executed the audit tools.
else
    echo Failed to run audit tools.
    exit 1
fi

# Pydocstyle:
#   - D101: Missing docstring in public class.
#   - D102: Missing docstring in public method.
#   - D103: Missing docstring in public function.
if poetry run pydocstyle --select=D101,D102,D103 server
then
    echo Verified the docstring on python files.
else
    echo Missing docstring on python files.
    exit 1
fi

# Run black formatter for verify errors, do not fix them (--check flag).
if poetry run black --check server
then
    echo Run black formatter correctly.
else
    echo Failed to run the black formatter.
    exit 1
fi