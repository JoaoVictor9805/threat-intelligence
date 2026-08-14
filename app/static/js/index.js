const form = document.getElementById("form-consulta");
const input = document.getElementById("indicator");
const mensagem = document.getElementById("mensagem");
const dashboard = document.getElementById("dashboard");


// ============================================================
// GRÁFICOS
// ============================================================

let malwareChart = null;
let countriesChart = null;
let industriesChart = null;
let attackChart = null;


// ============================================================
// PAGINAÇÃO DOS PULSES
// ============================================================

let pulses = [];
let pulsesExibidos = 0;

const PULSES_POR_PAGINA = 5;


// ============================================================
// PAGINAÇÃO DO CONTEXTO DE AMEAÇA
// ============================================================

const ITEMS_POR_PAGINA = 10;

let malwareFamilies = [];
let malwareExibidos = 0;

let attackIds = [];
let attacksExibidos = 0;

let targetedCountries = [];
let countriesExibidos = 0;

let industriesList = [];
let industriesExibidos = 0;


// ============================================================
// FORMULÁRIO
// ============================================================

form.addEventListener("submit", async function(event) {

    event.preventDefault();

    const indicator = input.value.trim();

    if (!indicator) {

        mensagem.textContent = "Digite um indicador.";
        dashboard.style.display = "none";

        return;
    }


    mensagem.textContent = "Consultando...";
    dashboard.style.display = "none";


    try {

        const response = await fetch(
            `/indicators/${encodeURIComponent(indicator)}`
        );


        const dados = await response.json();


        if (!response.ok) {

            mensagem.textContent =
                `Erro ${response.status}: ${
                    dados.detail || "Erro ao realizar consulta."
                }`;

            return;
        }


        mensagem.textContent =
            "Consulta realizada com sucesso.";


        dashboard.style.display = "block";


        renderDashboard(dados);


    } catch (erro) {

        mensagem.textContent =
            "Erro ao conectar com o servidor.";

        console.error(erro);
    }

});


// ============================================================
// DASHBOARD
// ============================================================

function renderDashboard(dados) {

    renderIndicator(dados);

    renderKPIs(dados);

    renderLocation(dados);

    renderInfrastructure(dados);

    renderThreatContext(dados);

    renderCharts(dados);

    renderValidations(dados);

    renderFalsePositives(dados);

    setupPulses(dados.pulses || []);
}


// ============================================================
// INDICADOR
// ============================================================

function renderIndicator(dados) {

    document.getElementById("indicator-value").textContent =
        dados.indicador || "-";


    document.getElementById("indicator-type").textContent =
        dados.tipo || "-";
}


// ============================================================
// KPIs
// ============================================================

function renderKPIs(dados) {

    document.getElementById("reputacao").textContent =
        dados.reputacao ?? "-";


    document.getElementById("quantidade-pulses").textContent =
        dados.quantidade_pulses ?? 0;


    document.getElementById("quantidade-validation").textContent =
        (dados.validation || []).length;


    document.getElementById("quantidade-false-positive").textContent =
        (dados.false_positive || []).length;
}


// ============================================================
// LOCALIZAÇÃO
// ============================================================

function renderLocation(dados) {

    const container =
        document.getElementById("localizacao");


    const campos = [
        ["País", dados.pais],
        ["Código do país", dados.codigo_pais],
        ["Continente", dados.continente],
        ["Cidade", dados.cidade],
        ["Região", dados.regiao],
        ["Subdivisão", dados.subdivisao]
    ];


    container.innerHTML = "";


    let encontrouDados = false;


    campos.forEach(([label, value]) => {

        if (
            value !== null &&
            value !== undefined &&
            value !== ""
        ) {

            encontrouDados = true;

            container.innerHTML += `
                <div class="info-row">

                    <span class="info-label">
                        ${escapeHtml(label)}
                    </span>

                    <span class="info-value">
                        ${escapeHtml(String(value))}
                    </span>

                </div>
            `;
        }

    });


    if (!encontrouDados) {

        container.innerHTML =
            `<div class="empty">
                Nenhuma informação de localização disponível.
            </div>`;
    }
}


