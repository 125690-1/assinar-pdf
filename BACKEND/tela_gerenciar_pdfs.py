from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session
from werkzeug.utils import secure_filename
from .drive_service import criar_servico_drive
from BACKEND.models import Assinatura, AssinaturaStatus, db
import io
import os

bp = Blueprint("gerenciar_pdfs", __name__)
PASTA_PENDENTES_ID = '1F1sKFKavdwa-pVOO8erEVCxrPECMYjMF'

@bp.route('/gerenciar-pdfs')
def pagina_gerenciar_pdfs():
    if not session.get('logado'):
        return redirect(url_for('auth.login'))

    drive = criar_servico_drive()
    arquivos = drive.files().list(
        q=f"'{PASTA_PENDENTES_ID}' in parents and trashed = false",
        fields="files(id, name, createdTime)",
        orderBy="createdTime desc"
    ).execute().get('files', [])

    return render_template('tela_gerenciar_pdfs.html', arquivos=arquivos)

@bp.route('/enviar-pdf', methods=['POST'])
def enviar_pdf():
    if not session.get('logado'):
        return jsonify({'erro': 'Usuário não autenticado'}), 401

    arquivo = request.files.get('arquivo')
    if not arquivo or not arquivo.filename.endswith('.pdf'):
        return jsonify({'erro': 'Arquivo inválido'}), 400

    drive = criar_servico_drive()

    nome_seguro = secure_filename(arquivo.filename)
    media = arquivo.stream

    drive.files().create(
        media_body=media,
        body={
            'name': nome_seguro,
            'parents': [PASTA_PENDENTES_ID],
            'mimeType': 'application/pdf'
        },
        fields='id'
    ).execute()

    return jsonify({'mensagem': 'PDF enviado com sucesso!'}), 200

@bp.route('/excluir-pdf', methods=['POST'])
def excluir_pdf():
    if not session.get('logado'):
        return jsonify({'erro': 'Usuário não autenticado'}), 401

    id_pdf = request.form.get('id_pdf')
    if not id_pdf:
        return jsonify({'erro': 'ID do PDF ausente'}), 400

    drive = criar_servico_drive()

    # Exclui no Drive
    drive.files().delete(fileId=id_pdf).execute()

    # Exclui status no banco (se existir)
    status = AssinaturaStatus.query.filter_by(id_pdf=id_pdf).first()
    if status:
        db.session.delete(status)
        db.session.commit()

    return jsonify({'mensagem': 'PDF excluído com sucesso!'}), 200
