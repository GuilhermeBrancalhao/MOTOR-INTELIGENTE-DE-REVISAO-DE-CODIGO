---
volume: "40"
volume_nome: TEMPLATES
tipo: BIBLIOTECA
secao: 10-Anti-Patterns
status: PRONTO
atualizado_em: 2026-08-04
---

# Anti-Patterns

**Template com placeholder óbvio no nome, mas nenhuma lista formal de variável obrigatória.**
Viola AB1 — força quem usa o template a inspecionar o corpo manualmente para descobrir o que
precisa preencher, em vez de consultar uma declaração explícita.

**Copiar um template de outro projeto específico sem remover menção ao cliente ou sistema
original.** Viola AB4 diretamente — é exatamente a classe de erro que a verificação de domínio
neutro deste acervo existe para capturar antes de publicação.

**Reescrever a estrutura de um template amplamente usado sem incrementar versão.** Viola AB2 —
conteúdo gerado antes da mudança passa a ser silenciosamente incompatível com a nova estrutura,
sem que ninguém tenha sinalizado essa quebra.

**Template removido do catálogo sem aviso, quebrando geração que ainda dependia dele.** Viola
AB5 — a remoção silenciosa transforma uma migração planejável numa falha inesperada para quem
ainda usa o template antigo.

**Template genérico demais, sem escopo declarado, usado para produzir algo além do que foi
pensado para cobrir.** Viola AB6 — o template pode até "funcionar" tecnicamente fora do escopo
original, mas nada garante isso, porque nunca foi pensado para aquele caso.


**Assumir que um template "provavelmente ainda funciona" depois de meses sem revisão, sem
verificar contra o uso real atual.** A mesma armadilha de documentação desatualizada, aplicada
especificamente a um artefato que, por ser reutilizado com frequência, propaga qualquer problema
silencioso para cada novo uso subsequente.