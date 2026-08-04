# ROADMAP

**Atualizado em:** 2026-08-04

**Estado hoje: os 42 volumes do contrato estão `PRONTO`.** A cobertura integral foi alcançada em
2026-08-04, com o último lote (`41-SDK`, `42-PLUGINS`). Cada volume atravessou os quatro
critérios da Definição de PRONTO: gate estrutural, exemplo executável com testes, auditoria com
média ≥8,0 registrada em `auditorias/`, e entrada no `CHANGELOG.md`. `ferramentas.validar --tudo`
e `--cross-refs` sem violação. `volumes/prontos/` é artefato derivado, regenerado por
`ferramentas.sincronizar` — nunca editado à mão.

**Correção de 2026-08-04:** este arquivo afirmou antes que a "suíte completa do repositório
(motor + acervo + exemplos)" era de 449 testes. **Está errado.** 449 é só a suíte do motor, a
única que a raiz coleta — o `pytest.ini` explica por quê (dois pacotes `ferramentas`, o da raiz e
o de `acervo/`, colidem numa sessão só de pytest). Os números reais são **449 na raiz** e **789
rodando de dentro de `acervo/`**, e não existe comando único que rode as duas. Somar as duas ou
citar uma como se fosse o todo é o erro que estava aqui.

**Histórico da decisão de escopo (2026-08-03), mantido para contexto:** o ciclo daquele dia
fechava em motor + 10 volumes essenciais (`01`, `03`, `07`, `08`, `09`, `10`, `12`, `17`, `21`,
`31`), com os outros 32 em `RASCUNHO` declarado e cobertura dos 42 explicitamente fora de meta.
Essa decisão foi superada pela produção subsequente: os 32 restantes foram escritos em lotes ao
longo de 2026-08-03 e 2026-08-04, cada um pelo mesmo processo dos 10 primeiros, sem afrouxar
nenhum gate.

## Verificação do merge dos dois históricos (2026-08-04)

A unificação decidida em 2026-08-02 — motor de revisão de código + plataforma de engenharia de
projetos de IA num repositório só — foi conferida e **está íntegra**:

- `ecd5fdd` é merge real de dois pais (`544cc6b` do lado motor, `bf95c57` do lado plataforma),
  não uma reimportação achatada;
- o histórico tem **duas raízes** (`de733fb`, motor, 2026-07-30; `a553dfa`, plataforma,
  2026-07-29), confirmando que dois históricos independentes foram fundidos com autoria e datas
  preservadas;
- as três referências do remoto `plataforma` (`main`, `copilot/criar-interface-projeto`,
  `feat/volume-03-descoberta`) estão **totalmente contidas** em `HEAD` — nada ficou para trás;
- `HEAD`, `origin/master` e `motor/master` apontam para o mesmo commit.

### Dívida achada na conferência: `acervo-controladoria/` está fora de todo gate

Um segundo acervo, `acervo-controladoria/` (12 volumes, `43`–`54`, 262 arquivos), entrou no
repositório por commits de outra sessão durante a unificação. Ele tem `contrato.json` e
`Convencoes.md` próprios, mas **nenhuma ferramenta, teste ou gate deste repositório o referencia**:
não é validado por `ferramentas.validar`, não aparece na suíte, não é sincronizado para
`volumes/prontos/`, e não é mencionado em nenhum `CHANGELOG` ou `README`.

Consequência prática: a afirmação "42/42 `PRONTO`" é verdadeira sobre `acervo/` e **não diz nada**
sobre `acervo-controladoria/`. É preciso decidir — decisão do autor, não delegável — se esse
acervo (a) entra no contrato e passa a ser gated como os outros, (b) vira repositório próprio, ou
(c) é reduzido ao que nele é real.

**Medido em 2026-08-04, laudo completo em
[acervo-controladoria/ESTADO.md](../acervo-controladoria/ESTADO.md):** 420 violações no total.
Um volume conforme (`45-CONCILIACAO-CONTAS`, zero violações, 5.665 palavras, 6 módulos de
exemplo), um parcial (`54-INTEGRACAO-ERP`) e **dez esqueletos** de ~15 palavras por seção. Os 30
testes de `acervo-controladoria/exemplos/` passam mas **nenhuma suíte os coleta**.

