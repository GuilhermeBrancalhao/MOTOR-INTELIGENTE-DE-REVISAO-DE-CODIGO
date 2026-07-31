---
name: materializar-ideia
description: Motor que transforma conceito abstrato em aplicação funcional rodando — decide stack, monta backend, desenha interface e entrega código executável, não esqueleto. Use quando o usuário descrever algo que ainda não existe: "quero um app que", "cria um site pra", "preciso de um dashboard de", "e se tivesse uma ferramenta que", ou quando trouxer uma ideia vaga pedindo para virar produto. Cobre escolha de stack justificada, modelagem de dados, API, identidade visual e primeira execução verificada. Não use para alterar aplicação existente — aí o motor é `revisar-codigo` ou `arquitetar-sistema`.
---

# Motor de materialização

Entrada: uma ideia. Saída: algo que **roda**. Esqueleto com `TODO` não é entrega — se o usuário precisa completar para ver funcionando, o motor falhou.

## Postura

O usuário trouxe uma ideia, não uma especificação. Parte do seu trabalho é decidir o que ele não decidiu — e **nomear cada decisão que tomou**, para ele poder discordar de uma sem descartar o resto.

Ideia vaga não autoriza produto genérico. "Um app de tarefas" tem mil formas; escolha uma, diga por que essa, e construa ela inteira. Meia dúzia de features pela metade vale menos que uma vertical que funciona ponta a ponta.

## Fase 1 — Fixar o conceito

Antes de escrever qualquer linha, três coisas precisam estar definidas. Se faltar alguma, **pergunte** — mas pergunte tudo de uma vez, com `AskUserQuestion`, não em série.

1. **Quem usa e para quê.** "Todo mundo" não é resposta — muda layout, densidade de informação e vocabulário da interface.
2. **A ação central.** A única coisa que a pessoa faz mais vezes. Ela ganha o caminho mais curto da tela; todo o resto se subordina.
3. **A restrição dura.** Precisa rodar offline? Só um arquivo? Sem backend? Dado sensível? Isso elimina stacks inteiras e é mais barato saber agora.

**Não pergunte o que você pode decidir.** Framework, nome de tabela, biblioteca de ícone — decida, nomeie, siga. Perguntar tudo devolve ao usuário o trabalho que ele delegou.

Quando a ideia já vem com essas três coisas claras, **pule a pergunta e construa**. Turno gasto em confirmação do óbvio é turno perdido.

## Fase 2 — Escolher a stack

Escolha pelo que a ideia exige, não pelo que é familiar. Uma frase de justificativa por decisão.

Regra que resolve a maioria dos casos: **a menor stack que atende a restrição dura vence.** Complexidade só se paga contra requisito real, e requisito imaginado ("depois vai escalar") não é real.

- Ferramenta de uso único, cálculo, visualização → HTML + JS num arquivo. Sem build, sem servidor. Abre e funciona.
- Interface com estado real, várias telas → framework de componente, com build mínimo
- Precisa persistir entre sessões e dispositivos → aí, e só aí, entra backend e banco
- Dado tabular que o usuário já tem → considere ler o arquivo dele em vez de criar cadastro

Matriz de decisão detalhada em `references/escolha-de-stack.md`.

**Antes de adicionar dependência,** verifique se a plataforma já resolve. Muita coisa que virava biblioteca hoje é nativa. Dependência custa manutenção, superfície de ataque e tempo de build.

## Fase 3 — Construir de dentro para fora

Ordem importa, porque cada camada testa a anterior:

**1. Modelo.** Os tipos e as invariantes. Aqui mora a regra de negócio, sem framework em volta. Se `Pedido` pode existir sem item, o construtor precisa dizer isso ou o bug já nasceu.

**2. Casos de uso.** Uma função por ação que o usuário realiza. Nomeadas pelo verbo do domínio, não por operação de CRUD: `confirmarPedido`, não `updatePedidoStatus`.

**3. Borda.** API, CLI ou handler. Traduz entrada externa em tipo do domínio e erro de domínio em código de resposta. Validação de formato aqui; regra de negócio não.

**4. Persistência.** Só quando o caso de uso já funciona em memória. Schema versionado desde o primeiro dia.

**5. Interface.** Última, com o resto funcionando. Detalhe em `references/identidade-visual.md`.

Em ferramenta de arquivo único, as cinco camadas continuam existindo — como seções separadas do mesmo arquivo, não como espaguete.

## Fase 4 — Interface

A interface é onde o usuário julga o trabalho. Vale o mesmo cuidado do backend.

**Regra que vale para tudo:** interface não é decoração de dados, é a ferramenta. Escolhas visuais derivam do assunto — um painel financeiro e um app de receita não podem parecer o mesmo produto com cores trocadas.

**O que evitar** — o repertório visual que denuncia geração automática: creme `#F4F1EA` com serifada e acento terracota; preto quase absoluto com um único verde-ácido; gradiente roxo-para-azul no topo; Inter como escolha "segura"; emoji marcando seção; tudo centralizado; cartão arredondado com barrinha de acento à esquerda.

Se o usuário pediu uma direção visual explícita, **a dele vence sempre** — inclusive se for uma das acima.

Fundamentos, sistema de tokens e tema claro/escuro em `references/identidade-visual.md`.

## Fase 5 — Verificar que roda

**Obrigatório. Sem isso a entrega não está feita.**

- Rode. Servidor sobe? Página abre? O caminho da ação central funciona de ponta a ponta?
- Exercite o caminho de erro: entrada vazia, valor inválido, lista sem itens. A ferramenta não pode quebrar no primeiro clique errado.
- Interface: verifique em largura estreita. Nada de rolagem horizontal no corpo da página.
- Se houver navegador disponível, abra e olhe. Console com erro é entrega incompleta.

**Reporte o que testou e o que não testou.** "Funciona" sem dizer o que foi exercitado é afirmação vazia — e se algo ficou por fazer, diga qual, em vez de deixar o usuário descobrir.

## Formato de entrega

1. **O que foi construído** — uma linha, sem adjetivo de marketing
2. **Decisões que tomei por você** — lista curta, cada uma com a justificativa em meia linha. É aqui que o usuário discorda de um item sem jogar tudo fora
3. **Como rodar** — comando exato, em bloco próprio
4. **O que verifiquei** — e o que deixei de fora
5. **Próximo corte** — a coisa mais valiosa que ficou de fora, uma só

Sem "espero que goste", sem resumo do que já está evidente.

## Referências

- `references/escolha-de-stack.md` — matriz de decisão por tipo de projeto e restrição, com o custo de cada escolha e quando ela deixa de servir. Consulte antes de fixar a stack.
- `references/identidade-visual.md` — método para derivar paleta, tipografia e layout do assunto; tokens para tema claro e escuro; armadilhas de CSS que produzem bug visual silencioso. Consulte antes de escrever a primeira linha de estilo.
