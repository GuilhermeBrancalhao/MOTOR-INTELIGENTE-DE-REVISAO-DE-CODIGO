---
volume: "22"
volume_nome: FRONTEND-ARCHITECT
tipo: ARQUITETURA
secao: 07-Regras
status: PRONTO
atualizado_em: 2026-08-04
---

# Regras

**F1 — Todo elemento de interface dependente de resultado de IA declara estado de carregamento
distinto do carregamento genérico.** *Consequência:* a latência variável e frequentemente longa
de uma chamada de IA é percebida pelo usuário como diferente de uma espera de API comum, em vez
de escondida atrás de um indicador indistinguível.

**F2 — Saída incremental de IA é renderizada conforme chega, nunca armazenada em buffer para
parecer instantânea.** *Consequência:* a vantagem de latência percebida do streaming só existe se
a interface de fato expõe o progresso incremental ao usuário.

**F3 — Falha de ação dirigida por IA é estado visível e distinto; fallback para dado anterior
nunca é silencioso.** *Consequência:* o usuário sempre sabe se está vendo uma resposta fresca ou
um resultado de fallback, nunca confunde os dois.

**F4 — Resposta de IA pertence ao escopo do componente que a solicitou; promoção a estado global
exige decisão explícita.** *Consequência:* uma resposta de IA nunca vaza implicitamente para
partes não relacionadas da interface só por existir em algum lugar do estado da aplicação.

**F5 — Requisição de IA abandonada (componente desmontado, ação cancelada pelo usuário) é
cancelada, e fragmento recebido após cancelamento é descartado.** *Consequência:* nenhum recurso
é gasto processando uma resposta que já não tem consumidor, e nenhum estado é alterado por uma
resposta tardia que chegou depois do contexto que a solicitou ter mudado.

**F6 — A interface nunca consome o formato bruto de resposta de um provedor de IA diretamente;
toda tradução acontece numa camada de adaptação explícita.** *Consequência:* trocar de modelo ou
provedor não exige alterar cada componente que consome a resposta, apenas a camada de adaptação.
