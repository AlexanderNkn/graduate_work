import logging


class Logger:
    def __init__(self, name) -> None:
        self.logger = logging.getLogger(name)

        handler = logging.StreamHandler()
        format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(format)

        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def debug(self, data: str) -> None:
        self.logger.debug(data)

    def info(self, data: str) -> None:
        self.logger.info(data)

    def warning(self, data: str) -> None:
        self.logger.warning(data)

    def error(self, data: str) -> None:
        self.logger.error(data)

    def exception(self, data: str) -> None:
        self.logger.exception(data)
