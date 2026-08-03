---
volume: "01"
volume_nome: FUNDACAO
tipo: GOVERNANCA
secao: 10-Anti-Patterns
status: RASCUNHO
atualizado_em: 2026-08-03
---

# Anti-Patterns

**Declarar "entrega completa" citando contagem de teste do motor como prova de conteúdo do
acervo.** "449 testes passando" prova que o código do motor funciona; não diz nada sobre se as
dezoito seções de um volume têm prosa real. Foi exatamente essa confusão — presente no
`ENTREGA.md` anterior a 2026-08-03 — que permitiu declarar 39 volumes vazios como "estrutura
completa".

**Gerar conteúdo de vários volumes em lote com um único template preenchido por variável.** O
sintoma reconhecível é seções curtas e quase idênticas entre volumes diferentes, mudando só o
nome do domínio — é o padrão exato que a auditoria de 2026-08-03 encontrou em 39 dos 42 volumes,
`marcador-proibido` correndo dentro de código gerado sem revisão, e substância abaixo do mínimo
em praticamente toda seção.

**Escrever o arquivo `_VOLUME.yml` com encoding que introduz BOM (byte-order-mark) no início.**
`Path.read_text(encoding="utf-8")` do Python não remove BOM (só `"utf-8-sig"` remove), então a
primeira chave do YAML vira `"﻿volume"` em vez de `"volume"`, e o validador reporta "campo
ausente" mesmo com o campo presente — um bug real encontrado nesta plataforma em 2026-08-03,
afetando 39 arquivos e mascarando 618 violações adicionais que só apareceram depois do fix.

**Confundir `depende_de` com "assunto relacionado".** Dois volumes podem se citar mutuamente
como vizinhos de assunto (`07` e `28`, por exemplo) sem que um seja pré-requisito de leitura do
outro. Colocar os dois em `depende_de` recíproco cria ciclo, e `ferramentas.validar --cross-refs`
reprova exatamente por isso — a relação bidirecional pertence a `18-Referencias-Cruzadas.md`.

**Gravar `PRONTO` "porque o conteúdo parece bom" sem rodar o validador.** Julgamento humano sobre
qualidade de prosa não substitui a verificação mecânica do gate 1 — as duas coisas medem
categorias diferentes de erro, e pular a mecânica para confiar só no julgamento é exatamente como
o erro de BOM ficou invisível por tempo suficiente para se espalhar por 39 arquivos.
