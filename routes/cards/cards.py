from flask import Blueprint, request, jsonify
from routes.db_commands import get_all_cards, insert_new_card
from routes.cards.helper_functions import parse_card_input
from db_connection import get_db_connection

cards_blueprint = Blueprint('cards', __name__)

@cards_blueprint.route('/cards', methods=['GET'])
def get_cards():
    connection = get_db_connection()
    try:
        cards = get_all_cards(connection)
        json_cards = [{"card_number": card[0], "balance": card[1]} for card in cards]
        return jsonify(json_cards)
    
    except Exception as e: 
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()
    
# Below is what the input json should look like
# {
#     "number": "12123423",
#     "balance": 34 <--- This is optional, will default to 0
# }
@cards_blueprint.route('/cards', methods=['POST'])
def post_cards():
    connection = get_db_connection()
    try:
        input_data = request.json
        card_number, balance = parse_card_input(input_data)
        insert_new_card(connection, card_number, balance)
        return "Successfully added a card", 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except TypeError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e: 
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()