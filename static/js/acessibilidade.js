// Espera o documento carregar para executar o script
document.addEventListener('DOMContentLoaded', function() {
    
    // --- 1. Selecionando os Botões ---
    const btnAumentarFonte = document.getElementById('btn-aumentar-fonte');
    const btnDiminuirFonte = document.getElementById('btn-diminuir-fonte');
    const btnAltoContraste = document.getElementById('btn-alto-contraste');
    const htmlElement = document.documentElement; // A tag <html>
    const bodyElement = document.body;

    // --- 2. Estado Atual (Níveis de Fonte) ---
    // 0 = normal, 1 = media, 2 = grande
    let nivelFonte = 0;

    // --- 3. Funções ---

    function aplicarFonte() {
        // Remove classes anteriores
        htmlElement.classList.remove('fonte-media', 'fonte-grande');

        if (nivelFonte === 1) {
            htmlElement.classList.add('fonte-media');
        } else if (nivelFonte === 2) {
            htmlElement.classList.add('fonte-grande');
        }
        // Se for 0, não adiciona classe (volta ao normal)
        
        // Salva a preferência do usuário
        localStorage.setItem('nivelFonte', nivelFonte);
    }

    function aplicarContraste(ativo) {
        if (ativo) {
            bodyElement.classList.add('alto-contraste');
            localStorage.setItem('altoContraste', 'true');
        } else {
            bodyElement.classList.remove('alto-contraste');
            localStorage.setItem('altoContraste', 'false');
        }
    }

    // --- 4. Event Listeners (O que acontece ao clicar) ---

    // Botão Aumentar Fonte
    if (btnAumentarFonte) {
        btnAumentarFonte.addEventListener('click', function() {
            if (nivelFonte < 2) {
                nivelFonte++;
                aplicarFonte();
            }
        });
    }

    // Botão Diminuir Fonte
    if (btnDiminuirFonte) {
        btnDiminuirFonte.addEventListener('click', function() {
            if (nivelFonte > 0) {
                nivelFonte--;
                aplicarFonte();
            }
        });
    }

    // Botão Alto Contraste
    if (btnAltoContraste) {
        btnAltoContraste.addEventListener('click', function() {
            // Verifica se a classe JÁ existe para decidir se liga ou desliga
            const contrasteAtivo = bodyElement.classList.contains('alto-contraste');
            aplicarContraste(!contrasteAtivo); // Inverte o estado atual
        });
    }

    // --- 5. Carregar Preferências Salvas ---
    // Verifica se o usuário já tinha salvo preferências
    
    // Carrega a fonte salva
    const fonteSalva = localStorage.getItem('nivelFonte');
    if (fonteSalva) {
        nivelFonte = parseInt(fonteSalva, 10);
        aplicarFonte();
    }

    // Carrega o contraste salvo
    const contrasteSalvo = localStorage.getItem('altoContraste');
    if (contrasteSalvo === 'true') {
        aplicarContraste(true);
    }
});