---
volume: "37"
volume_nome: CODE-GENERATION
tipo: ENGINE
secao: 14-Metricas
status: PRONTO
atualizado_em: 2026-08-04
---

# Métricas

**Proporção de código gerado que passa validação na primeira tentativa.** Uma proporção baixa
pode indicar que a especificação está ambígua ou que o gerador precisa de ajuste — o problema
raramente está apenas em "a IA errou desta vez".

**Proporção de código gerado aprovado versus rejeitado na revisão humana.** Uma taxa de rejeição
alta merece investigação sobre se o processo de especificação está capturando os requisitos
corretamente antes da geração acontecer.

**Frequência de tentativa de edição manual bloqueada sobre código gerado.** Um número
persistentemente alto sugere que o processo de ajustar especificação e regerar está mais lento ou
mais custoso do que deveria, incentivando o atalho que Y2 proíbe.

**Tempo entre geração e revisão humana concluída.** Mede se o portão de revisão obrigatória está
sendo respeitado com agilidade, não apenas existindo como etapa formal que atrasa entrega sem
necessidade real.


Estas quatro métricas, lidas em conjunto, revelam se o processo de geração está amadurecendo ao
longo do tempo — proporção crescente de sucesso na primeira tentativa e tempo de revisão estável
são os dois sinais mais diretos de que especificação e gerador estão convergindo para um padrão
confiável, não apenas produzindo resultado aceitável por sorte pontual.

Nenhuma delas substitui investigação direta de um caso de geração específico que falhou repetidamente, mas juntas orientam onde vale a pena investigar primeiro.