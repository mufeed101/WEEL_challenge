from flask import Blueprint, request, jsonify
from routes.db_commands import get_all_transactions, get_card_balance_for_card_number, get_card_controls_for_card_number, insert_transaction, ammend_card_amount_for_card_number
from routes.transactions.helper_functions import parse_transactions_input, check_valid_merchant_type, check_valid_category_type, check_max_amount, check_min_amount
from collections import defaultdict
from db_connection import get_db_connection

transactions_blueprint = Blueprint('transactions', __name__)

@transactions_blueprint.route('/transactions', methods=['GET'])
def get_transactions():
    connection = get_db_connection()
    # If more time then check if card number actually exists
    try:

        transactions = get_all_transactions(connection)
        json_cards = [{"card_number": transaction[0], "amount": transaction[1], "merchant": transaction[2], "category": transaction[3], "approved": transaction[4]} for transaction in transactions]
        return jsonify(json_cards)
    
    except Exception as e: 
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()


# {
#     "card": <card number>,
#     "amount": "45.50",
#     "merchant": "Woolworths",
#     "merchant_category": "5411"
# }
@transactions_blueprint.route('/transactions', methods=['POST'])
def post_transactions():
    connection = get_db_connection()
    try:

        input_data = request.json
        card_number, amount, merchant, merchant_category = parse_transactions_input(input_data)           

        # Check if the card has enough balance for the transaction
        balance = get_card_balance_for_card_number(connection, card_number)
        if balance < amount:
            print("Makes it here")
            raise ValueError("You do not have enough balance")

        # Get card controls for each card
        card_controls = get_card_controls_for_card_number(connection, card_number)
        card_controls_dict = defaultdict(list)
        for control_type, value in card_controls:
            card_controls_dict[control_type].append(value)

        # Throw appropriate error if transaction is not compliant to the controls
        check_valid_merchant_type(merchant, card_controls_dict.get("merchant"))
        check_valid_category_type(merchant_category, card_controls_dict.get("category"))
        check_max_amount(amount, card_controls_dict.get("max_amount"))
        check_min_amount(amount, card_controls_dict.get("min_amount"))

        insert_transaction(connection, amount, merchant, merchant_category, True , card_number)
        new_balance = balance - amount
        ammend_card_amount_for_card_number(connection, new_balance, card_number)

        return "Transaction Successful", 201
        
    except ValueError as e:
        insert_transaction(connection, amount, merchant, merchant_category, False , card_number)
        return jsonify({"error": str(e)}), 400
    except TypeError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e: 
        return jsonify({"error": str(e)}), 500
    finally:
        connection.commit()
        connection.close()


