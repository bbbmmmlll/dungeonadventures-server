"""
Configuration for Dungeon Adventures.
"""
TEST_MODE = True

DEBUG_LOGFILE = 'log/debug.log'
DEFAULT_LOGFILE = 'log/dad.log'
HTTP_LOGFILE = 'log/http.log'
LOG_FORMAT = '%(asctime)s.%(msecs)d %(module)s[%(levelname)s]: %(message)s'
LOG_TIME_FORMAT = '%m-%d-%Y %H:%M:%S'

# Number of seconds between task queue check.
TIMER_SLEEP_INTERVAL = 20

# Number of workers.
TIMER_MAX_WORKERS = 4

