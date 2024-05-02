import mysql.connector
from flask import Flask, flash,render_template, request, session, redirect, url_for
from datetime import datetime


#=============================================#

app = Flask(__name__)
app.secret_key = '12345'


##############################################################################################################
############################################## ROTAS DO CLIENTE ##############################################
##############################################################################################################

@app.route("/")
def home():
    session["produtos"] = []
    return render_template("index.html")


@app.route("/index.html")
def home_():
    return(render_template("index.html"))

@app.route('/login_and_register.html', methods=['GET'])
def login_screen():
    email = request.args.get("email")
    senha = request.args.get("senha")
    conexao = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = 'niojo123',
        database = 'livraria_bd',
    )
    cursor = conexao.cursor(prepared=True)

    sql_vendedor = f'SELECT email,senha,id FROM cliente WHERE email = %s AND senha = %s'
    valores = (email, senha)
    cursor.execute(sql_vendedor, valores)
    resultado_vendedor = cursor.fetchall() # Ler o banco de dados
    
    if(resultado_vendedor):
        id_cliente = resultado_vendedor[0][2] 
        session['id_cliente'] = id_cliente  # Armazena o ID do cliente na sessão 'id_cliente'
        conexao.close()
        return render_template("homepage_cliente.html")
    else:
        conexao.close()
        return render_template("login_and_register.html")  
    
    
    
    return render_template("login_and_register.html")

@app.route('/login_and_register.html', methods=['POST'])
def login_usuario():
    nome = request.form['nome_cliente']
    senha = request.form['senha_cliente'] 

    conexao = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = 'niojo123',
        database = 'livraria_bd',
    )
    
    cursor = conexao.cursor(prepared=True)

    sql_vendedor = f'SELECT * FROM vendedor WHERE nome = %s AND cpf = %s'
    valores = (nome, senha)
    cursor.execute(sql_vendedor, valores)
    resultado_vendedor = cursor.fetchall() # Ler o banco de dados
    
    session["produtos"] = []
    session["valor_total"] = 0.0
    if(nome == 'admin' and senha == 'admin'): # Se for o admin logando, mande ele para o painel de admin
        return render_template("homepage_admin.html")
    
    if resultado_vendedor:
        # Login bem sucedido
        conexao.close()
        return render_template("homepage_vendedor.html")
    else:
        sql_cliente = f'SELECT * FROM cliente WHERE nome = %s AND cpf = %s'
        valores = (nome, senha)
        cursor.execute(sql_cliente, valores)
        resultado_cliente = cursor.fetchall() # Ler o banco de dados
        
        if resultado_cliente:
        # Login bem sucedido
            id_cliente = resultado_cliente[0][0] 
            session['id_cliente'] = id_cliente  # Armazena o ID do cliente na sessão 'id_cliente'
            conexao.close()
            return render_template("homepage_cliente.html")
        else:
        # Login mal sucedido
            conexao.close()
            return render_template("tela_login.html")   
    
# id_cliente = session.get('id_cliente') # Comando pra pegar o ID do cliente logado
#==============================================================================#

@app.route("/homepage_cliente.html")
def home_cliente():
    return render_template("homepage_cliente.html")

#==============================================================================#
@app.route("/Cadastre-se.html") #CREATE
def pagina_cadastrarCliente():
    return render_template("Cadastre-se.html")

#envio feito pelo cliente, na pagina de login
@app.route('/submit_cliente', methods=['POST'])
def submit_cliente():
    name = request.form['nome_cliente']
    cpf = request.form['cpf_cliente']
    telefone = request.form['telefone_cliente']
    email = request.form['email_cliente']
    cidade = request.form['cidade_cliente'].lower()

    if cidade == 'sousa':
        desconto = True
    else:
        desconto = False

    conexao = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = 'niojo123',
        database = 'livraria_bd',
    )

    cursor = conexao.cursor(prepared=True)
    sql = f'INSERT INTO cliente (nome, cpf, telefone, email, is_desconto) VALUES (%s, %s, %s, %s, %s)'
    valores = (name, cpf, telefone, email, desconto)
    cursor.execute(sql, valores)
    conexao.commit()
    conexao.close()

    return login_screen()
