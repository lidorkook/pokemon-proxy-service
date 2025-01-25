import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger("LOGGER")
logger.setLevel(logging.DEBUG)

all_handler = RotatingFileHandler("all.log", maxBytes=5_000_000, backupCount=3)
all_handler.setLevel(logging.DEBUG)

info_handler = RotatingFileHandler("info.log", maxBytes=5_000_000, backupCount=3)
info_handler.setLevel(logging.INFO)

error_handler = RotatingFileHandler("error.log", maxBytes=5_000_000, backupCount=3)
error_handler.setLevel(logging.ERROR)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

all_handler.setFormatter(formatter)
info_handler.setFormatter(formatter)
error_handler.setFormatter(formatter)

logger.addHandler(all_handler)
logger.addHandler(info_handler)
logger.addHandler(error_handler)
