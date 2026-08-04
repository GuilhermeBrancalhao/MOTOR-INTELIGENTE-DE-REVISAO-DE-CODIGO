---
volume: "54"
volume_nome: INTEGRACAO-ERP
tipo: ARQUITETURA
secao: 02-Objetivos
status: RASCUNHO
atualizado_em: 2026-08-04
---

# Objetivos

**Implementados e testados hoje:**

- Normalizar o CSV nativo de qualquer banco ou fintech de comissão para o modelo `PROCESSADO`
  de 36 colunas, sem exigir mapeamento manual coluna-a-coluna por banco — a razão de existir de
  `normalizar.py`, dado que a operação real trabalha com 40+ bancos diferentes.
- Detectar automaticamente as colunas críticas (comissão, data, proposta, valor bruto, base de
  comissão, status) por padrão de nome combinado com validação de tipo e unicidade, e falhar de
  forma explícita (`ValueError`) quando uma coluna obrigatória não é encontrada — errar em
  silêncio aqui produz conciliação errada mais adiante, e é preferível travar cedo.
- Validar a transformação contra a origem antes de aceitar o resultado: soma de comissão bate,
  contagem de linha bate, proposta sem duplicata, nenhuma comissão negativa, coluna de comissão
  não pode ter ficado vazia. Nenhuma dessas checagens existia na primeira versão do script — o
  bug real que motivou cada uma está registrado em `12-Exemplos.md`.

**Apenas declarados, sem implementação:**

- Consumir a API de um ERP (SAP, Oracle, Omie, IFS) diretamente, para os casos em que ela
  existir — hoje nenhum banco de comissão trabalhado neste projeto expõe API real, então este
  objetivo permanece aspiracional até que apareça um caso concreto que precise dele.
- Conformidade regulatória automatizada (SPED, CFC, NBC-T) — fora do escopo deste volume; seria
  responsabilidade de `43-CONTABILIDADE-BASICA` e `50-COMPLIANCE-FISCAL` (removidos deste acervo
  por serem esqueleto sem conteúdo real, recuperáveis pelo histórico do git quando existir
  intenção concreta de escrevê-los).
