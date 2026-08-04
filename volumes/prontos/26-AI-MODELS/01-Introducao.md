---
volume: "26"
volume_nome: AI-MODELS
tipo: ENGINE
secao: 01-Introducao
status: PRONTO
atualizado_em: 2026-08-04
---

# Introdução

Este é um volume perecível (regra 9 de `00-INTRODUCAO/Convencoes.md`): o assunto muda em semanas,
não em anos. Nenhum preço, janela de contexto ou nome de modelo específico entra aqui como fato
duradouro — o volume descreve o método de decidir, não o resultado de uma decisão tomada numa
data específica. Um número concreto, quando aparece, é sempre ilustração de método, datado e com
fonte, nunca referência a ser reutilizada depois que a data passar.

Selecionar entre modelos de IA para uma tarefa é uma decisão que se degrada rápido se feita por
impressão ("o mais novo", "o mais comentado") em vez de por critério verificável. Este volume
trata do método: qual capacidade a tarefa exige, como validar um candidato contra casos de ouro
antes de confiar nele, o que acontece quando o modelo escolhido fica indisponível, e como comparar
custo pela tarefa inteira, não pelo preço isolado de um token.

`27-LLM-ROUTER` trata do mecanismo que roteia uma chamada entre modelos já selecionados por este
método — este volume decide quais modelos entram na lista de candidatos e sob qual critério; o 27
decide, em tempo de execução, qual candidato específico atende uma chamada.

O gate estrutural deste acervo (`ferramentas.validar`) exige um piso de substância por seção
independente de um volume ser perecível ou não — a regra de volume perecível governa o que pode
ser dito (nunca fixar número que expira), não quanto precisa ser dito para passar no gate. Este
volume, portanto, é fino no que afirma como fato duradouro, mas ainda completo na explicação do
método, que é a parte que de fato não expira.