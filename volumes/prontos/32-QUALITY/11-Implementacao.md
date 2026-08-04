---
volume: "32"
volume_nome: QUALITY
tipo: PROCESSO
secao: 11-Implementacao
status: PRONTO
atualizado_em: 2026-08-04
---

# Implementação

<!-- exemplo: exemplos/32-quality/indicador_de_qualidade.py -->

`indicador_de_qualidade.py`, citado acima, formaliza H1-H6: `Medicao.taxa_prova_de_mutacao`
calcula a partir de `regras_com_prova_de_mutacao / regras_totais`, nunca de
`cobertura_de_linha` (H1); `GateDeQualidade.verificar` levanta `LimiarNaoAtingido` quando a taxa
cai abaixo do limiar sem exceção registrada (H2); `ItemDeDivida` recusa criação com qualquer dos
quatro campos vazio (H3); `detectar_regressao` exige duas medições no histórico, retornando
`None` com menos de duas (H4); o mesmo `detectar_regressao` retorna um objeto `Regressao`
explícito com os dois valores específicos quando a taxa cai (H5); `Medicao` mantém três campos
nomeados separados em vez de um único score (H6).

`GateDeQualidade` e `HistoricoDeQualidade` são componentes separados, não uma única classe que
faz as duas coisas — o gate decide sobre uma medição isolada; o histórico acumula múltiplas
medições ao longo do tempo, e a separação reflete que os dois podem evoluir independentemente,
inclusive com implementações completamente diferentes de armazenamento por trás de cada um.

Essa independência também facilita testar cada componente isoladamente, sem precisar simular o outro só para verificar uma regra específica de um deles.

A troca de uma implementação de armazenamento por outra, para qualquer um dos dois, nunca
exigiria alterar o outro componente correspondente — cada um permanece funcional e testável mesmo
que o outro seja completamente reescrito por baixo, contanto que a interface pública se mantenha.