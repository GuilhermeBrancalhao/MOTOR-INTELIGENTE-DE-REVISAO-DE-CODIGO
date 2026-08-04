---
volume: "16"
volume_nome: INTEGRATION
tipo: ARQUITETURA
secao: 03-Escopo
status: PRONTO
atualizado_em: 2026-08-04
---

# Escopo

## Dentro deste volume

Versionamento de contrato de integração externa, verificação de compatibilidade antes de
consumir resposta, idempotência de toda chamada com efeito colateral, timeout e retry explícitos
por integração, e isolamento de falha externa para que não se propague como indisponibilidade
interna.

## Fora deste volume, e para onde vai

**Chamada entre camadas do mesmo produto** (frontend consultando backend, backend consultando seu
próprio banco) é `22`-`25` — este volume não trata dessas chamadas, mesmo que tecnicamente
atravessem rede, porque o outro lado está sob o mesmo controle de release.

**Decisão de portfólio sobre concentração de fornecedor** é `06-ENTERPRISE-ARCHITECTURE` — este
volume trata do contrato técnico de uma integração específica; aquele trata de quantas integrações
com o mesmo fornecedor existem no portfólio inteiro e se isso é aceitável.

**Seleção de modelo de linguagem por provedor** é `27-LLM-ROUTER` — uma chamada a provedor de
modelo é, tecnicamente, uma integração externa que este volume cobriria, mas a decisão de qual
provedor usar e como rotear entre eles é daquele volume específico.

**Segurança de dado que cruza a fronteira** é `17-SECURITY` — este volume garante que a chamada em
si é robusta (versão, idempotência, timeout); a decisão sobre o que pode ou não atravessar a
fronteira em termos de sensibilidade de dado é daquele volume.

## Fronteira deliberada

Este volume nunca assume que o outro lado de uma integração é confiável por padrão — mesmo uma
integração interna a uma mesma empresa, mas fora do controle direto de quem consome, é tratada
com o mesmo rigor de contrato versionado e falha isolada que uma integração com fornecedor
externo.
