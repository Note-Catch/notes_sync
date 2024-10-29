import logging


class Config:
    @staticmethod
    def get_logger() -> logging.Logger:
        handler = logging.FileHandler("notes_sync.log")
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)

        logger = logging.getLogger("notes_sync")
        logger.setLevel(logging.DEBUG)
        logger.addHandler(handler)

        return logger
