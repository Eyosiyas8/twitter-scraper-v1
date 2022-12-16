import logging
import os
import sys
basedir = os.path.dirname(os.path.abspath(__file__))
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
rerun = False
class Log(object):
    def __init__(self):
        self.orgstdout = sys.stdout
        log_file = os.path.join(basedir, '../log/library_log.py')
        self.log = open(log_file, "a")

    def write(self, msg):
        self.orgstdout.write(msg)
        if ('Finished: Successfully collected' in msg) and ('+0300' not in msg):
            info_log(msg)
            if ' 0 ' in msg:
                rerun = True

    def flush(self):
        pass
    
sys.stdout = Log()

def setup_logger(name, log_file, level=logging.INFO):

    """
    :param name: name of the log type.
    :param log_file: the name and the location of a log file.
    :param level: the minimum degree for logging a file.

    This function helps to setup as many logger files as needed.
    """

    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

# INFO logger file
def info_log(message):
    '''
    :param message: Information and status specific message that is defined before calling this function.

    This function takes the custom message and produces the ../log/INFO.log file if it's not already created and append the info message into the file.
    '''
    info_file_path = os.path.join(basedir, '../log/INFO.log')
    info_logger = setup_logger('info', info_file_path)
    info_logger.info(message)

# WARNING logger file
def warning_log(message):
    '''
    :param message: Warning situation specific message that is defined before calling this function.

    This function takes the custom message and produces the ../log/WARNING.log file if it's not already created and append the warning message into the file.
    '''
    warning_file_path = os.path.join(basedir, '../log/WARNING.log')
    warning_logger = setup_logger('warning', warning_file_path)
    warning_logger.warning(message)

# ERROR logger file
def error_log(message):
    '''
    :param message: Error specific message that is defined before calling this function.

    This function takes the custom message and produces the ../log/ERROR.log file if it's not already created and append the error message into the file.
    '''
    error_file_path = os.path.join(basedir, '../log/ERROR.log')
    error_logger = setup_logger('error', error_file_path)
    error_logger.error(message)

# CRITICAL logger file
def critical_log(message):
    '''
    :param message: Critical situation specific message that is defined before calling this function.

    This function takes the custom message and produces the ../log/CRITICAL.log file if it's not already created and append the critical message into the file.
    '''
    critical_file_path = os.path.join(basedir, '../log/CRITICAL.log')
    critical_logger = setup_logger('critical', critical_file_path)
    critical_logger.critical(message)

def system_log(message):
    '''
    :param message: Critical situation specific message that is defined before calling this function.

    This function takes the custom message and produces the ../log/SYSTEM.log file if it's not already created and append the system message into the file.
    '''
    system_log_file_path = os.path.join(basedir, '../log/SYSTEM.log')
    critical_logger = setup_logger('system', system_log_file_path)
    critical_logger.error(message)

# def another_method():
#    # using logger defined above also works here
#    logger.info('Inside method')
