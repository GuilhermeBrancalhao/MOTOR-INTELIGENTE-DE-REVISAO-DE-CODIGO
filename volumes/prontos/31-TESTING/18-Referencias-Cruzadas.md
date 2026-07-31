---
volume: "31"
volume_nome: TESTING
tipo: PROCESSO
secao: 18-Referencias-Cruzadas
status: PRONTO
atualizado_em: 2026-07-30
---

# Referências Cruzadas

`depende_de` está vazio no `_VOLUME.yml` deste volume, e a razão está documentada ali
mesmo: o vizinho mais próximo, [`32-QUALITY`](../32-QUALITY/), ainda não tem seção
escrita, e apontar pré-requisito de leitura para volume sem conteúdo produziria uma
dependência que não pode ser lida. A vizinhança abaixo é lateral, não pré-requisito --
fica em prosa de propósito, para que o grafo de `--cross-refs` continue acíclico.

- [`32-QUALITY`](../32-QUALITY/) -- o indicador agregado que consome a prática descrita
  aqui; fronteira em `03-Escopo.md`.
- [`17-SECURITY`](../17-SECURITY/) e [`18-DEVSECOPS`](../18-DEVSECOPS/) -- política de
  segurança e o processo que roda seus controles no pipeline; a estrutura de teste
  genérica é deste volume, o controle específico de segurança é de lá.
- [`33-PERFORMANCE`](../33-PERFORMANCE/) -- taxonomia de teste sob carga; a taxonomia de
  unitário/integração daqui continua valendo, o desenho de carga não.
- [`16-INTEGRATION`](../16-INTEGRATION/) -- teste de contrato entre fronteiras de
  produto diferentes.
- [`07-PROMPT-ENGINE/13-Testes.md`](../07-PROMPT-ENGINE/13-Testes.md) -- avaliação de
  prompt por caso de ouro, específica o bastante para viver naquele volume em vez de
  duplicar aqui.
- [`exemplos/31-testing/conftest.py`](../exemplos/31-testing/conftest.py) -- o mecanismo
  de import descrito em `11-Implementacao.md`.
