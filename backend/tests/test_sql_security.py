import pytest

from app.sql_agent_v1 import validate_sql

@pytest.mark.parametrize('sql', ['UPDATE customers SET name=\'x\'', 'DELETE FROM customers', 'DROP TABLE customers', 'SELECT 1; DELETE FROM customers'])
def test_blocks_mutations(sql):
    with pytest.raises(ValueError): validate_sql(sql)

def test_allows_select():
    assert validate_sql('SELECT id, name FROM customers') == 'SELECT id, name FROM customers'
