import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "chave-de-desenvolvimento-troque-em-producao")

    # Banco SQLite salvo em instance/loja.db
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "instance", "loja.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Upload de imagens
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
    EXTENSOES_PERMITIDAS = {"png", "jpg", "jpeg", "gif"}
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024  # 2 MB
