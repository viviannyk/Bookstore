// Menu lateral
const btnMenu = document.getElementById('btn_mobile');
const menu = document.getElementById('menu');

const toggleMenu = (aberto) => {
    menu.classList.toggle('ativo', aberto);
    btnMenu.setAttribute('aria-expanded', aberto);
    btnMenu.setAttribute('aria-label', aberto ? 'Fechar menu' : 'Abrir menu');
    menu.inert = !aberto;
};

if (btnMenu) {
    menu.inert = true;
    btnMenu.addEventListener('click', () => toggleMenu(true));
    document.getElementById('btn_fechar_menu').addEventListener('click', () => toggleMenu(false));
    menu.addEventListener('click', (event) => {
        if (event.target === menu) toggleMenu(false);
    });
    document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape') toggleMenu(false);
    });
}

// Abas e busca filtram os mesmos cards
const cards = document.querySelectorAll('[data-aba]');
const abas = document.querySelectorAll('.aba');
const inputBusca = document.getElementById('busca_cards');
let abaAtual = document.querySelector('.aba[aria-pressed="true"]')?.dataset.alvo ?? 'todos';

const filtrarCards = () => {
    const termo = inputBusca ? inputBusca.value.trim().toLowerCase() : '';

    cards.forEach((card) => {
        const naAba = abaAtual === 'todos' || card.dataset.aba === abaAtual;
        const naBusca = card.textContent.toLowerCase().includes(termo);
        card.hidden = !(naAba && naBusca);
    });
};

abas.forEach((aba) => {
    aba.addEventListener('click', () => {
        abaAtual = aba.dataset.alvo;
        abas.forEach((item) => item.setAttribute('aria-pressed', item === aba));
        filtrarCards();
    });
});

filtrarCards();

if (inputBusca) {
    const secaoLivros = document.getElementById('livros');

    inputBusca.addEventListener('input', () => {
        filtrarCards();
        if (secaoLivros) secaoLivros.scrollIntoView();
    });

    document.getElementById('btn_busca').addEventListener('click', () => {
        const aberta = document.getElementById('caixa_busca').classList.toggle('aberta');
        if (aberta) inputBusca.focus();
    });
}

// Máscaras
const mask_cpf = (text) => {
    return text
        .replace(/\D+/g, '')
        .replace(/(\d{3})(\d)/, '$1.$2')
        .replace(/(\d{3})(\d)/, '$1.$2')
        .replace(/(\d{3})(\d{1,2})/, '$1-$2')
        .replace(/(-\d{2})\d+?$/, '$1');
};

const mask_phone = (text) => {
    return text
        .replace(/\D+/g, '')
        .replace(/(\d{2})(\d)/, '($1) $2')
        .replace(/(\d{4})(\d)/, '$1-$2')
        .replace(/(\d{4})-(\d)(\d{4})/, '$1$2-$3')
        .replace(/(-\d{4})\d+?$/, '$1');
};

const mascaras = { cpf: mask_cpf, telefone: mask_phone };

document.querySelectorAll('[data-mascara]').forEach((input) => {
    input.addEventListener('keyup', () => {
        input.value = mascaras[input.dataset.mascara](input.value);
    });
});

// Quantidade na pesquisa de livros
const rangeQtd = document.getElementById('qtd');

if (rangeQtd) {
    rangeQtd.addEventListener('input', () => {
        document.getElementById('qtd_prod').textContent = `Até ${rangeQtd.value} Produtos`;
    });
}
