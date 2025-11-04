describe('Login Page', () => {
  beforeEach(() => {
    cy.visit('/login');
  });

  it('Verificar se o formulário de login é exibido corretamente', () => {
    cy.get('h1').should('contain', 'Login');
    cy.get('form').should('exist');
    cy.get('input[name="username"]').should('be.visible');
    cy.get('input[name="password"]').should('be.visible');
    cy.get('input[type="submit"]').should('be.visible');
  });

  it('Fazer login com credenciais válidas', () => {
    cy.get('input[name="username"]').type('PI2');
    cy.get('input[name="password"]').type('123456');
    cy.get('input[type="submit"]').click();
    cy.url().should('include', '/admin');
  });

  it('Mostrar erro com usuário inválido', () => {
    cy.get('input[name="username"]').type('nonexistent');
    cy.get('input[name="password"]').type('wrongpassword');
    cy.get('input[type="submit"]').click();
    cy.url().should('include', '/login');
  });

  it('Mostrar erro com senha incorreta', () => {
    cy.get('input[name="username"]').type('admin');
    cy.get('input[name="password"]').type('wrongpassword');
    cy.get('input[type="submit"]').click();
    cy.url().should('include', '/login');
  });

  it('Validar campos obrigatórios', () => {
    cy.get('input[type="submit"]').click();
    cy.url().should('include', '/login');
  });

  it('Mostrar mensagem de erro ao deixar campos vazios', () => {
    cy.get('input[type="submit"]').click();
    cy.contains('[This field is required.]').should('be.visible');
  });

  it('Redirecionar para admin se já autenticado', () => {
    cy.get('input[name="username"]').type('PI2');
    cy.get('input[name="password"]').type('123456');
    cy.get('input[type="submit"]').click();
    
    cy.visit('/login');
    cy.url().should('include', '/admin');
  });
});
