from extensions import db


class Categoria(db.Model):
    """Lado '1' do relacionamento 1:N."""
    __tablename__ = "categoria"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False, unique=True)

    # Uma categoria possui vários produtos
    produtos = db.relationship("Produto", backref="categoria", lazy=True)

    def __repr__(self):
        return f"<Categoria {self.nome}>"


class Produto(db.Model):
    """Lado 'N' do relacionamento 1:N."""
    __tablename__ = "produto"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    imagem = db.Column(db.String(255), nullable=False, default="padrao.png")

    # Chave estrangeira apontando para a categoria
    categoria_id = db.Column(db.Integer, db.ForeignKey("categoria.id"), nullable=False)

    def __repr__(self):
        return f"<Produto {self.nome}>"
