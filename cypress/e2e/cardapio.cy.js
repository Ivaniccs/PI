describe('Cardápio - Testes da página de produtos', () => {
  beforeEach(() => {
    cy.visit('/Cardapio')
  })

  it('Deve exibir a lista de produtos', () => {
    cy.get('.produtos').should('be.visible')
    cy.get('.produto').should('have.length.greaterThan', 0)
  })

  it('Deve exibir imagem, nome e preço de cada produto', () => {
    cy.get('.produto').first().within(() => {
      cy.get('img').should('be.visible')
      cy.get('.nome_produto h4').should('be.visible')
      cy.get('.preco_pos h4').should('be.visible')
    })
  })

  it('Deve exibir os botões de Detalhes e Comprar', () => {
    cy.get('.produto').first().within(() => {
      cy.get('.botoes_produto_rodape a').should('have.length', 2)
      cy.get('.botoes_produto_rodape a').first().should('contain', 'Detalhes')
      cy.get('.botoes_produto_rodape a').eq(1).should('contain', 'Comprar')
    })
  })

  it('Deve abrir o popup ao clicar em Detalhes', () => {
    cy.get('.produto').first().find('a').first().click()
    cy.get('#popup-overlay').should('have.css', 'display', 'flex')
    cy.get('.popup-content').should('be.visible')
  })

  it('Deve exibir nome, imagem e descrição do produto no popup', () => {
    cy.get('.produto').first().find('a').first().click()
    cy.get('.popup-body h2').should('be.visible')
    cy.get('.popup-body img').should('be.visible')
    cy.get('.popup-body p').should('be.visible')
  })

  it('Deve fechar o popup ao clicar no botão de fechar', () => {
    cy.get('.produto').first().find('a').first().click()
    cy.get('#popup-overlay').should('have.css', 'display', 'flex')
    cy.get('.close-btn').click()
    cy.get('#popup-overlay').should('have.css', 'display', 'none')
  })


  it('Deve adicionar produto ao carrinho ao clicar em Comprar', () => {
    cy.get('.produto').first().find('form').submit()
    cy.url().should('include', '/carrinho')
  })

});
