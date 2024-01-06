def parse_card_input(input_data):
    card_number = input_data.get("number")
    if not card_number:
        raise ValueError("The Key 'number' doesn't exist in the input json")
    
    balance = input_data.get("balance", 0)
    if not isinstance(balance, (int, float)):
        raise TypeError("Please ensure that the balance is a number")

    return card_number, balance
