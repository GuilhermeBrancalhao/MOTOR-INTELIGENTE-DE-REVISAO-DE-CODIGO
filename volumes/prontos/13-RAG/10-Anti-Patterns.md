---
volume: "13"
volume_nome: RAG
tipo: ENGINE
secao: 10-Anti-Patterns
status: PRONTO
atualizado_em: 2026-08-04
---

# Anti-Patterns

**Tratar proximidade vetorial alta como relevância garantida, pulando a etapa de reordenação.**
Um documento pode estar vetorialmente próximo da pergunta por similaridade superficial de
vocabulário sem de fato responder à pergunta específica — R3 existe precisamente para essa
distinção.

**Aceitar citação sem verificar validade atual do documento**, confiando que "se foi indexado, é
válido". Isso ignora R6 e pode citar documento que expirou entre a indexação e a consulta como se
ainda fosse fonte confiável.

**Gerar resposta e assumir fidelidade pela presença de citação**, sem medir de fato quanto do
conteúdo gerado se sustenta no que foi citado. Um modelo pode citar um documento real e ainda
assim extrapolar além do que ele afirma — citação presente não é prova de fidelidade.

**Preferir sempre gerar alguma resposta a recusar explicitamente**, mesmo quando a base não tem
fonte suficiente. Isso produz o modo de falha mais caro de sistemas de RAG: resposta convincente
e sem fundamento verificável, que é mais perigosa que ausência de resposta.

**Confundir bug de fonte desatualizada com bug de recuperação.** Se uma resposta cita informação
errada porque o documento estava desatualizado, o bug é em `11-KNOWLEDGE` (documento deveria ter
expirado e não expirou), não neste volume — mas na prática, sem a fronteira clara de R5, a
investigação tende a procurar o problema no lugar errado primeiro.
