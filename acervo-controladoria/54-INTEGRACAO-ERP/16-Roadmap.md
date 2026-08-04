---
volume: "54"
volume_nome: INTEGRACAO-ERP
tipo: ARQUITETURA
secao: 16-Roadmap
status: RASCUNHO
atualizado_em: 2026-08-04
---

# Roadmap

## O que este volume ainda não cobre

Correção do bug de BOM UTF-8 na detecção de separador de `ler_csv` — identificado contra o
arquivo de julho do DIGIO, ainda sem correção. Cobertura contra bancos além do DIGIO — a lógica
de detecção foi desenhada para generalizar a 40+ bancos, mas só foi provada contra um. Conector
de API de ERP (SAP, Oracle, Omie, IFS) — hoje só intenção declarada, sem nenhum caso real que
justifique a implementação, já que nenhum banco de comissão trabalhado neste projeto expõe API.

## Ordem de cobertura pretendida

Primeiro, o bug do BOM, porque é uma falha conhecida e concreta, não uma extensão de escopo.
Depois, testar contra três a cinco bancos reais adicionais — cada banco novo tende a revelar uma
peculiaridade de formato que os testes sintéticos de `test_normalizar.py` não previram, do mesmo
jeito que o CSV real do DIGIO revelou o problema de parsing numérico brasileiro que a lógica de
desempate, sozinha, não bastava para resolver. Só depois disso caberia decidir se o conector de
API de ERP é sequer necessário no curto prazo.

## O que este volume assume que pode mudar

A lista de padrões de nome usada na detecção (`comiss`, `commission`, `incentiv`, `fee` para
comissão; `data`, `date`, `dt.` para data; e assim por diante) é hoje uma lista fixa em código.
Conforme mais bancos passarem pelo script, é provável que apareça um nome de coluna que nenhum
padrão atual cobre — nesse momento, a lista cresce, e o teste correspondente registra o caso
novo, seguindo o mesmo padrão que corrigiu o bug do percentual.

## Dívida técnica registrada, não deste volume especificamente

Os 30 testes de `acervo-controladoria/exemplos/` (os 7 deste volume mais os 23 de
`45-CONCILIACAO-CONTAS`) não são coletados por nenhuma suíte automática de `pytest` — ver
`13-Testes.md`. Resolver isso é do repositório como um todo, não deste volume isolado, mas fica
registrado aqui porque afeta diretamente a confiança que se pode ter em "os testes passam".
