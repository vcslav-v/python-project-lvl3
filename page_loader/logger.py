import logging
import logging.config

logging.config.fileConfig('logger.cfg')
logger = logging.getLogger("root")
