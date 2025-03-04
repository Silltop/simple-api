logging_config = {
    "version": 1,
    "formatters": {
        "detailed": {
            "format": "[%(asctime)s | %(levelname)s | line:%(lineno)d] | %(name)s | %(module)s: %(message)s",
            "datefmt": "%Y-%m-%dT%H:%M:%S%z",
        },
    },
    "handlers": {
        "stdout": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "formatter": "detailed",
            "level": "INFO",
        },
    },
    "loggers": {
        "root": {"level": "INFO", "handlers": ["stdout"]},
        "werkzeug": {"level": "INFO", "propagate": True},
    },
}