#==============================================================================#

@app.route("/Alterar_dados_cliente.html") #UPDATE
def pagina_alterar_dados_cliente():
    return render_template("Pages_cliente/Alterar_dados_cliente.html")

@app.route("/alterar_dados_cliente", methods=['POST']) #UPDATE
def alterar_dados_cliente():
    id_usuario = session.get('id_cliente') # Comando pra pegar o ID do cliente logado
    
    nome_atlz = request.form['nome_atlzd']
    cpf_atlz = request.form['cpf_atlzd']
    email_atlz = request.form['email_atlzd']
    telefone_atlz = request.form['telefone_atlzd']
    cidade_atlz = request.form['cidade_atlz'].lower()

    if cidade_atlz == 'sousa':
        desconto_atlz = True
    else:
        desconto_atlz = False
    
    conexao = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = 'niojo123',
        database = 'livraria_bd',
    )
    cursor = conexao.cursor(prepared=True)
    comando = f'UPDATE cliente SET nome = %s, cpf = %s, telefone = %s, email = %s, is_desconto = %s WHERE id = %s' #UPDATE
    valores = (nome_atlz, cpf_atlz, telefone_atlz, email_atlz, desconto_atlz, id_usuario)
    cursor.execute(comando, valores)
    conexao.commit() # Edita o banco de dados
    conexao.close()
    
    return pagina_alterar_dados_cliente()

#==============================================================================#

############################################################################################################
############################################ ROTAS DOS VENDEDORES ##########################################
############################################################################################################

############################################################################################################
################################################# Clientes #################################################
############################################################################################################

#==============================================================================#
@app.route("/homepage_vendedor.html")
def home_vendedor():
    return render_template("homepage_vendedor.html")
#==============================================================================#

@app.route("/Cadastrar_cliente_vendedor.html") #CREATE
def pagina_cadastrarCliente_vendedor():
    return render_template("Pages_vendedor/Cadastrar_cliente_vendedor.html")

#envio feito pelo perfil do vendedor
@app.route('/submit_vendedor', methods=['POST'])
def submit_vendedor():
    name = request.form['nome_cliente']
    cpf = request.form['cpf_cliente']
    telefone = request.form['telefone_cliente']
    email = request.form['email_cliente']
    cidade = request.form['cidade_cliente'].lower()

    if cidade == 'sousa':
        desconto = True
    else:
        desconto = False

    conexao = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = 'niojo123',
        database = 'livraria_bd',
    )
    
    cursor = conexao.cursor(prepared=True)
    sql = f'INSERT INTO cliente (nome, cpf, telefone, email, is_desconto) VALUES (%s, %s, %s, %s, %s)'
    valores = (name, cpf, telefone, email, desconto)
    cursor.execute(sql, valores)
    conexao.commit()
    conexao.close()

    return render_template("Pages_vendedor/Cadastrar_cliente_vendedor.html")


#==============================================================================#

@app.route("/Pesquisar_cliente_vendedor.html")
def pagina_pesquisar_cliente_vendedor():
    return render_template("Pages_vendedor/Pesquisar_cliente_vendedor.html")

@app.route("/pesquisar_cliente_vend", methods=['POST'])
def pesquisar_cliente_vendedor():
    pesquisar_nome = request.form['nome_cliente']

    conexao = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = 'niojo123',
        database = 'livraria_bd',
    )
    cursor = conexao.cursor(prepared=True)
    comando = f'SELECT * FROM cliente WHERE nome LIKE %s' #READ
    valores = ('%' + pesquisar_nome + '%',)
    cursor.execute(comando, valores)
    resultado = cursor.fetchall() # Ler o banco de dados
    conexao.close()

    return render_template('Pages_vendedor/Pesquisar_cliente_vendedor.html', cliente = resultado)

#==============================================================================#
@app.route("/listar_all_clientes_vendedor.html")
def pagina_listarAllClientes_vendedor():
    return render_template("Pages_vendedor/listar_all_clientes_vendedor.html")


