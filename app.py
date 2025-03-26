from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bolos_da_ana.db'
db = SQLAlchemy(app)

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    estoque = db.Column(db.Integer, nullable=False)
    imagem = db.Column(db.String(200))

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    produtos = Produto.query.all()
    return render_template('index.html', produtos=produtos)

@app.route('/carrinho', methods=['GET', 'POST'])
def carrinho():
    if request.method == 'POST':
        produto_id = request.form['produto_id']
        produto = Produto.query.get(produto_id)
        # inserir lógica para adicionar o produto ao carrinho
    # inserir Lógica para exibir os produtos no carrinho e o valor total
    return render_template('carrinho.html')

@app.route('/Contato', methods=['GET', 'POST'])
def Contato():
    return render_template('Contato.html')

@app.route('/Cardapio', methods=['GET', 'POST'])
def Cardapio():
    produtos = Produto.query.all()
    return render_template('index.html', produtos=produtos)

if __name__ == '__main__':
    app.run(debug=True)