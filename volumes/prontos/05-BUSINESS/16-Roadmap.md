---
volume: "05"
volume_nome: BUSINESS
tipo: PROCESSO
secao: 16-Roadmap
status: PRONTO
atualizado_em: 2026-08-04
---

# Roadmap

## O que este volume ainda não cobre

Hierarquia formal entre stakeholders com autoridade quando a discordância não se resolve por
escalonamento simples (por exemplo, dois patrocinadores de mesmo nível hierárquico, sem terceiro
com autoridade sobre os dois) — hoje o processo registra a discordância e força decisão, mas não
prescreve mecanismo de desempate quando não existe hierarquia natural.

Revalidação de objetivo quando o projeto muda de fase significativamente (de descoberta para
entrega, por exemplo) — o volume menciona a prática em `09-Boas-Praticas.md`, mas não define
gatilho formal de quando a revalidação é obrigatória versus opcional.

Integração formal com `38-PROJECT-PLANNER` — este volume produz o objetivo validado que
alimentaria o planejamento de entrega, mas a interface entre os dois (que campo do objetivo vira
que campo do plano) ainda não está especificada.

## Ordem de cobertura pretendida

Primeiro, extrair o processo de captura como código de referência mínimo (modelo de dado +
validação), testado por mutação nas seis regras. Depois, a integração real com `03-DISCOVERY` e
`04-REQUIREMENTS`, verificando que o objetivo validado por este processo chega íntegro como
entrada dos outros dois.

## O que este volume assume que pode mudar

A tríade decide/consultado/informado é o modelo mínimo suficiente para a maioria dos projetos —
um projeto com estrutura de governança mais complexa (comitê de decisão colegiada, por exemplo)
pode exigir uma quarta categoria, mas isso não foi observado como necessário na prática que
motivou este volume.
