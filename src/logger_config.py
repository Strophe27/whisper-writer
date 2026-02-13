# -*- coding: utf-8 -*-
"""
Configuration de la journalisation persistante pour WhisperWriter.
Écrit dans logs/whisper-writer.log (rotation pour éviter des fichiers énormes).
Les messages contenant des données binaires/hex (ex. audio) sont tronqués pour garder les logs lisibles.
"""

import os
import sys
import re
import logging
from logging.handlers import RotatingFileHandler

LOG_DIR = "logs"
LOG_FILENAME = "whisper-writer.log"
LOG_MAX_BYTES = 2 * 1024 * 1024  # 2 Mo
LOG_BACKUP_COUNT = 3
# Longueur max d’un message (évite d’écrire des buffers audio / hex en entier)
LOG_MESSAGE_MAX_LEN = 3500
# Séquence hex au-delà de laquelle on remplace par un placeholder
LOG_HEX_REPLACE_THRESHOLD = 60


def _sanitize_message(msg):
    """Tronque les messages trop longs et remplace les longues séquences hex/binaires."""
    if not msg:
        return msg
    # Séquences type repr(bytes): \x00\x01\x02...
    long_escape_hex = re.compile(r"(\\x[0-9a-fA-F]{2}){40,}")
    msg = long_escape_hex.sub(r"[... données binaires omises ...]", msg)
    # Longues séquences hex (chiffres/lettres a-f, espaces, virgules)
    long_hex = re.compile(
        r"([0-9a-fA-Fx\s,]{"
        + str(LOG_HEX_REPLACE_THRESHOLD)
        + r",})"
    )
    msg = long_hex.sub(r"[... données binaires/hex omises ...]", msg)
    if len(msg) > LOG_MESSAGE_MAX_LEN:
        msg = msg[:LOG_MESSAGE_MAX_LEN] + "\n... [message tronqué - données volumineuses omises]"
    return msg


class SanitizingFormatter(logging.Formatter):
    """Formatter qui tronque et nettoie les messages pour éviter d’écrire de l’audio binaire/hex en clair."""

    def format(self, record):
        result = super().format(record)
        return _sanitize_message(result)


def _log_file_path():
    """Chemin du fichier de log (répertoire du projet = cwd au lancement)."""
    base = os.getcwd()
    return os.path.join(base, LOG_DIR, LOG_FILENAME)


def setup_logging():
    """
    Configure le logging racine avec un fichier persistant.
    Peut être appelé plusieurs fois (ex. run.py et main.py) : les handlers
    ne sont ajoutés qu'une fois.
    """
    root = logging.getLogger()
    log_path = _log_file_path()
    for h in root.handlers:
        if isinstance(h, RotatingFileHandler) and getattr(h, "baseFilename", "") == log_path:
            return
    try:
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
    except OSError:
        pass

    formatter = SanitizingFormatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = RotatingFileHandler(
        log_path,
        encoding="utf-8",
        maxBytes=LOG_MAX_BYTES,
        backupCount=LOG_BACKUP_COUNT,
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)
    root.addHandler(file_handler)
    root.setLevel(logging.DEBUG)

    # Éviter la prolifération de messages des librairies (et données audio/binaires)
    logging.getLogger("PyQt5").setLevel(logging.WARNING)
    logging.getLogger("pynput").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("sounddevice").setLevel(logging.WARNING)
    logging.getLogger("numpy").setLevel(logging.WARNING)


def install_excepthook():
    """
    Installe un excepthook qui enregistre toute exception non gérée
    dans le fichier de log avant de laisser le programme crasher.
    """
    def _log_exception(exc_type, exc_value, exc_tb):
        import traceback
        logger = logging.getLogger(__name__)
        lines = traceback.format_exception(exc_type, exc_value, exc_tb)
        msg = "".join(lines).strip()
        logger.critical("Exception non gérée:\n%s", msg)
        # Comportement par défaut
        sys.__excepthook__(exc_type, exc_value, exc_tb)

    sys.excepthook = _log_exception


def get_log_path():
    """Retourne le chemin du fichier de log (utile pour l’affichage à l’utilisateur)."""
    return _log_file_path()
