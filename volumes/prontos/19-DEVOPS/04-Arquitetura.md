---
volume: "19"
volume_nome: DEVOPS
tipo: ARQUITETURA
secao: 04-Arquitetura
status: PRONTO
atualizado_em: 2026-08-04
---

# Arquitetura

O componente central é o `Pipeline`, construído em torno de um único `Artefato` imutável
(identificado por hash e commit de origem) — o mesmo artefato flui por todos os estágios, nunca é
substituído no meio do caminho. `Pipeline` é um dataclass congelado: reatribuir seu artefato
depois de criado levanta erro em tempo de execução, tornando a paridade entre o que foi testado e
o que é implantado uma garantia estrutural, não uma convenção que depende de disciplina.

Os estágios (`Estagio`, enumerado: BUILD, TESTE, SEGURANCA, STAGING, PRODUCAO) têm ordem fixa.
`Pipeline.executar_estagio` recusa um estágio fora da posição esperada e recusa avançar quando o
estágio anterior falhou — não existe caminho de código que permita pular um estágio, mesmo
chamando os métodos diretamente.

O `GerenciadorDeploy` mantém o histórico de artefatos efetivamente implantados em produção, na
ordem em que aconteceram. Consultar "o que está rodando agora" é sempre uma leitura do último
registro do histórico, nunca uma suposição; reverter é sempre promover o artefato do registro
anterior, nunca uma operação especial que ignora o histórico.


A separação entre `Pipeline` (execução de estágios) e `GerenciadorDeploy` (histórico e reversão)
é deliberada: um pipeline representa uma única passagem de um artefato pelos estágios, e termina
quando chega a produção ou falha; o gerenciador persiste através de múltiplos pipelines,
acumulando o histórico que torna possível responder "o que está rodando" e "para onde reverter" a
qualquer momento, independente de qual pipeline específico produziu cada entrada.