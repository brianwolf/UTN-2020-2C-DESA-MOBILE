from os import path

from flask import Flask

from logic.app.configs import config
from logic.libs.logger import logger
from logic.libs.rest import rest

directorio_logs = config.DIRECTORIO_LOGS
nivel_logs = config.NIVEL_LOGS
logger.iniciar(directorio_logs, nivel_logs)

app = Flask(__name__)
rest.iniciar(app, 'logic/app/routes')


if __name__ == "__main__":
    flask_host = config.PYTHON_HOST
    flask_port = int(config.PYTHON_PORT)

    app.run(host=flask_host, port=flask_port, debug=True)
