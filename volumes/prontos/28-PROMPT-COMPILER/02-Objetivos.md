---
volume: "28"
volume_nome: PROMPT-COMPILER
tipo: ENGINE
secao: 02-Objetivos
status: PRONTO
atualizado_em: 2026-08-04
---

# Objetivos

Compilar apenas prompt no estado PROMOVIDO do `07-PROMPT-ENGINE` — nunca uma versão em rascunho
ou ainda em avaliação, que não passou pela barra de qualidade que o 07 exige.

Garantir que a compilação seja determinística: a mesma combinação de prompt, variáveis e dialeto
sempre produz o mesmo payload, byte a byte — dois payloads diferentes da mesma origem seriam uma
divergência impossível de rastrear.

Verificar orçamento de tokens contra o payload já compilado, nunca assumido, e falhar
explicitamente quando excedido — nunca truncar silenciosamente o conteúdo para caber.

Isolar toda lógica específica de dialeto de provedor atrás de um adaptador explícito — o núcleo do
compilador nunca contém condicional espalhado por provedor.

Nunca permitir que uma variável declarada no contrato do prompt fique sem valor no momento da
compilação — ausência de variável é erro de compilação explícito, nunca substituição silenciosa
por texto vazio ou placeholder.

Os cinco objetivos formam duas categorias: os que protegem a integridade do que é enviado ao
provedor (Q1, Q6 — só prompt validado, nunca lacuna de variável) e os que protegem o custo e a
previsibilidade da chamada (Q2, Q3 — determinismo, orçamento verificado). Isolamento de dialeto
(Q4) é o que torna os outros quatro objetivos independentes de qual provedor está em uso —
nenhuma dessas garantias deveria enfraquecer só porque o provedor mudou.