@app.route("/exibir_clientes_vendedor") #READ
def exibirClientes_vendedor():
    conexao = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = 'niojo123',
        database = 'livraria_bd',
    )
    
    cursor = conexao.cursor()
    sql = f'SELECT * FROM cliente' #READ
    cursor.execute(sql)
    resultado = cursor.fetchall() # Ler o banco de dados
    conexao.close()
    
    return render_template('Pages_vendedor/listar_all_clientes_vendedor.html', cliente = resultado)

#==============================================================================#
############################################################################################################
################################################## Livros ##################################################
############################################################################################################

#==============================================================================#
@app.route("/Pesquisar_livro_vendedor.html")
def pagina_pesquisar_livros_vendedor():
    return render_template("Pages_vendedor/Pesquisar_livro_vendedor.html")

@app.route("/pesquisar_livro_vendedor", methods=['POST'])
def pesquisar_livros_vendedor():
    pesquisar_nome = request.form['nome_livro']
    categoria = request.form['categoria_livro']
    preco_min = request.form['preco_min']
    preco_max = request.form['preco_max']
    qtd_produtos = request.form['quantidade']
    local  = request.form['local_fabric']

    if preco_min == '':
        preco_min = '0'
    
    if preco_max == '':
        preco_max = '99999'
    
    conexao = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = 'niojo123',
        database = 'livraria_bd',
    )
    cursor = conexao.cursor(prepared=True)
    
    comando = f'SELECT * FROM livro WHERE 1=1'
    valores = []

    # Adicionar critérios de pesquisa à consulta e à lista de valores
    if pesquisar_nome:
        comando += f' AND nome LIKE %s'
        valores.append('%' + pesquisar_nome + '%')

    if categoria != '0':
        comando += f' AND id_categoria = %s'
        valores.append(categoria)

    if preco_min and preco_max:
        comando += f' AND ROUND(preco, 2) BETWEEN %s AND %s'
        valores.append(preco_min)
        valores.append(preco_max)

    if qtd_produtos:
        comando += f' AND quantidade_estoq <= %s'
        valores.append(qtd_produtos)

    if local:
        comando += f' AND local_fabricacao LIKE %s'
        valores.append('%' + local + '%')

    # Executar a consulta com os critérios de pesquisa
    cursor = conexao.cursor()
    cursor.execute(comando, tuple(valores))

    resultado = cursor.fetchall() # Ler o banco de dados
    conexao.close()

    return render_template('Pages_vendedor/Pesquisar_livro_vendedor.html', livro = resultado)

#==============================================================================#
@app.route("/listar_all_livros_vendedor.html")
def pagina_listarAllLivros_vendedor():
    return render_template("Pages_vendedor/listar_all_livros_vendedor.html")

@app.route("/exibir_livros_vendedor") #READ
def exibirLivros_vendedor():
    conexao = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = 'niojo123',
        database = 'livraria_bd',
    )
    
    cursor = conexao.cursor()
    sql = f'SELECT * FROM livro' #READ
    cursor.execute(sql)
    resultado = cursor.fetchall() # Ler o banco de dados
    conexao.close()
    
    return render_template('Pages_vendedor/listar_all_livros_vendedor.html', livro = resultado)
#==============================================================================#

@app.route("/Gerar_relatorio_vendedores.html")
def pagina_gerarRelatorio_vendedor():
    return render_template("Pages_vendedor/Gerar_relatorio_vendedores.html")

@app.route("/exibir_relatorio_vendedor" , methods=['POST'])
def gerarRelatorio_vendedor():
    id_vend = request.form['id_vendedor']
    data_i = request.form['data_inicial']
    data_f = request.form['data_final'] 

    conexao = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = 'niojo123',
        database = 'livraria_bd',
    )
    
    cursor = conexao.cursor()
    sql = f'CALL relatorio_de_vendas_mensal(%s, DATE(%s), DATE(%s))'
    valores = (id_vend, data_i, data_f)
    cursor.execute(sql, valores)
    resultado = cursor.fetchall()
    cursor.close()
    conexao.close()

    return render_template('Pages_vendedor/Gerar_relatorio_vendedores.html', relatorio_vendedor = resultado)

