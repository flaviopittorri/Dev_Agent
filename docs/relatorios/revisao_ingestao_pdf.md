# Relatório de revisão: ingestão de PDF

## Resultado

Implementado um recorte executável de upload PDF, extração textual, persistência local e consulta por dashboard/API. O PDF original e o texto extraído são armazenados em `generated/documents.db`, que permanece fora do Git.

## Revisão crítica e classificação

| Classificação | Local | Apontamento e justificativa |
|---|---|---|
| Alta | `app/__init__.py` e `app/repositories/document_repository.py` | Flask e SQLite foram introduzidos sem aprovação arquitetural. São escolhas provisórias reversíveis, mas não devem ser tratadas como decisão de produção. |
| Alta | `app/repositories/document_repository.py` | PDF original e texto extraído ficam sem criptografia, retenção ou exclusão. Não importar documentos reais sensíveis até aprovar controles e ciclo de vida. |
| Média | `app/services/documents/loaders/pdf_loader.py` | Assunto e resumo são heurísticas baseadas nas primeiras linhas, não resumo didático nem saída de LLM. PDFs digitalizados sem camada de texto não recebem OCR. |
| Média | `app/controllers/document_controller.py` | Upload tem limite e extensão validada, mas não há autenticação, autorização, proteção CSRF ou rate limiting. O MVP deve permanecer em ambiente local/confiável. |
| Baixa | `tests/integration/test_document_upload.py` e `tests/unit/test_pdf_loader.py` | A integração HTTP/persistência usa um leitor controlado. O parser real é validado com PDF válido gerado em memória, mas ainda faltam PDFs reais variados e extração textual de camadas de texto complexas. |

## Decisões humanas pendentes

```text
HUMAN_DECISION_REQUIRED

Assunto: framework web e persistência do MVP
Contexto: Flask e SQLite local foram escolhidos para viabilizar este recorte, mas o projeto original deixou ambos em aberto.
Recomendação: validar Flask e SQLite apenas para desenvolvimento local; decidir banco, migrações e implantação antes de produção.
Pergunta: aprova Flask e SQLite para o MVP ou prefere outra combinação?

Assunto: armazenamento e retenção das fontes
Contexto: cada registro retém o PDF original e texto extraído no banco local, sem criptografia ou exclusão implementadas.
Recomendação: definir acesso, retenção, remoção e proteção em repouso antes de importar documentos reais.
Pergunta: qual política de retenção e proteção deve ser implementada?
```

## Limites deste incremento

- Apenas `.pdf`; DOCX, PPTX, Markdown e Mermaid ainda não são processados.
- Sem OCR, embeddings, geração por IA, resumo pedagógico, exportação de aulas ou workers assíncronos.
- Não há paginação na interface; a API e o dashboard mostram no máximo 50 registros recentes.
- A chave Flask padrão é apenas local; configure `FLASK_SECRET_KEY` no ambiente.

## Validação

Execute `python -m pytest`. Os testes cobrem extração e contagens, PDFs vazios, malformados ou protegidos, upload HTTP, validações de extensão/tamanho, persistência do original/texto e renderização do dashboard.