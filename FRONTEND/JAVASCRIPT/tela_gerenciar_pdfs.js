document.getElementById("form-upload").addEventListener("submit", async (e) => {
  e.preventDefault();

  const formData = new FormData(e.target);
  const resposta = await fetch("/enviar-pdf", {
    method: "POST",
    body: formData
  });

  const dados = await resposta.json();
  document.getElementById("mensagem").innerText = dados.mensagem || dados.erro;

  if (resposta.ok) {
    setTimeout(() => location.reload(), 1000);
  }
});

async function excluirPdf(id) {
  const confirmado = confirm("Tem certeza que deseja excluir este PDF?");
  if (!confirmado) return;

  const formData = new FormData();
  formData.append("id_pdf", id);

  const resposta = await fetch("/excluir-pdf", {
    method: "POST",
    body: formData
  });

  const dados = await resposta.json();
  alert(dados.mensagem || dados.erro);

  if (resposta.ok) {
    location.reload();
  }
}
