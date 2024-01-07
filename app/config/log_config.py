import logging


def setup_logging():
    """
    Configures the logging settings for the application.

    This function sets up logging to output error level messages with
    a specific format that includes the timestamp, logger name, log level,
    message, file name, line number, and function name.
    """
    logging.basicConfig(
        level=logging.ERROR,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s "
        "(%(filename)s:%(lineno)d, %(funcName)s)",
    )
