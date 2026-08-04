---
volume: "42"
volume_nome: PLUGINS
tipo: ENGINE
secao: 15-Checklist
status: RASCUNHO
atualizado_em: 2026-08-04
---

# Checklist

- [ ] Todo plugin ativado passou pela verificação de compatibilidade de contrato antes do
  primeiro hook ser chamado.
- [ ] Toda chamada de hook de plugin passa por isolamento de falha explícito.
- [ ] Toda capacidade usada por um plugin está declarada em sua ativação.
- [ ] Nenhum plugin foi ativado por execução implícita de código encontrado em caminho de busca.
- [ ] Toda desativação de plugin libera recurso associado, sem resíduo.
- [ ] Mudança que quebra hook existente está versionada como versão maior nova do contrato.

- [ ] O contrato do host expõe changelog de mudança de hook por versão maior.
- [ ] Toda reativação de plugin repete a verificação de compatibilidade de contrato.