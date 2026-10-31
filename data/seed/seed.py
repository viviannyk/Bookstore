"""Popula o livraria_bd com dados fictícios. Com a mesma semente, gera sempre os mesmos dados.

Uso, a partir da raiz do repositório:
    python data/seed/seed.py          # recusa rodar se o banco já tiver dados
    python data/seed/seed.py --reset  # apaga tudo antes de popular
"""
import argparse
import os
import random
from datetime import date, timedelta
from decimal import Decimal
from pathlib import Path

import mysql.connector
from dotenv import load_dotenv
from faker import Faker

SEMENTE = 42
DIAS_DE_HISTORICO = 730
CATEGORIAS = ["Fantasia", "Ficção Científica", "Educação"]  # A ordem define os IDs usados nos templates
PAGAMENTOS = ["Pix", "Cartão de crédito", "Cartão de débito", "Boleto"]
LOCAIS = ["São Paulo", "Rio de Janeiro", "Recife", "Porto Alegre", "João Pessoa", "Belo Horizonte"]
TITULOS = {
    1: (["O Reino", "A Espada", "O Dragão", "A Coroa", "A Floresta"], ["de Cristal", "das Sombras", "do Norte", "Perdida", "de Prata", "Encantada"]),
    2: (["A Colônia", "O Código", "A Estação", "O Protocolo", "A Órbita"], ["de Marte", "Quântico", "Final", "Zero", "de Titã", "Infinita"]),
    3: (["Introdução à Lógica", "Didática", "Fundamentos da Matemática", "Pedagogia", "História da Ciência"], ["na Prática", "para Iniciantes", "Moderna", "Aplicada", "em Debate", "Essencial"]),
}
TABELAS = ["venda", "livro", "cliente", "vendedor", "pagamento", "categoria"]


def conectar():
    load_dotenv(Path(__file__).parents[1] / ".env")
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password=os.environ["MYSQL_ROOT_PASSWORD"],
        database="livraria_bd",
    )


def limpar(cursor):
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
    for tabela in TABELAS:
        cursor.execute(f"TRUNCATE TABLE {tabela}")
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1")


def gerar_clientes(fake, quantidade):
    # O primeiro cliente é uma conta fixa para testar o login
    clientes = [("Cliente Demo", "000.000.000-00", "(83) 90000-0000", "demo@bookstore.local", True, "demo123")]
    for _ in range(quantidade - 1):
        clientes.append((fake.name(), fake.unique.cpf(), fake.phone_number()[:20], fake.unique.email(), fake.boolean(15), None))
    return clientes


def gerar_livros(quantidade):
    livros = []
    usados = set()
    while len(livros) < quantidade:
        categoria = random.randint(1, 3)
        inicio, fim = TITULOS[categoria]
        titulo = f"{random.choice(inicio)} {random.choice(fim)}"
        if titulo in usados:
            titulo = f"{titulo}, Vol. {random.randint(2, 9)}"
        if titulo in usados:
            continue
        usados.add(titulo)
        preco = Decimal(random.randint(2500, 15000)) / 100
        livros.append((categoria, titulo, preco, random.choice(LOCAIS), random.randint(20, 300)))
    return livros


def gerar_vendas(quantidade, clientes, livros, total_vendedores):
    hoje = date.today()
    # Alguns livros e clientes vendem bem mais que outros, como em uma loja real
    pesos_livros = [random.paretovariate(2.5) for _ in livros]
    pesos_clientes = [random.paretovariate(1.5) for _ in clientes]
    ids_livros = random.choices(range(1, len(livros) + 1), weights=pesos_livros, k=quantidade)
    ids_clientes = random.choices(range(1, len(clientes) + 1), weights=pesos_clientes, k=quantidade)

    vendas = []
    for id_livro, id_cliente in zip(ids_livros, ids_clientes):
        dias_atras = int(random.triangular(0, DIAS_DE_HISTORICO, 0))  # Vendas crescem com o tempo
        quantidade_item = random.choices([1, 2, 3], weights=[80, 15, 5])[0]
        # O preço antigo era um pouco menor: é por isso que a venda guarda o próprio preço
        ajuste = Decimal(1) - Decimal(dias_atras) / Decimal(DIAS_DE_HISTORICO) * Decimal("0.15")
        preco = (livros[id_livro - 1][2] * ajuste).quantize(Decimal("0.01"))
        desconto = Decimal(10) if clientes[id_cliente - 1][4] else Decimal(0)
        total = (preco * quantidade_item * (1 - desconto / 100)).quantize(Decimal("0.01"))
        vendas.append((
            id_cliente, random.randint(1, len(PAGAMENTOS)), random.randint(1, total_vendedores), id_livro,
            quantidade_item, preco, desconto, total, hoje - timedelta(days=dias_atras),
        ))
    return vendas


def inserir_em_lotes(cursor, sql, linhas, tamanho=2000):
    for inicio in range(0, len(linhas), tamanho):
        cursor.executemany(sql, linhas[inicio:inicio + tamanho])


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--reset", action="store_true", help="apaga os dados existentes antes de popular")
    parser.add_argument("--clientes", type=int, default=500)
    parser.add_argument("--livros", type=int, default=120)
    parser.add_argument("--vendedores", type=int, default=10)
    parser.add_argument("--vendas", type=int, default=20000)
    args = parser.parse_args()

    random.seed(SEMENTE)
    Faker.seed(SEMENTE)
    fake = Faker("pt_BR")

    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT COUNT(*) FROM cliente")
    if cursor.fetchone()[0] and not args.reset:
        raise SystemExit("O banco já tem dados. Use --reset para apagar tudo e popular de novo.")
    if args.reset:
        limpar(cursor)

    clientes = gerar_clientes(fake, args.clientes)
    livros = gerar_livros(args.livros)
    vendedores = [(fake.name(), fake.unique.cpf(), fake.phone_number()[:20], fake.unique.email()) for _ in range(args.vendedores)]
    vendas = gerar_vendas(args.vendas, clientes, livros, args.vendedores)

    cursor.executemany("INSERT INTO categoria (nome) VALUES (%s)", [(nome,) for nome in CATEGORIAS])
    cursor.executemany("INSERT INTO pagamento (nome) VALUES (%s)", [(nome,) for nome in PAGAMENTOS])
    inserir_em_lotes(cursor, "INSERT INTO vendedor (nome, cpf, telefone, email) VALUES (%s, %s, %s, %s)", vendedores)
    inserir_em_lotes(cursor, "INSERT INTO cliente (nome, cpf, telefone, email, is_desconto, senha) VALUES (%s, %s, %s, %s, %s, %s)", clientes)
    inserir_em_lotes(cursor, "INSERT INTO livro (id_categoria, nome, preco, local_fabricacao, quantidade_estoq) VALUES (%s, %s, %s, %s, %s)", livros)
    inserir_em_lotes(
        cursor,
        """INSERT INTO venda (id_cliente, id_pagamento, id_vendedor, id_livro, quantidade,
                              preco_unitario, percentual_desconto, valor_total, data_venda)
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        vendas,
    )
    conexao.commit()
    conexao.close()
    print(f"Pronto: {len(clientes)} clientes, {len(livros)} livros, {len(vendedores)} vendedores e {len(vendas)} vendas.")


if __name__ == "__main__":
    main()
