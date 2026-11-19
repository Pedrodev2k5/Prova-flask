import os

from flask import Flask

from config import Config
from extensions import db
from models import Categoria
from routes import bp

CATEGORIAS_INICIAIS = ["Eletrônicos", "Roupas", "Alimentos", "Livros"]


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Garante que as pastas existam
    os.makedirs(os.path.join(app.root_path, "instance"), exist_ok=True)
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    db.init_app(app)
    app.register_blueprint(bp)

    # Cria o banco automaticamente e popula as categorias (somente se estiver vazio)
    with app.app_context():
        db.create_all()
        if Categoria.query.count() == 0:
            db.session.add_all([Categoria(nome=n) for n in CATEGORIAS_INICIAIS])
            db.session.commit()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
