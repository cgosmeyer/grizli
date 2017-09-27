"""
Setup logging and decorators to help record metadata.

This perhaps should not even be in my grizli fork, but rather in my 
imports library.

"""

import datetime
import getpass
import logging
import os
import socket
import sys
import time

from collections import OrderedDict
from functools import wraps


LOG_FILE_LOC = config.PATH_LOGS

#-----------------------------------------------------------------------------#

def setup_logging(module, path_logs='', stdout=True):
    """Setup the logging file.

    Authors
    -------
    A. Viana
    C.M. Gosmeyer

    Parameters
    ----------
    module : string
        The name of the module being logged.
    path_logs : string
        Path at which to write log file.
    stdout : {True, False}
        Set to True to print to BOTH standard out and logging file.

    Outputs
    -------
    A log file.

    References
    ----------
    https://stackoverflow.com/questions/14058453/making-python-loggers-output-all-messages-to-stdout-in-addition-to-log
    """
    # if user specifies a different location from default, 
    # supersede the default from config.
    if path_logs != '':
        log_file = make_log_file(module, path_logs)
    else:
        log_file = make_log_file(module, LOG_FILE_LOC)
    #global LOG_FILE_LOC
    #LOG_FILE_LOC = log_file
    print("log file: {}".format(log_file))
    logging.basicConfig(filename=log_file,
                        format='%(asctime)s %(levelname)s: %(message)s',
                        datefmt='%m/%d/%Y %H:%M:%S %p',
                        level=logging.INFO)

    # also print to standard out?
    if stdout:
        stderrLogger=logging.StreamHandler()
        stderrLogger.setFormatter(logging.Formatter(logging.BASIC_FORMAT))
        logging.getLogger().addHandler(stderrLogger)


#-----------------------------------------------------------------------------#

def make_log_file(module, path_logs):
    """Return the name of the log file based on the module name.

    The name of the logfile is a combination of the name of the module
    being logged and the current datetime. 

    Parameters
    ----------
    module : string
        The name of the module being logged.


    Returns
    -------
    log_file : string
        The full path to where the log file will be written to.

    """

    timestamp = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M')
    filename = '{0}_{1}.log'.format(module, timestamp)

    if not os.path.isdir(path_logs):
        os.mkdir(path_logs)

    log_file = os.path.join(path_logs, filename)

    return log_file


#-----------------------------------------------------------------------------#

def log_info(func):
    """Decorator to log useful system information.

    This function can be used as a decorator to log user environment
    and system information.

    Authors
    -------
    A. Viana
    C.M. Gosmeyer

    Use
    ---
        @log_info
        def function_doing_stuff(args, more_args):
            pass


    Parameters
    ----------
    func : function
        The function to decorate.

    Returns
    -------
    wrapped : function
        The wrapped function.

    """

    @wraps(func)
    def wrapped(*a, **kw):

        # Log environment information
        logging.info('User: ' + getpass.getuser())
        logging.info('System: ' + socket.gethostname())
        logging.info('Python Version: ' + sys.version.replace('\n', ''))
        logging.info('Python Executable Path: ' + sys.executable)

        # Call the function and time it
        t1_cpu = time.clock()
        t1_time = time.time()
        func(*a, **kw)
        t2_cpu = time.clock()
        t2_time = time.time()

        # Log execution time
        hours_cpu, remainder_cpu = divmod(t2_cpu - t1_cpu, 60 * 60)
        minutes_cpu, seconds_cpu = divmod(remainder_cpu, 60)
        hours_time, remainder_time = divmod(t2_time - t1_time, 60 * 60)
        minutes_time, seconds_time = divmod(remainder_time, 60)
        logging.info('Elapsed Real Time: {0:.0f}:{1:.0f}:{2:f}'.format(hours_time, minutes_time, seconds_time))
        logging.info('Elapsed CPU Time: {0:.0f}:{1:.0f}:{2:f}'.format(hours_cpu, minutes_cpu, seconds_cpu))

    return wrapped


#-----------------------------------------------------------------------------#

def log_metadata(func):
    """ Decorator to print to log file the metadata of a function.

    Author
    ------
    C.M. Gosmeyer

    Use
    ---
        @log_metadata
        def function_doing_stuff(args, more_args):
            pass

    Returns
    -------
    func_wrapper : function
        The wrapped function.

    """
    @wraps(func)
    def wrapped(*a, **kw):

        # Fetch function metadata.
        current_params = locals()
        func_name = func.__name__

        # Order the current_params dictionary
        # Because I like stuff alphabetical. 
        current_params = OrderedDict(sorted(current_params.items(), key=lambda t: t[0]))

        logging.info("")
        logging.info("FUNCTION: {}".format(func_name.upper()))
        logging.info("   PARAMETER : VALUE ")
        #for param, value in current_params['kw'].iteritems(): #python 2
        for param, value in current_params['kw'].items():
            logging.info("   {} : {}".format(param, value))
        logging.info("")

        return func(*a, **kw)

    return wrapped

    