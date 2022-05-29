from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/bd_ingresso'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class EventModel(db.Model):
    __tablename__ = 'eventos'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(20), nullable=False)
    descricao = db.Column(db.Text)
    datas = db.Column(db.Date)

    def __init__(self, titulo, descricao, datas):
        self.titulo = titulo
        self.descricao = descricao
        self.datas = datas

    def __repr__(self):
        return f"<Evento {self.titulo}: {self.descricao}>"

class CategoryModel(db.Model):
    __tablename__ = 'categorias'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(20), nullable=False)

    def __init__(self, nome):
        self.nome = nome

    def __repr__(self):
        return f"<Categoria {self.nome}>"


@app.route("/eventos", methods=['GET'])
def eventos():
    """if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            novo_evento = EventModel(titulo=data["titulo"], descricao=data["descricao"], datas=data["datas"])
            db.session.add(novo_evento)
            db.session.commit()
            return {"message": f"Evento {novo_evento.titulo} criado com sucesso!"}
        else:
            return {"error": "invalid request format"}"""
    if request.method == 'GET':
        eventos = EventModel.query.all()
        resposta = [{
        "id": evento.id,
        "titulo": evento.titulo,
        "descricao": evento.descricao,
        "datas": evento.datas} for evento in eventos]
        #resposta = [[evento.titulo, evento.descricao, evento.datas] for evento in eventos]
        return render_template("index.html", valores=resposta)

@app.route("/categorias", methods=['GET'])
def categorias():
    if request.method == 'GET':
        categorias = CategoryModel.query.all()
        resposta = [{"nome": categoria.nome} for categoria in categorias]
        return render_template("categorias.html", valores=resposta)

@app.route("/")
def hello():
    return redirect(url_for("eventos"))

@app.route("/editar_<tabela>", methods=['GET','POST'])
def editar(tabela):
    if request.method == 'GET':
        return render_template("edit.html", tabela=tabela)
    elif request.method == 'POST':
        if request.is_json:
            return request.get_json()
        else:
            return {"error": "invalid request format"}

if __name__ == "__main__":
    app.run(debug=True)
