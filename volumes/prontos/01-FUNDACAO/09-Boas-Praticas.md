---
volume: "01"
volume_nome: FUNDACAO
tipo: GOVERNANCA
secao: 09-Boas-Praticas
status: PRONTO
atualizado_em: 2026-08-03
---

# Boas Práticas

**Rodar o gate estrutural antes de escrever a segunda seção, não depois da dezoito.** Um erro de
front-matter ou de tipo declarado errado se repete em todas as seções seguintes se descoberto
tarde — descobrir na primeira seção custa uma correção; descobrir na dezoitava custa dezoito.

**Escrever a seção `03-Escopo` com o nome do volume vizinho explícito, não uma frase genérica
como "não cobre integrações".** "Integrações externas ficam em `54-INTEGRACAO-ERP`" é uma
fronteira verificável; "não cobre integrações" não diz a quem perguntar. A convenção deste
acervo, estabelecida em `07-PROMPT-ENGINE`, é nomear o volume vizinho sempre.

**Tratar o mínimo de palavras como piso, não meta.** Escrever exatamente 200 palavras de prosa
enrolada para bater o número é enchimento disfarçado de conformidade — o próprio `Convencoes.md`
nomeia esse risco explicitamente. A meta é responder à pergunta que a seção existe para
responder; o número é só o alarme de "resposta vazia demais para ser real".

**Preferir citar a regra pelo nome (`substancia-curta`, `marcador-proibido`) ao discutir uma
violação**, em vez de descrever o simptoma em prosa própria — o nome ancora a conversa no que a
máquina de fato verifica, evitando debate sobre impressão de leitura em vez de fato mensurável.

**Registrar decisão de escopo com data e autor**, nunca como fato atemporal. "Cobertura dos 42
não é meta" só é uma frase útil porque `ROADMAP.md` registra quando essa decisão foi tomada e por
quem — sem data, a frase seria indistinguível de opinião pessoal de quem a escreveu.

**Auditar antes de reescrever em lote.** A tentação de gerar as dezoito seções de vários volumes
de uma vez, com um script ou um agente, produz exatamente o padrão que a auditoria de 2026-08-03
encontrou: esqueleto estruturalmente válido mas vazio de conteúdo real. Escrever um volume por
vez, validando cada um antes do próximo, é mais lento e produz menos volumes por sessão — e é
por isso mais confiável, porque cada erro aparece isolado, não multiplicado por trinta e nove.
