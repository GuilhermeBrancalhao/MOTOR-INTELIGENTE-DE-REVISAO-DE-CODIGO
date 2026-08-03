---
volume: "01"
volume_nome: FUNDACAO
tipo: GOVERNANCA
secao: 15-Checklist
status: RASCUNHO
atualizado_em: 2026-08-03
---

# Checklist

Antes de considerar QUALQUER volume do acervo pronto para auditoria (não confundir com PRONTO —
isso é o passo anterior):

- [x] `_VOLUME.yml` tem os 7 campos, sem BOM, `tipo` coerente com `contrato.json`.
- [x] As seções obrigatórias do tipo existem (conferir em `Contrato.secoes_de(tipo)`).
- [x] Cada seção tem front-matter de 6 campos, coerente com `_VOLUME.yml`.
- [x] Prosa de cada seção está acima do mínimo (`Contrato.minimo_de(secao)`), medida por
      `python -m ferramentas.validar NN`, não por leitura visual.
- [x] Nenhum marcador proibido (`TODO`, `PENDENTE`, `TBD`, `FIXME`, `XXX`, `preencher aqui`) fora
      de code span.
- [x] Todo bloco Mermaid é seguido imediatamente de parágrafo de prosa descritivo.
- [x] Diagramas obrigatórios do tipo estão presentes em algum lugar do volume.
- [x] Todo exemplo de código citado existe como arquivo e tem teste correspondente.
- [x] Todo link relativo resolve no disco.
- [ ] `python -m ferramentas.validar NN` retorna exit 0 — sem esse passo, os itens acima são
      inspeção visual, não verificação.

Este último item não é opcional nem redundante com os anteriores: é a diferença entre "eu revisei
e parece certo" e "a máquina confirmou". A auditoria de 2026-08-03 encontrou 39 volumes que
provavelmente pareciam certos numa leitura rápida e falhavam de forma reprodutível no gate real.
