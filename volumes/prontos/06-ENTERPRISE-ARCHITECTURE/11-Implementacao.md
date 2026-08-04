---
volume: "06"
volume_nome: ENTERPRISE-ARCHITECTURE
tipo: ARQUITETURA
secao: 11-Implementacao
status: PRONTO
atualizado_em: 2026-08-04
---

# Implementação

<!-- exemplo: exemplos/06-enterprise-architecture/inventario.py -->

`inventario.py`, citado acima, formaliza E1-E6: `Sistema` exige fornecedor/modelo/fonte de dado
explícitos (E1); `Inventario.decisao_de_portfolio` só dispara quando há consequência nomeada,
nunca por reflexo (E2); `custo_total_agregado` soma por fornecedor entre todos os sistemas
registrados, não por sistema isolado (E3); `duplicacoes` detecta par de sistemas com a mesma
categoria de capacidade sem que nenhum saiba do outro (E5).

## Como o processo real aplicaria isto

A implementação mínima é um registro estruturado (uma linha por sistema, com os três campos
obrigatórios) mais uma consulta periódica que agrupa por fornecedor e por categoria de
capacidade — não é preciso ferramenta especializada de gestão de portfólio para o volume de
sistemas que a maioria das empresas tem; a mesma disciplina de texto versionado que
`04-REQUIREMENTS/11-Implementacao.md` recomenda para requisito vale aqui.

A ordem de implementação recomendada é: modelo de dado (`Sistema`, `Inventario`) primeiro,
testado contra os seis cenários de violação de regra. Consulta de concentração e duplicação
depois. Integração com `30-AI-GOVERNANCE` (sinalizar quando dependência cruza fronteira de dado
sensível) por último — este volume produz o sinal, aquele decide a política.

## Onde a integração com outros volumes acontece

O achado de duplicação (E5) é o dado que `16-INTEGRATION` consumiria para decidir se dois sistemas
deveriam se integrar em vez de duplicar capacidade — este volume identifica o par candidato,
aquele desenha o contrato técnico entre os dois, se a decisão de portfólio for consolidar.
