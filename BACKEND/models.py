from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Assinatura(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    br = db.Column(db.String(12), unique=True, nullable=False)  # Ex: BR0123456789
    nome = db.Column(db.String(50), nullable=False)             # Nome real do usuário
    senha = db.Column(db.String(50), nullable=False)
    tipo = db.Column(db.String(20))  # 'MRO' ou 'OPERAÇÃO'
    imagem = db.Column(db.String(100))  # caminho do arquivo de assinatura (png)

class AssinaturaStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_pdf = db.Column(db.String(100), nullable=False, unique=True)
    mro_assinou = db.Column(db.Boolean, default=False)
    operacao_assinou = db.Column(db.Boolean, default=False)
    nome_mro = db.Column(db.String(100))
    nome_operacao = db.Column(db.String(100))
    data_mro = db.Column(db.String(20))
    data_operacao = db.Column(db.String(20))
