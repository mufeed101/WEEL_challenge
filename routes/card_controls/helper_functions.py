def parse_card_controls_input(input_data):
    # If more time then check the validity of the input, raise appropriate exceptions if invalid
    return input_data.get("card_number"), input_data.get("control_type"), input_data.get("value")