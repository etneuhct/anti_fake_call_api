import os
from django.utils.log import DEFAULT_LOGGING


LOGLEVEL = os.environ.get('LOGLEVEL', 'info').upper()

PRODUCTION_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            # exact format is not important, this is the minimum information
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        },
        'django.server': DEFAULT_LOGGING['formatters']['django.server'],
        'large':{
			'format':'%(asctime)s  %(levelname)s  %(process)d  %(pathname)s  %(funcName)s  %(lineno)d  %(message)s  '
		},
		'tiny':{
			'format':'%(asctime)s  %(message)s  '
		}
    },
    'handlers': {
        # console logs to stderr
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
        'django.server': DEFAULT_LOGGING['handlers']['django.server'],
        'django_error_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.TimedRotatingFileHandler',
			'when': 'midnight',
			'interval': 1,
			'filename': 'logs/djangoErrorLoggers.log',
			'formatter': 'large'
        },
        'django_debug_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
			'when': 'midnight',
			'interval': 1,
			'filename': 'logs/djangoDebugLoggers.log',
			'formatter': 'tiny'
        },
        'app_error_file': {
			'level': 'ERROR',
            'class': 'logging.handlers.TimedRotatingFileHandler',
			'when': 'midnight',
			'interval': 1,
			'filename': 'logs/appErrorLoggers.log',
			'formatter': 'large'
		},
        'app_info_file': {
			'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
			'when': 'midnight',
			'interval': 1,
			'filename': 'logs/appInfoLoggers.log',
			'formatter': 'default'
		}
    },
    'loggers': {
        # default for all undefined Python modules
        '': {
            'level': 'WARNING',
            'handlers': ['console'],
        },
        # Our application code logging
        'app': {
            'level': LOGLEVEL,
            'handlers': ['app_info_file', 'app_error_file'],
            # Avoid double logging because of root logger
            'propagate': False,
        },
        # Default runserver request logging
        'django.server': {
            'level': 'DEBUG',
            'handlers': ['django_debug_file', 'console'],
            'propagate': False,
        },
        'django': {
            'level': 'INFO',
            'handlers': ['django_debug_file', 'django_error_file', 'console']
        },
    },
}

DEVELOPMENT_LOGGING = {key: val for key, val in PRODUCTION_LOGGING.items()}
DEVELOPMENT_LOGGING['loggers'] = {
     # default for all undefined Python modules
    '': {
        'level': 'WARNING',
        'handlers': ['console'],
    },
    # Our application code logging
    'app': {
        'level': 'DEBUG',
        'handlers': ['console', 'app_error_file'],
        # Avoid double logging because of root logger
        'propagate': False,
    },
    # Default runserver request logging
    'django.server': {
        'level': 'DEBUG',
        'handlers': ['django_error_file', 'console'],
        'propagate': False,
    },
    'django': {
        'level': 'INFO',
        'handlers': ['django_error_file', 'console']
    },
}
