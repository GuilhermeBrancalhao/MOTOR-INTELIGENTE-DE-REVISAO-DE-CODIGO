---
volume: "28"
volume_nome: PROMPT-COMPILER
tipo: ENGINE
secao: 09-Boas-Praticas
status: PRONTO
atualizado_em: 2026-08-04
---

# Boas Práticas

Testar cada adaptador de dialeto isoladamente contra um conjunto fixo de prompts de referência,
antes de usá-lo em compilação real — um adaptador com bug de formatação afeta toda chamada que o
usa, silenciosamente, até alguém notar resposta malformada do provedor.

Registrar o `hash_origem` de todo payload compilado em log de chamada, não apenas o payload em
si — a rastreabilidade até o prompt exato que produziu uma chamada específica é o que torna
possível diagnosticar comportamento inesperado depois.

Calcular orçamento de tokens com margem de segurança, não no limite exato do que o provedor
aceita — a estimativa de token de um compilador é aproximada; uma margem evita que uma pequena
imprecisão de contagem vire rejeição do provedor.

Revisar posição de ponto de cache sempre que o corpo do prompt mudar de versão — uma posição que
fazia sentido para uma versão anterior pode não fazer mais sentido depois de reestruturação do
corpo.


Versionar o adaptador de dialeto junto do formato que ele produz, para que uma mudança na API do
provedor não exija adivinhar qual parte do sistema precisa de ajuste correspondente.

Manter os dois artefatos versionados juntos evita a situação em que o formato mudou mas ninguém lembrou de atualizar o adaptador correspondente.