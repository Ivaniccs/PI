describe('Admin - Testes da página administrativa', () => {
  beforeEach(() => {
    cy.visit('/login')
    cy.get('input[name="username"]').type('PI2')
    cy.get('input[name="password"]').type('123456')
    cy.get('input[type="submit"]').click()
    cy.url().should('include', '/admin')
  })

  it('Deve exibir a página de admin com a lista de produtos', () => {
    cy.contains('Adicionar Novo Produto').should('be.visible')
    cy.get('.produtos').should('be.visible')
    cy.get('.produto').should('have.length.greaterThan', 0)
  })

  it('Deve exibir o botão para adicionar novo produto', () => {
    cy.contains('Adicionar Novo Produto').should('be.visible')
    cy.contains('Adicionar Novo Produto').should('have.attr', 'href', '/novo_produto')
  })

  it('Deve exibir botões de Editar e Apagar em cada produto', () => {
    cy.get('.produto').first().within(() => {
      cy.get('a').should('contain', 'Editar')
      cy.get('a').should('contain', 'Apagar')
    })
  })

  it('Deve redirecionar para página de novo produto ao clicar no botão', () => {
    cy.contains('Adicionar Novo Produto').click()
    cy.url().should('include', '/novo_produto')
    cy.get('h1').should('contain', 'Novo Produto')
  })

  it('Deve criar um novo produto com todos os campos preenchidos', () => {
    cy.contains('Adicionar Novo Produto').click()
    cy.get('#nome').type('Bolo de Teste')
    cy.get('#categoria').type('Bolos Especiais')
    cy.get('#descricao').type('Um bolo delicioso para teste')
    cy.get('#preco').type('50.00')
    cy.get('#estoque').type('10')
    cy.get('input[type="submit"]').click()
    cy.url().should('include', '/admin')
  })

  it('Deve editar um produto existente', () => {
    cy.get('.produto').first().find('a').first().click()
    cy.url().should('include', '/editar_produto')
    cy.get('h1').should('contain', 'Editar Produto')
    
    cy.get('#nome').clear().type('Bolo Editado')
    cy.get('#categoria').clear().type('Categoria Editada')
    cy.get('#descricao').clear().type('Descrição Editada')
    cy.get('#preco').clear().type('75.00')
    cy.get('#estoque').clear().type('20')
    cy.get('input[type="submit"]').click()
    cy.url().should('include', '/admin')
  })

  it('Deve validar que os campos são obrigatórios ao editar', () => {
    cy.get('.produto').first().find('a').first().click()
    cy.get('#nome').clear()
    cy.get('input[type="submit"]').click()
  })

  it.skip('Deve apagar um produto', () => {
    cy.get('.produto').first().find('a').eq(1).click()
    cy.url().should('include', '/apagar_produto')
    cy.get('h1').should('contain', 'Apagar Produto')
    cy.get('input[type="submit"]').click()
    cy.url().should('include', '/admin')
  })

  it('Deve fazer logout da página admin', () => {
    cy.get('a').contains('Logout').click()
    cy.url().should('include', '/')
  })

  it('Deve criar uma nova conta de admin', () => {
    cy.visit('/register')
    cy.get('h1').should('contain', 'Criar Nova Conta')
    
    cy.get('input[name="username"]').type('NovoAdmin2')
    cy.get('input[name="password"]').type('SenhaForte123')
    cy.get('input[name="password2"]').type('SenhaForte123')
    cy.get('input[type="submit"]').click()
    cy.get('a').contains('Logout').click()
  })

});
