from logging.config import dictConfig

def configure_logging(app, name, log_level):
    debug = False
    if log_level == "DEBUG":
        debug = True

    dictConfig({
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
            },
            "access": {
                "format": "%(message)s",
            }
        },
        "handlers": {
            "console": {
                "level": log_level,
                "class": "logging.StreamHandler",
                "formatter": "default",
                "stream": "ext://sys.stdout",
            },
            "email": {
                "class": "logging.handlers.SMTPHandler",
                "formatter": "default",
                "level": log_level,
                "mailhost": ("smtp.example.com", 587),
                "fromaddr": "devops@example.com",
                "toaddrs": ["receiver@example.com", "receiver2@example.com"],
                "subject": "Error Logs",
                "credentials": ("username", "password"),
            },
            # "slack": {
            #     "class": "app.HTTPSlackHandler",
            #     "formatter": "default",
            #     "level": log_level,
            # },
            "error_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "default",
                "filename": "/var/log/gunicorn.error.log",
                "maxBytes": 10000,
                "backupCount": 10,
                "delay": "True",
            },
            "access_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "access",
                "filename": "/var/log/gunicorn.access.log",
                "maxBytes": 10000,
                "backupCount": 10,
                "delay": "True",
            }
        },
        "loggers": {
            "gunicorn.error": {
                "handlers": ["console"] if debug else ["console", "slack", "error_file"],
                "level": log_level,
                "propagate": False,
            },
            "gunicorn.access": {
                "handlers": ["console"] if debug else ["console", "access_file"],
                "level": log_level,
                "propagate": False,
            }
        },
        "root": {
            "level": log_level if debug else "INFO",
            "handlers": ["console"] if debug else ["console", "slack"],
        }
    })
