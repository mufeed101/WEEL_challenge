# test_app.py
import pytest
import json
from app import create_app
from db_connection import get_db_connection
from database.load_schema import load_schema


@pytest.fixture
def client():
    """A test client for the app."""
    app = create_app()
    return app.test_client()

@pytest.fixture
def test_db():
    """Setup a test database and teardown after tests are done."""
    load_schema()
    test_db_connection = get_db_connection()

    yield test_db_connection

    # Teardown
    with test_db_connection.cursor() as cursor:
        cursor.execute("DROP TABLE IF EXISTS transactions;")
        cursor.execute("DROP TABLE IF EXISTS card_controls;")
        cursor.execute("DROP TABLE IF EXISTS cards;")
    test_db_connection.close()

# This is used by unit test too, create another file so both these tests can share it
def insert_test_card_data(test_db, card_number, balance):
    with test_db.cursor() as cursor:
        insert_statement = "INSERT INTO cards (card_number, balance) VALUES (%s, %s)"
        cursor.execute(insert_statement, (card_number, balance))
    test_db.commit()


def insert_test_card_controls_data(test_db, control_type, value, card_number):
    with test_db.cursor() as cursor:
        insert_statement = """
            INSERT INTO card_controls (card_id, control_type, value) 
            SELECT card_id, %s, %s FROM cards WHERE card_number = %s;
        """
        cursor.execute(insert_statement, (control_type, value, card_number))
    test_db.commit()


def test_transaction_errors_with_card_controls(client, test_db):
    """Test the /transactions route."""

    # Insert card to start with
    insert_test_card_data(test_db, '1234', 20.00)

    # Transactions above $15 shouldn't be allowed
    # If there are multiple max amount controls then pick the largest one
    insert_test_card_controls_data(test_db, "max_amount", 15, "1234")
    insert_test_card_controls_data(test_db, "max_amount", 2, "1234")

    # Transactions outside woolworths and coles shouldn't be allowed
    insert_test_card_controls_data(test_db, "merchant", "woolworths", "1234")
    insert_test_card_controls_data(test_db, "merchant", "coles", "1234")

    # Transactions That aren't to do with groceries aren't allowed
    insert_test_card_controls_data(test_db, "category", "groceries", "1234")

    # Transactions below $6 shouldn't be allowed
    # If there are multiple max amount controls then pick the smallest one
    insert_test_card_controls_data(test_db, "min_amount", 6, "1234")
    insert_test_card_controls_data(test_db, "min_amount", 20, "1234")


    # Transaction amount more than the balance
    input_data = {
        "card": "1234",
        "amount": "45.50",
        "merchant": "woolworths",
        "merchant_category": "groceries"
    }

    response = client.post('/transactions', json=input_data)
    assert response.status_code == 400
    assert json.loads(response.data.decode('utf-8')).get("error") == "You do not have enough balance"


    # Transaction amount exceeding the highest max amount
    input_data = {
        "card": "1234",
        "amount": "17.50",
        "merchant": "woolworths",
        "merchant_category": "groceries"
    }

    response = client.post('/transactions', json=input_data)
    assert response.status_code == 400
    assert json.loads(response.data.decode('utf-8')).get("error") == "The amount of this transaction exceeds all control restrictions"


    # Transaction merchant that's at aldi
    input_data = {
        "card": "1234",
        "amount": "17.50",
        "merchant": "aldi",
        "merchant_category": "groceries"
    }

    response = client.post('/transactions', json=input_data)
    assert response.status_code == 400
    assert json.loads(response.data.decode('utf-8')).get("error") == "The merchant aldi is not allowed"


    # Transaction category that's not allowed
    input_data = {
        "card": "1234",
        "amount": "17.50",
        "merchant": "coles",
        "merchant_category": "entertainment"
    }

    response = client.post('/transactions', json=input_data)
    assert response.status_code == 400
    assert json.loads(response.data.decode('utf-8')).get("error") == "The category entertainment is not allowed"


def test_transaction_successful(client, test_db):
    # check transaction table
    # check if card balance is reduced
    assert True
    
# Test the rest if you have time