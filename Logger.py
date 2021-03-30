import logging

sh = logging.StreamHandler(stream=None)
fh = logging.FileHandler("log.log", mode='w', encoding=None, delay=False)
logger = logging.getLogger("log")
logger.setLevel(logging.WARNING)
logger.addHandler(sh)
logger.addHandler(fh)
