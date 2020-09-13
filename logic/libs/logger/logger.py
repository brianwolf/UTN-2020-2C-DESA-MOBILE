"""
Logger
-------

Crea logs de la aplicacion
"""
import logging

from logic.libs.logger.src import config
from logic.libs.logger.src.archivo import crear_log


def iniciar(directorio: str, nivel: str):
    """
    Configura el logger para el proyecto
    """
    config.DIRECTORIO_LOGS = directorio
    config.NIVEL_LOGS = nivel


def log(nombre: str = 'app') -> logging.Logger:
    """
    Devuelve un objeto logger por un nombre, en caso de que no exista lo crea
    """
    if nombre not in config.LOGGERS:
        config.LOGGERS[nombre] = crear_log(nombre)

    return config.LOGGERS[nombre]
