import logging.config
import os

GAME_LOG_DIR_NAME = '.game_log'

GAME_LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__name__)), '.game_log')

GAME_SCORES = 1
HEIGHT_MAP = 5
WIDTH_MAP = 5

LOG_FILE_POSTFIX = '.json'


LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',  # Default is stderr
        },
    },
    'loggers': {
        '': {  # root logger
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': False
        },
    }
}

logging.config.dictConfig(LOGGING_CONFIG)
