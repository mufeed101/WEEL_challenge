from flask import Blueprint, request, jsonify
from routes.db_commands import get_all_card_controls, insert_new_card_control, delete_card_control
from routes.card_controls.helper_functions import parse_card_controls_input
from db_connection import get_db_connection

card_controls_blueprint = Blueprint('card_controls', __name__)

@card_controls_blueprint.route('/card-controls', methods=['GET'])
def get_card_controls():
    connection = get_db_connection()
    try:
        card_controls = get_all_card_controls(connection)
        json_card_controls = [{"card_number": card[0], "control_type": card[1], "value": card[2]} for card in card_controls]
        return jsonify(json_card_controls)
    
    except Exception as e: 
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()

# Below is what the input json should look like
# {
#     "card_number": "12123423",
#     "control_type": "category"
#     "value": "groceries"
# }
@card_controls_blueprint.route('/card-controls', methods=['POST'])
def post_card_controls():
    connection = get_db_connection()
    try:
        # If more time then check if cardnumber actually exists
        input_data = request.json
        card_number, control_type, value = parse_card_controls_input(input_data)
        insert_new_card_control(connection, control_type, value, card_number)
        return "Successfully added card control", 201
        
    except Exception as e: 
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()



# Below is what the input json should look like
# {
#     "card_number": "12123423",
#     "control_type": "category"
#     "value": "groceries"
# }
@card_controls_blueprint.route('/card-controls', methods=['DELETE'])
def delete_card_controls():
    connection = get_db_connection()
    # If more time then check if card number actually exists
    try:
        input_data = request.json
        card_number, control_type, value = parse_card_controls_input(input_data)
        delete_card_control(connection, control_type, value, card_number)
        return "Successfully deleted card control", 201
        
    except Exception as e: 
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()
