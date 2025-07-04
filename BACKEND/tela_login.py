from flask import Blueprint, render_template, request, redirect, url_for, session
from BACKEND.models import Assinatura, AssinaturaStatus, db

bp = Blueprint('login', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        br_digitado = request.form.get('usuario')
        senha_digitada = request.form.get('senha')

        # Busca no banco usando o BR digitado
        usuario = Assinatura.query.filter_by(br=br_digitado).first()

        if usuario and usuario.senha == senha_digitada:
            session['logado'] = True
            session['usuario'] = usuario.nome
            session['tipo'] = usuario.tipo
            return redirect(url_for('pendentes.pagina_pendentes'))
        else:
            erro = 'BR ou senha inválidos.'
            return render_template('tela_login.html', erro=erro)

    return render_template('tela_login.html')
