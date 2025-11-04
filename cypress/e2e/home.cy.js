describe('Validação da exibição dos principais elementos da página inicial', () => {
  beforeEach(() => {
    cy.visit('/Inicio')
  })
   it('Deve exibir o texto de apresentação da página inicial corretamente', () => {
    cy.get('[data-testid="texto-inicio"]')
    .should('be.visible')
    .should('contain.text', 'A empresa Bolos da Ana está fazendo a vida mais doce desde 2015')
    .should('contain.text', 'Em parceria com a escola Poliedro-SJC')
    .should('contain.text', 'Siga-nos')
  })
  it('deve redirecionar para o perfil do Instagram', () => {
    cy.get('[data-testid="instagram-link"]').click()
    .should('have.attr', 'href', 'https://www.instagram.com/bolosdaanaclaudia/')
  })
  it('deve exibir o carrossel na página inicial', () => {
    cy.get('#carrosselPaginaInicial').should('be.visible')
  })
  it('deve exibir as 3 imagens do carrossel', () => {
    cy.get('.carousel-item img').should('have.length', 3)
    cy.get('.carousel-item img').eq(0).should('have.attr', 'alt', 'Bolos Caseiros')
    cy.get('.carousel-item img').eq(1).should('have.attr', 'alt', 'Bolo de Festa')
    cy.get('.carousel-item img').eq(2).should('have.attr', 'alt', 'Docinhos')
  })
  it('deve exibir os 3 indicadores do carrossel', () => {
    cy.get('.carousel-indicators button').should('have.length', 3)
    cy.get('.carousel-indicators button').eq(0).should('have.class', 'active')
  })
  it('deve navegar para o próximo slide', () => {
    cy.get('.carousel-item').eq(0).should('have.class', 'active')
    cy.get('.carousel-control-next').click()
    cy.wait(500)
    cy.get('.carousel-item').eq(1).should('have.class', 'active')
  })
  
})