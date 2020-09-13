"""
Exception
---------

Objetos genericos para manejo de exepciones en los proyectos
"""

from dataclasses import dataclass
from enum import Enum

from flask import jsonify

from logic.libs.excepcion.src import config


@dataclass
class AppException(Exception):
    """
    Clase de error basico para manejar errores de negocio o errores dentro de la aplicacion
    que son esperados sus atributos son:

    codigo: usado para quien quiera atrapar la excepcion, se puede usar un str de la forma 'ERROR_ALTA_USUARIO'
    o un codigo numerico, la idea es que alguien pueda hacer un if con este codigo pudiendo hacer algo al respecto

    mensaje: contiene informacion extra en formato texto para una mayor informacion, esto es para quien use la api,
    un ejemplo puede ser: 'el usuario ya existe en la base de datos'
    """
    codigo: Enum
    mensaje: str = None
    error: Exception = None

    def to_json(self) -> dict:
        d = {'codigo': self.codigo.value, 'mensaje': self.mensaje}
        if self.error:
            d['error'] = str(self.error)
        return d

    def respuesta_json(self) -> (dict, int):
        return jsonify(self.to_json()), config.HTTP_STATUS_ERROR_NEGOCIO


@dataclass
class UnknownException(Exception):
    error: Exception

    def to_json(self) -> dict:
        d = {'causa': str(self.error)}
        return d

    def respuesta_json(self) -> (dict, int):
        return jsonify(self.to_json()), config.HTTP_STATUS_ERROR_DESCONOCIDO
