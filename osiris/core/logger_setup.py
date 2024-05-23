import yaml
import logging.config

from osiris import settings

# ToDo: Check config is working
def setup_logging() -> None:
    with open(settings.logger_cfg) as file:
        config = yaml.safe_load(file.read())
        logging.config.dictConfig(config)
