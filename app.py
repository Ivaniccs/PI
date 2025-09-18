# app.py - VERSÃO FINAL CORRIGIDA

import os
from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from dotenv import load_dotenv
import mercadopago

load_dotenv()

# Verificação de segurança para o token
mp_token = os.getenv('MP_ACCESS_TOKEN')
if not mp_token:
    raise RuntimeError("A variável MP_ACCESS_TOKEN não foi encontrada. Verifique seu arquivo .env.")

# inicializa o SDK existente
sdk = mercadopago.SDK(mp_token)

# --- 1. INICIALIZAÇÃO DAS EXTENSÕES ---
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message = "Por favor, faça login para acessar esta página."
login_manager.login_message_category = "info"


# --- 2. MODELOS DO BANCO DE DADOS ---
class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    estoque = db.Column(db.Integer, nullable=False)
    imagem = db.Column(db.String(200))
    descricao = db.Column(db.String(200), nullable=False)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# --- 3. FORMULÁRIOS ---
class RegistrationForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    password2 = PasswordField(
        'Repita a Senha', validators=[DataRequired(), EqualTo('password', message='As senhas devem ser iguais.')])
    submit = SubmitField('Registrar')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Este nome de usuário já está em uso.')

class LoginForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Login')


# --- 4. FÁBRICA DE APLICAÇÃO ---
def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', '102030')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'bolos_da_ana.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    login_manager.init_app(app)

    # --- 5. ROTAS DA APLICAÇÃO ---
    
    # ROTAS PÚBLICAS E DE AUTENTICAÇÃO
    @app.route('/')
    def index():
        produtos = Produto.query.all()
        return render_template('index.html', produtos=produtos)
    
    @app.route('/Inicio')
    def Inicio():
        return render_template('Inicio.html')
    
    @app.route('/contato')
    def Contato():
        return render_template('Contato.html')
    
    @app.route('/Cardapio')
    def Cardapio():
        produtos = Produto.query.all()
        return render_template('index.html', produtos=produtos)
        
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('admin'))
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user is None or not user.check_password(form.password.data):
                flash('Usuário ou senha inválidos.', 'danger')
                return redirect(url_for('login'))
            login_user(user)
            return redirect(url_for('admin'))
        return render_template('login.html', form=form)

    @app.route('/logout')
    def logout():
        logout_user()
        flash('Você foi desconectado.', 'success')
        return redirect(url_for('index'))

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        # Em uma aplicação real, você pode querer desabilitar o registro aberto
        #if current_user.is_authenticated:
        #    return redirect(url_for('admin'))
        form = RegistrationForm()
        if form.validate_on_submit():
            user = User(username=form.username.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Parabéns, sua conta foi criada! Faça o login.', 'success')
            return redirect(url_for('login'))
        return render_template('register.html', form=form)

    # ROTAS DO CARRINHO
    @app.route('/carrinho', methods=['GET', 'POST'])
    def carrinho():
        if 'carrinho' not in session:
            session['carrinho'] = []
        
        if request.method == 'POST':
            produto_id = request.form.get('produto_id')
            produto = Produto.query.get(produto_id)
            if produto:
                if produto.estoque > 0:
                    item_existente = next((item for item in session['carrinho'] if item['id'] == produto.id), None)
                    if item_existente:
                        if item_existente['quantidade'] < produto.estoque:
                            item_existente['quantidade'] += 1
                    else:
                        session['carrinho'].append({'id': produto.id, 'nome': produto.nome, 'preco': float(produto.preco), 'quantidade': 1, 'imagem': produto.imagem})
                    flash(f'{produto.nome} adicionado ao carrinho!', 'success')
                else:
                    flash('Este produto está esgotado!', 'danger')
            session.modified = True
            return redirect(url_for('carrinho'))
        
        # Lógica GET para exibir o carrinho
        carrinho_itens = session.get('carrinho', [])
        total = sum(item['preco'] * item['quantidade'] for item in carrinho_itens)
        return render_template('carrinho.html', carrinho_itens=carrinho_itens, total=total)

    # Adicione esta rota DENTRO da função create_app(), junto com as outras

    @app.route('/produto/<int:id>')
    def get_produto(id):
        produto = Produto.query.get_or_404(id)
        # Usamos url_for para gerar o caminho correto para a imagem
        imagem_url = url_for('static', filename=produto.imagem.replace('static/', '')) if produto.imagem else ''

        return jsonify({
            'nome': produto.nome,
            'descricao': produto.descricao,
            'preco': produto.preco,
            'imagem': imagem_url
        })

    @app.route('/remover-do-carrinho/<int:produto_id>')
    def remover_do_carrinho(produto_id):
        if 'carrinho' in session:
            session['carrinho'] = [item for item in session['carrinho'] if item['id'] != produto_id]
            session.modified = True
            flash('Produto removido do carrinho!', 'info')
        return redirect(url_for('carrinho'))

    @app.route('/atualizar-carrinho', methods=['POST'])
    def atualizar_carrinho():
        produto_id = int(request.form.get('produto_id'))
        nova_quantidade = int(request.form.get('quantidade'))
        produto = Produto.query.get(produto_id)
        if produto and nova_quantidade > 0:
            if nova_quantidade <= produto.estoque:
                for item in session['carrinho']:
                    if item['id'] == produto_id:
                        item['quantidade'] = nova_quantidade
                        break
                session.modified = True
            else:
                flash(f'Estoque insuficiente. Apenas {produto.estoque} disponíveis.', 'warning')
        return redirect(url_for('carrinho'))
    
    # Em app.py, dentro de create_app()

    @app.route('/gerar_qrcode_pix', methods=['POST'])
    def gerar_qrcode_pix():
        # Validação de segurança: o total é calculado no back-end, não confiando no front-end.
        if 'carrinho' not in session or not session['carrinho']:
            return jsonify({'success': False, 'error': 'Seu carrinho está vazio.'}), 400

        total = sum(item['preco'] * item['quantidade'] for item in session['carrinho'])
        total = round(total, 2)

        if total <= 0:
            return jsonify({'success': False, 'error': 'O valor total do carrinho deve ser positivo.'}), 400

        # Pega dados enviados pelo JavaScript
        request_data = request.get_json()
        nome_cliente = request_data.get('nome', 'Cliente Anônimo')

        # Cria o payload para o Mercado Pago
        payment_data = {
            "transaction_amount": total,
            "description": "Pagamento de pedido - Bolos da Ana",
            "payment_method_id": "pix",
            "payer": {
                "email": "cliente@example.com", # Você pode adicionar um campo de e-mail no modal se quiser
                "first_name": nome_cliente
            }
        }

        try:
            # A chamada REAL para a API do Mercado Pago
            payment_response = sdk.payment().create(payment_data)
            payment = payment_response.get("response")

            if not payment or 'point_of_interaction' not in payment:
                app.logger.error(f"Resposta inválida do MP: {payment}")
                return jsonify({'success': False, 'error': 'Resposta inválida do gateway de pagamento.'}), 500

            # Retorna os dados necessários para o front-end
            return jsonify({
                'success': True,
                'qr_code_base64': payment['point_of_interaction']['transaction_data']['qr_code_base64'],
                'qr_code_text': payment['point_of_interaction']['transaction_data']['qr_code']
            })

        except Exception as e:
            app.logger.error(f"Erro ao criar pagamento PIX: {e}")
            return jsonify({'success': False, 'error': f'Erro de comunicação com o serviço de pagamento. Detalhe: {str(e)}'}), 500

   
    # ROTAS DE ADMINISTRAÇÃO (PROTEGIDAS)
    @app.route('/admin')
    @login_required
    def admin():
        produtos = Produto.query.all()
        return render_template('admin.html', produtos=produtos)

    @app.route('/novo_produto', methods=['GET', 'POST'])
    @login_required
    def novo_produto():
        if request.method == 'POST':
            produto = Produto(
                nome=request.form['nome'],
                categoria=request.form['categoria'],
                preco=float(request.form['preco']),
                estoque=int(request.form['estoque']),
                imagem="static/fotos/" + request.form['imagem'],
                descricao=request.form['descricao']
            )
            db.session.add(produto)
            db.session.commit()
            return redirect(url_for('admin'))
        return render_template('novo_produto.html')

    @app.route('/editar_produto_<int:id>', methods=['GET', 'POST'])
    @login_required 
    def editar_produto(id):
        produto = Produto.query.get_or_404(id)
        if request.method == 'POST':
            produto.nome = request.form['nome']
            produto.categoria = request.form['categoria']
            produto.preco = float(request.form['preco'])
            produto.estoque = int(request.form['estoque'])
            produto.descricao = request.form['descricao']
            if request.form.get('novaimagem'):
                produto.imagem = "static/fotos/" + request.form['novaimagem']
            db.session.commit()
            return redirect(url_for('admin'))
        # CORREÇÃO: A variável 'produto' precisa ser passada para o template
        return render_template('editar_produto.html', produto=produto)

    @app.route('/apagar_produto_<int:id>', methods=['GET', 'POST'])
    @login_required
    def apagar_produto(id):
        produto = Produto.query.get_or_404(id)
        if request.method == 'POST':
            db.session.delete(produto)
            db.session.commit()
            return redirect(url_for('admin'))
        # CORREÇÃO: A variável 'produto' precisa ser passada para o template
        return render_template('apagar_produto.html', produto=produto)

    return app

# --- 6. EXECUÇÃO ---
app = create_app()

@app.cli.command('init-db')
def init_db_command():
    """Cria as tabelas do banco de dados."""
    with app.app_context():
        db.create_all()
    print('Banco de dados inicializado.')

if __name__ == '__main__':
    app.run(debug=True)