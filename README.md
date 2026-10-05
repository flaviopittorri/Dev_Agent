# AI Course Content Builder

> **Status:** MVP de ingestão de PDFs implementado; decisões de arquitetura aguardam aprovação humana.

Projeto de uma aplicação Web para apoiar professores na criação de materiais didáticos a partir de documentos de referência e instruções fornecidas pelo professor. A especificação funcional completa está em [Prompt_Mestre_AI_Course_Content_Builder.md](Prompt_Mestre_AI_Course_Content_Builder.md).

## Escopo

O sistema deverá receber arquivos PDF, DOCX, PPTX, Markdown e Mermaid, processar e rastrear suas fontes, e permitir a geração de:

- `lesson_summary.md`, limitado a cinco páginas equivalentes;
- `lesson_slides.md`, limitado a seis slides.

Os materiais deverão poder incluir diagramas Mermaid e PlantUML, indicar fontes e distinguir conteúdo fundamentado nos documentos de conteúdo complementar gerado por IA.

Gestão de alunos, turmas, matrículas, notas, presença, progresso acadêmico e funcionalidades de LMS estão fora do escopo.

## Estrutura prevista

```text
app/
├── api/                      # Endpoints e contratos HTTP
├── config/                   # Configuração da aplicação
├── controllers/              # Coordenação das requisições
├── jobs/                     # Processamento assíncrono
├── models/                   # Entidades do domínio
├── prompts/                  # Instruções versionadas para IA
├── repositories/             # Persistência e acesso a dados
├── schemas/                  # Validação e serialização
├── services/
│   ├── documents/loaders/    # Carregadores por formato
│   ├── export/               # Exportação dos materiais
│   ├── generation/           # Geração didática
│   ├── llm/                  # Abstrações de provedores
│   ├── rag/                  # Embeddings, índice e retrieval
│   └── validation/           # Verificação e rastreabilidade
├── static/                   # CSS e JavaScript do frontend
├── templates/                # Templates HTML
├── utils/                    # Utilitários compartilhados
└── views/                    # Apresentação Web
docs/
├── adr/                      # Registros de decisões arquiteturais
├── api/                      # Documentação da API
└── architecture/             # Diagramas e visão da arquitetura
tests/
├── e2e/                      # Testes ponta a ponta
├── integration/              # Testes de integração
└── unit/                     # Testes unitários
uploads/                      # Arquivos de entrada em tempo de execução
generated/                    # Materiais gerados em tempo de execução
```

O primeiro incremento implementa somente a importação de PDF e a consulta dos registros. Os demais formatos, a geração de aulas, embeddings e integração com LLM permanecem fora deste recorte.

## Arquitetura prevista

O incremento utiliza Flask e SQLite como escolhas provisórias e substituíveis. Os arquivos PDF e textos extraídos são gravados em `generated/documents.db`, diretório local ignorado pelo Git.

## Executar

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
python run.py
```

Acesse `http://127.0.0.1:5000/`. A API oferece `POST /api/documents` (multipart com o campo `file`), `GET /api/documents` e `GET /api/documents/<id>`. O limite de PDF é 20 MiB. Defina `DATABASE_PATH` para mudar o banco e `FLASK_SECRET_KEY` antes de qualquer implantação.

Execute os testes com `python -m pytest`.

## Decisões pendentes

Antes da implementação, devem ser apresentados para aprovação humana, entre outros pontos:

- confirmação do framework Web Python e estratégia de templates;
- confirmação do banco relacional e estratégia de migrações;
- fila/worker para jobs assíncronos;
- provedor de embeddings e armazenamento vetorial;
- provedor de LLM e configuração de credenciais;
- aprovação da persistência do arquivo original no SQLite e política de retenção;
- autenticação, implantação e requisitos operacionais.

O relatório de revisão em `docs/relatorios/revisao_ingestao_pdf.md` registra as decisões provisórias, riscos e pontos que requerem orientação humana. A aprovação dessas escolhas continua pendente.

## Segurança e dados locais

Uploads e materiais gerados são dados de execução e não devem ser versionados. Credenciais devem ser fornecidas por configuração segura do ambiente, nunca adicionadas ao código ou ao Git. Documentos importados deverão ser tratados como conteúdo não confiável, inclusive contra prompt injection.

## Estado atual

- Estrutura de diretórios criada conforme a arquitetura proposta.
- Repositório Git inicializado, sem commit inicial.
- Upload, validação, extração heurística, armazenamento SQLite e dashboard para PDFs;
- API de consulta e testes unitários/de integração;
- framework e persistência ainda dependem de aprovação antes de evoluir o MVP.