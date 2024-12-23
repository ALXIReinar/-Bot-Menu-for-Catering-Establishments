import logging

class LoggerSettings(logging.Formatter):
    white = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.INFO: white + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset
    }

    def format(self, record):
        log_fmts = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmts)
        return formatter.format(record)


logger = logging.getLogger(__name__)

sh = logging.StreamHandler()
sh.setLevel('INFO')
sh.setFormatter(LoggerSettings())