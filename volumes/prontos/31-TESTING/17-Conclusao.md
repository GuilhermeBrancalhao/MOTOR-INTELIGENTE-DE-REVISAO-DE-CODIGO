---
volume: "31"
volume_nome: TESTING
tipo: PROCESSO
secao: 17-Conclusao
status: PRONTO
atualizado_em: 2026-07-30
---

# Conclusão

As três formas de defeito listadas em `01-Introducao.md` -- dependência de tempo real,
acoplamento a detalhe de implementação, e duplo de teste que substitui verificação por
teatro -- reaparecem nos três módulos como três decisões concretas, não como três
regras abstratas: `agora` sem valor padrão em `limitador_de_taxa.py`; asserção sobre o
valor de retorno preferida à asserção de interação sempre que o retorno já bastasse, em
`notificacao.py`; e a checagem explícita de repdígito em `validador_cpf.py`, que existe
justamente porque a fórmula sozinha confirmaria uma entrada que o domínio rejeita.

A suíte inteira -- 23 funções, 48 casos, os três arquivos -- roda em menos de duas
décimas de segundo porque nenhum teste toca relógio, rede ou disco reais. Essa
velocidade não é otimização à parte: é consequência direta de ter resolvido as três
decisões acima corretamente. Uma suíte lenta e instável quase sempre está pagando o
custo de uma das três formas de defeito, não de falta de hardware.

O limite honesto deste volume está em `03-Escopo.md` e em `16-Roadmap.md`: ele ensina a
estrutura do teste, não o indicador agregado que diz se a cobertura está subindo
(`32-QUALITY`), não testa carga ou concorrência, e não usa nenhuma biblioteca externa
de geração de caso -- por decisão de manter os exemplos no mesmo nível de restrição de
`ferramentas/`, não por esquecimento.
