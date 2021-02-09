import logging
import logging.config

LOGGING_CONFIG = {
    'version': 1,
    'formatters': {
        'standart': {
            'format': '%(asctime)s - %(levelname)s: %(message)s'
        },
        'error': {
            'format': '%(levelname)s: %(message)s'
        },
    },
    'handlers': {
        'file_handler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'DEBUG',
            'filename': 'page_loader.log',
            'mode': 'a',
            'maxBytes': 10240,
            'backupCount': 0,
            'formatter': 'standart',
        },
        'error_handler': {
            'class': 'logging.StreamHandler',
            'level': 'ERROR',
            'stream': 'ext://sys.stderr',
            'formatter': 'error',
        },
    },
    'loggers': {
        'root': {
            'handlers': ['file_handler', 'error_handler'],
            'level': 'DEBUG',
        },
        'script': {
            'handlers': ['file_handler', 'error_handler'],
            'level': 'DEBUG',
        }
    },
}

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger('root')
