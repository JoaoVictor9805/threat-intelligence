/* =========================================================
   CONFIGURAÇÃO
========================================================= */

const ITENS_POR_PAGINA = 10;


/* =========================================================
   ELEMENTOS
========================================================= */

const consultas =
    document.querySelectorAll(".consulta");

const botaoVerMais =
    document.getElementById("show-more");

const contador =
    document.getElementById("history-count");


/* =========================================================
   ESTADO
========================================================= */

let quantidadeVisivel =
    ITENS_POR_PAGINA;


/* =========================================================
   INICIALIZAÇÃO
========================================================= */

function inicializarHistorico() {

    if (!consultas.length) {

        if (botaoVerMais) {
            botaoVerMais.style.display = "none";
        }

        return;
    }


    atualizarLista();

}


/* =========================================================
   ATUALIZAÇÃO DA LISTA
========================================================= */

function atualizarLista() {

    consultas.forEach((consulta, index) => {

        if (index < quantidadeVisivel) {

            consulta.style.display = "flex";

        } else {

            consulta.style.display = "none";

        }

    });


    atualizarContador();


    atualizarBotao();

}


/* =========================================================
   CONTADOR
========================================================= */

function atualizarContador() {

    const quantidadeAtual =
        Math.min(
            quantidadeVisivel,
            consultas.length
        );


    if (contador) {

        contador.textContent =
            quantidadeAtual;

    }

}


/* =========================================================
   BOTÃO VER MAIS
========================================================= */

function atualizarBotao() {

    if (!botaoVerMais) {
        return;
    }


    if (quantidadeVisivel >= consultas.length) {

        botaoVerMais.style.display =
            "none";

        return;
    }


    botaoVerMais.style.display =
        "block";

}


/* =========================================================
   CLIQUE EM "VER MAIS"
========================================================= */

if (botaoVerMais) {

    botaoVerMais.addEventListener(
        "click",
        function () {

            quantidadeVisivel +=
                ITENS_POR_PAGINA;


            atualizarLista();

        }
    );

}


/* =========================================================
   INICIAR
========================================================= */

inicializarHistorico();