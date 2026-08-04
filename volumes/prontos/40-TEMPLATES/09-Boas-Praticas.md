---
volume: "40"
volume_nome: TEMPLATES
tipo: BIBLIOTECA
secao: 09-Boas-Praticas
status: PRONTO
atualizado_em: 2026-08-04
---

# Boas Práticas

Revisar o catálogo de templates periodicamente contra o uso real nos volumes e exemplos deste
acervo — um template descrito no catálogo mas nunca de fato usado pode já estar obsoleto sem que
ninguém tenha percebido.

Ao depreciar um template amplamente usado, migrar os usos existentes antes de remover qualquer
referência ao template antigo — depreciação explícita (AB5) não significa remoção imediata, apenas
sinalização clara de que uma transição precisa acontecer.

Testar a rejeição de conteúdo de domínio específico com os mesmos termos que o restante do acervo
já usa para essa verificação — manter a lista de termos proibidos sincronizada entre o processo
de auditoria de volume e o catálogo de template evita que os dois divirjam silenciosamente.

Nomear versão de template de forma semântica (major.minor), não apenas incremental — permite
distinguir mudança que quebra compatibilidade de mudança aditiva que não exige migração de uso
existente.


Manter changelog próprio por template significativo, separado do CHANGELOG geral do acervo — um
template usado dezenas de vezes merece histórico de mudança específico, mais fácil de consultar
do que buscar entre todas as entradas do changelog geral do projeto inteiro.

Esse changelog dedicado facilita também comunicar a quem usa o template exatamente o que mudou entre uma versão e a próxima, sem precisar comparar diffs manualmente.