from flask import Blueprint, request, jsonify, session
from BACKEND.models import Assinatura, AssinaturaStatus, db
from .drive_service import criar_servico_drive
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
import io
from datetime import datetime

bp = Blueprint("assinar_pdf", __name__)

def inserir_assinatura_pdf(pdf_original, imagem_assinatura, tipo, nome_usuario, timestamp):
    # Define posição da assinatura com base no tipo
    posicoes = {
        'MRO': {'x': 85, 'y': 60},
        'OPERAÇÃO': {'x': 380, 'y': 60}
    }

    if tipo not in posicoes:
        raise ValueError("Tipo de assinatura inválido")

    pos = posicoes[tipo]
    largura = 160
    altura = 80

    # Criar camada de assinatura (canvas)
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    # Desenhar imagem da assinatura
    assinatura = ImageReader(imagem_assinatura)
    c.drawImage(assinatura, pos['x'], pos['y'] + 20, width=largura, height=40, preserveAspectRatio=True, mask='auto')

    # Nome e timestamp
    c.setFont("Helvetica", 8)
    c.drawCentredString(pos['x'] + largura / 2, pos['y'] + 10, f"{tipo} – {timestamp}")
    c.drawCentredString(pos['x'] + largura / 2, pos['y'], nome_usuario.upper())

    c.save()
    buffer.seek(0)

    # Carrega o PDF original e mescla com o canvas da assinatura
    pdf_reader = PdfReader(pdf_original)
    pdf_writer = PdfWriter()
    assinatura_pdf = PdfReader(buffer)

    # Aplica assinatura apenas na primeira página
    pagina_original = pdf_reader.pages[0]
    pagina_original.merge_page(assinatura_pdf.pages[0])
    pdf_writer.add_page(pagina_original)

    # Adiciona demais páginas (se houver)
    for i in range(1, len(pdf_reader.pages)):
        pdf_writer.add_page(pdf_reader.pages[i])

    # Salva novo PDF em memória
    saida = io.BytesIO()
    pdf_writer.write(saida)
    saida.seek(0)

    return saida  # Retorna o novo PDF assinado


# ID da pasta de destino dos PDFs assinados
PASTA_ASSINADOS_ID = '1BUXvC_IQ_EdZm_HKjL-SKs-t52zVBQCq'
PASTA_PENDENTES_ID = '1F1sKFKavdwa-pVOO8erEVCxrPECMYjMF'
PASTA_IMAGENS_ID = '1EaFUXuLdYTKQmqxRAN037IyRiTIL7AYZ'


@bp.route('/assinar-pdf', methods=['POST'])
def assinar_pdf():
    if not session.get('logado'):
        return jsonify({'erro': 'Usuário não autenticado'}), 401

    id_pdf = request.form.get('id_pdf')
    senha_digitada = request.form.get('senha')

    usuario = Assinatura.query.filter_by(nome=session['usuario']).first()
    if not usuario or usuario.senha != senha_digitada:
        return jsonify({'erro': 'Senha incorreta'}), 403

    tipo = usuario.tipo
    nome = usuario.nome
    timestamp = datetime.now().strftime('%d/%m/%Y %H:%M')

    try:
        drive = criar_servico_drive()

        # Baixar o PDF original
        pdf_bytes = io.BytesIO()
        drive.files().get_media(fileId=id_pdf).execute_to_stream(pdf_bytes)
        pdf_bytes.seek(0)

        # Baixar imagem da assinatura
        arquivos = drive.files().list(
            q=f"name='{usuario.imagem}' and '{PASTA_IMAGENS_ID}' in parents and trashed = false",
            fields="files(id, name)"
        ).execute().get('files', [])

        if not arquivos:
            return jsonify({'erro': 'Imagem da assinatura não encontrada'}), 404

        id_imagem = arquivos[0]['id']
        imagem_bytes = io.BytesIO()
        drive.files().get_media(fileId=id_imagem).execute_to_stream(imagem_bytes)
        imagem_bytes.seek(0)

        # Inserir assinatura
        novo_pdf = inserir_assinatura_pdf(pdf_bytes, imagem_bytes, tipo, nome, timestamp)

        # Substituir o PDF no Drive
        drive.files().update(
            fileId=id_pdf,
            media_body=io.BytesIO(novo_pdf.read()),
            fields="id"
        ).execute()

        # Atualizar status no banco
        status = AssinaturaStatus.query.filter_by(id_pdf=id_pdf).first()
        if not status:
            status = AssinaturaStatus(id_pdf=id_pdf)
            db.session.add(status)

        if tipo == 'MRO':
            status.mro_assinou = True
            status.nome_mro = nome
            status.data_mro = timestamp
        elif tipo == 'OPERAÇÃO':
            status.operacao_assinou = True
            status.nome_operacao = nome
            status.data_operacao = timestamp

        db.session.commit()

        # Se ambos assinaram, mover para a pasta "Assinados"
        if status.mro_assinou and status.operacao_assinou:
            drive.files().update(
                fileId=id_pdf,
                addParents=PASTA_ASSINADOS_ID,
                removeParents=PASTA_PENDENTES_ID,
                fields="id, parents"
            ).execute()

        return jsonify({'mensagem': 'Assinatura aplicada com sucesso!'}), 200

    except Exception as e:
        return jsonify({'erro': f'Erro ao assinar: {str(e)}'}), 500
