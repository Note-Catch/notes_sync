from notes_sync.logger.config import Config


class Logger:
    logger = Config.get_logger()

    @staticmethod
    def debug(message: str):
        Logger.logger.debug(message)

    @staticmethod
    def info(message: str):
        Logger.logger.info(message)

    @staticmethod
    def warning(message: str):
        Logger.logger.warning(message)

    @staticmethod
    def error(message: str):
        Logger.logger.error(message)
