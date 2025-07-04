from flask import Blueprint, request, jsonify
from googleapiclient.discovery import build
import google.auth
import io
from googleapiclient.http import MediaIoBaseUpload

bp = Blueprint('drive', __name__)

# ID da pasta no Drive (PENDENTES DE ASSINATURA)
PASTA_PENDENTES_ID = '1F1sKFKavdwa-pVOO8erEVCxrPECMYjMF'

# Autenticação automática via Service Account do projeto (Cloud Run)
def criar_servico_drive():
    creds, _ = google.auth.default(scopes=["https://www.googleapis.com/auth/drive"])
    return build('drive', 'v3', credentials=creds)

# Função para listar PDFs da pasta
def listar_pdfs_pendentes(folder_id):
    servico = criar_servico_drive()

    query = f"'{folder_id}' in parents and mimeType='application/pdf' and trashed = false"
    resultados = servico.files().list(q=query, fields="files(id, name)").execute()
    arquivos = resultados.get('files', [])

    pdfs = []
    for arquivo in arquivos:
        pdfs.append({
            'id': arquivo['id'],
            'nome': arquivo['name'],
            'link': f"https://drive.google.com/file/d/{arquivo['id']}/view"
        })

    return pdfs

# 🔽 Função para enviar PDF para o Drive
def enviar_pdf_para_drive(arquivo, folder_id):
    servico = criar_servico_drive()

    media = MediaIoBaseUpload(arquivo.stream, mimetype='application/pdf')
    nome_arquivo = arquivo.filename

    file_metadata = {
        'name': nome_arquivo,
        'parents': [folder_id]
    }

    arquivo_drive = servico.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()

    return arquivo_drive.get('id')

# 📥 Endpoint: /upload-pdf
@bp.route('/upload-pdf', methods=['POST'])
def upload_pdf():
    if 'arquivo' not in request.files:
        return jsonify({'erro': 'Nenhum arquivo enviado'}), 400

    arquivo = request.files['arquivo']

    if not arquivo.filename.endswith('.pdf'):
        return jsonify({'erro': 'Apenas arquivos PDF são permitidos'}), 400

    try:
        id_arquivo = enviar_pdf_para_drive(arquivo, PASTA_PENDENTES_ID)
        return jsonify({'mensagem': 'PDF enviado com sucesso', 'id': id_arquivo}), 200
    except Exception as e:
        return jsonify({'erro': f'Erro ao enviar: {str(e)}'}), 500
