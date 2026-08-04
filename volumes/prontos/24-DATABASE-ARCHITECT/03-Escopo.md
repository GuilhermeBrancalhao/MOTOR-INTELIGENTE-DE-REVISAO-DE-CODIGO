---
volume: "24"
volume_nome: DATABASE-ARCHITECT
tipo: ARQUITETURA
secao: 03-Escopo
status: PRONTO
atualizado_em: 2026-08-04
---

# Escopo

Este volume cobre a camada de persistência estruturada dentro do mesmo produto: evolução de
schema, proveniência de conteúdo gerado por IA, controle de concorrência, retenção, e
compatibilidade de leitura.

**Fronteira com `14-VECTOR`.** Índice vetorial, embedding e métrica de similaridade são daquele
volume. Este volume trata de persistência de registro estruturado — o mesmo produto pode usar os
dois lado a lado, cada um sob sua própria disciplina.

**Fronteira com `23-BACKEND-ARCHITECT`.** A decisão de quando e o quê gravar — a orquestração que
processa um trabalho e decide persistir seu resultado — é daquele volume. Este volume trata de
como a gravação em si preserva schema, proveniência e consistência, independente de qual lógica
de negócio decidiu fazer a escrita.

**Fronteira com `25-API-ARCHITECT`.** O formato exposto ao cliente através de um endpoint é
daquele volume, e pode divergir intencionalmente do formato de persistência interno — este volume
não assume que o schema de banco e o contrato de API são a mesma coisa.

Não cobre escolha de tecnologia de banco específica (relacional, documento, coluna larga) — os
princípios deste volume (migração compatível, proveniência, concorrência, retenção, leitura
tolerante) valem independentemente da tecnologia escolhida para implementá-los.


A decisão de não cobrir escolha de tecnologia específica é deliberada: um produto real pode
combinar banco relacional, documento e índice vetorial ao mesmo tempo, cada peça sob sua
tecnologia mais adequada — as seis regras deste volume deveriam se aplicar igualmente a qualquer
combinação escolhida, sem favorecer nenhuma tecnologia particular como pré-requisito.