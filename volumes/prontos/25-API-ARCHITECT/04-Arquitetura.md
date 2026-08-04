---
volume: "25"
volume_nome: API-ARCHITECT
tipo: ARQUITETURA
secao: 04-Arquitetura
status: PRONTO
atualizado_em: 2026-08-04
---

# Arquitetura

`ContratoDeEndpoint` mantém o mapa de campos expostos por um endpoint numa versão específica —
`declarar_campo` recusa redeclarar um campo já existente com um tipo diferente sob a mesma
versão, tornando mudança de significado de campo (T1/T5) uma verificação, não uma convenção que
depende de revisão manual cuidadosa.

`traduzir_para_resposta` é o único ponto que produz a resposta enviada ao cliente a partir de um
registro interno — ele nunca copia o registro inteiro, apenas os campos explicitamente
permitidos, o que torna impossível vazar um campo interno (como controle de concorrência ou
proveniência bruta) só porque ele existe no objeto de origem.

`ErroDeAPI` é o único tipo usado para representar erro em qualquer endpoint — não existe um
segundo formato de erro paralelo em nenhuma parte do exemplo, o que é a garantia estrutural de
consistência que T3 exige.

`status_do_trabalho` traduz o estado interno de um trabalho (do modelo do 23) para um recurso
consultável com URL própria — o cliente nunca precisa saber a representação interna do estado,
apenas consultar o recurso que este volume expõe.

`declarar_endpoint_sincrono` recusa aceitar um endpoint síncrono sem orçamento de latência
declarado, tornando a ausência de expectativa de tempo de resposta uma falha detectável antes de
o endpoint entrar em uso, não uma surpresa descoberta pelo cliente em produção.
