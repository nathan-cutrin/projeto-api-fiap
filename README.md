# API Pública de Vitivinicultura - Embrapa

Esta API tem como objetivo disponibilizar, em tempo real, os dados de vitivinicultura fornecidos pela Embrapa, incluindo informações sobre Produção, Processamento, Comercialização, Importação e Exportação.

## Objetivo Técnico

- Construir a API em Python utilizando Flask, FastAPI, Django REST ou framework equivalente.
- Realizar web scraping diretamente do site da Embrapa para obter os dados.
    - Sugestão de ferramentas: BeautifulSoup, Selenium, Scrapy, Playwright ou similar.
- Criar rotas que retornem as tabelas raspadas em formato JSON.
- Persistência de dados não é obrigatória.
    - Em caso de instabilidade do site:
        1. Tentar a raspagem ao vivo.
        2. Caso falhe, servir um arquivo CSV/JSON local previamente baixado.
- O endpoint deve sempre tentar acessar o site primeiro para validação da raspagem.

---

Mais informações e instruções de uso serão adicionadas posteriormente.