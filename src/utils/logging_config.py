import os
import logging
import sys

def setup_logger(dev_mode=True, console_output=True, file_output=False, disable_logging=False):
    """
    Set up and configure the logger for the application.
    
    Args:
        dev_mode (bool): If True, sets log level to DEBUG, otherwise INFO.
        console_output (bool): If True, logs to console, otherwise only to file.
        file_output (bool): If True, logs to file, otherwise only to console.
        disable_logging (bool): If True, disables all logging (for performance).
    """
    # TODO: Add environment variables for configuration
    
    # Create a logger
    logger = logging.getLogger('wordle')
    
    # Clear existing handlers to avoid duplicates when called multiple times
    if logger.hasHandlers():
        logger.handlers.clear()
    
    # Add a special NullHandler that completely discards log messages when logging is disabled
    if disable_logging:
        # Create a no-op logger that has minimal overhead
        class NullLogger:
            def __init__(self):
                pass
                
            def __getattr__(self, name):
                # Return a no-op function for any method call
                return lambda *args, **kwargs: None

        # Return our special null logger instead
        return NullLogger()

    # Otherwise, configure logger based on settings
    log_level = logging.DEBUG if dev_mode else logging.INFO
    logger.setLevel(log_level)
    
    # Create formatters
    # Standard formatter for regular logs
    standard_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # Detailed formatter for error logs to include exception info
    detailed_formatter = logging.Formatter(
        'Exception: %(exc_info)s\n'
        'Stack Trace: %(stack_info)s'
    )
    
    # Add file handler for persistent logs (only if file_output is True)
    if file_output:
        log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs')
        os.makedirs(log_dir, exist_ok=True)

        file_handler = logging.FileHandler(os.path.join(log_dir, 'wordle.log'))
        file_handler.setLevel(log_level)
        file_handler.setFormatter(standard_formatter)
        logger.addHandler(file_handler)

    # Add console handlers only if console_output is True
    if console_output:
        # Regular console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_handler.setFormatter(standard_formatter)
        logger.addHandler(console_handler)
        
        # Add error handler for exceptions if in dev mode
        if dev_mode:
            error_handler = logging.StreamHandler(sys.stderr)
            error_handler.setLevel(logging.ERROR)
            error_handler.setFormatter(detailed_formatter)
            logger.addHandler(error_handler)
    
    return logger

# Initialize logger based on environment variables
logger = setup_logger()