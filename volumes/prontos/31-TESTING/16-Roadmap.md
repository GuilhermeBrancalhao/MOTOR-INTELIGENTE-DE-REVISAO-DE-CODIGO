---
volume: "31"
volume_nome: TESTING
tipo: PROCESSO
secao: 16-Roadmap
status: PRONTO
atualizado_em: 2026-07-30
---

# Roadmap

1. **Teste de propriedade (property-based testing).** Uma técnica real e útil,
   especialmente para `validador_cpf` (gerar entradas aleatórias e verificar invariante
   em vez de listar casos), mas a biblioteca de referência do ecossistema Python
   (Hypothesis) é dependência externa, e os exemplos desta plataforma seguem a mesma
   restrição de `ferramentas/`: biblioteca padrão apenas. Entra se essa restrição for
   revisada para `exemplos/` especificamente -- não antes, porque relaxar a regra
   silenciosamente por um volume só criaria inconsistência entre exemplos do acervo.
2. **Integração com pipeline de CI real.** `ROADMAP.md` da plataforma já registra
   "integração contínua rodando os gates a cada push" como fora do ciclo atual. Quando
   esse item avançar, este volume ganha um exemplo concreto de configuração de
   pipeline aplicada aos próprios três módulos, coisa que hoje só existe em prosa.
3. **Teste de concorrência.** Nenhum dos três módulos promete segurança de thread; testar
   concorrência sobre um componente que não a promete produziria uma garantia que o
   código não sustenta. Entra apenas se um módulo futuro do acervo declarar
   explicitamente essa propriedade.
4. **Teste de mutação como auditoria da própria suíte.** Rodar um mutador sobre
   `validador_cpf.py` e confirmar que a suíte mata as mutações é uma forma de validar
   que os testes verificam comportamento, não só executam linha. Não entra agora pelo
   mesmo motivo do item 1 -- ferramenta externa, fora da restrição de biblioteca padrão.
5. **Ligação formal com a seção de testes de `07-PROMPT-ENGINE`.** Aquele volume já tem
   `13-Testes.md` próprio, específico para avaliação de prompt por caso de ouro.
   `18-Referencias-Cruzadas.md` já aponta a fronteira; falta, em um ciclo futuro, uma
   frase em cada um dos dois volumes remetendo explicitamente ao outro para quem chega
   por um e precisa do outro.
