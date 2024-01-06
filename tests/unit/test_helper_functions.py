import pytest
from routes.cards.helper_functions import parse_card_input

def test_parse_card_input_no_card_number():
    no_card_number = {"balance": 0}
    with pytest.raises(ValueError) as e:
        parse_card_input(no_card_number)
    assert str(e.value) == "The Key 'number' doesn't exist in the input json"

def test_parse_card_input_balance_is_str():
    input_balance_is_str = {"number": "123", "balance": "str"}
    with pytest.raises(TypeError) as e:
        parse_card_input(input_balance_is_str)
    assert str(e.value) == "Please ensure that the balance is a number"


# Do the rest if you have time