document.addEventListener("DOMContentLoaded", function () {
  const modal = document.getElementById("modalAssinar");
  const iframe = document.getElementById("pdfViewer");
  const btnFechar = document.getElementById("btnFecharModal");
  const btnConfirmar = document.getElementById("btnConfirmarAssinatura");
  const btnAbrir = document.getElementById("btnAbrirPdf");
  const inputSenha = document.getElementById("senhaAssinatura");
  const btnAssinar = document.querySelectorAll(".btnAssinar");

  let idPdfAtual = null;

  btnFechar.addEventListener("click", () => {
    modal.style.display = "none";
    iframe.src = "";
    inputSenha.value = "";
  });

  btnAssinar.forEach((botao) => {
    botao.addEventListener("click", () => {
      idPdfAtual = botao.getAttribute("data-id");
      modal.style.display = "block";
      iframe.src = ""; // Limpa antes de abrir
    });
  });

  btnAbrir.addEventListener("click", () => {
    if (idPdfAtual) {
      iframe.src = `https://drive.google.com/file/d/${idPdfAtual}/preview`;
    }
  });

  btnConfirmar.addEventListener("click", async () => {
    const senha = inputSenha.value;

    if (!senha) {
      alert("Digite sua senha para confirmar.");
      return;
    }

    try {
      const formData = new FormData();
      formData.append("id_pdf", idPdfAtual);
      formData.append("senha", senha);

      const resposta = await fetch("/assinar-pdf", {
        method: "POST",
        body: formData,
      });

      const resultado = await resposta.json();

      if (resposta.ok) {
        alert("PDF assinado com sucesso!");
        location.reload();
      } else {
        alert(resultado.erro || "Erro ao assinar o PDF.");
      }
    } catch (erro) {
      console.error("Erro na requisição:", erro);
      alert("Erro na requisição.");
    }
  });
});
