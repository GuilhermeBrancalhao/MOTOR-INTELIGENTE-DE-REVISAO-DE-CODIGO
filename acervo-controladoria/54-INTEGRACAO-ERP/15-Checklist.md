---
volume: "54"
volume_nome: INTEGRACAO-ERP
tipo: ARQUITETURA
secao: 15-Checklist
status: RASCUNHO
atualizado_em: 2026-08-04
---

# Checklist

Antes de considerar este volume pronto para uso em produção — não confundir com a Definição de
PRONTO do acervo, tratada em `00-INTRODUCAO/Convencoes.md`:

- [x] `normalizar.py` existe, é testado (10 testes) e roda contra pelo menos um CSV real de
      produção com resultado conferido à mão.
- [x] O bug real do percentual escolhido em vez do valor pago está corrigido e coberto por teste
      que falha se for reintroduzido.
- [x] Os dois diagramas exigidos pelo tipo `ARQUITETURA` (`C4Context` em `04-Arquitetura.md`,
      `sequenceDiagram` em `05-Diagramas.md`) existem e têm parágrafo descritivo logo depois.
- [x] Todo exemplo citado no volume existe como arquivo e tem teste correspondente.
- [x] Bug do BOM UTF-8 e coluna única silenciosa em `ler_csv` (arquivo de julho do DIGIO,
      `12-Exemplos.md`) — corrigido em 2026-08-04, coberto por 3 testes.
- [ ] Testado contra mais de um banco — hoje só DIGIO; os outros 39+ ainda não passaram pelo
      script.
- [ ] Conector de API de ERP (SAP, Oracle, Omie, IFS) — só intenção declarada em
      `02-Objetivos.md`, zero linha de código.
- [ ] `depende_de` aponta para `45-CONCILIACAO-CONTAS` e `43-CONTABILIDADE-BASICA` assim que o
      segundo for reescrito com o mesmo rigor — hoje fica vazio de propósito, ver `_VOLUME.yml`.
- [ ] Auditoria por outro modelo, com média maior ou igual a 8,0 e nenhuma seção abaixo de 6,
      registrada em `auditorias/`.
- [ ] Resultado registrado em `CHANGELOG.md` com a data do dia.

Os quatro últimos itens são o que falta para o `status` no front-matter passar de `RASCUNHO`
para `PRONTO` — os gates mecânicos (estrutural e executável) já rodam verdes, mas isso não
substitui auditoria de qualidade nem cobertura real contra mais de um banco.
