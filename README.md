# Loja Flask – Cadastro de Produtos

Sistema web de cadastro de produtos com categorias, desenvolvido em Flask para a **Avaliação Final de DS1 (Etec de Itaquera)**.
Os dados agora são gravados em um banco **SQLite** e não se perdem ao reiniciar o servidor.

## Funcionalidades

- Cadastro, edição, listagem e exclusão de produtos (CRUD completo)
- Relacionamento 1:N: uma **Categoria** possui vários **Produtos**
- Upload de imagem com validação de extensão (`png`, `jpg`, `jpeg`, `gif`) e imagem padrão (`padrao.png`) quando não há foto
- Busca por nome com resultado em ordem alfabética
- Validações: nome com no mínimo 3 caracteres, preço maior que zero e conversão de preço protegida contra valores vazios/inválidos
- Limpeza de disco: a foto antiga é removida ao trocar a imagem e ao excluir o produto (a `padrao.png` é sempre preservada)

## Tecnologias

- Python 3
- Flask
- Flask-SQLAlchemy (ORM)
- SQLite
- HTML, CSS e Jinja2

## Estrutura de pastas

```
loja_flask/
├── app.py            # cria o app, o banco e as categorias iniciais
├── config.py         # configurações (banco, uploads, extensões)
├── extensions.py     # instância do SQLAlchemy
├── models.py         # tabelas Categoria e Produto
├── routes.py         # rotas e validações
├── requirements.txt
├── .gitignore
├── README.md
├── instance/         # loja.db é criado automaticamente aqui
├── static/
│   ├── css/style.css
│   └── uploads/padrao.png
└── templates/
    ├── base.html
    ├── index.html
    └── editar.html
```

## Como rodar localmente

```bash
# 1. Clone o repositório
git clone https://github.com/SEU-USUARIO/loja_flask.git
cd loja_flask

# 2. Crie e ative o ambiente virtual
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # Linux/macOS

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Execute a aplicação
python app.py
```

Acesse em: http://127.0.0.1:5000

O banco `instance/loja.db` e as categorias iniciais (Eletrônicos, Roupas, Alimentos e Livros) são criados automaticamente na primeira execução.

## Comandos Git utilizados

```bash
git init                                   # inicializa o repositório Git local
git add .                                  # adiciona todos os arquivos (respeitando o .gitignore) à área de preparação
git commit -m "Projeto Flask com SQLite, CRUD e validações"   # registra o primeiro commit
git branch -M main                         # renomeia a branch principal para "main"
git remote add origin https://github.com/SEU-USUARIO/loja_flask.git   # liga o repositório local ao do GitHub
git push -u origin main                    # envia o projeto para o GitHub
```

Para enviar alterações futuras:

```bash
git add .
git commit -m "Descrição da alteração"
git push
```
