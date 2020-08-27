import logging
import traceback
import typing as t


class ContextualLogger:
    """
    Class that provides contextual data (via log record extra data) to logging calls similar to
    ``logging.LoggerAdapter``.

    Contextual data can be set during initialization or via the :meth:`update` method.
    """

    def __init__(self, logger: logging.Logger, **extra: t.Any):

        self.logger = logger
        self.extra = extra

    def update(self, **extra: t.Any):
        """Update :attr:`extra` with additional data."""
        self.extra.update(extra)

    def clear(self):
        """Clear :attr:`extra` of all data."""
        self.extra = {}

    def log(self, level: int, message: str, extra: t.Optional[t.Dict[str, t.Any]] = None):
        """
        Log `message` with log `level` and additional `extra` data if provided.

        By default, the `stacklevel` is set to ``2`` since this method wraps ``self.logger.log`` so we need to tell it
        get the stack info one more level up so that log caller is captured correctly. For the other logging methods,
        they should override the stacklevel to ``3`` since those methods add an additional stack entry.
        """
        if extra is None:
            extra = {}
        extra = {**self.extra, **extra}
        self.logger.log(level, message, extra=extra)

    def info(self, message: str, **extra: t.Any):
        """Log `message` and additional `extra` data with log level INFO."""
        self.log(logging.INFO, message, extra)

    def warning(self, message: str, **extra: t.Any):
        """Log `message` and additional `extra` data with log level INFO."""
        self.log(logging.WARNING, message, extra)

    def error(self, message: str, **extra: t.Any):
        """Log `message` and additional `extra` data with log level ERROR."""
        self.log(logging.ERROR, message, extra)

    def exception(self, message: str, **extra: t.Any):
        """
        Log `message` and additional `extra` data with log level ERROR and automatically adds `traceback` to `extra` if
        it's not already set.
        """
        if "traceback" not in extra:
            extra["traceback"] = traceback.format_exc()
        self.log(logging.ERROR, message, extra)

    def critical(self, message: str, **extra: t.Any):
        """Log `message` and additional `extra` data with log level CRITICAL."""
        self.log(logging.CRITICAL, message, extra)

    def debug(self, message: str, **extra: t.Any):
        """Log `message` and additional `extra` data with log level DEBUG."""
        self.log(logging.DEBUG, message, extra)
