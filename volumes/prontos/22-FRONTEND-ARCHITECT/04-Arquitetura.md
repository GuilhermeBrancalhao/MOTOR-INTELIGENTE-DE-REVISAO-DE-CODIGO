---
volume: "22"
volume_nome: FRONTEND-ARCHITECT
tipo: ARQUITETURA
secao: 04-Arquitetura
status: PRONTO
atualizado_em: 2026-08-04
---

# Arquitetura

O componente central é `RequisicaoDeIA` — representa o ciclo de vida completo de uma chamada
dirigida por IA do ponto de vista da interface: ociosa, carregando, com fragmentos acumulando
incrementalmente, concluída, com erro, ou cancelada. Cada transição de estado é uma operação
explícita (`iniciar`, `receber_fragmento`, `concluir`, `falhar`, `cancelar`), nunca uma mudança
implícita de campo — isso torna o ciclo de vida auditável e testável sem depender de simular a
interface real.

`resolver_exibicao` é a função que decide o que a interface deveria mostrar, dado o estado atual
de uma requisição e um cache anterior opcional — ela nunca retorna um resultado ambíguo entre
"resposta fresca" e "fallback de cache", sempre marcando explicitamente qual dos dois é o caso
(`ResultadoExibido.e_fallback`).

A fronteira entre escopo de componente e escopo global é imposta por `promover_para_global`, que
recusa a promoção sem autorização explícita — não existe caminho implícito de código que faça uma
resposta de IA vazar para estado compartilhado só porque ela existe.

`adaptar_resposta_do_provedor` isola o formato bruto de um provedor específico atrás de uma
função de tradução — a interface nunca lida diretamente com a forma exata da resposta de um
modelo ou provedor, apenas com o resultado já traduzido para o formato que os componentes
esperam.
