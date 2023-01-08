import logging
import sys


def attach_stdout_handler(logger: logging.Logger) -> None:
    """
    Attaches a stdout handler to the given logger.
    """
    out_handler = logging.StreamHandler(sys.stdout)
    out_handler.setLevel(logging.INFO)
    out_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    out_handler.setFormatter(out_formatter)
    logger.addHandler(out_handler)
