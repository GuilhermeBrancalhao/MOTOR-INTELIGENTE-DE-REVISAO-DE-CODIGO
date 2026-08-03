---
volume: "21"
volume_nome: OBSERVABILITY
tipo: GOVERNANCA
secao: 16-Roadmap
status: PRONTO
atualizado_em: 2026-08-03
---

# Roadmap

## O que este volume ainda não cobre

Integração entre os motores deste ciclo. O exemplo deste volume prova o contrato isoladamente;
a ponte com os volumes vizinhos — traduzir os tipos de um para os do outro — ainda não tem teste
que a exercite de ponta a ponta.

Recalibração automática de limiar a partir de detecção estatística de deriva (drift) na
distribuição do sinal — hoje a recalibração descrita em `06-Fluxogramas.md` é processo manual
com disciplina de investigação prévia; automatizar a detecção de quando recalibrar (sem
automatizar a decisão de qual novo valor usar, que continua exigindo julgamento humano sobre
causa) é extensão possível, não parte do contrato mínimo atual.

Correlação automática entre sinais de categorias diferentes (por exemplo, um pico de intervenção
humana correlacionado com uma mudança recente de versão de modelo) — hoje cada categoria de
sinal é tratada independentemente; correlação exigiria infraestrutura de análise adicional não
especificada neste volume.

## Ordem de cobertura pretendida

Primeiro, código de referência mínimo (modelo de dados + coletor + avaliador de limiar), testado
com coletor fake antes de integração com motor real. Depois, integração real com pelo menos um
dos três motores essenciais (`08`, `09` ou `10`) para validar o formato de emissão de sinal na
ponta de origem.

## O que este volume assume que pode mudar

O conjunto de três categorias de sinal específicas de sistema com IA pode crescer se um caso de
uso real expuser uma quarta categoria relevante — qualquer categoria nova precisa manter a
mesma disciplina de distinção entre "observável" e "alertável" descrita em `07-Regras.md`.
