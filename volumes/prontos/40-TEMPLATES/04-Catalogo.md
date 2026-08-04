---
volume: "40"
volume_nome: TEMPLATES
tipo: BIBLIOTECA
secao: 04-Catalogo
status: PRONTO
atualizado_em: 2026-08-04
---

# Catálogo

**Template de front-matter de seção** — usado por toda seção de todo volume deste acervo.
Variáveis obrigatórias: `volume`, `volume_nome`, `tipo`, `secao`, `status`, `atualizado_em`.
Escopo: cabeçalho estrutural lido por `ferramentas/frontmatter.py`; não inclui o corpo da seção
em si.

**Template de `_VOLUME.yml`** — usado na criação de todo volume novo. Variáveis obrigatórias:
`volume`, `nome`, `tipo`, `status`, `perecivel`, `depende_de`, `escopo`. Escopo: metadado de
volume consultado por `ferramentas/contrato.py`; não inclui conteúdo de nenhuma seção específica.

**Template de `conftest.py` de exemplo** — copiado para toda pasta `exemplos/<volume>/`.
Variáveis obrigatórias: nenhuma — o template é idêntico em toda instância, sua função é apenas
inserir o diretório do exemplo no caminho de import, evitando colisão de nome de módulo entre
pastas de exemplo diferentes. Escopo: configuração de teste; não gera nenhum código de produção.

**Template de prompt versionado** — ponto de partida para um prompt formalizado pelo
`07-PROMPT-ENGINE`. Variáveis obrigatórias: `nome`, `corpo_inicial`, `variaveis_do_prompt`.
Escopo: rascunho de prompt antes de entrar na máquina de estados do 07; não substitui o
versionamento formal daquele volume.

Cada entrada deste catálogo carrega versão própria e é verificada, na criação, contra a mesma
disciplina de domínio neutro que qualquer conteúdo deste acervo já precisa atravessar.


Cada uma dessas quatro entradas já está em uso real neste acervo hoje — não são exemplos
hipotéticos, são os templates efetivamente aplicados toda vez que um volume novo é criado ou uma
pasta de exemplo nova é adicionada, o que torna este catálogo uma descrição fiel da prática
atual, não uma aspiração futura ainda não implementada.