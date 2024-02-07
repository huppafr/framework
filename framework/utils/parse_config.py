import logging
from pathlib import Path

import yaml


logger = logging.getLogger(__name__)


def parse_properties() -> dict:
    """
    Load and merge properties from ssh-config.yaml into dictionary
    """
    config_path = Path(__file__).parents[2] / 'ssh-config.yaml'

    try:
        with config_path.open('r') as config_file:
            config = yaml.load(config_file, Loader=yaml.FullLoader)
            logger.debug(f'Loaded config for tests running: {config}')
            return config
    except Exception as e:
        logger.error(f'Error occurred during properties loading: {e}')
        raise UserWarning(f'Error occurred during properties loading: {e}')
