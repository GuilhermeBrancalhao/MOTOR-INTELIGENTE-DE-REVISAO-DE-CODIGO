---
volume: "06"
volume_nome: ENTERPRISE-ARCHITECTURE
tipo: ARQUITETURA
secao: 12-Exemplos
status: PRONTO
atualizado_em: 2026-08-04
---

# Exemplos

## Caso 1 — três projetos, mesmo fornecedor, sinalização correta

Três projetos diferentes registram, ao longo de seis meses, dependência do mesmo provedor de
modelo de linguagem. O terceiro registro dispara sinalização de concentração para o arquiteto de
portfólio, que revisa e decide: a concentração é aceitável porque o volume agregado já garante
desconto contratual — decisão de portfólio registrada, nenhum dos três projetos precisou mudar.

## Caso 2 — decisão de portfólio vetando escolha de projeto

Um quarto projeto propõe usar um fornecedor diferente dos três anteriores, especificamente para
processar dado classificado como sensível pela política de governança. O inventário sinaliza que
essa fonte de dado nunca cruzou fronteira de fornecedor externo antes — o arquiteto de portfólio,
em conjunto com `30-AI-GOVERNANCE`, veta a escolha e exige fornecedor já homologado para esse tipo
de dado. Este é o caso concreto de E2: consequência nomeável (fronteira de governança de dado)
justificando decisão de portfólio sobre escolha de projeto.

## Caso 3 — duplicação descoberta tarde

Dois times, sem visibilidade um do outro, constroem pipelines de recuperação de conhecimento
funcionalmente equivalentes ao longo do mesmo trimestre. Nenhum dos dois registrou a categoria de
capacidade no inventário de forma que permitisse comparação — só quando um terceiro projeto
consulta o inventário buscando exemplo de pipeline existente, a duplicação aparece. O achado vira
decisão de portfólio (consolidar os dois em um serviço compartilhado), mas seis meses depois do
ponto em que registro correto teria revelado a duplicação de imediato.
