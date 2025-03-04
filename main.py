from logging.config import dictConfig
from log_config import logging_config
from flask_config import app, override_flask_exceptions
from api import app
from routes import v1

if __name__ == "__main__":
    dictConfig(config=logging_config)
    override_flask_exceptions()
    app.register_blueprint(v1)
    app.run(host="0.0.0.0", debug=True, use_reloader=True, port=6622)
