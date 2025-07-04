from flask import Blueprint, render_template, session, redirect, url_for
from BACKEND.drive_service import listar_pdfs_pendentes

bp = Blueprint('pendentes', __name__)

# ID da pasta "PENDENTES DE ASSINATURA" no seu Google Drive
PASTA_PENDENTES_ID = '1F1sKFKavdwa-pVOO8erEVCxrPECMYjMF'

@bp.route('/pendentes')
def pagina_pendentes():
    if not session.get('logado'):
        return redirect(url_for('login.login'))

    # Chama a função que lista os PDFs no Google Drive
    arquivos = listar_pdfs_pendentes(PASTA_PENDENTES_ID)

    return render_template('tela_pendentes.html', arquivos=arquivos)
