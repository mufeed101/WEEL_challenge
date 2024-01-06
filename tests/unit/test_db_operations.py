from database.load_schema import load_schema
from db_connection import get_db_connection
from routes.db_commands import insert_new_card, get_all_cards, ammend_card_amount_for_card_number
import pytest


@pytest.fixture
def test_db():
    test_db="test_weel"
    load_schema(test_db)
    test_db_connection = get_db_connection(test_db)

    yield test_db_connection
    # Teardown (drop the table and close the connection)
    with test_db_connection.cursor() as cursor:
        cursor.execute("DROP TABLE IF EXISTS transactions;")
        cursor.execute("DROP TABLE IF EXISTS card_controls;")
        cursor.execute("DROP TABLE IF EXISTS cards;")
    test_db_connection.close()

def insert_test_card_data(test_db, card_number, balance):
    with test_db.cursor() as cursor:
        insert_statement = "INSERT INTO cards (card_number, balance) VALUES (%s, %s)"
        cursor.execute(insert_statement, (card_number, balance))
    test_db.commit()

def test_insert_new_card(test_db):
    # Insert a new card and commit the transaction
    insert_new_card(test_db, '1234567890', 100.00)
    with test_db.cursor() as cursor:
        cursor.execute("SELECT * FROM cards WHERE card_number = %s", ('1234567890',))
        result = cursor.fetchone()
    assert result is not None
    assert result[1] == '1234567890'
    assert result[2] == 100.00


def test_get_all_cards_single_entry(test_db):
    # Insert an entry into the database
    insert_test_card_data(test_db, '1234567890', 100.00)
    cards = get_all_cards(test_db)
    assert len(cards) == 1
    assert cards[0][0] == '1234567890'
    assert cards[0][1] == 100.00


def test_get_all_cards_multiple_entries(test_db):
    insert_test_card_data(test_db, '1234567890', 100.00)
    insert_test_card_data(test_db, '9876543210', 200.00)
    cards = get_all_cards(test_db)
    assert len(cards) == 2
    assert cards[0][0] == '1234567890'
    assert cards[0][1] == 100.00
    assert cards[1][0] == '9876543210'
    assert cards[1][1] == 200.00


def test_ammend_card_amount_for_card_number(test_db):
    # Insert an entry into the database
    insert_test_card_data(test_db, '1234567890', 100.00)
    ammend_card_amount_for_card_number(test_db, 200, '1234567890')
    with test_db.cursor() as cursor:
        cursor.execute("SELECT balance FROM cards WHERE card_number = %s", ('1234567890',))
        result = cursor.fetchone()
    assert result[0] == 200.00


## Do the rest if you have time
def test_get_card_balance_for_card_number(test_db):
    assert True


def test_get_all_card_controls(test_db):
    assert True


def test_get_card_controls_for_card_number(test_db):
    assert True


def test_insert_new_card_control(test_db):
    assert True


def test_delete_card_control(test_db):
    assert True


def test_get_all_transactions(test_db):
    assert True

    
def test_insert_transaction(test_db):
    assert True