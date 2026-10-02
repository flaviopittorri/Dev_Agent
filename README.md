# AI Course Content Builder

> **Status:** estrutura inicial. Este repositório ainda não contém aplicação executável.

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

Os diretórios estão vazios intencionalmente. Os arquivos `.gitkeep` apenas permitem que essa estrutura seja versionada.

## Arquitetura prevista

O prompt define um monólito modular Python com separação MVC e serviços, frontend HTML, processamento assíncrono e abstrações substituíveis para loaders de documentos, provedores de LLM e armazenamento vetorial. Nenhum framework, banco de dados, provedor de IA ou dependência foi selecionado nesta etapa.

## Decisões pendentes

Antes da implementação, devem ser apresentados para aprovação humana, entre outros pontos:

- framework Web Python e estratégia de templates;
- banco relacional e estratégia de migrações;
- fila/worker para jobs assíncronos;
- provedor de embeddings e armazenamento vetorial;
- provedor de LLM e configuração de credenciais;
- armazenamento dos documentos e política de retenção;
- autenticação, implantação e requisitos operacionais.

Essas decisões não foram tomadas ao criar o esqueleto. O próximo passo do projeto deve seguir as fases de análise, proposta técnica, diagramas, plano de implementação e aprovação descritas no prompt mestre.

## Segurança e dados locais

Uploads e materiais gerados são dados de execução e não devem ser versionados. Credenciais devem ser fornecidas por configuração segura do ambiente, nunca adicionadas ao código ou ao Git. Documentos importados deverão ser tratados como conteúdo não confiável, inclusive contra prompt injection.

## Estado atual

- Estrutura de diretórios criada conforme a arquitetura proposta.
- Repositório Git inicializado, sem commit inicial.
- Sem implementação, dependências, comandos de execução ou testes nesta etapa.
- Framework e demais escolhas estruturais aguardam aprovação.