import logging
import os

from logic.libs.logger.src import config


def crear_log(nombre: str = 'app') -> logging.Logger:
    """
    Devuelve un objeto logger por un nombre, en caso de que no exista lo crea
    """
    if not os.path.exists(config.DIRECTORIO_LOGS):
        os.makedirs(config.DIRECTORIO_LOGS, exist_ok=True)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s (%(process)d) - %(levelname)s - %(message)s')

    sh = logging.StreamHandler()
    sh.setLevel(config.NIVEL_LOGS)
    sh.setFormatter(formatter)

    ruta_log = os.path.join(config.DIRECTORIO_LOGS, f'{nombre}.log')
    fh = logging.FileHandler(ruta_log)
    fh.setLevel(config.NIVEL_LOGS)
    fh.setFormatter(formatter)

    logger = logging.getLogger(nombre)
    logger.setLevel(config.NIVEL_LOGS)
    logger.addHandler(sh)
    logger.addHandler(fh)

    return logger
