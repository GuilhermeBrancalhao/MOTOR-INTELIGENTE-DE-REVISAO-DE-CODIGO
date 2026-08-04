---
volume: "37"
volume_nome: CODE-GENERATION
tipo: ENGINE
secao: 09-Boas-Praticas
status: PRONTO
atualizado_em: 2026-08-04
---

# Boas Práticas

Revisar a especificação com o mesmo cuidado que se revisaria o código gerado — uma especificação
ambígua ou incompleta tende a produzir geração inconsistente entre execuções, mesmo com um
gerador determinístico por trás.

Manter um histórico de gerações tentadas para a mesma especificação, não apenas a última — útil
para entender se ajustes incrementais na especificação estão de fato convergindo para o resultado
esperado.

Testar o caminho de rejeição por falta de revisão humana ativamente, garantindo que o portão de
fato bloqueia — um portão de revisão nunca testado pode ter sido contornado silenciosamente sem
que ninguém perceba.

Nomear, no escopo declarado do código gerado, os casos de borda explicitamente considerados fora
do alcance — não apenas o que o código faz, mas os cenários específicos que alguém poderia
razoavelmente esperar que ele cobrisse e não cobre.


Manter um repositório de especificações de geração bem-sucedidas como referência para
especificações futuras semelhantes — um padrão de especificação que historicamente produz
geração confiável vale mais que reinventar a estrutura a cada nova necessidade de geração.

Esse acervo de referência cresce organicamente com o uso real, tornando-se mais valioso à medida que mais especificações bem-sucedidas são documentadas ao longo do tempo.

Documentar tanto os sucessos quanto os fracassos de especificação anterior evita repetir o mesmo erro de ambiguidade que já causou geração inconsistente no passado.