from flask import Blueprint
from werkzeug.exceptions import HTTPException

from logic.libs.excepcion.excepcion import AppException, UnknownException
from logic.libs.logger.logger import log

error_handler_bp = Blueprint('handlers', __name__)


@error_handler_bp.app_errorhandler(HTTPException)
def handle_exception(httpe):
    return '', httpe.code


@error_handler_bp.app_errorhandler(Exception)
def handle_exception(e: Exception):
    log().exception(e)
    return UnknownException(e).respuesta_json()


@error_handler_bp.app_errorhandler(AppException)
def handle_business_exception(ae: AppException):
    log().warning(ae.to_json())
    return ae.respuesta_json()
