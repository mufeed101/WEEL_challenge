CREATE DATABASE IF NOT EXISTS {db};
USE {db};

DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS card_controls;
DROP TABLE IF EXISTS cards;

CREATE TABLE cards (
    card_id INT AUTO_INCREMENT PRIMARY KEY,
    card_number VARCHAR(255) UNIQUE NOT NULL,
    balance DECIMAL(10, 2) DEFAULT 0.00 NOT NULL,
    INDEX card_id_index (card_id)
);


# Assumption: These are the only TYPES of controls available, if we want to add/ remove more types, we would require another table;
# Assumption: Multiple controls of the same type could be attached to the same card. eg. Can allow a card to work at Woolworths and Coles (Merchant) by adding 2 merchant controls to the card

CREATE TABLE card_controls (
    control_id INT AUTO_INCREMENT PRIMARY KEY,
    card_id INT NOT NULL,
    control_type ENUM('category', 'merchant', 'max_amount', 'min_amount') NOT NULL,
    value VARCHAR(255) NOT NULL,
    FOREIGN KEY (card_id) REFERENCES cards(card_id),
    INDEX card_id_index (card_id),
    UNIQUE (card_id, control_type, value)
);


CREATE TABLE transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    card_id INT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    merchant VARCHAR(100),
    category VARCHAR(100),
    approved BOOLEAN NOT NULL,
    FOREIGN KEY (card_id) REFERENCES cards(card_id)
);
