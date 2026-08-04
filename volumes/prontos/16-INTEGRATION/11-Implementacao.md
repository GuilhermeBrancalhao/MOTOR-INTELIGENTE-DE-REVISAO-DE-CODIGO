---
volume: "16"
volume_nome: INTEGRATION
tipo: ARQUITETURA
secao: 11-Implementacao
status: PRONTO
atualizado_em: 2026-08-04
---

# Implementação

<!-- exemplo: exemplos/16-integration/gateway.py -->

`gateway.py`, citado acima, formaliza I1-I4 e I6: `verificar_versao` rejeita `major`
incompatível (I1); `ChamadaIdempotente` garante que a mesma chave nunca dispara efeito duplicado
(I2); `PoliticaDeRetry` é obrigatória por chamada, sem padrão implícito (I3); `CircuitBreaker`
isola falha externa, parando de tentar depois do limiar de falhas consecutivas (I4).

## Como o motor real aplicaria isto

A implementação mínima separa claramente três preocupações que é tentador misturar num único
cliente HTTP genérico: verificação de contrato (o que a resposta deveria conter), idempotência
(o que garante que repetir não duplica), e proteção de circuito (o que decide se vale a pena
tentar). Misturar as três numa única função dificulta testar cada uma isoladamente e tende a
produzir integração onde uma falha de configuração numa preocupação mascara as outras duas.

## Onde a integração com outros volumes acontece

Uma integração especificamente com provedor de modelo de linguagem usaria este volume como base
de robustez de chamada, com `27-LLM-ROUTER` decidindo qual provedor específico chamar em cada
momento — este volume garante que qualquer chamada, uma vez decidido o destino, é robusta a
falha, versão incompatível e retry duplicado.

## Onde a integração com outros volumes acontece

Uma implementação real conectaria este gateway a `21-OBSERVABILITY` para que abertura de
circuito, falha de versão e taxa de idempotência virem sinais monitorados — este volume produz
os eventos (falha, sucesso, abertura de circuito), mas não define como eles são instrumentados
para alerta, que é responsabilidade daquele volume.
