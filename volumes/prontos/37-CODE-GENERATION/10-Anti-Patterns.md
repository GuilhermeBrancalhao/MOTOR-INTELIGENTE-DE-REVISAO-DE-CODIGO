---
volume: "37"
volume_nome: CODE-GENERATION
tipo: ENGINE
secao: 10-Anti-Patterns
status: PRONTO
atualizado_em: 2026-08-04
---

# Anti-Patterns

**Aceitar código gerado sem rodar a suíte de teste, "porque a IA geralmente acerta".** Viola Y1
diretamente — a origem do código nunca substitui verificação real.

**Editar diretamente um arquivo de código marcado como gerado, sem atualizar a especificação
correspondente.** Viola Y2 — a próxima geração apaga a edição manual sem que quem a fez perceba
até tarde demais.

**Merge automático de código gerado que passou toda validação, sem revisão humana.** Viola Y4 —
validação automatizada prova correção técnica, não que o código faz a coisa certa do ponto de
vista de negócio ou de manutenibilidade futura.

**Especificação de geração não versionada, apenas o código de saída commitado.** Viola Y5 —
perde a rastreabilidade até a intenção original que produziu aquele código específico.

**Código gerado usado além do escopo que sua especificação declarou, sem gerar uma especificação
nova para o caso adicional.** Viola Y6 — o código pode funcionar por acidente fora do escopo
original, mas nada garante isso, porque nunca foi pensado para aquele caso.


**Confiar que um modelo de IA mais recente ou mais capaz dispensa a mesma disciplina de
validação e revisão exigida de versões anteriores.** A capacidade do modelo gerador nunca é
motivo para relaxar verificação — a disciplina deste volume vale igualmente, independente de
quão sofisticado o gerador se torne ao longo do tempo.