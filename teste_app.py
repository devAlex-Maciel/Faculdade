import unittest
from app_postgresql import app, db, Usuario, Produto, Pedido, ItensPedido

class TestApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Configuração inicial para todos os testes."""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Banco de dados em memória para testes
        cls.client = app.test_client()
        with app.app_context():
            db.create_all()
            # Adicionar dados iniciais para testes
            produto = Produto(nome="Cupcake Teste", descricao="Teste", preco=10.00)
            db.session.add(produto)
            db.session.commit()
            cls.produto_id = produto.id  # Armazena o ID do produto para usar nos testes

    @classmethod
    def tearDownClass(cls):
        """Limpar após os testes."""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_home(self):
        """Testar a página inicial."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_cadastro_usuario(self):
        """Testar o cadastro de usuário."""
        with app.app_context():
            Usuario.query.delete()  # Limpa a tabela de usuários para evitar duplicação

        response = self.client.post('/cadastro', data={
            'nome': 'Teste Usuario',
            'email': 'teste@teste.com',
            'senha': '123456'
        })
        self.assertEqual(response.status_code, 302)  # Redireciona após cadastro
        with app.app_context():
            usuario = Usuario.query.filter_by(email='teste@teste.com').first()
            self.assertIsNotNone(usuario)

    def test_produtos(self):
        """Testar a rota de produtos."""
        response = self.client.get('/produtos')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Cupcake Teste', response.data)

    def test_adicionar_ao_carrinho(self):
        """Testar a adição de um produto ao carrinho."""
        response = self.client.get(f'/adicionar_ao_carrinho/{self.produto_id}')
        self.assertEqual(response.status_code, 302)  # Redireciona após adicionar
        with self.client.session_transaction() as session:
            self.assertIn('carrinho', session)
            self.assertEqual(len(session['carrinho']), 1)

    def test_finalizar_pedido(self):
        """Testar a finalização de pedido."""
        with self.client.session_transaction() as session:
            session['carrinho'] = [{'id': self.produto_id, 'nome': "Cupcake Teste", 'preco': 10.00, 'quantidade': 2}]

        response = self.client.post('/finalizar_pedido')
        self.assertEqual(response.status_code, 302)  # Redireciona após finalizar
        with app.app_context():
            pedido = Pedido.query.first()
            self.assertIsNotNone(pedido)
            self.assertEqual(pedido.total, 20.00)  # 2x R$ 10.00

    def test_pedidos(self):
        """Testar a rota de pedidos."""
        response = self.client.get('/pedidos')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Seus Pedidos', response.data)

if __name__ == '__main__':
    unittest.main()