############################################################################################################
############################################## ROTAS DO ADMIN ##############################################
############################################################################################################

############################################################################################################
################################################# Clientes #################################################
############################################################################################################

#==============================================================================#
@app.route("/homepage_admin.html")
def home_admin():
    return render_template("homepage_admin.html")
#==============================================================================#

@app.route("/Cadastrar_vendedor_admin.html")
def pagina_cadastrarVendedor_admin():
    return render_template("Pages_admin/Cadastrar_vendedor_admin.html")

@app.route('/cadastro_vendedor', methods=['POST'])
def cadastro_vendedor_admin():
    nome = request.form['nome_vendedor']
    cpf = request.form['cpf_vendedor']
    telefone = request.form['telefone_vendedor']
    email = request.form['email_vendedor']

    conexao = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = 'niojo123',
        database = 'livraria_bd',
    )
    
    cursor = conexao.cursor(prepared=True)
    sql = f'INSERT INTO vendedor (nome, cpf, telefone, email) VALUES (%s, %s, %s, %s)'
    valores = (nome, cpf, telefone, email)
    cursor.execute(sql, valores)
    conexao.commit()
    conexao.close()

    return render_template("Pages_admin/Cadastrar_vendedor_admin.html")


#==============================================================================#
@app.route("/Cadastrar_cliente_admin.html") #CREATE
def pagina_cadastrarCliente_admin():
    return render_template("Pages_admin/Cadastrar_cliente_admin.html")

#envio feito pelo perfil do administrador
@app.route('/submit_admin', methods=['POST'])
def submit_admin():
    name = request.form['nome_cliente']
    cpf = request.form['cpf_cliente']
    telefone = request.form['telefone_cliente']
    email = request.form['email_cliente']
    cidade = request.form['cidade_cliente'].lower()

    if cidade == 'sousa':
        desconto = True
    else:
        desconto = False

    conexao = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = 'niojo123',
        database = 'livraria_bd',
    )
    
    cursor = conexao.cursor(prepared=True)
    sql = f'INSERT INTO cliente (nome, cpf, telefone, email, is_desconto) VALUES (%s, %s, %s, %s, %s)'
    valores = (name, cpf, telefone, email, desconto)
    cursor.execute(sql, valores)
    conexao.commit()
    conexao.close()

    return render_template("Pages_admin/Cadastrar_cliente_admin.html")
#==============================================================================#

@app.route("/Alterar_cadastro_cliente_admin.html") #UPDATE
def pagina_alterar_cadastro_cliente():
    return render_template("Pages_admin/Alterar_cadastro_cliente_admin.html")

@app.route("/alterar_cliente", methods=['POST']) #UPDATE
def alterar_cadastro_cliente():
    id_usuario = request.form['id']
    nome_atlz = request.form['nome_atlzd']
    cpf_atlz = request.form['cpf_atlzd']
    email_atlz = request.form['email_atlzd']
    telefone_atlz = request.form['telefone_atlzd']
    cidade_atlz = request.form['cidade_atlz'].lower()

    if cidade_atlz == 'sousa':
        desconto_atlz = True
    else:
        desconto_atlz = False


    conexao = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = 'niojo123',
        database = 'livraria_bd',
    )
    cursor = conexao.cursor(prepared=True)
    comando = f'UPDATE cliente SET nome = %s, cpf = %s, telefone = %s, email = %s, is_desconto = %s WHERE id = %s' #UPDATE
    valores = (nome_atlz, cpf_atlz, telefone_atlz, email_atlz, desconto_atlz, id_usuario)
    cursor.execute(comando, valores)
    conexao.commit() # Edita o banco de dados
    conexao.close()
    
    return pagina_alterar_cadastro_cliente()
#==============================================================================#

@app.route("/Pesquisar_cliente_admin.html")
def pagina_pesquisar_cliente():
    return render_template("Pages_admin/Pesquisar_cliente.html")

