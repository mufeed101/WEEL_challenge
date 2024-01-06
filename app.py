from flask import Flask
from routes.cards.cards import cards_blueprint
from routes.transactions.transactions import transactions_blueprint
from routes.card_controls.card_controls import card_controls_blueprint

def create_app():    
    app = Flask(__name__)

    app.register_blueprint(cards_blueprint)
    app.register_blueprint(transactions_blueprint)
    app.register_blueprint(card_controls_blueprint)
    return app


if __name__ == '__main__':
    app = create_app()      
    app.run(debug=True)
