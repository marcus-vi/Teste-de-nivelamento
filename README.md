# Teste de Nivelamento

Este projeto consiste em uma aplicação web para busca e manipulação de dados de operadoras de saúde. Ele utiliza um backend em Python com FastAPI, um frontend em Vue.js, scripts auxiliares para manipulação de dados e web scraping, e scripts SQL para criação e manipulação de tabelas no banco de dados.

---

## Estrutura do Projeto

- **Backend**: Implementado com FastAPI, responsável por fornecer as APIs para busca e manipulação de dados.
- **Frontend**: Desenvolvido com Vue.js, fornece a interface para interação com o usuário.
- **Scripts**: Scripts em Python para tarefas de transformação de dados e web scraping.
- **SQL**: Scripts SQL para criação de tabelas e consultas no banco de dados.
- **Banco de Dados**: Os dados são carregados a partir de um arquivo CSV (`relatorio_cadop.csv`).

---

## Funcionalidades

### Backend (FastAPI)

1. **Buscar Operadoras**:
   - Rota: `GET /buscar-operadoras/`
   - Descrição: Realiza uma busca textual nas operadoras.
   - Parâmetro: `query` (texto para busca).

---

### Frontend (Vue.js)

1. **Busca de Operadoras**:

   - Componente: `Search.vue`
   - Permite buscar operadoras com base em um texto.

---

### Scripts

1. **Web Scraping**:

   - Arquivo: `scripts/web_scraping.py`
   - Descrição: Realiza o download de arquivos PDF do site da ANS e os compacta em um arquivo ZIP.
   - Bibliotecas utilizadas:
     - `selenium`
     - `urllib.request`
     - `zipfile`

2. **Transformação de Dados**:
   - Arquivo: `scripts/transformacao.py`
   - Descrição: Processa arquivos PDF, extrai tabelas e salva os dados em um arquivo CSV compactado em ZIP.
   - Bibliotecas utilizadas:
     - `pandas`
     - `fitz` (PyMuPDF)
     - `tabula`
     - `zipfile`

---

### SQL

1. **Criação de Tabelas**:

   - Arquivo: `sql/schema.sql`
   - Descrição: Contém os comandos para criar as tabelas `operadoras` e `demonstracoes_contabeis` no banco de dados.

2. **Consultas SQL**:
   - Arquivo: `sql/queries.sql`
   - Descrição: Contém consultas SQL para análise de dados, como:
     - Listar as 10 operadoras com maiores despesas no ultimo trimestre.
     - Listar as 10 operadoras com maiores despesas no último ano.

---

## Tecnologias Utilizadas

### Backend

- **[FastAPI](https://fastapi.tiangolo.com/)**: Framework para construção de APIs rápidas e eficientes.
- **Pandas**: Manipulação e análise de dados.
- **Uvicorn**: Servidor ASGI para rodar o FastAPI.
- **CORS Middleware**: Para permitir requisições do frontend.

### Frontend

- **[Vue.js](https://vuejs.org/)**: Framework JavaScript para construção de interfaces web.
- **Axios**: Biblioteca para realizar requisições HTTP.

### Scripts

- **Selenium**: Automação de navegadores para web scraping.
- **PyMuPDF (fitz)**: Extração de texto de arquivos PDF.
- **Tabula**: Extração de tabelas de arquivos PDF.
- **Zipfile**: Manipulação de arquivos ZIP.

### SQL

- **MySQL**: Banco de dados relacional para armazenamento e consulta de dados.

---

## Requisitos

### Backend

- Python 3.9+
- Bibliotecas Python:
  - `fastapi`
  - `uvicorn`
  - `pandas`

### Frontend

- Node.js 16+
- Gerenciador de pacotes `npm` ou `yarn`

### Scripts

- Bibliotecas Python:
  - `selenium`
  - `urllib3`
  - `fitz` (PyMuPDF)
  - `tabula-py`
  - `pandas`

### SQL

- MySQL instalado e configurado.

---

## Como Executar

### Backend

1. Instale as dependências:
   ```bash
   pip install fastapi uvicorn pandas
   ```
2. Certifique-se de que o arquivo `relatorio_cadop.csv` está no diretório `downloads/`.
3. Inicie o servidor:
   ```bash
   uvicorn main:app --reload
   ```
4. O backend estará disponível em `http://localhost:8000`.

### Frontend

1. Navegue até o diretório `frontend`.
2. Instale as dependências:
   ```bash
   npm install
   ```
3. Inicie o servidor de desenvolvimento:
   ```bash
   npm run dev
   ```
4. Acesse a interface em `http://localhost:5173`.

### Scripts

1. **Web Scraping**:

   - Execute o script `web_scraping.py` para baixar e compactar os arquivos PDF:
     ```bash
     python scripts/web_scraping.py
     ```

2. **Transformação de Dados**:
   - Execute o script `transformacao.py` para processar os PDFs e gerar o CSV:
     ```bash
     python scripts/transformacao.py
     ```

### SQL

1. **Criação de Tabelas**:

 **Consultas SQL**:
   - Execute o script `queries.sql` no MySQL para realizar as consultas e para criar as tabelas:
     ```sql
     SOURCE sql/queries.sql;
     ```

---

## Estrutura de Diretórios

```
finish/
├── api/
│   └── main.py          # Backend FastAPI
├── frontend/
│   ├── src/
│   │   ├── App.vue      # Componente principal
│   │   ├── components/
│   │   │   ├── Search.vue           # Busca de operadoras
│   │   │   ├── ListOperators.vue    # Listar operadoras
│   │   │   └── FindByRegistroANS.vue # Buscar por Registro ANS
├── scripts/
│   ├── web_scraping.py  # Script de web scraping
│   └── transformacao.py # Script de transformação de dados
├── sql/
│   ├── schema.sql       # Criação de tabelas no banco de dados
│   └── queries.sql      # Consultas SQL para análise de dados
├── downloads/
│   └── relatorio_cadop.csv # Arquivo CSV com os dados
└── README.md              # Documentação do projeto
```

---

## Observações

- Certifique-se de que o arquivo `relatorio_cadop.csv` está no local correto antes de iniciar o backend.
- O frontend e o backend devem estar rodando simultaneamente para que a aplicação funcione corretamente.
- Os scripts SQL devem ser executados em um banco de dados MySQL ou MariaDB configurado.
- Os scripts Python devem ser executados separadamente para realizar tarefas específicas.