// ============================================================
// INFRAESTRUTURA
// ============================================================

function renderInfrastructure(dados) {

    const container =
        document.getElementById("infraestrutura");


    container.innerHTML = "";


    const campos = [
        ["ASN", dados.asn],
        ["WHOIS", dados.whois]
    ];


    let encontrouDados = false;


    campos.forEach(([label, value]) => {

        if (
            value !== null &&
            value !== undefined &&
            value !== ""
        ) {

            encontrouDados = true;

            container.innerHTML += `
                <div class="info-row">

                    <span class="info-label">
                        ${escapeHtml(label)}
                    </span>

                    <span class="info-value">
                        ${escapeHtml(String(value))}
                    </span>

                </div>
            `;
        }

    });


    if (!encontrouDados) {

        container.innerHTML =
            `<div class="empty">
                Nenhuma informação de infraestrutura disponível.
            </div>`;
    }
}


// ============================================================
// CONTEXTO DE AMEAÇA
// ============================================================

function renderThreatContext(dados) {

    renderMalwareFamilies(dados);

    renderAttackIds(dados);

    renderCountries(dados);

    renderIndustries(dados);
}


// ============================================================
// MALWARE FAMILIES
// ============================================================

function renderMalwareFamilies(dados) {

    const families =
        dados.pulses?.flatMap(
            pulse => pulse.malware_families || []
        ) || [];


    malwareFamilies = [];


    families.forEach(family => {

        const exists =
            malwareFamilies.some(
                item => item.id === family.id
            );


        if (!exists) {

            malwareFamilies.push(family);

        }

    });


    malwareExibidos = 0;


    const container =
        document.getElementById("malware-families");

    container.innerHTML = "";


    document.getElementById("malware-count").textContent =
        malwareFamilies.length;


    if (malwareFamilies.length === 0) {

        container.innerHTML =
            `<div class="empty-state">
                Nenhuma informação disponível.
            </div>`;

        document.getElementById(
            "show-more-malware"
        ).style.display = "none";

        return;
    }


    renderMoreMalware();
}


// ============================================================
// MAIS MALWARE FAMILIES
// ============================================================

function renderMoreMalware() {

    const container =
        document.getElementById("malware-families");


    const inicio =
        malwareExibidos;


    const fim =
        Math.min(
            inicio + ITEMS_POR_PAGINA,
            malwareFamilies.length
        );


    for (let i = inicio; i < fim; i++) {

        const family =
            malwareFamilies[i];


        container.innerHTML += `

            <div class="threat-item">

                <strong>
                    ${escapeHtml(
                        family.display_name ||
                        family.id
                    )}
                </strong>

                ${
                    family.target
                        ? `
                            <small>
                                ${escapeHtml(family.target)}
                            </small>
                          `
                        : ""
                }

            </div>

        `;
    }


    malwareExibidos = fim;


    updateThreatButton(
        "show-more-malware",
        malwareExibidos,
        malwareFamilies.length
    );
}


// ============================================================
// MITRE ATT&CK
// ============================================================

function renderAttackIds(dados) {

    const attacks =
        dados.pulses?.flatMap(
            pulse => pulse.attack_ids || []
        ) || [];


    attackIds = [];


    attacks.forEach(attack => {

        const exists =
            attackIds.some(
                item => item.id === attack.id
            );


        if (!exists) {

            attackIds.push(attack);

        }

    });


    attacksExibidos = 0;


    const container =
        document.getElementById("attack-ids");

    container.innerHTML = "";


    document.getElementById("attack-count").textContent =
        attackIds.length;


    if (attackIds.length === 0) {

        container.innerHTML =
            `<div class="empty-state">
                Nenhuma informação disponível.
            </div>`;

        document.getElementById(
            "show-more-attack"
        ).style.display = "none";

        return;
    }


    renderMoreAttacks();
}

// ============================================================
// MAIS MITRE ATT&CK
// ============================================================

