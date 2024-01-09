import logging

# Configure logging to save errors in error.log file
logging.basicConfig(
    format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('error.log', mode='a', encoding='utf-8'),  # Save errors to error.log file
        logging.StreamHandler()  # Print log messages to the console
    ]
)

# Now you can use the logger to log messages
logger = logging.getLogger(__name__)

# Example usage
try:
    raise Exception("An error occurred")
except Exception as e:
    # Log the exception with the ERROR level
    logger.error("An error occurred: %s", str(e))
