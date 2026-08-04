# Auditoria — Volume 40 TEMPLATES

**Data:** 2026-08-04 | **Revisão:** 1 | **Auditor:** Opus 5 (redator: Opus 5, mesma sessão)

```
$ python -m ferramentas.validar 40
ok: volume 40 sem violacoes
$ python -m ferramentas.validar --cross-refs
ok: referencias cruzadas sem violacoes
$ python -m pytest exemplos/40-templates -q
7 passed
```

## Método

Verificadas as seis regras (AB1-AB6) contra `catalogo_de_templates.py`: AB1/AB6 via
`TemplateIncompleto`; AB5 via `DepreciacaoSemMotivo`; AB4 via `ConteudoDeDominioDetectado`; AB3
via `VariavelAusente` nos dois sentidos; AB2 via `VersaoDeTemplateIncompativel` nos dois sentidos.
Verificada a estrutura de seções específica de tipo BIBLIOTECA (`04-Catalogo`) e a fronteira com
`36-DIAGRAMS`, `35-DOCUMENTATION` e `07-PROMPT-ENGINE`.

## Verificação do domínio neutro — nota especial

```
$ grep -rli "concilia|controladoria|omie|sicoob" 40-TEMPLATES/ exemplos/40-templates/
40-TEMPLATES/06-Fluxogramas.md
40-TEMPLATES/08-Modelos.md
exemplos/40-templates/catalogo_de_templates.py
exemplos/40-templates/tests/test_catalogo_de_templates.py
```

Diferente dos falsos positivos por substring já vistos em `20-CLOUD` e `24-DATABASE-ARCHITECT`
("reconciliar", "Reconciliação"), estas quatro ocorrências são **intencionais**: este volume
implementa e documenta o próprio mecanismo de verificação de domínio neutro do acervo, usando o
conjunto real de termos proibidos (`_PALAVRAS_DE_DOMINIO_PROIBIDAS`) como exemplo central de AB4.
Confirmado por leitura direta de cada ocorrência: `06-Fluxogramas.md` e `08-Modelos.md` citam o
comando `grep` real usado pela auditoria de volume; o código implementa e testa exatamente essa
verificação, incluindo um caso de teste (`test_template_com_conteudo_de_dominio_e_rejeitado`) que
usa "Sicoob" como termo de exemplo do que deveria ser rejeitado — nenhuma menção é referência real
a conteúdo do projeto irmão, todas são auto-referência ao mecanismo de proteção em si.

## Notas por seção

| Seção | Nota | Observação |
|---|---|---|
| 01-Introducao | 8.5 | Nomeia a prática já existente informalmente antes de formalizá-la, sem exagero. |
| 02-Objetivos | 8 | Cinco objetivos protegendo reutilização real, não apenas teórica. |
| 03-Escopo | 8 | Três fronteiras nomeadas (36, 35, 07), evitando catálogo genérico demais. |
| 04-Catalogo | 8 | Quatro entradas reais já em uso neste acervo, não hipotéticas. |
| 06-Fluxogramas | 8.5 | flowchart reaproveitando literalmente o mecanismo de verificação de domínio do acervo. |
| 07-Regras | 8 | Seis regras, cada uma com consequência prática nomeada. |
| 08-Modelos | 8 | Imutabilidade justificada pelo mesmo padrão de outros volumes que representam fato histórico. |
| 09-Boas-Praticas | 8 | Quatro práticas, incluindo changelog próprio por template significativo. |
| 10-Anti-Patterns | 8 | Cinco padrões, incluindo o mais direto (template copiado de projeto real sem limpeza). |
| 11-Implementacao | 8 | Justifica centralização da lista de termos proibidos como fonte única de verdade. |
| 12-Exemplos | 8 | Cinco casos, Caso 2 didático para o mecanismo central de neutralidade. |
| 13-Testes | 8 | Prova por mutação nomeada; suíte livre de dependência de motor de template real. |
| 14-Metricas | 8 | Quatro métricas com ênfase em vazamento de domínio como alerta prioritário. |
| 15-Checklist | 8 | Nove itens desmarcados, convenção correta. |
| 16-Roadmap | 8 | Três lacunas reais (migração automática, extração de variável, integração com scaffold real). |
| 17-Conclusao | 8 | Fecha reafirmando valor de nomear prática já existente, sem meio-termo. |
| 18-Referencias-Cruzadas | 8 | Três vizinhos, `depende_de: []` justificado. |

media: 8.1

## Veredicto

**Aprovado. Volume promovido a PRONTO.** Média 8.1, nenhuma seção abaixo de 6. Os quatro
critérios satisfeitos: gate estrutural verde, 7 testes passando, auditoria acima de 8,0, registro
no `CHANGELOG.md`. Domínio neutro confirmado — as quatro ocorrências de termo proibido são
auto-referência intencional ao próprio mecanismo de verificação, não vazamento real.