A medição também expôs um mascaramento: o total aparente era 186 porque seis volumes reprovavam
por `volume-tipo` e o validador parava ali, sem examinar as 18 seções. Alinhados os tipos ao
contrato, apareceram as 234 violações restantes. **É a mesma classe do bug de BOM UTF-8 de
2026-08-03** (39 aparentes → 657 reais): erro que reprova cedo esconde todo o resto. Regra geral
para este repositório — quando um gate reprovar por metadado, o total não é confiável até o
metadado estar correto.

Verificado também que `acervo-controladoria/` **não vaza o projeto vizinho**: as únicas
ocorrências de "Omie" o citam como fornecedor de ERP genérico ao lado de SAP, Oracle e IFS, e não
há qualquer menção a Sicoob, Rezoluti ou nome de cliente. Mesma conclusão para
`ferramentas/web.py` e `chatgpt_app/widget.html`, onde "Omie" aparece só como exemplo em
`placeholder` de formulário.

A ordem de produção não é a ordem numérica. Um volume só deve ser escrito depois dos volumes
que ele declara em `depende_de`, porque `depende_de` significa pré-requisito de leitura — e
escrever fora de ordem produz seções que citam contrato que ainda não existe.

## Metas numéricas do autor

A especificação original declarava, como resultado esperado:

- 8.000+ páginas
- 2.000+ prompts
- 300+ agentes
- 500+ exemplos de código funcionais

**Estes números são estimativa da especificação original e explicitamente não são critério de
aceite desta plataforma.** Ficam registrados aqui para preservar a intenção do autor, não
para medir progresso.

A razão é direta: **contagem de páginas premia enchimento.** Um acervo avaliado por volume de
texto tem incentivo para escrever mais, não melhor — e a única forma de preencher 42 volumes
por 18 seções, ou seja 744 arquivos de seção, é deixar o conteúdo genérico. Isso contradiz a
regra que a própria especificação estabeleceu: nunca gerar conteúdo superficial. Duas metas
que se anulam não são duas metas; são uma escolha adiada.

O critério de aceite é a **Definição de PRONTO**, descrita em
[00-INTRODUCAO/Convencoes.md](00-INTRODUCAO/Convencoes.md): gate estrutural verde, testes dos
exemplos verdes, auditoria com média maior ou igual a 8,0 sem nenhuma seção abaixo de 6, e
registro datado no `CHANGELOG.md`. É um critério que o **gate mede** em vez de estimar — ele
reprova prosa abaixo do mínimo, diagrama sem descrição, exemplo sem teste e link morto, e não
tem nenhuma opinião sobre quantas páginas o volume tem.

Consequência prática, para quem for produzir: se um volume ficar mais curto do que a
estimativa sugeria e passar nos três gates com auditoria acima de 8,0, ele está pronto. Se
ficar longo e reprovar, não está. O número de páginas nunca entra na decisão.

Um contraponto honesto: o limiar de palavras por seção (200 no geral, menos em quatro seções
naturalmente curtas) é uma contagem, e portanto tem o mesmo defeito em miniatura. Ele existe
como **piso, não como meta** — reprova vazio, não premia extensão — e conta apenas palavras
de prosa, ignorando código, justamente para não poder ser satisfeito colando arquivos.

## Volumes pendentes

Quantidade de seções por tipo: `ENGINE`, `ARQUITETURA` e `GOVERNANCA` exigem as 18 da base;
`PROCESSO` dispensa `08-Modelos` (17); `BIBLIOTECA` troca `04-Arquitetura` e `05-Diagramas`
por `04-Catalogo` (17). Somados, os 40 pendentes representam 708 arquivos de seção.

