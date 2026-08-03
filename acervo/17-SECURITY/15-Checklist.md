---
volume: "17"
volume_nome: SECURITY
tipo: GOVERNANCA
secao: 15-Checklist
status: RASCUNHO
atualizado_em: 2026-08-03
---

# Checklist

Antes de considerar a política de segurança de um sistema com IA madura para produção. Nenhum
item vem marcado: quem verifica marca cada um com evidência à mão — um teste que roda, um vetor
concreto documentado — e item que não pode ser marcado é o que falta, não detalhe a contornar.

- [ ] Toda ação de risco não comprovadamente inócua trava ou é rastreada — nenhuma exceção por
      conveniência de desenvolvimento.
- [ ] Dado de origem `Processado` nunca é indistinguível de instrução do operador no momento da
      decisão de ação de alto risco.
- [ ] Toda chamada de ferramenta com efeito de saída de dado é auditada contra lista de destinos
      autorizados.
- [ ] Comando de shell, especificamente, nunca é classificado como execução livre.
- [ ] O próprio mecanismo de segurança (arquivo de configuração, estado do classificador) está
      sob a mesma política de proteção que qualquer outra ação de alto risco.
- [ ] Cada família de controle tem vetor concreto documentado, não só a regra abstrata.
- [ ] Existe teste estrutural que trava a política contra reintrodução acidental de exceção
      (equivalente a `test_nenhum_comando_de_shell_e_livre`).
- [ ] Processo de verificação contínua no pipeline (CI/CD) — descrito em `18-DEVSECOPS`, fora do
      contrato mínimo deste volume, que define a política, não o processo de execução contínua.

O último item aponta para `18-DEVSECOPS` de propósito, não é lacuna deste volume — é a fronteira
declarada em `03-Escopo.md`.
