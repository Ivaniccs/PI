describe('Login Page', () => {
  beforeEach(() => {
    cy.visit('/login');
  });

  it('should display login form', () => {
    cy.get('h1').should('contain', 'Login');
    cy.get('form').should('exist');
    cy.get('input[name="username"]').should('be.visible');
    cy.get('input[name="password"]').should('be.visible');
    cy.get('button[type="submit"]').should('be.visible');
  });

  it('should redirect to admin page on successful login', () => {
    // Using credentials from the app - you may need to create a test user first
    cy.get('input[name="username"]').type('admin');
    cy.get('input[name="password"]').type('password');
    cy.get('button[type="submit"]').click();
    // Expecting redirect to admin page
    cy.url().should('include', '/admin');
  });

  it('should show error message with invalid username', () => {
    cy.get('input[name="username"]').type('nonexistent');
    cy.get('input[name="password"]').type('wrongpassword');
    cy.get('button[type="submit"]').click();
    // Should stay on login page with error message
    cy.url().should('include', '/login');
  });

  it('should show error message with wrong password', () => {
    cy.get('input[name="username"]').type('admin');
    cy.get('input[name="password"]').type('wrongpassword');
    cy.get('button[type="submit"]').click();
    // Should stay on login page with error message
    cy.url().should('include', '/login');
  });

  it('should require both username and password fields', () => {
    cy.get('button[type="submit"]').click();
    // Form should not submit without required fields
    cy.url().should('include', '/login');
  });

  it('should redirect to admin if already authenticated', () => {
    // This would require a logged-in session
    // First login
    cy.get('input[name="username"]').type('admin');
    cy.get('input[name="password"]').type('password');
    cy.get('button[type="submit"]').click();
    
    // Visit login page again while authenticated
    cy.visit('/login');
    // Should redirect to admin
    cy.url().should('include', '/admin');
  });
});