@app.route("/pesquisar_cliente", methods=['POST'])
def pesquisar_cliente():
    pesquisar_nome = request.form['nome_cliente']

    conexao = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = 'niojo123',
        database = 'livraria_bd',
    )
    cursor = conexao.cursor(prepared=True)
    comando = f'SELECT * FROM cliente WHERE nome LIKE %s' #READ
    valores = ('%' + pesquisar_nome + '%',)
    cursor.execute(comando, valores)
    resultado = cursor.fetchall() # Ler o banco de dados
    conexao.close()

    return render_template('Pages_admin/Pesquisar_cliente.html', cliente = resultado)
#==============================================================================#

@app.route("/Remover_cliente_admin.html")
def pagina_remover_cliente():
    return render_template("Pages_admin/Remover_cliente.html")

@app.route("/remover_cliente", methods=['POST'])
def remover_cliente():
    id = request.form['id']

    conexao = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = 'niojo123',
        database = 'livraria_bd',
    )
    cursor = conexao.cursor(prepared=True)
    comando = f'DELETE FROM cliente WHERE id = %s' # DELETE
    valores = (id,)
    cursor.execute(comando, valores)
    conexao.commit() # Edita o banco de dados
    conexao.close()
    
    return pagina_remover_cliente()

#==============================================================================#

@app.route("/listar_all_clientes_admin.html")
def pagina_listarAllClientes():
    return render_template("Pages_admin/listar_all_clientes.html")


@app.route("/exibir_clientes") #READ
def exibirClientes():
    conexao = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = 'niojo123',
        database = 'livraria_bd',
    )
    
    cursor = conexao.cursor()
    sql = f'SELECT * FROM cliente' #READ
    cursor.execute(sql)
    resultado = cursor.fetchall() # Ler o banco de dados
    conexao.close()
    
    return render_template('Pages_admin/listar_all_clientes.html', cliente = resultado)
#==============================================================================#

############################################################################################################
################################################## Livros ##################################################
############################################################################################################

#==============================================================================#

@app.route("/Cadastrar_livro_admin.html")
def cadastrar_livro():
    return render_template("Pages_admin/Cadastrar_livro.html")

@app.route('/submit_livro', methods=['POST'])
def submit_livro():
    nome = request.form['nome_livro']
    preco = request.form['preco_livro']
    local  = request.form['local_fabric']
    qtd_livro = request.form['quantidade_livro']
    categoria = request.form['categoria_livro']

    conexao = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = 'niojo123',
        database = 'livraria_bd',
    )
    
    cursor = conexao.cursor(prepared=True)
    sql = f'INSERT INTO livro (id_categoria, nome, preco, local_fabricacao, quantidade_estoq) VALUES (%s, %s, %s, %s, %s)'
    valores = (categoria, nome, preco, local, qtd_livro)
    cursor.execute(sql, valores)
    conexao.commit()
    conexao.close()

    return cadastrar_livro()

#==============================================================================#

@app.route("/Alterar_cadastro_livro_admin.html") #UPDATE
def pagina_alterar_cadastro_livro():
    return render_template("Pages_admin/Alterar_cadastro_livro_admin.html")

@app.route("/alterar_livro", methods=['POST']) #UPDATE
def alterar_cadastro_livro():
    id_livro = request.form['id']
    nome_atlz = request.form['nome_atlzd']
    preco_atlz = request.form['preco_atlzd']
    local_atlz  = request.form['local_fabric_atlz']
    qtd_atlz = request.form['quantidade_atlzd']
    categoria_atlz = request.form['categoria_livro_atlz']


    conexao = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = 'niojo123',
        database = 'livraria_bd',
    )
    cursor = conexao.cursor(prepared=True)
    comando = f'UPDATE livro SET id_categoria = %s, nome = %s, preco = %s, local_fabricacao = %s, quantidade_estoq = %s WHERE id = %s' #UPDATE
    valores = (categoria_atlz, nome_atlz, preco_atlz, local_atlz, qtd_atlz, id_livro)
    cursor.execute(comando, valores)
    conexao.commit() # Edita o banco de dados
    conexao.close()
    
    return pagina_alterar_cadastro_livro()

