def get_all_cards(connection):
    with connection.cursor() as cursor:
        cursor.execute("SELECT card_number, balance FROM cards")
        return cursor.fetchall()
    

def insert_new_card(connection, card_number, balance):
    with connection.cursor() as cursor:
        insert_statement = "INSERT INTO cards (card_number, balance) VALUES (%s, %s)"
        cursor.execute(insert_statement, (card_number, balance))
    connection.commit()
    

def ammend_card_amount_for_card_number(connection, new_balance, card_number):
    ammend_card_str = """
        UPDATE cards
        SET balance = %s
        WHERE card_number = %s;
    """
    with connection.cursor() as cursor:
        cursor.execute(ammend_card_str, (new_balance, card_number))
    connection.commit()


def get_card_balance_for_card_number(connection, card_number):
    with connection.cursor() as cursor:
        balance_statement = """
            SELECT balance         
            FROM cards
            WHERE card_number = %s;
        """
        cursor.execute(balance_statement, (card_number))
        return float(cursor.fetchone()[0])
    

def get_all_card_controls(connection):
    with connection.cursor() as cursor:
        cursor.execute("""
                SELECT cards.card_number, card_controls.control_type, card_controls.value            
                FROM card_controls 
                LEFT JOIN cards ON card_controls.card_id = cards.card_id;
            """)
        return cursor.fetchall()


def get_card_controls_for_card_number(connection, card_number):
    with connection.cursor() as cursor:
        controls_statement = """
            SELECT card_controls.control_type, card_controls.value            
            FROM card_controls 
            LEFT JOIN cards ON card_controls.card_id = cards.card_id
            WHERE cards.card_number = %s;
        """
        cursor.execute(controls_statement, (card_number))
        return cursor.fetchall()


def insert_new_card_control(connection, control_type, value, card_number):
    with connection.cursor() as cursor:
        insert_statement = """
            INSERT INTO card_controls (card_id, control_type, value) 
            SELECT card_id, %s, %s FROM cards WHERE card_number = %s;
        """
        cursor.execute(insert_statement, (control_type, value, card_number))
    connection.commit()


def delete_card_control(connection, control_type, value, card_number):
    with connection.cursor() as cursor:
        delete_statement = """
            DELETE card_controls FROM card_controls 
            LEFT JOIN cards ON card_controls.card_id = cards.card_id 
            WHERE card_controls.control_type = %s
            AND card_controls.value = %s
            AND cards.card_number = %s;
        """
        cursor.execute(delete_statement, (control_type, value, card_number))
    connection.commit()


def get_all_transactions(connection):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT cards.card_number, transactions.amount, transactions.merchant, transactions.category , transactions.approved 
            FROM transactions 
            LEFT JOIN cards ON transactions.card_id = cards.card_id;
        """)
        return cursor.fetchall()

    
def insert_transaction(connection, amount, merchant, merchant_category, approved , card_number):
    transaction_insert_str = """
        INSERT INTO transactions (card_id, amount, merchant, category, approved ) 
        SELECT card_id, %s, %s, %s, %s FROM cards WHERE card_number = %s;
    """
    with connection.cursor() as cursor:
        cursor.execute(transaction_insert_str, (amount, merchant, merchant_category, approved, card_number))
    connection.commit()