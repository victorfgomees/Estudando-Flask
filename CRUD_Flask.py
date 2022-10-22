from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
import json


# Inicialização do Flask

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/flask_db'

db = SQLAlchemy(app)


# Classe usuário

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(30))
    email = db.Column(db.String(50))

    def to_json(self):
        return {"id": self.id, "nome": self.nome, "email":self.email}



# Selecionar todos os usuarios
@app.route("/usuarios", methods = ["GET"])
def seleciona_usuarios():
    usuarios_objeto = Usuario.query.all()
    usuarios_json = [usuario.to_json() for usuario in usuarios_objeto]
    return gera_resposta(200, "usuarios", usuarios_json)


# Selecionar apenas um usuário
@app.route("/usuario/<id>", methods = ["GET"])
def seleciona_usuario(id):
    usuario_objeto = Usuario.query.filter_by(id = id).first()
    usuario_json = usuario_objeto.to_json()
    return gera_resposta(200, "usuarios", usuario_json)

# Cadastrar um novo usuário
@app.route("/usuario", methods = ["POST"])
def cria_usuario():
    body = request.get_json()


    try:
        usuario = Usuario(nome = body["nome"], email = body["email"])
        db.session.add(usuario)
        db.session.commit()
        return gera_resposta(201, "usuario", usuario.to_json(), "Usuário cadastrado com sucesso")
    except Exception as e:
        print('Erro', e)
        return gera_resposta(400, "usuario", {}, "Erro ao cadastrar o usuário")






# Atualizar um usuário
@app.route("/usuario/<id>", methods=["PUT"])
def atualiza_usuario(id):
    usuario_objeto = Usuario.query.filter_by(id=id).first()
    body = request.get_json()

    try:
        if('nome' in body):
            usuario_objeto.nome = body['nome']
        if('email' in body):
            usuario_objeto.email = body['email']
        
        db.session.add(usuario_objeto)
        db.session.commit()
        return gera_resposta(200, "usuario", usuario_objeto.to_json(), "Usuário atualizado com sucesso")
    except Exception as e:
        print('Erro', e)
        return gera_resposta(400, "usuario", {}, "Erro ao atualizar usuário")


# Deletar um usuário
@app.route("/usuario/<id>", methods=["DELETE"])
def deleta_usuario(id):
    usuario_objeto = Usuario.query.filter_by(id=id).first()

    try:
        db.session.delete(usuario_objeto)
        db.session.commit()
        return gera_resposta(200, "usuario", usuario_objeto.to_json(), "Deletado com sucesso")
    except Exception as e:
        print('Erro', e)
        return gera_resposta(400, "usuario", {}, "Erro ao deletar")




# Função para gerar uma resposta

# Códigos de status: 200 = OK, 201 = Criado e 400 = Bad Request
def gera_resposta(status, nome_do_conteudo, conteudo, mensagem=False):
    body = {}
    body[nome_do_conteudo] = conteudo

    if(mensagem):
        body["mensagem"] = mensagem

    return Response(json.dumps(body), status=status, mimetype="application/json")


app.run()