function renderMoreAttacks() {

    const container =
        document.getElementById("attack-ids");


    const inicio =
        attacksExibidos;


    const fim =
        Math.min(
            inicio + ITEMS_POR_PAGINA,
            attackIds.length
        );


    for (let i = inicio; i < fim; i++) {

        const attack =
            attackIds[i];


        container.innerHTML += `

            <div class="threat-item">

                <strong>
                    ${escapeHtml(
                        attack.display_name ||
                        attack.name ||
                        attack.id ||
                        "Técnica"
                    )}
                </strong>

                ${
                    attack.id
                        ? `
                            <small>
                                ID:
                                ${escapeHtml(attack.id)}
                            </small>
                          `
                        : ""
                }

            </div>

        `;
    }


    attacksExibidos = fim;


    updateThreatButton(
        "show-more-attack",
        attacksExibidos,
        attackIds.length
    );
}


// ============================================================
// PAÍSES-ALVO
// ============================================================

function renderCountries(dados) {

    const countries =
        dados.pulses?.flatMap(
            pulse => pulse.targeted_countries || []
        ) || [];


    targetedCountries =
        [...new Set(countries)];


    countriesExibidos = 0;


    const container =
        document.getElementById("targeted-countries");

    container.innerHTML = "";


    document.getElementById("countries-count").textContent =
        targetedCountries.length;


    if (targetedCountries.length === 0) {

        container.innerHTML =
            `<div class="empty-state">
                Nenhuma informação disponível.
            </div>`;

        document.getElementById(
            "show-more-countries"
        ).style.display = "none";

        return;
    }


    renderMoreCountries();
}


// ============================================================
// MAIS PAÍSES
// ============================================================

function renderMoreCountries() {

    const container =
        document.getElementById("targeted-countries");


    const inicio =
        countriesExibidos;


    const fim =
        Math.min(
            inicio + ITEMS_POR_PAGINA,
            targetedCountries.length
        );


    for (let i = inicio; i < fim; i++) {

        const country =
            targetedCountries[i];


        container.innerHTML += `

            <div class="threat-item">

                <strong>
                    ${escapeHtml(country)}
                </strong>

            </div>

        `;
    }


    countriesExibidos = fim;


    updateThreatButton(
        "show-more-countries",
        countriesExibidos,
        targetedCountries.length
    );
}


// ============================================================
// INDÚSTRIAS
// ============================================================

function renderIndustries(dados) {

    const industries =
        dados.pulses?.flatMap(
            pulse => pulse.industries || []
        ) || [];


    industriesList =
        [...new Set(industries)];


    industriesExibidos = 0;


    const container =
        document.getElementById("industries");

    container.innerHTML = "";


    document.getElementById("industries-count").textContent =
        industriesList.length;


    if (industriesList.length === 0) {

        container.innerHTML =
            `<div class="empty-state">
                Nenhuma informação disponível.
            </div>`;

        document.getElementById(
            "show-more-industries"
        ).style.display = "none";

        return;
    }


    renderMoreIndustries();
}


// ============================================================
// MAIS INDÚSTRIAS
// ============================================================

function renderMoreIndustries() {

    const container =
        document.getElementById("industries");


    const inicio =
        industriesExibidos;


    const fim =
        Math.min(
            inicio + ITEMS_POR_PAGINA,
            industriesList.length
        );


    for (let i = inicio; i < fim; i++) {

        const industry =
            industriesList[i];


        container.innerHTML += `

            <div class="threat-item">

                <strong>
                    ${escapeHtml(industry)}
                </strong>

            </div>

        `;
    }


    industriesExibidos = fim;


    updateThreatButton(
        "show-more-industries",
        industriesExibidos,
        industriesList.length
    );
}


// ============================================================
// CONTROLE DOS BOTÕES "VER MAIS"
// ============================================================

function updateThreatButton(
    buttonId,
    exibidos,
    total
) {

    const button =
        document.getElementById(buttonId);


    if (!button) {
        return;
    }


    if (exibidos >= total) {

        button.style.display = "none";

    } else {

        button.style.display = "block";

    }
}


// ============================================================
// GRÁFICOS
// ============================================================

