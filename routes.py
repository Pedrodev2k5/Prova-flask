import math
import os
import uuid

from flask import (Blueprint, current_app, flash, redirect, render_template,
                   request, url_for)
from sqlalchemy import func

from extensions import db
from models import Categoria, Produto

bp = Blueprint("main", __name__)

IMAGEM_PADRAO = "padrao.png"


# ---------------------------------------------------------------- utilidades
def extensao_permitida(nome_arquivo):
    """Aceita apenas as extensões definidas em config.py."""
    if "." not in nome_arquivo:
        return False
    ext = nome_arquivo.rsplit(".", 1)[1].lower()
    return ext in current_app.config["EXTENSOES_PERMITIDAS"]


def salvar_imagem(arquivo):
    """Salva o arquivo com nome único e devolve o nome gravado."""
    ext = arquivo.filename.rsplit(".", 1)[1].lower()
    nome_final = f"{uuid.uuid4().hex}.{ext}"
    arquivo.save(os.path.join(current_app.config["UPLOAD_FOLDER"], nome_final))
    return nome_final


def remover_imagem(nome_arquivo):
    """Apaga a imagem do disco, preservando sempre a padrao.png."""
    if not nome_arquivo or nome_arquivo == IMAGEM_PADRAO:
        return
    caminho = os.path.join(current_app.config["UPLOAD_FOLDER"],
                           os.path.basename(nome_arquivo))
    if os.path.isfile(caminho):
        os.remove(caminho)


def validar_formulario(form, arquivo):
    """Valida os campos e devolve (nome, preco, categoria, erros)."""
    erros = []

    # Nome: mínimo 3 caracteres
    nome = (form.get("nome") or "").strip()
    if len(nome) < 3:
        erros.append("O nome do produto deve ter pelo menos 3 caracteres.")

    # Preço: conversão protegida (vazio, texto, NaN, infinito)
    preco = None
    bruto = (form.get("preco") or "").strip().replace(",", ".")
    try:
        preco = float(bruto)
        if not math.isfinite(preco):
            raise ValueError
    except ValueError:
        preco = None
        erros.append("Preço inválido. Informe um número, por exemplo 19,90.")
    else:
        if preco <= 0:
            erros.append("O preço deve ser maior que zero.")

    # Categoria precisa existir
    categoria = None
    categoria_id = form.get("categoria_id", type=int)
    if categoria_id:
        categoria = db.session.get(Categoria, categoria_id)
    if categoria is None:
        erros.append("Selecione uma categoria válida.")

    # Extensão da imagem (somente se enviou arquivo)
    if arquivo and arquivo.filename and not extensao_permitida(arquivo.filename):
        permitidas = ", ".join(sorted(current_app.config["EXTENSOES_PERMITIDAS"]))
        erros.append(f"Extensão de imagem não permitida. Use: {permitidas}.")

    return nome, preco, categoria, erros


# -------------------------------------------------------------------- rotas
@bp.route("/")
def index():
    busca = (request.args.get("busca") or "").strip()

    consulta = Produto.query
    if busca:
        consulta = consulta.filter(Produto.nome.ilike(f"%{busca}%"))
    produtos = consulta.order_by(func.lower(Produto.nome)).all()

    categorias = Categoria.query.order_by(Categoria.nome).all()
    return render_template("index.html", produtos=produtos,
                           categorias=categorias, busca=busca, form={})


@bp.route("/cadastrar", methods=["POST"])
def cadastrar():
    arquivo = request.files.get("imagem")
    nome, preco, categoria, erros = validar_formulario(request.form, arquivo)

    if erros:
        for erro in erros:
            flash(erro, "erro")
        produtos = Produto.query.order_by(func.lower(Produto.nome)).all()
        categorias = Categoria.query.order_by(Categoria.nome).all()
        return render_template("index.html", produtos=produtos,
                               categorias=categorias, busca="",
                               form=request.form), 400

    nome_imagem = IMAGEM_PADRAO
    if arquivo and arquivo.filename:
        nome_imagem = salvar_imagem(arquivo)

    produto = Produto(nome=nome, preco=preco, imagem=nome_imagem,
                      categoria_id=categoria.id)
    db.session.add(produto)
    db.session.commit()

    flash("Produto cadastrado com sucesso!", "sucesso")
    return redirect(url_for("main.index"))


@bp.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    produto = db.get_or_404(Produto, id)
    categorias = Categoria.query.order_by(Categoria.nome).all()

    if request.method == "POST":
        arquivo = request.files.get("imagem")
        nome, preco, categoria, erros = validar_formulario(request.form, arquivo)

        if erros:
            for erro in erros:
                flash(erro, "erro")
            return render_template("editar.html", produto=produto,
                                   categorias=categorias,
                                   form=request.form), 400

        imagem_antiga = None
        if arquivo and arquivo.filename:
            imagem_antiga = produto.imagem
            produto.imagem = salvar_imagem(arquivo)

        produto.nome = nome
        produto.preco = preco
        produto.categoria_id = categoria.id
        db.session.commit()

        # Só apaga a foto antiga depois de gravar no banco com sucesso
        remover_imagem(imagem_antiga)

        flash("Produto atualizado com sucesso!", "sucesso")
        return redirect(url_for("main.index"))

    return render_template("editar.html", produto=produto,
                           categorias=categorias, form={})


@bp.route("/excluir/<int:id>", methods=["POST"])
def excluir(id):
    produto = db.get_or_404(Produto, id)
    imagem = produto.imagem

    db.session.delete(produto)
    db.session.commit()

    remover_imagem(imagem)

    flash("Produto excluído com sucesso!", "sucesso")
    return redirect(url_for("main.index"))
