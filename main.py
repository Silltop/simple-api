from logging.config import dictConfig

import logging
from log_config import logging_config
from flask_config import override_flask_exceptions
from api import app, db
from routes import v1
from sqlalchemy.exc import OperationalError

if __name__ == "__main__":
    dictConfig(config=logging_config)
    override_flask_exceptions()
    app.register_blueprint(v1)
    with app.app_context():
        try:
            db.create_all()
        except OperationalError as e:
            logging.error(f"SqlAlchemy OperationalError: Could not connect to the database. Details: {e}")
    app.run(host="0.0.0.0", debug=True, use_reloader=True, port=6622)