function renderCharts(dados) {

    const pulses =
        dados.pulses || [];


    // ----------------------------------------
    // MALWARE
    // ----------------------------------------

    const malware = countValues(
        pulses.flatMap(
            pulse =>
                (pulse.malware_families || [])
                    .map(
                        malware =>
                            malware.display_name ||
                            malware.id
                    )
        )
    );


    // ----------------------------------------
    // PAÍSES
    // ----------------------------------------

    const countries = countValues(
        pulses.flatMap(
            pulse =>
                pulse.targeted_countries || []
        )
    );


    // ----------------------------------------
    // INDÚSTRIAS
    // ----------------------------------------

    const industries = countValues(
        pulses.flatMap(
            pulse =>
                pulse.industries || []
        )
    );


    // ----------------------------------------
    // MITRE
    // ----------------------------------------

    const attacks = countValues(
        pulses.flatMap(
            pulse =>
                (pulse.attack_ids || [])
                    .map(
                        attack =>
                            attack.display_name ||
                            attack.name ||
                            attack.id
                    )
        )
    );


    malwareChart = createBarChart(
        "malware-chart",
        malwareChart,
        malware
    );


    countriesChart = createBarChart(
        "countries-chart",
        countriesChart,
        countries
    );


    industriesChart = createBarChart(
        "industries-chart",
        industriesChart,
        industries
    );


    attackChart = createBarChart(
        "attack-chart",
        attackChart,
        attacks
    );
}


// ============================================================
// CRIAÇÃO DOS GRÁFICOS
// ============================================================

function createBarChart(
    canvasId,
    existingChart,
    data
) {

    if (existingChart) {

        existingChart.destroy();

    }


    const canvas =
        document.getElementById(canvasId);


    const empty =
        document.getElementById(
            `${canvasId}-empty`
        );


    const labels =
        Object.keys(data);


    const values =
        Object.values(data);


    if (labels.length === 0) {

        canvas.style.display = "none";

        empty.style.display = "flex";

        return null;
    }


    canvas.style.display = "block";

    empty.style.display = "none";


    return new Chart(canvas, {

        type: "bar",

        data: {

            labels: labels,

            datasets: [

                {
                    data: values
                }

            ]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            indexAxis: "y",

            plugins: {

                legend: {
                    display: false
                }

            },

            scales: {

                x: {

                    beginAtZero: true,

                    ticks: {
                        precision: 0
                    }

                }

            }

        }

    });
}

// ============================================================
// CONTAGEM DOS DADOS
// ============================================================

function countValues(values) {

    const result = {};


    values.forEach(value => {

        if (!value) {
            return;
        }


        result[value] =
            (result[value] || 0) + 1;

    });


    return Object.fromEntries(

        Object.entries(result)
            .sort(
                (a, b) =>
                    b[1] - a[1]
            )

    );
}


// ============================================================
// VALIDAÇÕES
// ============================================================

function renderValidations(dados) {

    const container =
        document.getElementById("validation-list");


    container.innerHTML = "";


    const validations =
        dados.validation || [];


    if (validations.length === 0) {

        container.innerHTML =
            `<div class="empty">
                Nenhuma validação encontrada.
            </div>`;

        return;
    }


    validations.forEach(validation => {

        container.innerHTML += `

            <div class="validation">

                <strong>
                    ${escapeHtml(
                        validation.name ||
                        "Validação"
                    )}
                </strong>

                <span>
                    ${escapeHtml(
                        validation.message || ""
                    )}
                </span>

            </div>

        `;

    });
}


// ============================================================
// FALSOS POSITIVOS
// ============================================================

function renderFalsePositives(dados) {

    const container =
        document.getElementById(
            "false-positive-list"
        );


    container.innerHTML = "";


    const falsePositives =
        dados.false_positive || [];


    if (falsePositives.length === 0) {

        container.innerHTML =
            `<div class="empty">
                Nenhuma avaliação de falso positivo encontrada.
            </div>`;

        return;
    }


    falsePositives.forEach(item => {

        container.innerHTML += `

            <div class="false-positive">

                <strong>
                    ${escapeHtml(
                        item.assessment ||
                        "Não informado"
                    )}
                </strong>

                <div>
                    Reportado:
                    ${formatDate(
                        item.report_date
                    )}
                </div>

                <div>
                    Avaliado:
                    ${formatDate(
                        item.assessment_date
                    )}
                </div>

            </div>

        `;

    });
}


