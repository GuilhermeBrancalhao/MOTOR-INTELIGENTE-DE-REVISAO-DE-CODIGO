---
volume: "22"
volume_nome: FRONTEND-ARCHITECT
tipo: ARQUITETURA
secao: 15-Checklist
status: PRONTO
atualizado_em: 2026-08-04
---

# Checklist

- [ ] Todo elemento dependente de IA tem estado de carregamento visualmente distinto do
  carregamento genérico.
- [ ] Resposta em stream é renderizada incrementalmente, nunca em buffer completo.
- [ ] Toda falha de ação de IA é visível; fallback para dado anterior é sempre sinalizado.
- [ ] Resposta de IA permanece no escopo do componente, salvo promoção explícita e justificada.
- [ ] Requisição abandonada é cancelada; fragmento tardio é descartado.
- [ ] Nenhum componente consome o formato bruto de resposta do provedor diretamente.
- [ ] A camada de adaptação de resposta é coberta por teste sempre que um formato novo é
  adicionado.


- [ ] Nenhum teste automatizado cobre apenas o caminho de sucesso, ignorando cancelamento.
- [ ] Toda transição de estado passa por um método nomeado, nunca por atribuição direta ao campo
  de estado.
