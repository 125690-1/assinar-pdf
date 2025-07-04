from flask import Blueprint, render_template, session, redirect, url_for
from BACKEND.models import Assinatura, AssinaturaStatus, db
from .drive_service import criar_servico_drive

bp = Blueprint("tela_assinados", __name__)

PASTA_ASSINADOS_ID = '1BUXvC_IQ_EdZm_HKjL-SKs-t52zVBQCq'

@bp.route("/assinados")
def pagina_assinados():
    if not session.get("logado"):
        return redirect(url_for("auth.login"))

    drive = criar_servico_drive()

    # Buscar arquivos da pasta Assinados
    resultados = drive.files().list(
        q=f"'{PASTA_ASSINADOS_ID}' in parents and trashed = false",
        fields="files(id, name, modifiedTime)",
        orderBy="modifiedTime desc"
    ).execute()

    arquivos = resultados.get("files", [])

    dados = []
    for arquivo in arquivos:
        status = AssinaturaStatus.query.filter_by(id_pdf=arquivo["id"]).first()

        dados.append({
            "id": arquivo["id"],
            "nome_pdf": arquivo["name"],
            "nome_mro": status.nome_mro if status else "",
            "data_mro": status.data_mro if status else "",
            "nome_operacao": status.nome_operacao if status else "",
            "data_operacao": status.data_operacao if status else "",
        })

    return render_template("tela_assinados.html", arquivos=dados)
