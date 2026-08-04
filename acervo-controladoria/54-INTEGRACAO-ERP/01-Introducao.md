---
volume: "54"
volume_nome: INTEGRACAO-ERP
tipo: ARQUITETURA
secao: 01-Introducao
status: RASCUNHO
atualizado_em: 2026-08-04
---

# INTEGRACAO-ERP

Duas superfícies diferentes de "trazer dado de fora para dentro": consumir API de ERP (SAP,
Oracle, Omie, IFS) quando ela existe, e normalizar arquivo de exportação quando ela não existe.
O caso real que preenche este volume hoje é o segundo: 40+ bancos e fintechs de comissão não
expõem API — o dado chega como CSV de exportação, um formato nativo diferente por banco, sem
padrão nenhum entre eles.

`normalizar.py`, em `exemplos/54-integracao-erp/`, resolve essa segunda superfície: lê o CSV
nativo de um banco, detecta automaticamente qual coluna é comissão, qual é data, qual é
identificador de proposta — por padrão de nome mais validação de tipo, não por mapeamento
manual — e grava um modelo padrão de 36 colunas (`PROCESSADO`, documentado em
`MODELO_UNIVERSAL.md`) que qualquer volume seguinte da cadeia de conciliação pode consumir sem
saber nada sobre o banco de origem. Foi testado contra CSV real de produção (DIGIO), e um bug
real de detecção — descrito em `12-Exemplos.md` — foi encontrado e corrigido nesse teste, não
imaginado.

A primeira superfície, consumo de API de ERP, permanece só intenção declarada em
`02-Objetivos.md`: nenhuma linha de código deste volume fala com SAP, Oracle, Omie ou IFS hoje.
Misturar as duas no mesmo texto sem marcar a diferença seria inflar o que existe — por isso todo
capítulo deste volume distingue explicitamente o que foi implementado e testado do que é
intenção.

Tipo: ARQUITETURA — este volume não tem estado próprio nem ciclo de vida (isso é do
`45-CONCILIACAO-CONTAS`); é a camada que entrega dado externo já normalizado para quem tem.
