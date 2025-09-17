import os
from pathlib import Path

def get_logging_config(base_dir):

    logs_dir = base_dir / 'logs'
    logs_dir.mkdir(exist_ok=True)
    
    for log_type in ['info_logs', 'warning_logs', 'error_logs', 'general_logs']:
        (logs_dir / log_type).mkdir(exist_ok=True)
    
    # LOGGER
    return {
        'version': 1,
        'disable_existing_loggers': False,
        "formatters": {
            "verbose": {
                "format": "{levelname} {asctime} {module} {message}",
                "style": "{",
            },
            "simple": {
                "format": "{levelname} {message}",
                "style": "{",
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'simple',
            },
            "info_file": {
                "level": "INFO",
                "class": "logging.handlers.TimedRotatingFileHandler",
                "filename": os.path.join(base_dir, 'logs/info_logs/notes_app_info.log'),
                "when": "midnight",
                "interval": 1,
                "backupCount": 7,
                "formatter": "verbose",
                "encoding": "utf-8",
            },
            "warning_file": {
                "level": "WARNING",
                "class": "logging.handlers.TimedRotatingFileHandler",
                "filename": os.path.join(base_dir, 'logs/warning_logs/notes_app_warning.log'),
                "when": "midnight",
                "interval": 1,
                "backupCount": 7,
                "formatter": "verbose",
                "encoding": "utf-8",
            },
            "error_file": {
                "level": "ERROR",
                "class": "logging.handlers.TimedRotatingFileHandler",
                "filename": os.path.join(base_dir, 'logs/error_logs/notes_app_error.log'),
                "when": "midnight",
                "interval": 1,
                "backupCount": 7,
                "formatter": "verbose",
                "encoding": "utf-8",
            },
            "general_file": {
                "level": "DEBUG",
                "class": "logging.handlers.TimedRotatingFileHandler",
                "filename": os.path.join(base_dir, 'logs/general_logs/notes_app_general.log'),
                "when": "midnight",
                "interval": 1,
                "backupCount": 7,
                "formatter": "verbose",
                "encoding": "utf-8",
            },
        },
        'loggers': {
            'notes_app': {
                'handlers': ['console', 'general_file'],
                'level': 'DEBUG',
                'propagate': False,
            },
            'notes_app.info': {
                'handlers': ['info_file', 'general_file'],
                'level': 'INFO',
                'propagate': False,
            },
            'notes_app.warning': {
                'handlers': ['warning_file', 'general_file'],
                'level': 'WARNING',
                'propagate': False,
            },
            'notes_app.error': {
                'handlers': ['error_file', 'general_file'],
                'level': 'ERROR',
                'propagate': False,
            },
        },
    }