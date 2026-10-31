-- Schema da livraria, reconstruído a partir do que o app.py lê e grava.
-- A ordem das colunas importa: o app acessa as linhas por posição (ex.: livro[3] é o preço).

CREATE DATABASE IF NOT EXISTS livraria_bd CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE livraria_bd;

CREATE TABLE categoria (
    id   INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(60) NOT NULL UNIQUE
);

CREATE TABLE cliente (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    nome        VARCHAR(120) NOT NULL,
    cpf         VARCHAR(14)  NOT NULL,
    telefone    VARCHAR(20)  NOT NULL,
    email       VARCHAR(120) NOT NULL,
    is_desconto BOOLEAN      NOT NULL DEFAULT FALSE,
    senha       VARCHAR(255) NULL -- Fica vazia em quem vem do formulário Cadastre-se
);

CREATE TABLE vendedor (
    id       INT AUTO_INCREMENT PRIMARY KEY,
    nome     VARCHAR(120) NOT NULL,
    cpf      VARCHAR(14)  NOT NULL,
    telefone VARCHAR(20)  NOT NULL,
    email    VARCHAR(120) NOT NULL
);

CREATE TABLE pagamento (
    id   INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(60) NOT NULL UNIQUE
);

CREATE TABLE livro (
    id               INT AUTO_INCREMENT PRIMARY KEY,
    id_categoria     INT NOT NULL,
    nome             VARCHAR(200)  NOT NULL,
    preco            DECIMAL(10,2) NOT NULL,
    local_fabricacao VARCHAR(120)  NOT NULL,
    quantidade_estoq INT NOT NULL, -- Pode ficar negativo: é assim que realizar_compra detecta falta de estoque
    CONSTRAINT fk_livro_categoria FOREIGN KEY (id_categoria) REFERENCES categoria (id)
);

-- Uma linha por livro vendido. Preço e desconto são copiados no momento da venda,
-- porque livro.preco muda com o tempo e a venda não pode mudar junto.
-- Cliente e livro removidos viram NULL para o histórico de vendas não se perder.
CREATE TABLE venda (
    id                  INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente          INT NULL,
    id_pagamento        INT NOT NULL,
    id_vendedor         INT NOT NULL,
    id_livro            INT NULL,
    quantidade          INT NOT NULL,
    preco_unitario      DECIMAL(10,2) NOT NULL,
    percentual_desconto DECIMAL(5,2)  NOT NULL DEFAULT 0,
    valor_total         DECIMAL(12,2) NOT NULL,
    data_venda          DATE NOT NULL,
    criado_em           TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT ck_venda_quantidade CHECK (quantidade > 0),
    CONSTRAINT fk_venda_cliente   FOREIGN KEY (id_cliente)   REFERENCES cliente (id)   ON DELETE SET NULL,
    CONSTRAINT fk_venda_pagamento FOREIGN KEY (id_pagamento) REFERENCES pagamento (id),
    CONSTRAINT fk_venda_vendedor  FOREIGN KEY (id_vendedor)  REFERENCES vendedor (id),
    CONSTRAINT fk_venda_livro     FOREIGN KEY (id_livro)     REFERENCES livro (id)     ON DELETE SET NULL,
    INDEX idx_venda_data (data_venda)
);

CREATE VIEW livros_mais_vendidos AS
SELECT l.id, l.nome AS titulo, SUM(v.quantidade) AS total_vendas
FROM venda v
JOIN livro l ON l.id = v.id_livro
GROUP BY l.id, l.nome
ORDER BY total_vendas DESC
LIMIT 10;

DELIMITER $$

-- Sem COMMIT aqui: quem controla a transação é o app, para o carrinho ser tudo ou nada.
-- O estoque já baixa em /adicionar-produto, então esta procedure só confere o saldo.
CREATE PROCEDURE realizar_compra(
    IN p_id_cliente   INT,
    IN p_id_pagamento INT,
    IN p_id_vendedor  INT,
    IN p_id_livro     INT,
    IN p_quantidade   INT,
    IN p_data         DATE
)
BEGIN
    DECLARE v_preco DECIMAL(10,2);
    DECLARE v_estoque INT;
    DECLARE v_tem_desconto BOOLEAN;
    DECLARE v_percentual DECIMAL(5,2);

    SELECT preco, quantidade_estoq INTO v_preco, v_estoque FROM livro WHERE id = p_id_livro;
    SELECT is_desconto INTO v_tem_desconto FROM cliente WHERE id = p_id_cliente;

    IF v_estoque < 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Estoque insuficiente';
    END IF;

    SET v_percentual = IF(v_tem_desconto, 10, 0);

    INSERT INTO venda (id_cliente, id_pagamento, id_vendedor, id_livro, quantidade,
                       preco_unitario, percentual_desconto, valor_total, data_venda)
    VALUES (p_id_cliente, p_id_pagamento, p_id_vendedor, p_id_livro, p_quantidade,
            v_preco, v_percentual, ROUND(v_preco * p_quantidade * (1 - v_percentual / 100), 2), p_data);
END$$

CREATE PROCEDURE historico_de_compras(IN p_id_cliente INT)
BEGIN
    SELECT v.id, v.data_venda, COALESCE(l.nome, 'Livro removido'), v.quantidade, v.valor_total
    FROM venda v
    LEFT JOIN livro l ON l.id = v.id_livro
    WHERE v.id_cliente = p_id_cliente
    ORDER BY v.data_venda DESC, v.id DESC;
END$$

CREATE PROCEDURE relatorio_de_vendas_mensal(
    IN p_id_vendedor INT,
    IN p_data_inicial DATE,
    IN p_data_final DATE
)
BEGIN
    SELECT ve.id, ve.nome, COUNT(v.id), COALESCE(SUM(v.quantidade), 0), COALESCE(SUM(v.valor_total), 0)
    FROM vendedor ve
    LEFT JOIN venda v ON v.id_vendedor = ve.id AND v.data_venda BETWEEN p_data_inicial AND p_data_final
    WHERE ve.id = p_id_vendedor
    GROUP BY ve.id, ve.nome;
END$$

DELIMITER ;
