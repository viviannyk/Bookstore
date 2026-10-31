# Bookstore

Livraria web feita com **Flask** e **MySQL**, com área para clientes, vendedores e administradores. Tem catálogo com filtros, carrinho, histórico de compras e relatórios de vendas, tudo em um visual pastel que funciona no computador e no celular.

![Página inicial da Bookstore](docs/screenshots/home.png)

## Funcionalidades

**Visitantes**

- Catálogo na página inicial, com abas por categoria e busca
- Ranking dos livros mais vendidos
- Cadastro e login de clientes

**Clientes**

- Compra com carrinho, escolha de pagamento e vendedor
- Histórico de compras
- Edição dos dados pessoais

**Vendedores**

- Cadastro, busca e listagem de clientes
- Busca de livros por nome, preço, local, categoria e estoque
- Relatório de vendas por período

**Administradores**

- Tudo o que o vendedor faz, mais o cadastro de vendedores
- Cadastro, alteração e remoção de clientes e livros
- Relatório geral com clientes, livros, estoque e valor armazenado

## Telas

| Painel do administrador                                       | Compra                                         |
| ------------------------------------------------------------- | ---------------------------------------------- |
| ![Painel do administrador](docs/screenshots/painel-admin.png) | ![Tela de compra](docs/screenshots/compra.png) |

<img src="docs/screenshots/home-mobile.png" alt="Página inicial no celular" width="280">

## Tecnologias

- **Back-end:** Python, Flask e `mysql-connector-python`
- **Banco de dados:** MySQL
- **Front-end:** templates Jinja2, CSS e JavaScript puros, sem framework
- **Acessibilidade:** widget [VLibras](https://vlibras.gov.br/) em todas as páginas

## Como rodar

Você vai precisar de Python 3.10 ou mais recente e de um servidor MySQL.

**1. Clone o repositório**

```bash
git clone git@github.com:viviannyk/Bookstore.git
cd Bookstore
```

**2. Instale as dependências**

```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Linux e macOS
pip install flask mysql-connector-python
```

**3. Prepare o banco de dados**

O script do banco não está neste repositório, então é preciso ter um banco `livraria_bd` em `localhost` com estes objetos:

| Tipo       | Nome                                                                          |
| ---------- | ----------------------------------------------------------------------------- |
| Tabelas    | `cliente`, `vendedor`, `livro`, `pagamento`                           |
| View       | `livros_mais_vendidos`                                                      |
| Procedures | `realizar_compra`, `historico_de_compras`, `relatorio_de_vendas_mensal` |

As credenciais de conexão ficam em [`Parte 2/app.py`](<Parte%202/app.py>). Ajuste-as para as do seu MySQL.

**4. Inicie o servidor**

```bash
cd "Parte 2"
python app.py
```

Depois é só abrir [http://localhost:5000](http://localhost:5000). Se o MySQL estiver fora do ar, a página inicial abre mesmo assim, sem o catálogo; as demais páginas que usam o banco não funcionam.

## Estrutura

```
Parte 2/
├── app.py                 # Rotas e consultas ao banco
├── static/
│   ├── css/bookstore.css  # Tema do site
│   ├── js/                # Menu, abas, busca e máscaras
│   └── img/               # Ilustração, capas e formas em SVG
└── templates/
    ├── base.html          # Layout comum: barra do topo e rodapé
    ├── _macros.html       # Componentes: cards, abas, campos e tabelas
    ├── partials/          # Telas compartilhadas por admin e vendedor
    ├── Pages_admin/
    ├── Pages_cliente/
    └── Pages_vendedor/
```

## Licença

Distribuído sob a licença MIT. Veja o arquivo [LICENSE](LICENSE).
