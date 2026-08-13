const form = document.getElementById("form-consulta");
const input = document.getElementById("indicator");
const mensagem = document.getElementById("mensagem");
const resultado = document.getElementById("resultado");


form.addEventListener("submit", async function(event) {

    event.preventDefault();

    const indicator = input.value.trim();

    if (!indicator) {
        mensagem.textContent = "Digite um indicador.";
        resultado.textContent = "";
        return;
    }

    mensagem.textContent = "Consultando...";
    resultado.textContent = "";

    try {

        const response = await fetch(
            `/indicators/${encodeURIComponent(indicator)}`
        );

        const dados = await response.json();

        if (!response.ok) {
            mensagem.textContent = `Erro ${response.status}`;
            resultado.textContent = dados.detail || "Erro ao realizar consulta.";
            return;
        }

        mensagem.textContent = "Consulta realizada com sucesso.";

        resultado.textContent = JSON.stringify(dados, null, 4);

    } catch (erro) {

        mensagem.textContent = "Erro ao conectar com o servidor.";
        resultado.textContent = erro.message;
    }
});