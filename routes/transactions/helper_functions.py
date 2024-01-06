def parse_transactions_input(input_data):
    # If more time then check the validity of the input, raise appropriate exceptions if invalid
    return input_data.get("card"), float(input_data.get("amount")), input_data.get("merchant"), input_data.get("merchant_category")

def check_valid_merchant_type(transaction_value, list_merchant_values_allowed):
    if list_merchant_values_allowed and transaction_value not in list_merchant_values_allowed:
        raise ValueError(f"The merchant {transaction_value} is not allowed")

def check_valid_category_type(transaction_value, list_category_values_allowed):
    if list_category_values_allowed and transaction_value not in list_category_values_allowed:
        raise ValueError(f"The category {transaction_value} is not allowed")

def check_max_amount(transaction_value, list_control_values_allowed):
    if list_control_values_allowed and not any(float(amount) >= transaction_value for amount in list_control_values_allowed):
        raise ValueError("The amount of this transaction exceeds all control restrictions")

def check_min_amount(transaction_value, list_control_values_allowed):  
    if list_control_values_allowed and not any(float(amount) <= transaction_value for amount in list_control_values_allowed):
        raise ValueError("The amount of this transaction subceed all control restrictions")
