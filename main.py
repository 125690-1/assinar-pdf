from flask import Flask
from BACKEND import tela_login
from BACKEND.models import db
from BACKEND import tela_pendentes
from BACKEND import drive_service
from BACKEND import tela_assinados
from BACKEND import tela_gerenciar_usuarios
from BACKEND import tela_assinar_pdf
from BACKEND import tela_gerenciar_pdfs

app = Flask(
    __name__,
    template_folder='HTML',
    static_folder='.'
)

# Chave da sessão
app.secret_key = 'sua_chave_secreta_aqui'

# 🔧 Configuração do banco (substitua pela URI real)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:RTf4j@.Z4u*._9e@db.yuqpyivmuwrjcybbhmbw.supabase.co:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa o banco
db.init_app(app)

# Registros dos blueprints
app.register_blueprint(tela_login.bp)
app.register_blueprint(tela_pendentes.bp)
app.register_blueprint(tela_assinados.bp)
app.register_blueprint(tela_assinar_pdf.bp)
app.register_blueprint(tela_gerenciar_usuarios.bp)
app.register_blueprint(tela_gerenciar_pdfs.bp)
app.register_blueprint(drive_service.bp)

@app.route("/")
def status():
    return "🚀 Backend funcionando com sucesso!"

if __name__ == '__main__':
    app.run(debug=True)
