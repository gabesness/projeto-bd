"""
Universidade Federal de Sergipe
Projeto Final de Banco de Dados
Prof. Andre Carvalho
Alunos:
Gabriel Cardoso Barreto Lima de Meneses
Joao Victor de Oliveira Dantas
"""


from flask import Flask, request, render_template, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/bd_ingresso'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Tabela de relacionamento entre Evento e Categoria
possui = db.Table('possui',
    db.Column('evento_id', db.Integer, db.ForeignKey('eventos.id')),
    db.Column('categoria_id', db.Integer, db.ForeignKey('categorias.id'))
)

# Modelagem da tabela eventos
class EventModel(db.Model):
    __tablename__ = 'eventos'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(20), nullable=False)
    descricao = db.Column(db.Text)
    datas = db.Column(db.Date)
    categorias = db.relationship('CategoryModel', secondary=possui, backref="categorias")

    def __init__(self, titulo, descricao, datas):
        self.titulo = titulo
        self.descricao = descricao
        self.datas = datas

    def __repr__(self):
        return f"<Evento {self.titulo}: {self.descricao}>"

# Modelagem da tabela categorias
class CategoryModel(db.Model):
    __tablename__ = 'categorias'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(20), nullable=False)

    def __init__(self, nome):
        self.nome = nome

    def __repr__(self):
        return f"<Categoria {self.nome}>"


# *** R O T A S ***

# Pagina principal
@app.route("/eventos", methods=['GET'])
def eventos():
    if request.method == 'GET':
        # listagem dos eventos
        eventos = EventModel.query.all()
        resposta = []
        for evento in eventos:
            lista_categoria = [c.nome for c in evento.categorias]
            json = {
            "id": evento.id,
            "titulo": evento.titulo,
            "descricao": evento.descricao,
            "datas": evento.datas,
            "categorias": ', '.join(lista_categoria)
            }
            resposta.append(json)

        return render_template("index.html", valores=resposta)

# Pagina das categorias
@app.route("/categorias", methods=['GET'])
def categorias():
    if request.method == 'GET':
        # listagem das categorias
        categorias = CategoryModel.query.all()
        resposta = [{"id": categoria.id, "nome": categoria.nome} for categoria in categorias]
        return render_template("categorias.html", valores=resposta)

@app.route("/")
def hello():
    # redireciona para a pagina de eventos
    return redirect(url_for("eventos"))

# Criacao de um novo evento ou categoria
@app.route("/criar_<tabela>", methods=['GET','POST'])
def criar(tabela):
    if request.method == 'GET':  # visualizacao
        return render_template("edit.html", tabela=tabela, json={})
    elif request.method == 'POST':  # criacao
        try:
            data = request.form
            json = jsonify(data).get_json()
            if tabela == "eventos":
                novo = EventModel(titulo=json["titulo"], descricao=json["descricao"], datas=json["datas"])
            elif tabela == "categorias":
                novo = CategoryModel(nome=data["nome"])
            db.session.add(novo)
            db.session.commit()
            return redirect(url_for(f"{tabela}"))  # retorna para a lista respectiva
        except Exception as e:
            return {"error": str(e)}

# Alteracao de evento ou categoria ja existente
@app.route("/editar_<tabela>",methods=['GET', 'POST'])
def editar(tabela):
    if request.method == 'GET':
        args = request.args.to_dict()  # recebe os argumentos passados para exibi-los nos campos
        if tabela == "eventos":
            e = EventModel.query.filter_by(id=int(args["id"])).first()
            json = {
            "id": e.id,
            "titulo": e.titulo,
            "descricao": e.descricao,
            "datas": e.datas
            }
        elif tabela == "categorias":
            c = CategoryModel.query.filter_by(id=int(args["id"])).first()
            json = {
            "id": c.id,
            "nome": c.nome
            }
        return render_template("edit.html", tabela=tabela, json=json)
    elif request.method == 'POST':
        data = request.form
        resposta = jsonify(data).get_json()
        if tabela == "eventos":
            e = EventModel.query.filter_by(titulo=resposta["titulo"]).first()
            e.titulo = resposta["titulo"]
            e.descricao = resposta["descricao"]
            e.datas = resposta["datas"]
        db.session.commit()
        return redirect(url_for(f"{tabela}"))  # retorna para a lista

# Exclusao de um evento ou categoria
@app.route("/deletar_<tabela>", methods=['GET'])
def deletar(tabela):
    valor = request.args.to_dict()
    id = int(valor["id"])
    if tabela == "eventos":
        # E necessario deletar primeiro as entradas no relacionamento possui e depois na propria tabela
        db.session.execute("DELETE FROM possui WHERE evento_id=:id", {'id': id})
        EventModel.query.filter_by(id=id).delete()
        db.session.commit()
    elif tabela == "categorias":
        db.session.execute("DELETE FROM possui WHERE categoria_id=:id", {'id': id})
        CategoryModel.query.filter_by(id=id).delete()
        db.session.commit()
    return redirect(url_for(f"{tabela}"))  # retorna para a lista

if __name__ == "__main__":
    app.run(debug=True)  # executa a aplicacao
