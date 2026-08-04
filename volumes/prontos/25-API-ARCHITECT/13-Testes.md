---
volume: "25"
volume_nome: API-ARCHITECT
tipo: ARQUITETURA
secao: 13-Testes
status: PRONTO
atualizado_em: 2026-08-04
---

# Testes

A mutação alvo de cada teste é nomeada no docstring.

`test_campo_com_tipo_diferente_na_mesma_versao_e_rejeitado` prova T1/T5: a mutação alvo é aceitar
a redeclaração de tipo diferente sem levantar exceção.

`test_campo_com_mesmo_tipo_pode_ser_redeclarado` prova o caso negativo correspondente — sem ele,
a suíte provaria apenas que mudança é rejeitada, não que redeclaração legítima continua
funcionando.

`test_traducao_nunca_expoe_campo_nao_permitido` prova T2: confirma que campos de controle interno
presentes no registro de origem não aparecem na resposta traduzida.

`test_erro_de_diferentes_origens_tem_mesmo_formato` prova T3: duas chamadas de `formatar_erro`
com códigos e mensagens diferentes produzem instâncias do mesmo tipo `ErroDeAPI`, com os mesmos
campos disponíveis.

`test_status_de_trabalho_e_recurso_consultavel_em_qualquer_estado` prova T4: confirma que
diferentes estados de trabalho produzem recursos de status com a mesma estrutura consultável.

`test_endpoint_sincrono_sem_orcamento_de_latencia_e_rejeitado` prova T6: a mutação alvo é aceitar
`limite_ms=None` sem levantar exceção.


Nenhum teste depende de um servidor HTTP real ou de biblioteca de framework web específica — todo
o exemplo opera sobre estruturas de dado Python puras, o que permite verificar as seis regras de
contrato independente de qual tecnologia de API é usada na implementação real.

`test_erro_de_diferentes_origens_tem_mesmo_formato` compara `type()` e o conjunto de atributos das
duas instâncias, não apenas seus valores — a mutação que esse teste mata é a introdução de um
segundo tipo de erro paralelo com campos diferentes, que poderia coincidentemente ter valores
plausíveis mas ainda assim quebrar a consistência estrutural que T3 exige.