// ============================================================
// PULSES
// ============================================================

function setupPulses(lista) {

    pulses = lista;

    pulsesExibidos = 0;


    const container =
        document.getElementById("pulse-list");

    container.innerHTML = "";


    const button =
        document.getElementById(
            "show-more-pulses"
        );


    if (pulses.length === 0) {

        container.innerHTML =
            `<div class="empty-state">
                Nenhuma informação disponível.
            </div>`;

        button.style.display = "none";

        return;
    }


    renderMorePulses();
}


// ============================================================
// MAIS PULSES
// ============================================================

function renderMorePulses() {

    const container =
        document.getElementById(
            "pulse-list"
        );


    const inicio =
        pulsesExibidos;


    const fim =
        Math.min(
            inicio + PULSES_POR_PAGINA,
            pulses.length
        );


    for (
        let i = inicio;
        i < fim;
        i++
    ) {

        const pulse =
            pulses[i];


        const tags =
            pulse.tags || [];


        container.innerHTML += `

            <div class="pulse">

                <div class="pulse-title">

                    ${escapeHtml(
                        pulse.name ||
                        "Pulse sem nome"
                    )}

                </div>


                <div class="pulse-description">

                    ${escapeHtml(
                        pulse.description ||
                        "Sem descrição disponível."
                    )}

                </div>


                <div class="pulse-meta">

                    ${
                        pulse.adversary
                            ? `
                                <span>
                                    Adversário:
                                    ${escapeHtml(
                                        pulse.adversary
                                    )}
                                </span>
                              `
                            : ""
                    }


                    ${
                        pulse.tlp
                            ? `
                                <span>
                                    TLP:
                                    ${escapeHtml(
                                        pulse.tlp
                                    )}
                                </span>
                              `
                            : ""
                    }


                    ${
                        pulse.modified
                            ? `
                                <span>
                                    Modificado:
                                    ${formatDate(
                                        pulse.modified
                                    )}
                                </span>
                              `
                            : ""
                    }

                </div>


                ${
                    tags.length > 0
                        ? `
                            <div
                                class="tags"
                                style="margin-top:10px"
                            >

                                ${tags.map(
                                    tag => `
                                        <span class="tag">
                                            ${escapeHtml(tag)}
                                        </span>
                                    `
                                ).join("")}

                            </div>
                          `
                        : ""
                }

            </div>

        `;
    }


    pulsesExibidos = fim;


    const button =
        document.getElementById(
            "show-more-pulses"
        );


    if (
        pulsesExibidos >=
        pulses.length
    ) {

        button.style.display = "none";

    } else {

        button.style.display = "block";

    }
}


// ============================================================
// EVENTOS DOS BOTÕES
// ============================================================

document
    .getElementById("show-more-pulses")
    .addEventListener(
        "click",
        renderMorePulses
    );


document
    .getElementById("show-more-malware")
    .addEventListener(
        "click",
        renderMoreMalware
    );


document
    .getElementById("show-more-attack")
    .addEventListener(
        "click",
        renderMoreAttacks
    );


document
    .getElementById("show-more-countries")
    .addEventListener(
        "click",
        renderMoreCountries
    );


document
    .getElementById("show-more-industries")
    .addEventListener(
        "click",
        renderMoreIndustries
    );


// ============================================================
// FORMATAÇÃO DE DATA
// ============================================================

function formatDate(date) {

    if (!date) {
        return "-";
    }


    const parsed =
        new Date(date);


    if (isNaN(parsed.getTime())) {

        return date;

    }


    return parsed.toLocaleString(
        "pt-BR"
    );
}


// ============================================================
// SEGURANÇA
// ============================================================

function escapeHtml(value) {

    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}