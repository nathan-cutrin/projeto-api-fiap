# Projeto API FIAP - Vitivinicultura Embrapa

API para consulta, extração e fallback de dados públicos da vitivinicultura brasileira, baseada nos dados da Embrapa Uva e Vinho.

## Descrição

Este projeto expõe uma API REST desenvolvida em FastAPI para facilitar o acesso programático aos dados de produção, processamento, comercialização, importação e exportação do setor vitivinícola brasileiro.  
Os dados são extraídos diretamente do site da Embrapa Uva e Vinho, tratados e disponibilizados em formato JSON.

A API também implementa fallback automático para dados locais caso a fonte original esteja indisponível.

---

## Instalação

Você pode instalar as dependências do projeto de duas formas:

### 1. Usando [uv](https://github.com/astral-sh/uv) (recomendado para desenvolvimento)

Crie um ambiente virtual com uv:

```sh
uv venv .venv
source .venv/bin/activate  # Linux/macOS
# ou
.venv\Scripts\activate     # Windows
```

Instale as dependências:

```sh
uv pip install -r requirements.txt
uv pip install -r requirements-dev.txt
```

### 2. Usando pip

Crie um ambiente virtual com venv:

```sh
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# ou
.venv\Scripts\activate     # Windows
```

Instale as dependências:

```sh
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

---

## Execução

### Ambiente de desenvolvimento

Execute o servidor local com:

Usando o [taskipy](https://github.com/fabioz/taskipy):

```sh
task run
```

Acesse a documentação interativa em:  
[http://localhost:8000/docs](http://localhost:8000/docs)

---

## Testes

Usando taski.py

```sh
task test
```

---

## Estrutura das Rotas

A API possui as seguintes rotas principais:

- **Produção**
    - `GET /producao/{ano}`  
        Retorna dados de produção vitivinícola por ano.

- **Processamento**
    - `GET /processamento/{sub_aba}/{ano}`  
        Retorna dados de processamento de uvas e derivados.  
        O parâmetro `sub_aba` define o tipo de uva/processamento (ex: `viniferas`, `americanas`, `semclassificacao`).

- **Comercialização**
    - `GET /comercializacao/{ano}`  
        Retorna dados de comercialização de uvas, vinhos e derivados.

- **Importação**
    - `GET /importacao/{sub_aba}/{ano}`  
        Retorna dados de importação de derivados de uva.

- **Exportação**
    - `GET /exportacao/{sub_aba}/{ano}`  
        Retorna dados de exportação de derivados de uva.

---

## Observações

- Todas as rotas retornam dados em formato JSON.
- Em caso de falha na extração dos dados online, a API retorna dados de fallback local e adiciona o header `X-Fallback: true` na resposta.
- O projeto segue o padrão PEP8 e utiliza o Ruff para lint/format.

---

## Dependências principais

Veja os arquivos [`requirements.txt`](requirements.txt) e [`requirements-dev.txt`](requirements-dev.txt) para detalhes.