| Vol | Nome | Tipo | Seções | Observação |
|---|---|---|---|---|
| 01 | FUNDACAO | GOVERNANCA | 18 | base conceitual; candidato natural a ser o próximo |
| 02 | CORE | ARQUITETURA | 18 | depende de 01 |
| 03 | DISCOVERY | PROCESSO | 17 | |
| 04 | REQUIREMENTS | PROCESSO | 17 | |
| 05 | BUSINESS | PROCESSO | 17 | |
| 06 | ENTERPRISE-ARCHITECTURE | ARQUITETURA | 18 | |
| 08 | AGENT-ENGINE | ENGINE | 18 | vizinho direto do piloto; exemplos executáveis obrigatórios |
| 09 | ORCHESTRATOR | ENGINE | 18 | fronteira com 10 precisa ser explícita |
| 10 | WORKFLOW | ENGINE | 18 | fronteira com 09 precisa ser explícita |
| 11 | KNOWLEDGE | ENGINE | 18 | a fonte do conhecimento; fronteira decidida contra 13, 14 e 15 |
| 13 | RAG | ENGINE | 18 | o pipeline; depende de 11 e 14; fronteira decidida |
| 14 | VECTOR | ENGINE | 18 | o índice; fronteira decidida contra 11, 13 e 15 |
| 15 | CONTEXT | ENGINE | 18 | o orçamento da janela; vale sem RAG; fronteira decidida |
| 16 | INTEGRATION | ARQUITETURA | 18 | a fronteira do produto; 22 a 25 são as camadas internas |
| 17 | SECURITY | GOVERNANCA | 18 | política e controles; o processo é o 18 |
| 18 | DEVSECOPS | PROCESSO | 17 | o processo que roda os controles do 17 |
| 19 | DEVOPS | ARQUITETURA | 18 | |
| 20 | CLOUD | ARQUITETURA | 18 | |
| 21 | OBSERVABILITY | GOVERNANCA | 18 | |
| 22 | FRONTEND-ARCHITECT | ARQUITETURA | 18 | camada interna; o que cruza a fronteira do produto é 16 |
| 23 | BACKEND-ARCHITECT | ARQUITETURA | 18 | |
| 24 | DATABASE-ARCHITECT | ARQUITETURA | 18 | |
| 25 | API-ARCHITECT | ARQUITETURA | 18 | |
| 26 | AI-MODELS | ENGINE | 18 | **perecível**: fino, sem preço nem nome de modelo fixado |
| 27 | LLM-ROUTER | ENGINE | 18 | **perecível**: método de roteamento, não tabela de custo |
| 28 | PROMPT-COMPILER | ENGINE | 18 | compila o prompt do 07 para um provedor; depende de 07 |
| 29 | PROMPT-OPTIMIZER | ENGINE | 18 | busca variantes usando os casos de ouro do 07; depende de 07 |
| 30 | AI-GOVERNANCE | GOVERNANCA | 18 | |
| 31 | TESTING | PROCESSO | 17 | a prática de testar; o indicador agregado é o 32 |
| 32 | QUALITY | PROCESSO | 17 | o indicador agregado; a prática é o 31 |
| 33 | PERFORMANCE | PROCESSO | 17 | |
| 34 | COST-OPTIMIZATION | PROCESSO | 17 | **perecível**: método de medir custo por tarefa |
| 35 | DOCUMENTATION | GOVERNANCA | 18 | |
| 36 | DIAGRAMS | BIBLIOTECA | 17 | catálogo em `04-Catalogo`, sem arquitetura própria |
| 37 | CODE-GENERATION | ENGINE | 18 | |
| 38 | PROJECT-PLANNER | PROCESSO | 17 | |
| 39 | ROADMAP | PROCESSO | 17 | |
| 40 | TEMPLATES | BIBLIOTECA | 17 | catálogo em `04-Catalogo` |
| 41 | SDK | ENGINE | 18 | hoje só esqueleto e `README` de intenção |
| 42 | PLUGINS | ENGINE | 18 | |

## Decisão tomada: sobreposição de domínios resolvida por fronteira, não por fusão

**Data da decisão: 2026-07-29. Delegada pelo autor.**

Os 42 rótulos cobrem cerca de 25 domínios distintos, e quatro grupos se sobrepõem de forma que
geraria contradição entre volumes. Havia duas saídas: fundir volumes, reduzindo a contagem; ou
manter os 42 e declarar no `03-Escopo` de cada um o que pertence ao vizinho.

**Escolhida a segunda.** Fundir reduziria a contagem mas destruiria o índice que o autor
definiu, e o índice tem valor próprio: cada rótulo é um lugar onde alguém vai procurar
informação. O `03-Escopo` de `07-PROMPT-ENGINE` é a implementação de referência — ele declara,
em texto, que compilação multi-modelo é o volume 28 e otimização automática é o 29.

Regra que passa a valer: **todo volume de um grupo sobreposto declara a fronteira no seu
`03-Escopo`, nomeando o volume vizinho e o que pertence a ele.** Fronteira ausente é lacuna de
conteúdo, e é o que a auditoria deve cobrar na seção 03.

