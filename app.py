from flask import Flask, render_template, request, redirect, url_for, jsonify
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
    descricao = db.Column(db.String(200), nullable=False)

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

@app.route('/admin')
def admin():
    produtos = Produto.query.all()
    return render_template('admin.html', produtos=produtos)

@app.route('/admin/produtos/novo', methods=['GET', 'POST'])
def novo_produto():
    if request.method == 'POST':
        nome = request.form['nome']
        categoria = request.form['categoria']
        preco = float(request.form['preco'])
        estoque = int(request.form['estoque'])
        imagem = "static/fotos/" + request.form['imagem']
        descricao = request.form['descricao']
        produto = Produto(nome=nome, categoria=categoria, preco=preco, estoque=estoque, imagem=imagem, descricao=descricao) 
        db.session.add(produto)
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('novo_produto.html')

@app.route('/admin/produtos/editar/<int:id>', methods=['GET', 'POST'])
def editar_produto(id):
    produto = Produto.query.get_or_404(id)
    if request.method == 'POST':
        produto.nome = request.form['nome']
        produto.categoria = request.form['categoria']
        produto.preco = float(request.form['preco'])
        produto.estoque = int(request.form['estoque'])        
        produto.descricao = request.form['descricao']
        if request.form['novaimagem'] != '':
            produto.imagem =  "static/fotos/" + request.form['novaimagem']
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('editar_produto.html', produto=produto)

@app.route('/admin/produtos/apagar/<int:id>', methods=['GET', 'POST'])
def apagar_produto(id):
    produto = Produto.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(produto)
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('apagar_produto.html', produto=produto)

@app.route('/produto/<int:id>')
def get_produto(id):
    produto = Produto.query.get_or_404(id)
    return jsonify({
        'nome': produto.nome,
        'descricao': produto.descricao,
        'preco': produto.preco,
        'imagem': produto.imagem
    })

if __name__ == '__main__':
    app.run(debug=True)