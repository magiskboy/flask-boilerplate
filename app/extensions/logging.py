import logging as _logging
import click


class ColoredFormatter(_logging.Formatter):
    FORMATS = {
        _logging.NOTSET: lambda x: click.style(x, "gray"),
        _logging.DEBUG: lambda x: click.style(x, "blue"),
        _logging.INFO: lambda x: click.style(x, "green"),
        _logging.WARNING: lambda x: click.style(x, "yellow"),
        _logging.CRITICAL: lambda x: click.style(x, (230, 135, 41)),
        _logging.ERROR: lambda x: click.style(x, "red"),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def format(self, record):
        message = super().format(record)
        return self.FORMATS[record.levelno](message)


class ColoredLogger(_logging.Logger):
    def __init__(self, name, level=_logging.NOTSET):
        super().__init__(name, level)

        stream_handler = _logging.StreamHandler()
        stream_handler.setFormatter(ColoredFormatter(
            fmt="[%(asctime)s] [%(process)d] [%(levelname)s] [%(name)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S %z",
        ))
        self.addHandler(stream_handler)


def get_logger(name: str, level=_logging.CRITICAL):
    logger = ColoredLogger(name)
    return logger
