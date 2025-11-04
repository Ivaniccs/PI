describe('Validação da exibição dos principais elementos da página de contato', () => {
    beforeEach(() => {
        cy.visit('/contato')
    })
    it('deve exibir todos os elementos do formulário corretamente', () => {
        cy.get('label[for="nome"]').should('contain.text', 'Nome')
        cy.get('#nome').should('be.visible')
        cy.get('label[for="mensagem"]').should('contain.text', 'Mensagem')
        cy.get('#mensagem').should('be.visible')
        cy.get('button[type="submit"]').should('contain.text', 'Enviar via WhatsApp')
    })
    it('deve exibir a seção de informações de contato e endereço corretamente', () => {
        cy.get('h2').should('contain.text', 'Informações de Contato')
        cy.get('ul').should('contain.text', 'Rua Presidente Bernardes, 541 - Jardim Paulista, SJC-SP')
        cy.get('ul').should('contain.text', '(12) 98284-1105')
        cy.get('ul').should('contain.text', 'Bolosdaanaclaudia')
        cy.get('ul').should('contain.text', 'Todos os dias.')
        cy.get('iframe').should('be.visible')
    })
    it('o link do Instagram deve redirecionar para a página do Instagram corretamente', () => {
        cy.get('a[href="https://www.instagram.com/bolosdaanaclaudia/"]').should('be.visible')
        .should('have.attr', 'href', 'https://www.instagram.com/bolosdaanaclaudia/')
    })
    it('o footer deve exibir o texto corretamente', () => {
        cy.get('footer').should('be.visible')
        .should('contain.text', '© PI-2025-UNIVESP - Doce Conexão - Bolos da Ana')
    })
    it('o header deve exibir os itens do menu corretamente', () => {
        cy.get('header').should('be.visible')
        .should('contain.text', 'Início')
        .should('contain.text', 'Cardápio')
        .should('contain.text', 'Carrinho')
        .should('contain.text', 'Contato')
    })
    it('deve enviar mensagem via WhatsApp', () => {
        cy.get('#nome').type('Teste')
        cy.get('#mensagem').type('Teste automatizado')
        // Interceptar e mockar o wa.me
        cy.intercept('GET', '**/wa.me/**', { statusCode: 200 })
        cy.get('[type="submit"]').click()
        cy.get('#nome').should('have.value', ' ')
      })   
})