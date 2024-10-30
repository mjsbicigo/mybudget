# MyBudget - Continuous Integration (CI)

Este repositório contém o código-fonte das aplicações utilizadas no meu projeto de TCC, incluindo as configurações de CI. Ele é responsável pelo processo de **Integração Contínua** (CI) das aplicações de frontend e backend-api, assim como pelos testes e construção das imagens Docker dessas aplicações.

## Sobre a Aplicação - MyBudget

### Requisitos

- **MongoDB**
- **Redis**

### Front-end

O frontend é um dashboard de gerenciamento financeiro, desenvolvido em Python e projetado para rodar em um cenário de microsserviços. Com funcionalidades de controle de gastos, a aplicação oferece uma interface com gráficos e ferramentas para visualização financeira. Suas principais funcionalidades incluem:

- **Tela de Cadastro e Login**: Permite que o usuário se autentique e acesse o dashboard pessoal.
- **Inserção de Receitas e Despesas**: Permite inserir receitas e despesas.
- **Tabelasde Extratos**: Permite visualiazr um extrato de receitas e despesas.
- **Dashboard com Gráficos**: O usuário pode visualizar seu controle de gastos através de gráficos com busca por período.

### Back-end
O backend-api é uma API que faz a ponte entre o Dashboard e os bancos de dados MongoDB e Redis, necessários para a correta execução do ambiente completo. Suas principais funcionalidades incluem:

- **Controle de sessões**: A API se conecta ao Redis para adicionar, remover ou validar sessões.
- **CRUD com Banco de Dados**: A API também faz a ponte entre o frontend e o Servidor MongoDB, que armazena os databases de usuários cadastrados bem como logs em geral das transações.

## Estrutura do Repositório

- `backend-api/` - Código-fonte e `Dockerfile` do backend, construído com Python e biblioteca [FastAPI](https://fastapi.tiangolo.com/).
- `frontend/` - Código-fonte e `Dockerfile` do frontend, construído com Python e as bibliotecas [Flask](https://flask.palletsprojects.com/en/stable/), [Dash](https://dash.plotly.com/), [Plotly](https://plotly.com/python/) e [Pandas](https://pandas.pydata.org/).
- `.github/workflows/` - Pipeline de CI para automação do processo de construção e testes.

## Pipeline de CI

O pipeline de CI foi configurado com **GitHub Actions** para garantir a qualidade e integridade das aplicações. A cada alteração feita no código, o pipeline executa as seguintes etapas:
1. **Execução de Testes**: Testes automatizados de unidade para verificar o funcionamento do frontend e backend.
2. **Build das Imagens Docker**: Construção das imagens Docker das aplicações.
3. **Push para Docker Hub**: Publicação das imagens no repositório Docker Hub para disponibilizar as imagens para o processo de deploy.

## Deploy da Aplicação

Para este projeto de TCC, o deploy foi realizado em um cluster Kubernetes local, por meio de um ApplicationSet configurado no Argo CD. Mais detalhes no repositório [tcc-deploy-argocd](https://github.com/mjsbicigo/tcc-deploy-argocd).

## Como Contribuir

Para contribuir com melhorias no código ou nos workflows, faça um fork deste repositório, realize as alterações desejadas e envie um pull request.

## Contato

Qualquer dúvida ou sugestão, entre em contato pelo e-mail: [marciosbicigo@alunos.fho.edu.br](mailto:marciosbicigo@alunos.fho.edu.br).