### As fronteiras, por grupo

**Grupo 1 — prompts (`07`, `28`, `29`).** O eixo é *o que cada um faz com um prompt*.

| Volume | Fica com | Não fica com |
|---|---|---|
| `07-PROMPT-ENGINE` | o contrato do prompt: template tipado, versionamento por hash, casos de ouro, avaliação, ciclo de vida até a promoção | nada de provedor, nada de busca automática |
| `28-PROMPT-COMPILER` | transformar um prompt já versionado em payload concreto de um provedor: dialeto, ordem de mensagens, orçamento de tokens, pontos de cache | definir o contrato do prompt — ele **consome** o do 07 |
| `29-PROMPT-OPTIMIZER` | busca automática sobre variantes, usando os casos de ouro do 07 como função objetivo | definir contrato e compilar payload — ele **propõe** variantes que o 07 versiona e o 28 compila |

**Grupo 2 — conhecimento e contexto (`11`, `13`, `14`, `15`).** O eixo é *fonte, índice, pipeline e janela*.

| Volume | Fica com | Não fica com |
|---|---|---|
| `11-KNOWLEDGE` | a fonte: curadoria, ingestão, autoridade, ciclo de vida e expiração do documento | recuperação e ranqueamento |
| `14-VECTOR` | o índice: embedding, métrica de similaridade, particionamento, operação do banco vetorial | decidir o que fazer com o resultado da busca |
| `13-RAG` | o pipeline que junta 11 e 14 numa resposta: recuperar, reordenar, citar, medir fidelidade | curar a fonte e operar o índice |
| `15-CONTEXT` | o orçamento da janela: o que entra, em que ordem, o que é descartado, quando compactar | recuperação — o 15 vale mesmo em sistema **sem** RAG, e é por isso que é volume separado |

**Grupo 3 — segurança e qualidade (`17`/`18`, `31`/`32`).** O eixo é *o que precisa ser verdade* contra *como se verifica continuamente*.

| Volume | Fica com |
|---|---|
| `17-SECURITY` | a política e os controles: o que precisa ser verdade sobre o sistema |
| `18-DEVSECOPS` | o processo que faz os controles do 17 rodarem no pipeline, a cada mudança |
| `31-TESTING` | a prática: como se escreve, organiza e mantém teste |
| `32-QUALITY` | o indicador agregado: cobertura, gates de release, dívida, tendência ao longo do tempo |

**Grupo 4 — camadas contra integração (`22`–`25` vs `16`).** O eixo é a **fronteira do produto**.
Chamada entre camadas do mesmo produto é assunto de `22`–`25`. Chamada que cruza a fronteira
do produto — outro time, outro fornecedor, outro ciclo de release — é assunto de `16`, com o
que isso traz: contrato versionado, idempotência, tolerância a falha do outro lado.

### Consequência para o `depende_de`

Nos grupos 1 e 2 a fronteira implica pré-requisito de leitura, e o grafo continua acíclico:
`28` e `29` dependem de `07`; `13` depende de `11` e `14`. Nos grupos 3 e 4 a relação é lateral
— fica em `18-Referencias-Cruzadas`, fora do grafo, porque `depende_de` é pré-requisito, não
vizinhança.

## Decisão que permanece com o autor, e não pode ser delegada

Os 13 nomes de framework em `frameworks/_backlog.md` (ORBIT, FLOW, NEXUS, FUSION, GENESIS,
ATLAS, EVEREST, QUANTUM, IDEA+, PACE, BUILD, SMART-AI, ENTERPRISE-AI) vieram da especificação
**sem definição nenhuma**. Diferente da sobreposição de domínios — onde havia informação
suficiente para escolher um critério — aqui não há o que decidir: qualquer escopo que eu
atribuísse a esses nomes seria invenção, e inventar é a única coisa que esta plataforma proíbe
sem exceção. Eles permanecem no backlog até que o autor defina escopo, entradas e saídas.

## Dívida técnica registrada

### Colisão do pacote `tests` entre diretórios de exemplo

