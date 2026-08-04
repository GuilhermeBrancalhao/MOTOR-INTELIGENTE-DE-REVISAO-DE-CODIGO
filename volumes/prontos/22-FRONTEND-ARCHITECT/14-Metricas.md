---
volume: "22"
volume_nome: FRONTEND-ARCHITECT
tipo: ARQUITETURA
secao: 14-Metricas
status: PRONTO
atualizado_em: 2026-08-04
---

# Métricas

**Tempo até o primeiro fragmento renderizado (não até a resposta completa).** Mede a vantagem
real de latência percebida que o streaming (F2) está entregando na prática, não apenas o tempo
total da chamada.

**Proporção de falhas de IA que caem em fallback versus estado de erro puro.** Ajuda a entender
se o cache anterior está de fato cobrindo os cenários de falha mais comuns, ou se a maioria das
falhas deixa o usuário sem nenhum resultado utilizável.

**Número de requisições canceladas por abandono versus concluídas.** Um número alto de
cancelamento pode indicar que a latência percebida está afastando o usuário antes da resposta
chegar, não apenas uso normal de navegação.

**Contagem de promoções a estado global por sessão.** Deveria ser rara e sempre justificável — um
número crescente sem justificativa correspondente pode indicar que F4 está sendo contornado por
conveniência, não por necessidade real.


As quatro métricas juntas ajudam a distinguir um problema de latência real de um problema de
percepção de latência — um tempo até o primeiro fragmento baixo mas com alta taxa de cancelamento
pode indicar que o problema não é técnico, mas de expectativa do usuário sobre o que vai
acontecer depois daquele primeiro fragmento.

Nenhuma dessas métricas deveria ser otimizada isoladamente — perseguir tempo até o primeiro
fragmento sem considerar a taxa de cancelamento correspondente pode levar a otimizações que
melhoram um número sem de fato melhorar a experiência percebida pelo usuário final.