#==============================================================================#

@app.route("/Pesquisar_livro_admin.html")
def pagina_pesquisar_livros():
    return render_template("Pages_admin/Pesquisar_livro.html")

@app.route("/pesquisar_livro", methods=['POST'])
def pesquisar_livros():
    pesquisar_nome = request.form['nome_livro']
    categoria = request.form['categoria_livro']
    preco_min = request.form['preco_min']
    preco_max = request.form['preco_max']
    qtd_produtos = request.form['quantidade']
    local  = request.form['local_fabric']

    if preco_min == '':
        preco_min = '0'
    
    if preco_max == '':
        preco_max = '99999'
    
    conexao = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = 'niojo123',
        database = 'livraria_bd',
    )
    cursor = conexao.cursor(prepared=True)
    
    comando = f'SELECT * FROM livro WHERE 1=1'
    valores = []

    # Adicionar critérios de pesquisa à consulta e à lista de valores
    if pesquisar_nome:
        comando += f' AND nome LIKE %s'
        valores.append('%' + pesquisar_nome + '%')

    if categoria != '0':
        comando += f' AND id_categoria = %s'
        valores.append(categoria)

    if preco_min and preco_max:
        comando += f' AND ROUND(preco, 2) BETWEEN %s AND %s'
        valores.append(preco_min)
        valores.append(preco_max)

    if qtd_produtos:
        comando += f' AND quantidade_estoq <= %s'
        valores.append(qtd_produtos)

    if local:
        comando += f' AND local_fabricacao LIKE %s'
        valores.append('%' + local + '%')

    # Executar a consulta com os critérios de pesquisa
    cursor = conexao.cursor()
    cursor.execute(comando, tuple(valores))

    resultado = cursor.fetchall() # Ler o banco de dados
    conexao.close()

    return render_template('Pages_admin/Pesquisar_livro.html', livro = resultado)

#==============================================================================#

@app.route("/Remover_livro_admin.html")
def pagina_remover_livro():
    return render_template("Pages_admin/Remover_livro.html")

@app.route("/remover_livro", methods=['POST'])
def remover_livro():
    id = request.form['id']

    conexao = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = 'niojo123',
        database = 'livraria_bd',
    )
    cursor = conexao.cursor(prepared=True)
    comando = f'DELETE FROM livro WHERE id = %s' # DELETE
    valores = (id,)
    cursor.execute(comando, valores)
    conexao.commit() # Edita o banco de dados
    conexao.close()
    
    return pagina_remover_livro()

#==============================================================================#

@app.route("/listar_all_livros_admin.html")
def pagina_listarAllLivros():
    return render_template("Pages_admin/listar_all_livros.html")


@app.route("/exibir_livros") #READ
def exibirLivros():
    conexao = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = 'niojo123',
        database = 'livraria_bd',
    )
    
    cursor = conexao.cursor()
    sql = f'SELECT * FROM livro' #READ
    cursor.execute(sql)
    resultado = cursor.fetchall() # Ler o banco de dados
    conexao.close()
    
    return render_template('Pages_admin/listar_all_livros.html', livro = resultado)
#==============================================================================#

@app.route("/Gerar_relatorio_admin.html")
def pagina_gerarRelatorio():
    return render_template("Pages_admin/Gerar_relatorio.html")


@app.route("/exibir_relatorio") #READ 
def exibirRelatorio():
    conexao = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = 'niojo123',
        database = 'livraria_bd',
    )
    
    cursor = conexao.cursor()
    sql_1 = f'SELECT * FROM cliente'
    sql_2 = f'SELECT * FROM livro'
    cursor.execute(sql_1)
    clientes = cursor.fetchall() # Ler o banco de dados

    cursor.execute(sql_2)
    livros = cursor.fetchall()

    conexao.close()

    qtd_clientes = len(clientes) # pega a quantidade de elementos(as pessoas cadastradas) dentro da lista
    qtd_livros_diferente = len(livros)

    valor_total = sum(coluna[3] * coluna[5] for coluna in livros)# pega todos os valores das colunas 2(preço) e 3(quantidade), realiza a multiplicação (preço x quantidade), linha por linha,
                                                                 # e depois soma tudo para ter o valor total do estoque
    valor_total = round(valor_total, 2)

    total_livros = sum(coluna[5] for coluna in livros) # Soma todos os valores da coluna [3]
    


    return render_template('Pages_admin/Gerar_relatorio.html', cliente = clientes, total_clientes = qtd_clientes, livro = livros, total_livros_dif = qtd_livros_diferente, livros_total = total_livros, preco_total = valor_total)