**Sintoma.** Dois ou mais `exemplos/<vol>/tests/` com `__init__.py` reivindicam o mesmo nome de
pacote de topo, `tests`. Rodar a suíte de exemplos inteira — `python -m pytest exemplos -q` —
quebra com `ModuleNotFoundError` no segundo diretório coletado: o primeiro ganha o nome e o
segundo passa a procurar os seus módulos dentro dele. Rodar volume por volume
(`python -m pytest exemplos/12-memory -q`) esconde o problema, e é assim que o gate 2 roda hoje,
o que explica por que nada reprovou.

**Solução usada no `12-memory`.** O diretório `exemplos/12-memory/tests/` **não** tem
`__init__.py`, de modo que cada arquivo é importado pelo nome-base (`test_precedencia`), único no
acervo. O preço é que a pasta do exemplo deixa de entrar no caminho de import automaticamente, e
`exemplos/12-memory/conftest.py` paga esse preço em três linhas, inserindo o próprio diretório em
`sys.path`. A escolha está documentada no docstring do `conftest.py`.

**Estado do `07-prompt-engine`.** Continua na abordagem antiga. Não foi tocado de propósito: o
volume está selado, e unificar convenção mexendo em volume selado troca uma dívida registrada por
uma alteração não auditada.

**Estado em 2026-08-03.** O acervo passou de 2 para 9 pastas de exemplo, e as sete novas
(`01`, `08`, `09`, `10`, `17`, `21`, `31`) seguiram a convenção do `12-memory`: `tests/` sem
`__init__.py`, mais um `conftest.py` de três linhas por exemplo. **`07-prompt-engine` é agora o
único fora do padrão** — ainda tem `__init__.py` em `tests/`. Como só ele reivindica o nome de
pacote `tests`, a colisão não se manifesta, e `python -m pytest exemplos -q` roda inteiro:
**238 testes, todos verdes**.

**O que falta.** Remover o `__init__.py` de `exemplos/07-prompt-engine/tests/` e dar-lhe o mesmo
`conftest.py` dos outros oito — mexer em volume selado exige reauditoria do `07`, que é o motivo
de não ter sido feito ainda. E escrever a convenção em
[00-INTRODUCAO/Convencoes.md](00-INTRODUCAO/Convencoes.md), com uma verificação no gate que
reprove `__init__.py` dentro de `exemplos/*/tests/` — hoje nada impede o padrão errado de voltar.

**A previsão se confirmou em 2026-08-04.** `08-agent-engine/orcamento.py` e
`15-context/orcamento.py` reivindicaram o mesmo nome de módulo — sem `__init__.py`, pytest
importa cada `test_orcamento.py` pelo basename, e o segundo colide com o primeiro já em cache
(`import file mismatch`). Corrigido renomeando o de `15-context` para `orcamento_contexto.py`
(módulo e teste), mas a causa raiz continua: **nada além de escolha manual de nome único evita a
colisão**, e com 9 pastas de exemplo (crescendo a cada lote de volumes promovidos), a chance de
duas escolherem o mesmo nome genérico (`orcamento`, `modelo`, `processo`) só aumenta. A
verificação de gate que reprovaria isso automaticamente continua não implementada.

**Segunda colisão confirmada em 2026-08-04.** `13-rag/pipeline.py` e `19-devops/pipeline.py` —
mesmo padrão, mesmo tipo de nome genérico (`pipeline`). Corrigido renomeando o de `19-devops`
para `pipeline_deploy.py` (módulo e teste), citação em `11-Implementacao.md` atualizada. Duas
colisões reais em nomes genéricos diferentes (`orcamento`, `pipeline`) em menos de 24h de
produção reforça que isto não é caso isolado — a verificação de gate continua sendo o item mais
alto de prioridade desta dívida, não apenas uma melhoria nice-to-have.

## Fora de escopo neste ciclo

Registrado, não construído agora:

- os 41 volumes com conteúdo (apenas `_VOLUME.yml` e registro de pendência);
- o SDK além do esqueleto e um `README` de intenção;
- a biblioteca de agentes além do `_template-agente.md` e do `_catalogo.md`;
- as bibliotecas de prompts por stack, banco e framework além do que o piloto usa;
- diagramas soltos em `diagramas/` (o piloto tem os seus dentro do volume);
- integração contínua rodando os gates a cada push;
- os frameworks sem definição listados em `frameworks/_backlog.md`, que aguardam o autor
  definir escopo, entradas e saídas — não serão inventados.
