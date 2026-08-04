---
volume: "41"
volume_nome: SDK
tipo: ENGINE
secao: 15-Checklist
status: RASCUNHO
atualizado_em: 2026-08-04
---

# Checklist

- [ ] Toda mudança que quebra compatibilidade está versionada como versão maior nova.
- [ ] Todo elemento público tem justificativa explícita para ser público.
- [ ] Todo erro do SDK carrega orientação de correção, não apenas descrição do que falhou.
- [ ] Código escrito contra versão menor antiga continua funcionando na versão menor mais
  recente da mesma versão maior.
- [ ] Nenhum elemento público foi removido sem ciclo de depreciação prévio.
- [ ] Todo exemplo de documentação é executado como parte da suíte de teste automatizada.

- [ ] Nenhum elemento público foi removido na mesma versão em que foi marcado como depreciado.
- [ ] O changelog de superfície pública está atualizado com a mudança desta versão.