Projeto Integrador de Engenharia de Software II

Este é o repositório do Projeto Integrador de Engenharia de Software II, que consiste no desenvolvimento de um sistema para gestão de pedidos de cupcakes. O sistema inclui funcionalidades como cadastro de usuários, login, gerenciamento de produtos, carrinho de compras e finalização de pedidos.

Funcionalidades Principais
Cadastro e Login de usuários.
Exibição de uma vitrine de cupcakes.
Carrinho de compras com adição e remoção de produtos.
Finalização de pedidos.
Visualização de pedidos finalizados.
Tecnologias Utilizadas
Backend: Flask (Python)
Frontend: HTML, CSS
Banco de Dados: PostgreSQL
Testes Automatizados: unittest
Como Rodar o Projeto
Pré-requisitos
Python 3.10+ instalado.
PostgreSQL configurado e rodando localmente.
Virtualenv (opcional, mas recomendado).
Passos
Clone este repositório.
Instale as dependências com o comando pip install -r requirements.txt.

Configure o banco de dados no arquivo app_postgresql.py:
Atualize as credenciais do banco:
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://<usuario>:<senha>@localhost:5432/<nome_do_banco>'
Inicialize o banco de dados rodando o script principal.
Rode o servidor e acesse o sistema em http://127.0.0.1:5000/.
Estrutura do Projeto
app_postgresql.py: Código principal do sistema.
templates/: Arquivos HTML para as páginas do sistema.
static/: Arquivos CSS e outros assets estáticos.
test_app.py: Arquivo com testes automatizados.
Testes Automatizados
Os testes podem ser executados para validar as funcionalidades principais, como:

Cadastro de usuários.
Login.
Adição de produtos ao carrinho.
Finalização de pedidos.
Para executar os testes:
Use o comando python -m unittest test_app.py.

Feedback dos Usuários
Usuário 1: Sugestão para adicionar barra de progresso ao finalizar pedido.
Usuário 2: Destacar o botão "Finalizar Pedido".
Usuário 3: Permitir alteração de quantidade diretamente no carrinho.
Usuário 4: Adicionar modo escuro (dark mode).
Usuário 5: Melhorar a mensagem de sucesso ao finalizar pedido.
Conclusão
O sistema foi desenvolvido com sucesso, atendendo aos requisitos do projeto. Feedbacks foram coletados para futuras melhorias.
