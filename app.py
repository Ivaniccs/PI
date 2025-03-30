from flask import Flask, render_template, request, redirect, url_for, jsonify, session , flash  
import mercadopago
import os
from dotenv import load_dotenv
from mercadopago import SDK
from flask_sqlalchemy import SQLAlchemy

sdk = SDK("TEST-12345678-1234-1234-1234-123456789012")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bolos_da_ana.db'
db = SQLAlchemy(app)
app.secret_key = 'dificil'  # Adicione antes de usar sessions/flash

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

@app.route('/Inicio', methods=['GET', 'POST'])
def Inicio():
    return render_template('Inicio.html')

@app.route('/Contato', methods=['GET', 'POST'])
def Contato():
    return render_template('Contato.html')



@app.route('/gerar-qrcode', methods=['POST'])
def gerar_qrcode():
    try:
        data = request.json
        total = float(data['total'])
        
        # Criar preferência no Mercado Pago
        preference_data = {
            "items": [
                {
                    "title": "Pagamento do Pedido",
                    "quantity": 1,
                    "unit_price": total,
                    "currency_id": "BRL"
                }
            ],
            "payment_methods": {
                "excluded_payment_types": [
                    {"id": "credit_card"},
                    {"id": "debit_card"}
                ],
                "default_payment_method_id": "pix",
                "installments": 1
            }
        }
        
        preference_response = sdk.preference().create(preference_data)
        qr_code = preference_response['response']['point_of_interaction']['transaction_data']['qr_code']
        
        return jsonify({
            'success': True,
            'qr_code': qr_code,
            'qr_code_base64': preference_response['response']['point_of_interaction']['transaction_data']['qr_code_base64']
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500





@app.route('/Cardapio', methods=['GET', 'POST'])
def Cardapio():
    produtos = Produto.query.all()
    return render_template('index.html', produtos=produtos)

@app.route('/carrinho', methods=['GET', 'POST'])
def carrinho():
    # Inicializa o carrinho na sessão se não existir
    if 'carrinho' not in session:
        session['carrinho'] = []
    
    if request.method == 'POST':
        produto_id = request.form.get('produto_id')
        produto = Produto.query.get(produto_id)
        
        if produto:
            # Verifica se há estoque disponível
            if produto.estoque > 0:
                # Verifica se o produto já está no carrinho
                item_existente = next((item for item in session['carrinho'] if item['id'] == produto.id), None)
                
                if item_existente:
                    # Aumenta a quantidade se o produto já estiver no carrinho
                    if item_existente['quantidade'] < produto.estoque:
                        item_existente['quantidade'] += 1
                else:
                    # Adiciona novo item ao carrinho
                    session['carrinho'].append({
                        'id': produto.id,
                        'nome': produto.nome,
                        'preco': float(produto.preco),
                        'quantidade': 1,
                        'imagem': produto.imagem,
                        'estoque_disponivel': produto.estoque
                    })
                
                # Confirma a adição ao carrinho
                flash(f'{produto.nome} adicionado ao carrinho!', 'success')
            else:
                flash('Este produto está esgotado!', 'error')
        else:
            flash('Produto não encontrado!', 'error')
        
        session.modified = True  # Garante que a sessão será salva
        return redirect(url_for('carrinho'))
    
    # Lógica para GET (exibir o carrinho)
    carrinho_itens = []
    total = 0.0
    
    for item in session.get('carrinho', []):
        produto = Produto.query.get(item['id'])
        if produto:
            subtotal = item['preco'] * item['quantidade']
            total += subtotal
            
            carrinho_itens.append({
                'id': item['id'],
                'nome': item['nome'],
                'preco': item['preco'],
                'quantidade': item['quantidade'],
                'subtotal': subtotal,
                'imagem': item['imagem'],
                'estoque_disponivel': produto.estoque  # Atualiza com o estoque atual
            })
    
    return render_template('carrinho.html', 
                         carrinho_itens=carrinho_itens,                          
                         total=total)

@app.route('/remover-do-carrinho/<int:produto_id>')
def remover_do_carrinho(produto_id):
    if 'carrinho' in session:
        session['carrinho'] = [item for item in session['carrinho'] if item['id'] != produto_id]
        session.modified = True
        flash('Produto removido do carrinho!', 'info')
    return redirect(url_for('carrinho'))

@app.route('/atualizar-carrinho', methods=['POST'])
def atualizar_carrinho():
    try:
        # Verificação básica dos parâmetros
        produto_id = request.form.get('produto_id')
        nova_quantidade = request.form.get('quantidade')
        
        if not produto_id or not nova_quantidade:
            flash('Parâmetros inválidos para atualização', 'error')
            return redirect(url_for('carrinho'))

        # Conversão segura para inteiro
        try:
            nova_quantidade = int(nova_quantidade)
            if nova_quantidade <= 0:
                raise ValueError
        except ValueError:
            flash('Quantidade deve ser um número positivo', 'error')
            return redirect(url_for('carrinho'))

        # Verifica se o carrinho existe na sessão
        if 'carrinho' not in session or not session['carrinho']:
            flash('Carrinho não encontrado', 'error')
            return redirect(url_for('carrinho'))

        # Busca o produto no banco de dados
        produto = Produto.query.get(produto_id)
        if not produto:
            flash('Produto não encontrado', 'error')
            return redirect(url_for('carrinho'))

        # Atualiza a quantidade no carrinho
        carrinho_atualizado = False
        for item in session['carrinho']:
            if str(item['id']) == str(produto_id):  # Comparação segura como strings
                if nova_quantidade <= produto.estoque:
                    item['quantidade'] = nova_quantidade
                    flash(f'Quantidade de {produto.nome} atualizada para {nova_quantidade}', 'success')
                    carrinho_atualizado = True
                else:
                    flash(f'Estoque insuficiente. Máximo disponível: {produto.estoque}', 'error')
                break

        if not carrinho_atualizado:
            flash('Produto não encontrado no carrinho', 'error')

        # Força a atualização da sessão
        session.modified = True
        return redirect(url_for('carrinho'))

    except Exception as e:
        flash(f'Erro ao atualizar carrinho: {str(e)}', 'error')
        return redirect(url_for('carrinho'))

@app.route('/finalizar_compra', methods=['POST'])
def finalizar_compra():
    total = total
    return render_template('index.html', total=total)

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