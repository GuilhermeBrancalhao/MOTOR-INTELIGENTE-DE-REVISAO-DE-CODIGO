---
volume: "22"
volume_nome: FRONTEND-ARCHITECT
tipo: ARQUITETURA
secao: 10-Anti-Patterns
status: PRONTO
atualizado_em: 2026-08-04
---

# Anti-Patterns

**Spinner genérico idêntico para chamada de IA e chamada de CRUD comum.** Esconde do usuário a
diferença de latência esperada, que é informação real e útil sobre o que está acontecendo.

**Buffer que acumula toda a resposta de IA antes de exibir qualquer coisa, mesmo quando o
provedor entrega em stream.** Desperdiça a vantagem de latência percebida que o streaming
oferece, entregando a mesma experiência de uma chamada não incremental.

**Fallback para cache anterior sem nenhuma indicação visual de que é fallback.** É exatamente o
cenário que F3 existe para evitar — o usuário toma decisão achando que vê dado fresco.

**Resposta de IA promovida a estado global "porque outro componente também pode precisar dela
algum dia".** Promoção especulativa, sem uso real imediato, é a forma mais comum de F4 ser
violado — a decisão deveria vir de uma necessidade concreta, não de uma possibilidade futura.

**Requisição de IA que continua processando fragmentos depois que o componente que a originou já
foi desmontado.** Além do desperdício de recurso, é uma fonte comum de bug sutil quando o
fragmento tardio tenta atualizar um estado que já não existe mais no contexto esperado.


**Testar apenas o caminho de sucesso da chamada de IA, nunca o de cancelamento em teste
automatizado.** Cancelamento é justamente o caminho mais fácil de esquecer de testar e mais caro
de depurar quando falha em produção, porque depende de temporização específica difícil de
reproduzir manualmente.