#==============================================================================#

@app.route("/Gerar_relatorio_vendedores_admin.html")
def pagina_gerarRelatorio_vendedor_admin():
    return render_template("Pages_admin/Gerar_relatorio_vendedores_admin.html")

@app.route("/exibir_relatorio_vendedor_admin" , methods=['POST'])
def gerarRelatorio_vendedor_admin():
    id_vend = request.form['id_vendedor']
    data_i = request.form['data_inicial']
    data_f = request.form['data_final'] 

    conexao = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = 'niojo123',
        database = 'livraria_bd',
    )
    
    cursor = conexao.cursor()
    sql = f'CALL relatorio_de_vendas_mensal(%s, DATE(%s), DATE(%s))'
    valores = (id_vend, data_i, data_f)
    cursor.execute(sql, valores)
    resultado = cursor.fetchall()
    cursor.close()
    conexao.close()

    return render_template('Pages_admin/Gerar_relatorio_vendedores_admin.html', relatorio_vendedor = resultado)

#==============================================================================#
@app.route("/Historico_De_Compras.html")
def pagina_exibir_historico_de_compras_cliente():
    conexao = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = 'niojo123',
        database = 'livraria_bd',
    )
    
    cursor = conexao.cursor()
    sql = f'CALL historico_de_compras(%s)' #READ
    id_cliente = session.get('id_cliente')
    valores = (id_cliente)
    cursor.execute(sql, (valores , ))
    resultados = cursor.fetchall() # Ler o banco de dados
    conexao.close()
    return render_template("Pages_cliente/Historico_de_Compras.html",  resultados = resultados)



#=======================================================================================================#
@app.route("/Realizar_Compra.html")
def pagina_realizar_compra():
    conexao = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = 'niojo123',
        database = 'livraria_bd',
    )
    cursor = conexao.cursor()
    sql = f'SELECT * FROM livro' #READ
    cursor.execute(sql)
    livros = cursor.fetchall() # Ler o banco de dados
    sql = f'SELECT * FROM pagamento' #READ
    cursor.execute(sql)
    pagamentos = cursor.fetchall() # Ler o banco de dados
    sql = f'SELECT * FROM vendedor' #READ
    cursor.execute(sql)
    vendedores = cursor.fetchall() # Ler o banco de dados
    conexao.close()
    return render_template("Pages_cliente/Realizar_Compra.html",livros=livros, pagamentos=pagamentos, vendedores=vendedores)


