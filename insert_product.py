from app import app, db, Produto

with app.app_context():
    db.create_all() # Garante que as tabelas sejam criadas
    produto1 = Produto(nome='Bolo de Cenoura', categoria='Bolos', preco=30.00, estoque=15, imagem='static/bolo_tradicional.png')
    produto2 = Produto(nome='Beijinho', categoria='Doces', preco=4.50, estoque=60, imagem='static/brownie.png')
    produto3 = Produto(nome='Torta de Limão', categoria='Tortas', preco=40.00, estoque=8, imagem='static/cupcake.png'
    '')
    db.session.add_all([produto1, produto2, produto3])
    db.session.commit()

print('Dados inseridos com sucesso!')