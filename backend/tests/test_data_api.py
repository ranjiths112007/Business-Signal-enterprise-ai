from app.data_api import _suggest_mapping


def test_customer_mapping_accepts_common_alternate_names():
    mapping = _suggest_mapping("customers", ["Company Name", "Sector", "ARR"])
    assert mapping == {
        "name": "Company Name",
        "industry": "Sector",
        "annual_value": "ARR",
    }


def test_sales_mapping_accepts_customer_name_and_transaction_fields():
    mapping = _suggest_mapping("sales", ["Customer", "Deal Value", "Transaction Date"])
    assert mapping["customer_id"] == "Customer"
    assert mapping["amount"] == "Deal Value"
    assert mapping["sale_date"] == "Transaction Date"
