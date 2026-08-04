---
volume: "28"
volume_nome: PROMPT-COMPILER
tipo: ENGINE
secao: 01-Introducao
status: PRONTO
atualizado_em: 2026-08-04
---

# Introdução

`07-PROMPT-ENGINE` decide quando um prompt está pronto — versionado, testado contra caso de ouro,
promovido. Mas um prompt promovido ainda não é o que um provedor de modelo recebe: falta traduzir
o corpo e o contrato para o dialeto específico daquele provedor (formato de mensagem, papel de
sistema versus usuário, convenção de placeholder), decidir onde colocar ponto de cache, e
verificar que o resultado cabe no orçamento de tokens declarado. Esse é o trabalho deste volume.

A fronteira com o 07 é a implementação de referência da decisão de sobreposição de domínio
registrada em `ROADMAP.md`: o 07 define o contrato do prompt — o que ele é, suas variáveis, seu
hash, seu estado; este volume consome esse contrato já promovido e produz um payload concreto
para um provedor específico. Nunca o contrário — este volume não decide se um prompt está pronto
para produção, apenas traduz um que já foi decidido pronto.

Compilar não é uma operação neutra que só formata texto — decisões erradas aqui (variável não
substituída, orçamento estourado sem aviso, cache mal posicionado) produzem falha silenciosa que
só aparece quando a chamada ao provedor já foi feita, ou pior, quando a resposta chega malformada
e ninguém sabe se o problema é do modelo ou da compilação que o alimentou.
