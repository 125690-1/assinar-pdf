from flask import Blueprint, render_template, request, jsonify
from BACKEND.models import Assinatura, AssinaturaStatus, db
from werkzeug.utils import secure_filename
import os

bp = Blueprint("gerenciar_usuarios", __name__)
UPLOAD_DIR = os.path.join("uploads", "assinaturas")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@bp.route("/gerenciar-usuarios")
def pagina_usuarios():
    return render_template("tela_gerenciar_usuarios.html")

@bp.route("/usuarios", methods=["GET"])
def listar_usuarios():
    usuarios = Assinatura.query.all()
    dados = [
        {
            "id": u.id,
            "br": u.br,
            "nome": u.nome,
            "tipo": u.tipo,
            "imagem": u.imagem
        } for u in usuarios
    ]
    return jsonify(dados)

@bp.route("/usuarios", methods=["POST"])
def cadastrar_usuario():
    nome = request.form.get("nome")
    senha = request.form.get("senha")
    tipo = request.form.get("tipo")
    br = request.form.get("br")
    imagem = request.files.get("imagem")

    if not nome or not senha or not tipo or not br:
        return jsonify({"erro": "Campos obrigatórios ausentes."}), 400

    if Assinatura.query.filter_by(br=br).first():
        return jsonify({"erro": "BR já cadastrado."}), 400

    nome_arquivo = None
    if imagem:
        nome_arquivo = secure_filename(imagem.filename)
        caminho = os.path.join(UPLOAD_DIR, nome_arquivo)
        imagem.save(caminho)

    novo = Assinatura(
        br=br,
        nome=nome,
        senha=senha,
        tipo=tipo,
        imagem=nome_arquivo
    )
    db.session.add(novo)
    db.session.commit()

    return jsonify({"mensagem": "Usuário cadastrado com sucesso!"})

@bp.route("/usuarios/<int:id>", methods=["PUT"])
def editar_usuario(id):
    usuario = Assinatura.query.get(id)
    if not usuario:
        return jsonify({"erro": "Usuário não encontrado."}), 404

    dados = request.form
    usuario.nome = dados.get("nome", usuario.nome)
    usuario.senha = dados.get("senha", usuario.senha)
    usuario.tipo = dados.get("tipo", usuario.tipo)

    imagem = request.files.get("imagem")
    if imagem:
        nome_arquivo = secure_filename(imagem.filename)
        caminho = os.path.join(UPLOAD_DIR, nome_arquivo)
        imagem.save(caminho)
        usuario.imagem = nome_arquivo

    db.session.commit()
    return jsonify({"mensagem": "Usuário atualizado com sucesso!"})

@bp.route("/usuarios/<int:id>", methods=["DELETE"])
def excluir_usuario(id):
    usuario = Assinatura.query.get(id)
    if not usuario:
        return jsonify({"erro": "Usuário não encontrado."}), 404

    db.session.delete(usuario)
    db.session.commit()
    return jsonify({"mensagem": "Usuário excluído com sucesso!"})
