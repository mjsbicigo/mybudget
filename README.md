# MyBudget Applications - Continuous Integration (CI)

Este repositório contém o código-fonte das aplicações utilizadas no meu projeto de TCC, incluindo as configurações de CI. Ele é responsável pelo processo de **Integração Contínua** (CI) das aplicações de frontend e backend-api, assim como pelos testes e construção das imagens Docker dessas aplicações.

## Estrutura do Repositório

- `backend-api/` - Código-fonte e `Dockerfile` do backend, construído com Python e biblioteca [FastAPI](https://fastapi.tiangolo.com/).
- `frontend/` - Código-fonte e `Dockerfile` do frontend, construído com Python e as bibliotecas [Flask](https://flask.palletsprojects.com/en/stable/), [Dash](https://dash.plotly.com/), [Plotly](https://plotly.com/python/) e [Pandas](https://pandas.pydata.org/).
- `.github/workflows/` - Pipeline de CI para automação do processo de construção e testes.

## Pipeline de CI

O pipeline de CI foi configurado com **GitHub Actions** para garantir a qualidade e integridade das aplicações. A cada alteração feita no código, o pipeline executa as seguintes etapas:
1. **Execução de Testes**: Testes automatizados de unidade para verificar o funcionamento do frontend e backend.
2. **Build das Imagens Docker**: Construção das imagens Docker das aplicações.
3. **Push para Docker Hub**: Publicação das imagens no repositório Docker Hub para disponibilizar as imagens para o processo de deploy.

## Como Contribuir

Para contribuir com melhorias no código ou nos workflows, faça um fork deste repositório, realize as alterações desejadas e envie um pull request.

## Contato

Qualquer dúvida ou sugestão, entre em contato pelo e-mail: [marciosbicigo@alunos.fho.edu.br](mailto:marciosbicigo@alunos.fho.edu.br).
