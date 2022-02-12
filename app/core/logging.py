import logging

from loguru import logger

INTERCEPTS = ["uvicorn", "uvicorn.access"]


class InterceptHandler(logging.Handler):
    """Handler for intercepting records and outputting to loguru."""

    def emit(self, record: logging.LogRecord):
        """Intercepts log messages

        Intercepts log records sent to the handler, adds additional context to
        the records, and outputs the record to the default loguru logger.

        Args:
            record: The log record
        """
        level: int | str = ""
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = str(record.levelno)

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            if frame.f_back:
                frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def init():
    """Sets the loguru interceptor for the desired logs"""
    for log in INTERCEPTS:
        logging.getLogger(log).handlers = [InterceptHandler()]
