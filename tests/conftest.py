import pytest

# import os
# import json

# Import the fuctional fixtures as a plugin
# Note: fixtures with session scope need to be local

pytest_plugins = ["dbt.tests.fixtures.project"]


# The profile dictionary, used to write out profiles.yml
@pytest.fixture(scope="class")
def dbt_profile_target():
    return {
        "type": "databend",
        "host": "localhost",
        "port": 3307,
        "user": "root",
        "pass": "root",
        "schema": "default",
        "dbname": "default",
    }
