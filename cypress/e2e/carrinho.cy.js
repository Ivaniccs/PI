describe('Carrinho - Testes da página de carrinho', () => {
  beforeEach(() => {
    cy.visit('/carrinho')
  })

  it('Deve exibir mensagem quando o carrinho está vazio', () => {
    cy.get('h2').should('contain', 'Seu Carrinho')
    cy.contains('Seu carrinho está vazio').should('be.visible')
  })

  it('Deve exibir a tabela com as colunas corretas quando há itens', () => {
    cy.visit('/Cardapio')
    cy.get('.produto').first().find('form').submit()
    cy.visit('/carrinho')
    
    cy.get('table').should('exist')
    cy.get('thead th').should('contain', 'Produto')
    cy.get('thead th').should('contain', 'Preço')
    cy.get('thead th').should('contain', 'Quantidade')
    cy.get('thead th').should('contain', 'Subtotal')
    cy.get('thead th').should('contain', 'Ações')
  })

  it('Deve exibir informações do produto no carrinho', () => {
    cy.visit('/Cardapio')
    cy.get('.produto').first().find('form').submit()
    cy.visit('/carrinho')
    
    cy.get('tbody tr').first().within(() => {
      cy.get('img').should('be.visible')
      cy.get('td').eq(0).should('not.be.empty')
      cy.get('td').eq(1).should('contain', 'R$')
    })
  })

  it('Deve exibir o botão de Atualizar quantidade', () => {
    cy.visit('/Cardapio')
    cy.get('.produto').first().find('form').submit()
    cy.visit('/carrinho')
    
    cy.get('input[name="quantidade"]').should('be.visible')
    cy.get('button[type="submit"]').should('contain', 'Atualizar')
  })

  it('Deve remover um produto do carrinho', () => {
    cy.visit('/Cardapio')
    cy.get('.produto').first().find('form').submit()
    cy.visit('/carrinho')
    
    cy.get('tbody tr').should('have.length', 1)
    cy.get('.btn-danger').click()
    cy.contains('Seu carrinho está vazio').should('be.visible')
  })

  it('Deve exibir o total do carrinho', () => {
    cy.visit('/Cardapio')
    cy.get('.produto').first().find('form').submit()
    cy.visit('/carrinho')
    
    cy.get('.total h4').should('contain', 'Total:')
    cy.get('.total h4').should('contain', 'R$')
  })

  it('Deve exibir o botão Finalizar Compra', () => {
    cy.visit('/Cardapio')
    cy.get('.produto').first().find('form').submit()
    cy.visit('/carrinho')
    
    cy.get('#finalizarCompra').should('contain', 'Finalizar Compra')
    cy.get('#finalizarCompra').should('be.visible')
  })

  it('Deve abrir o modal ao clicar em Finalizar Compra', () => {
    cy.visit('/Cardapio')
    cy.get('.produto').first().find('form').submit()
    cy.visit('/carrinho')
    
    cy.get('#finalizarCompra').click()
    cy.get('#modalFinalizar').should('have.css', 'display', 'block')
    cy.get('.modal-content').should('be.visible')
  })

  it('Deve fechar o modal ao clicar no botão X', () => {
    cy.visit('/Cardapio')
    cy.get('.produto').first().find('form').submit()
    cy.visit('/carrinho')
    
    cy.get('#finalizarCompra').click()
    cy.get('#modalFinalizar').should('have.css', 'display', 'block')
    cy.get('.close').click()
    cy.get('#modalFinalizar').should('have.css', 'display', 'none')
  })

  it('Deve exibir os campos do formulário no modal', () => {
    cy.visit('/Cardapio')
    cy.get('.produto').first().find('form').submit()
    cy.visit('/carrinho')
    
    cy.get('#finalizarCompra').click()
    cy.get('#nomeCliente').should('be.visible')
    cy.get('#nomeAluno').should('be.visible')
    cy.get('#observacoes').should('be.visible')
    cy.get('#gerar-qrcode').should('contain', 'Pagamento')
  })

  it('Deve mostrar alerta se tentar gerar QR Code sem preencher o nome', () => {
    cy.visit('/Cardapio')
    cy.get('.produto').first().find('form').submit()
    cy.visit('/carrinho')
    
    cy.get('#finalizarCompra').click()
    cy.on('window:alert', (text) => {
      expect(text).to.contain('Por favor, preencha seu nome')
    })
    cy.get('#gerar-qrcode').click()
  })

  it('Deve preencher todos os campos e gerar o QR Code', () => {
    cy.visit('/Cardapio')
    cy.get('.produto').first().find('form').submit()
    cy.visit('/carrinho')
    
    cy.get('#finalizarCompra').click()
    cy.get('#nomeCliente').type('Teste')
    cy.get('#nomeAluno').type('Aluno Teste')
    cy.get('#observacoes').type('Observações de teste')
    
    cy.get('#gerar-qrcode').click()
    cy.get('#qrcode-container').should('have.css', 'display', 'block')
    cy.get('#qrcode-img').should('be.visible')
    cy.get('#whatsappBtn').should('be.visible')
    cy.get('#whatsappBtn').click()
  })

});
