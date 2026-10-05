# ADR 0001: armazenamento provisório de PDFs

- **Status:** provisório; aprovação humana pendente.
- **Contexto:** o incremento precisa armazenar arquivos importados para processamento didático futuro, mas a arquitetura e a política de retenção não foram aprovadas.
- **Decisão provisória:** usar SQLite local em `generated/documents.db` e armazenar PDF original, texto extraído e metadados no mesmo registro.
- **Alternativas:** armazenamento em diretório com metadados relacionais; banco relacional de servidor; armazenamento de objetos.
- **Justificativa:** reduz infraestrutura e mantém a prova de conceito reversível, com transação única para fonte e texto.
- **Consequências:** o banco contém material potencialmente sensível; não há exclusão, backup, criptografia em repouso ou política de retenção. SQLite local não foi validado para concorrência ou implantação distribuída.
- **Pergunta ao responsável:** aprova SQLite local para o MVP e o armazenamento do PDF original no banco? Qual política de retenção e proteção deve ser adotada antes de uso com documentos reais?