import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "backend"))

import pytest
from app.sql_agent import validate_sql


def test_select_allowed():
    assert validate_sql("SELECT * FROM customers") == "SELECT * FROM customers"

@pytest.mark.parametrize("sql", [
    "DROP TABLE customers",
    "DELETE FROM customers",
    "UPDATE customers SET name='x'",
    "SELECT * FROM customers; DELETE FROM customers",
])
def test_writes_rejected(sql):
    with pytest.raises(ValueError):
        validate_sql(sql)
