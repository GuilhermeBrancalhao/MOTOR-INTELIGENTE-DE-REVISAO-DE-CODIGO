---
volume: "28"
volume_nome: PROMPT-COMPILER
tipo: ENGINE
secao: 15-Checklist
status: PRONTO
atualizado_em: 2026-08-04
---

# Checklist

- [ ] Nenhum prompt fora do estado PROMOVIDO é compilado para uso real.
- [ ] Toda variável declarada no contrato do prompt é fornecida antes da renderização.
- [ ] Orçamento de tokens é verificado contra o payload já compilado, nunca assumido.
- [ ] Nenhuma lógica de dialeto de provedor está espalhada fora do adaptador correspondente.
- [ ] Todo ponto de cache está em conteúdo estável entre chamadas, nunca em variável dinâmica.
- [ ] O `hash_origem` de todo payload compilado é registrado junto do log de chamada.


- [ ] Nenhum caminho de código produz PayloadCompilado sem passar pelas quatro verificações em
  sequência.
- [ ] O adaptador de dialeto está versionado junto do formato de provedor que produz.
