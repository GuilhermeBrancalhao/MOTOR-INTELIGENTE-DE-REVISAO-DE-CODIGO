---
volume: "17"
volume_nome: SECURITY
tipo: GOVERNANCA
secao: 13-Testes
status: RASCUNHO
atualizado_em: 2026-08-03
---

# Testes

## Estratégia

Testar a política de segurança deste volume exige simular tentativa de contorno adversarial, não
só confirmar que o comportamento esperado ocorre com entrada bem comportada. A técnica é manter
um catálogo de vetores conhecidos (as doze variações de comando de shell do motor `ENGINE` são
um catálogo real, documentado em `README.md`) e testar cada um explicitamente, mais um teste
estrutural que trava a política inteira contra reintrodução acidental de exceção — o motor tem
esse teste com o nome `test_nenhum_comando_de_shell_e_livre`.

## O que a suíte precisa cobrir

Isolamento de origem: um teste que injeta instrução dentro de dado marcado como `Processado` e
verifica que a ação de alto risco decidida a partir dali exige confirmação, não executa
diretamente. Auditoria de destino: um teste que tenta uma chamada de ferramenta com destino fora
da lista autorizada e verifica travamento, mais um teste que confirma que destino autorizado
executa sem travamento indevido (a ausência de falso positivo sistemático também precisa de
prova, não só a presença de bloqueio no caso negativo). Sandboxing: para cada família de risco de
execução nomeada, pelo menos um teste que reproduz o vetor concreto documentado.

## Prova por mutação

Um teste forte para "comando de shell nunca é livre" é um que falha se alguém adicionar uma
exceção — por exemplo, classificar `ls` como `Livre` "porque é inócuo". O teste estrutural do
motor `ENGINE` prova exatamente isso: qualquer comando de shell, sem exceção por conteúdo
específico, precisa cair em `Travado` ou `Rastreado`. Sem esse teste, uma exceção pontual
adicionada por conveniência de desenvolvimento poderia reabrir uma classe inteira de risco.

## Testes de integração com volumes vizinhos

O processo que executa esses testes continuamente a cada mudança de código é assunto de
`18-DEVSECOPS` — este volume define os testes que deveriam existir; `18` define quando e como
eles rodam no pipeline.