@app.route("/adicionar-produto",  methods=['POST']) #READ
def realizar_compra():
    quantidade = request.form['qtd'] 
    livro = request.form['livro']
    pagamento = request.form['pagamento']
    vendedor = request.form['vendedor']
    conexao = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = 'niojo123',
        database = 'livraria_bd',
    )
    
    cursor = conexao.cursor()
    atualizacao_estoque_query = """
    UPDATE livro
    SET quantidade_estoq = quantidade_estoq - %s
    WHERE id = %s;
    """
    cursor.execute(atualizacao_estoque_query, (int(quantidade), int(livro)))
    conexao.commit()

    
    sql = f'SELECT * FROM livro WHERE id = %s' #READ
    valores = (livro)
    cursor.execute(sql, (valores , ))
    get_livro = cursor.fetchall() # Ler o banco de dados
    
    sql = f'SELECT * FROM pagamento WHERE id = %s' #READ
    valores = (pagamento)
    cursor.execute(sql, (valores , ))
    get_pagamento = cursor.fetchall() # Ler o banco de dados
    
    sql = f'SELECT * FROM vendedor WHERE id = %s' #READ
    valores = (vendedor)
    cursor.execute(sql, (valores , ))
    get_vendedor = cursor.fetchall() # Ler o banco de dados
    
    cursor = conexao.cursor()
    if 'produtos' in session:
        session["produtos"] = session.get('produtos') + [[livro, pagamento, vendedor, quantidade, get_livro[0][2], get_pagamento[0][1],  get_vendedor[0][1]]]

    sql = f'SELECT * FROM livro' #READ
    cursor.execute(sql)
    livros = cursor.fetchall() # Ler o banco de dados
    sql = f'SELECT * FROM pagamento' #READ
    cursor.execute(sql)
    pagamentos = cursor.fetchall() # Ler o banco de dados
    sql = f'SELECT * FROM vendedor' #READ
    cursor.execute(sql)
    vendedores = cursor.fetchall() # Ler o banco de dados
    cursor.close()
    conexao.close()
    
    print(session.get('produtos'))
    session["valor_total"] = 0
    session["valor_total"] = session.get('valor_total') + (livros[int(livro)-1][3]*int(quantidade)) 
    return render_template("Pages_cliente/Realizar_Compra.html",livros=livros, pagamentos=pagamentos, vendedores=vendedores, cart = session.get('produtos'), valorTotal=session.get('valor_total'))
    return redirect(url_for('historico_de_compras'))

@app.route("/finalizar-compra",  methods=['POST']) #READ
def finalizar_compra():
    id_cliente = session.get('id_cliente')
    produtos = session.get('produtos')


    conexao = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = 'niojo123',
        database = 'livraria_bd',
    )
    cursor = conexao.cursor()
    
    for i in produtos:
        valores = (id_cliente, int(i[1]),int(i[2]),int(i[0]),int(i[3]))
        try:
            sql = '''CALL realizar_compra(%d,%d,%d,%d,%d,CURRENT_DATE())'''%valores #READ
            cursor.execute(sql)
            conexao.commit()
            session["produtos"] = []
            session["valor_total"] = 0.0
            sql = f'CALL historico_de_compras(%s)' #READ
            id_cliente = session.get('id_cliente')
            valores = (id_cliente)
            cursor.execute(sql, (valores , ))
            resultados = cursor.fetchall() # Ler o banco de dados
            conexao.close()
            return render_template("Pages_cliente/Historico_de_Compras.html",  resultados = resultados)
        except:
            flash("Não tem livros suficiente no estoque!")
            session["produtos"] = []
            session["valor_total"] = 0.0
            cursor = conexao.cursor()
            sql = f'SELECT * FROM livro' #READ
            cursor.execute(sql)
            livros = cursor.fetchall() # Ler o banco de dados
            sql = f'SELECT * FROM pagamento' #READ
            cursor.execute(sql)
            pagamentos = cursor.fetchall() # Ler o banco de dados
            sql = f'SELECT * FROM vendedor' #READ
            cursor.execute(sql)
            vendedores = cursor.fetchall() # Ler o banco de dados
            conexao.close()
            return render_template("Pages_cliente/Realizar_Compra.html",livros=livros, pagamentos=pagamentos, vendedores=vendedores)
    
            return render_template("Pages_cliente/Historico_de_Compras.html", resultados=resultados)
        
@app.route("/livros_mais_vendidos")
def livros_mais_vendidos():
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='niojo123',
        database='livraria_bd',
    )
    print("Iniciando busca de livros mais vendidos")  # Debugging

    query = """
    SELECT * FROM livros_mais_vendidos;
    """
    cursor = conexao.cursor(prepared=True)
    cursor.execute(query)
    livros = cursor.fetchall()
    cursor.close()
    print(f"Livros: {livros}")  # Adicione esta linha para debug

    # Transforma os resultados em uma lista de dicionários
    livros_dict = [{"titulo": livro[1], "total_vendas": livro[2]} for livro in livros]

    return render_template("livros_mais_vendidos.html", livros=livros_dict)


    

#=======================================================================================================#
if __name__ == "__main__":
    app.run(debug=True,port=5000)
#=======================================================================================================#