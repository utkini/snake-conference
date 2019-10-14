import logging.config
import os

GAME_LOG_DIR_NAME = '.game_log'
GAME_LOG_DIR_DEFAULT = os.path.join(os.path.dirname(os.path.abspath(__file__)), GAME_LOG_DIR_NAME)
GAME_LOG_DIR = os.getenv('GAME_LOG_DIR', GAME_LOG_DIR_DEFAULT)

GAME_PLAYERS_DIR_NAME = os.getenv('GAME_PLAYERS_DIR_NAME', 'game_players')
GAME_PLAYERS_DIR_DEFAULT = os.path.join(os.path.dirname(os.path.abspath(__file__)), GAME_PLAYERS_DIR_NAME)
GAME_PLAYERS_DIR = os.getenv('GAME_PLAYERS_DIR', GAME_PLAYERS_DIR_DEFAULT)

PLAYER_FILE_PREFIX = 'player_'

GAME_MAX_ITERATION = 100

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
