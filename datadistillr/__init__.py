import logging


def init_logger(self):
    """
    This function sets up a very simple logging configuration (log everything on standard output)
    that is useful for troubleshooting.
    """

    logger = logging.getLogger(__name__)
    stream_handler = logging.StreamHandler()
    # Add Formatting
    my_format = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s")
    stream_handler.setFormatter(my_format)

    # Add Handler to Logger
    logger.addHandler(stream_handler)

    # Set the log level
    logger.setLevel(logging.DEBUG)
