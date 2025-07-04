document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("form-usuario");
  const tabela = document.getElementById("tabela-usuarios");

  function carregarUsuarios() {
    fetch("/usuarios")
      .then(res => res.json())
      .then(dados => {
        tabela.innerHTML = "";
        dados.forEach(usuario => {
          const linha = document.createElement("tr");
          linha.innerHTML = `
            <td>${usuario.br}</td>
            <td>${usuario.nome}</td>
            <td>${usuario.tipo}</td>
            <td>${usuario.imagem || ''}</td>
            <td>
              <button onclick="editar(${usuario.id}, '${usuario.br}', '${usuario.nome}', '${usuario.tipo}')">✏️</button>
              <button onclick="excluir(${usuario.id})">🗑️</button>
            </td>
          `;
          tabela.appendChild(linha);
        });
      });
  }

  form.addEventListener("submit", e => {
    e.preventDefault();

    const id = document.getElementById("id").value;
    const br = document.getElementById("br").value;
    const nome = document.getElementById("nome").value;
    const senha = document.getElementById("senha").value;
    const tipo = document.getElementById("tipo").value;
    const imagem = document.getElementById("imagem").files[0];

    const formData = new FormData();
    formData.append("br", br);
    formData.append("nome", nome);
    formData.append("senha", senha);
    formData.append("tipo", tipo);
    if (imagem) formData.append("imagem", imagem);

    const url = id ? `/usuarios/${id}` : "/usuarios";
    const metodo = id ? "PUT" : "POST";

    fetch(url, {
      method: metodo,
      body: formData
    }).then(() => {
      form.reset();
      carregarUsuarios();
    });
  });

  window.editar = (id, br, nome, tipo) => {
    document.getElementById("id").value = id;
    document.getElementById("br").value = br;
    document.getElementById("nome").value = nome;
    document.getElementById("tipo").value = tipo;
  };

  window.excluir = (id) => {
    if (confirm("Confirma a exclusão?")) {
      fetch(`/usuarios/${id}`, { method: "DELETE" })
        .then(() => carregarUsuarios());
    }
  };

  carregarUsuarios();
});
