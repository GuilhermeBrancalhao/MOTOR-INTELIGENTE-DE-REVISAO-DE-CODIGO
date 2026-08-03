# Escopo

## Dentro deste volume

Duas frentes, hoje com maturidade bem diferente:

1. **Normalização de arquivo de exportação sem API** — implementado e
   testado contra dado real: `normalizar.py` detecta automaticamente as
   colunas críticas de um CSV nativo de banco (comissão, data, proposta) por
   padrão de nome mais validação de tipo, e mapeia para um modelo padrão de
   36 colunas (`MODELO_UNIVERSAL.md`). Ver `exemplos/54-integracao-erp/`.
2. **Consumo de API de ERP** (SAP, Oracle, Omie, IFS) — ainda só a intenção
   declarada em `02-Objetivos.md`, sem implementação neste volume.

## Fora deste volume, e para onde vai

**Decidir se um movimento já normalizado casa com um título em aberto, com
que confiança, e se pode escrever sozinho** é `45-CONCILIACAO-CONTAS`:
aquele volume assume que o dado já chegou como `Movimento`/`TituloAberto` —
transformar CSV bruto de banco nesse formato é deste volume, não daquele.
`normalizar.py` é a peça que fecha essa lacuna, antes da conciliação.

**Categoria contábil e centro de custo do lançamento já normalizado** é
`43-CONTABILIDADE-BASICA`.

## Fronteira deliberada

Este volume não decide casamento nem confiança — só entrega o dado bancário
num formato padrão e validado. Misturar as duas responsabilidades faria o
mesmo módulo saber demais sobre formato de arquivo E sobre regra de negócio
de conciliação, dificultando testar as duas em isolamento.
