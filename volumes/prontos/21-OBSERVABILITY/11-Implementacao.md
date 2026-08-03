---
volume: "21"
volume_nome: OBSERVABILITY
tipo: GOVERNANCA
secao: 11-Implementacao
status: PRONTO
atualizado_em: 2026-08-03
---

# Implementação

<!-- exemplo: exemplos/21-observability/limiar.py -->

`limiar.py`, citado acima, é a implementação de referência: sinal, limiar com proveniência
obrigatória, avaliador que distingue "alertou" de "notificou", e a decomposição de custo em que
`tokens: None` significa não-aplicável e nunca zero. Os testes provam os dois caminhos de falha do
próprio mecanismo — canal indisponível e limiar sem proveniência.

## Como um motor real implementaria este contrato

O coletor de sinal recebe eventos diretamente dos motores que os produzem — a integração natural
é cada motor (`08`, `09`, `10`) emitir o `Sinal` no momento em que o evento correspondente
acontece (encerramento de agente, transição de estado de nó, entrada em `AguardandoSinal`), em
vez de este volume tentar inferir os mesmos sinais a partir de log genérico depois do fato. Essa
escolha reduz a chance de perder granularidade na tradução — o motor que produz o evento sabe
exatamente o motivo; um parser de log posterior teria que reconstituir essa informação de forma
mais frágil.

O avaliador de limiar precisa manter estado por categoria de sinal e por origem — o mesmo tipo de
sinal (`MotivoEncerramento`) pode ter limiares diferentes dependendo de qual motor o produziu,
porque a criticidade e a variabilidade esperada diferem por domínio, como `07-Regras.md` já
estabelece.

A ordem de implementação recomendada é: modelo de dados (`Sinal`, `Limiar`, `Alerta`) e coletor
primeiro, integrado com pelo menos um motor real para validar o formato de emissão de evento.
Avaliador de limiar segundo, com calibração inicial manual antes de qualquer automação de
recalibração. Verificação do canal de notificação (heartbeat) por último, mas não como
opcional — é o controle que fecha o ciclo completo de "detectar e de fato avisar".

## Onde a integração com outros volumes acontece

Cada motor essencial (`08`, `09`, `10`) já define, na própria seção `14-Metricas.md`, quais
sinais específicos produz — este volume consome essas definições como fonte, não as redefine.
