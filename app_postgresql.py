from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

# Configuração do aplicativo Flask
app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Necessário para sessões

# Configuração do banco de dados PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:592887@localhost:5432/meu_banco_de_dados'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelos do banco de dados
class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(80), nullable=False)

class Produto(db.Model):
    __tablename__ = 'produtos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    descricao = db.Column(db.String(255), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    imagem = db.Column(db.String(255), nullable=True)

class Pedido(db.Model):
    __tablename__ = 'pedidos'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    total = db.Column(db.Float, nullable=False)
    data_pedido = db.Column(db.DateTime, default=db.func.current_timestamp())

class ItensPedido(db.Model):
    __tablename__ = 'itens_pedido'
    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedidos.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    preco_unitario = db.Column(db.Float, nullable=False)

# Rotas do aplicativo
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        dados = request.form
        novo_usuario = Usuario(nome=dados['nome'], email=dados['email'], senha=dados['senha'])
        db.session.add(novo_usuario)
        db.session.commit()
        return redirect(url_for('produtos'))  # Redireciona para produtos após cadastro
    return render_template('cadastro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        dados = request.form
        usuario = Usuario.query.filter_by(email=dados['email'], senha=dados['senha']).first()
        if usuario:
            return redirect(url_for('produtos'))  # Redireciona para produtos após login
        return render_template('login.html', erro="Credenciais inválidas")
    return render_template('login.html')

@app.route('/produtos', methods=['GET'])
def produtos():
    produtos = Produto.query.all()
    carrinho = session.get('carrinho', [])
    return render_template('produtos.html', produtos=produtos, carrinho=carrinho)

@app.route('/adicionar_ao_carrinho/<int:produto_id>')
def adicionar_ao_carrinho(produto_id):
    produto = Produto.query.get(produto_id)
    if not produto:
        return redirect(url_for('produtos'))
    carrinho = session.get('carrinho', [])
    for item in carrinho:
        if item['id'] == produto.id:
            item['quantidade'] += 1
            break
    else:
        carrinho.append({'id': produto.id, 'nome': produto.nome, 'preco': produto.preco, 'quantidade': 1})
    session['carrinho'] = carrinho
    return redirect(url_for('produtos'))  # Permanece na página de produtos

@app.route('/carrinho')
def carrinho():
    carrinho = session.get('carrinho', [])
    total = sum(item['preco'] * item['quantidade'] for item in carrinho)
    return render_template('carrinho.html', carrinho=carrinho, total=total)

@app.route('/remover_do_carrinho/<int:produto_id>')
def remover_do_carrinho(produto_id):
    carrinho = session.get('carrinho', [])
    carrinho = [item for item in carrinho if item['id'] != produto_id]
    session['carrinho'] = carrinho
    return redirect(url_for('carrinho'))

@app.route('/finalizar_pedido', methods=['POST'])
def finalizar_pedido():
    carrinho = session.get('carrinho', [])
    if not carrinho:
        return redirect(url_for('carrinho'))

    # Criar um novo pedido
    total = sum(item['preco'] * item['quantidade'] for item in carrinho)
    novo_pedido = Pedido(usuario_id=1, total=total)  # Ajuste o usuario_id conforme necessário
    db.session.add(novo_pedido)
    db.session.commit()

    # Adicionar itens ao pedido
    for item in carrinho:
        item_pedido = ItensPedido(
            pedido_id=novo_pedido.id,
            produto_id=item['id'],
            quantidade=item['quantidade'],
            preco_unitario=item['preco']
        )
        db.session.add(item_pedido)

    db.session.commit()

    # Limpar o carrinho após finalizar o pedido
    session['carrinho'] = []

    return redirect(url_for('pedidos'))  # Redireciona para a página de pedidos

@app.route('/pedidos')
def pedidos():
    pedidos = Pedido.query.all()
    return render_template('pedidos.html', pedidos=pedidos)

# Inicialização do banco de dados e execução do servidor
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Cria as tabelas no banco de dados, se não existirem

        # Adiciona produtos padrão, se não houver produtos
        if Produto.query.count() == 0:
            produtos_iniciais = [
                Produto(nome="Cupcake de Chocolate", descricao="Delicioso cupcake de chocolate", preco=5.00, imagem="chocolate.jpg"),
                Produto(nome="Cupcake de Morango", descricao="Cupcake com cobertura de morango", preco=6.00, imagem="morango.jpg"),
                Produto(nome="Cupcake de Baunilha", descricao="Cupcake clássico de baunilha", preco=4.50, imagem="baunilha.jpg")
            ]
            db.session.bulk_save_objects(produtos_iniciais)
            db.session.commit()
            print("Produtos iniciais adicionados ao banco de dados!")

    app.run(debug=True)
