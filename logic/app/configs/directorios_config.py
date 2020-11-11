from pathlib import Path

from logic.app.configs import config


def iniciar_directorios():
    """
    crea los directorios requeridos por el proyecto
    """
    lista_directorios = [
        config.DIRECTORIO_DB,
        config.DIRECTORIO_QR
    ]

    for d in lista_directorios:
        Path(d).mkdir(parents=True, exist_ok=True)
