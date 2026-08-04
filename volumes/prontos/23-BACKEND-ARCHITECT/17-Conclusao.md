---
volume: "23"
volume_nome: BACKEND-ARCHITECT
tipo: ARQUITETURA
secao: 17-Conclusao
status: PRONTO
atualizado_em: 2026-08-04
---

# Conclusão

A diferença entre um backend que lida bem com chamada de IA e um que apenas reaproveita o padrão
de uma API CRUD tradicional está em reconhecer que a duração é variável, que o processamento pode
exceder o tempo de vida de uma única requisição HTTP, e que a demanda pode superar a capacidade
disponível de forma imprevisível. As seis regras deste volume convergem para tratar o
processamento de IA como o que ele é: um trabalho com ciclo de vida próprio, não uma extensão
mais lenta de uma chamada de função comum.

A regra mais fácil de subestimar sob pressão de entrega rápida é S2 — ausência de afinidade entre
worker e trabalho. Parece uma otimização de disponibilidade opcional até o momento em que um
worker específico cai no meio de um trabalho, e sem essa garantia, aquele trabalho simplesmente
desaparece, sem que nenhum outro worker jamais soubesse que precisava continuá-lo.
