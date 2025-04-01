
-- ESTE SCRIPT É RESPONSÁVEL POR CRIAR A TABELA OPERADORAS NO BANCO DE DADOS
CREATE TABLE operadoras (
    Registro_ANS INT NOT NULL,
    CNPJ BIGINT NOT NULL,
    Razao_Social VARCHAR(255) NOT NULL,
    Nome_Fantasia VARCHAR(255),
    Modalidade VARCHAR(255),
    Logradouro VARCHAR(255),
    Numero VARCHAR(50),
    Complemento VARCHAR(255),
    Bairro VARCHAR(255),
    Cidade VARCHAR(255),
    UF CHAR(2),
    CEP INT,
    DDD INT,
    Telefone BIGINT,
    Fax BIGINT,
    Endereco_eletronico VARCHAR(255),
    Representante VARCHAR(255),
    Cargo_Representante VARCHAR(255),
    Regiao_de_Comercializacao INT,
    Data_Registro_ANS DATE,
    PRIMARY KEY (Registro_ANS)
);

-- ESTE SCRIPT É RESPONSÁVEL POR CARREGAR OS DADOS DO ARQUIVO CSV NA TABELA OPERADORAS
LOAD DATA LOCAL INFILE '' --Coloque o caminho do arquivo CSV aqui
INTO TABLE operadoras
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(Registro_ANS, CNPJ, Razao_Social, Nome_Fantasia, Modalidade, Logradouro, Numero,
 Complemento, Bairro, Cidade, UF, CEP, DDD, Telefone, Fax, Endereco_eletronico,
 Representante, Cargo_Representante, Regiao_de_Comercializacao, Data_Registro_ANS);

-- ESTE SCRIPT É RESPONSÁVEL POR CRIAR A TABELA DEMONSTRACOES_CONTABEIS NO BANCO DE DADOS
CREATE TABLE demonstracoes_contabeis (
	id bigint NOT NULL AUTO_INCREMENT,
    DATA DATE NOT NULL,
    REG_ANS INT NOT NULL,
    CD_CONTA_CONTABIL INT NOT NULL,
    DESCRICAO VARCHAR(255) NOT NULL,
    VL_SALDO_INICIAL DECIMAL(15, 2) NOT NULL,
    VL_SALDO_FINAL DECIMAL(15, 2) NOT NULL,
    PRIMARY KEY (id)
);

-- ESTE SCRIPT É RESPONSÁVEL POR CARREGAR OS DADOS DO ARQUIVO CSV NA TABELA DEMONSTRACOES_CONTABEIS
LOAD DATA LOCAL INFILE '' 
INTO TABLE demonstracoes_contabeis
FIELDS TERMINATED BY ';'        
ENCLOSED BY '"'                
LINES TERMINATED BY '\n'       
IGNORE 1 LINES                 
(DATA, REG_ANS, CD_CONTA_CONTABIL, DESCRICAO, VL_SALDO_INICIAL, VL_SALDO_FINAL);


-- As 10 operadoras com maiores despesas em "EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR" no último trimestrea
WITH despesas AS (
    SELECT
        d.REG_ANS,
        d.VL_SALDO_FINAL
    FROM
        demonstracoes_contabeis d
    WHERE
        d.DESCRICAO LIKE '%EVENTOS/SINISTROS CONHECIDOS%' OR d.DESCRICAO LIKE '%AVISADOS DE ASSISTÊNCIA A SAÚDE MÉDICO HOSPITALAR%'
),
despesas_por_operadora AS (
    SELECT
        d.REG_ANS,
        SUM(CAST(d.VL_SALDO_FINAL AS DECIMAL(15, 2))) AS VL_SALDO_FINAL
    FROM
        despesas d
    GROUP BY
        d.REG_ANS
),
resultado AS (
    SELECT
        o.Razao_Social,
        d.VL_SALDO_FINAL
    FROM
        despesas_por_operadora d
    JOIN operadoras o ON d.REG_ANS = o.Registro_ANS
)
SELECT
    r.Razao_Social,
    r.VL_SALDO_FINAL
FROM
    resultado r
ORDER BY
    r.VL_SALDO_FINAL DESC
LIMIT 10;


-- As 10 operadoras com maiores despesas no último ano
WITH despesas_ultimo_ano AS (
    SELECT
        d.REG_ANS,
        d.VL_SALDO_FINAL
    FROM
        demonstracoes_contabeis d
    WHERE
        YEAR(d.DATA) = YEAR(CURDATE()) - 1
),
despesas_por_operadora_ano AS (
    SELECT
        d.REG_ANS,
        SUM(CAST(d.VL_SALDO_FINAL AS DECIMAL(15, 2))) AS VL_SALDO_FINAL
    FROM
        despesas_ultimo_ano d
    GROUP BY
        d.REG_ANS
),
resultado_ano AS (
    SELECT
        o.Razao_Social,
        d.VL_SALDO_FINAL
    FROM
        despesas_por_operadora_ano d
    JOIN operadoras o ON d.REG_ANS = o.Registro_ANS
)
SELECT
    r.Razao_Social,
    r.VL_SALDO_FINAL
FROM
    resultado_ano r
ORDER BY
    r.VL_SALDO_FINAL DESC
LIMIT 10;