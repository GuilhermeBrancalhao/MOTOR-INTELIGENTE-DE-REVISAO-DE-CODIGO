# Checklist expandido — condição de falha e correção

Referência consultada pelo motor `revisar-codigo`. Cada item é um par sintoma → condição que dispara → correção. Use para justificar achado com precisão, não como lista para percorrer inteira.

---

## Defeito — quebra com entrada alcançável

### Acesso a coleção sem verificar cardinalidade

`items[0]`, `.first()`, `.head`, desestruturação posicional.

**Dispara** com coleção vazia. Fonte mais comum: resultado de query filtrada, `split` de string sem o separador, resposta de API que retornou lista vazia em vez de erro.

**Correção** — acesso seguro com valor padrão explícito, ou guard no topo. Não envolva em `try/catch`: exceção como fluxo de controle esconde que o caso vazio é esperado.

### Erro engolido

`catch {}`, `except: pass`, `if err != nil {}` sem tratamento, `.catch(() => {})`.

**Dispara** sempre — o defeito é a invisibilidade. O sistema segue com estado inválido e falha depois, em lugar sem relação com a causa.

**Correção** — trate, propague ou registre com contexto. Se o erro é genuinamente ignorável, escreva o comentário dizendo por quê; `catch` vazio sem comentário é indistinguível de esquecimento.

### Aritmética sobre valor de origem externa

Divisão, módulo, índice calculado, alocação dimensionada por entrada.

**Dispara** com zero, negativo, ou valor acima do esperado. Divisão por zero e alocação por valor negativo são os dois caminhos.

**Correção** — valide faixa na borda, uma vez, e trafegue tipo já validado para dentro. Validação repetida em cada camada é sinal de que a borda não existe.

### Ponto flutuante comparado por igualdade

`if (a == b)` sobre `float`/`double`, acumulação de soma em laço, dinheiro em ponto flutuante.

**Dispara** com qualquer valor não representável em binário — `0.1 + 0.2 != 0.3`. Em dinheiro, dispara na primeira fatura.

**Correção** — tolerância explícita na comparação; para dinheiro, inteiro de centavos ou tipo decimal. Nunca `float` para valor monetário.

### Data sem fuso

`now()` sem timezone, data serializada sem offset, diferença entre datas em fusos distintos.

**Dispara** na virada de horário de verão, em usuário de outro fuso, ou em servidor com TZ diferente do banco. Bug clássico de "o relatório de ontem sumiu".

**Correção** — armazene em UTC com offset, converta só na apresentação. Aritmética de calendário com biblioteca de data, nunca somando segundos.

### Entrada concatenada em interpretador

SQL, comando de shell, path de arquivo, template de HTML, expressão de query NoSQL.

**Dispara** com entrada contendo o metacaractere do interpretador. Não depende de má-fé: `O'Brien` quebra SQL concatenado sem nenhum atacante envolvido.

**Correção** — parâmetro vinculado para SQL, argumento em vetor para processo, normalização e verificação de prefixo para path, escape do motor de template para HTML. Sanitização por lista de bloqueio não conta: a lista sempre está incompleta.

---

## Risco — quebra sob condição

### Retry sobre operação não idempotente

Reenvio automático de POST, retry em fila, cliente com política de repetição.

**Dispara** quando a primeira tentativa teve efeito mas a resposta se perdeu. Resultado: cobrança dupla, e-mail duplicado, registro repetido.

**Correção** — chave de idempotência propagada pelo chamador e verificada no servidor. Backoff exponencial com jitter. Sem a chave, o retry é aposta.

### Operação de rede sem timeout

Cliente HTTP, conexão de banco, chamada gRPC, leitura de socket com default do runtime.

**Dispara** quando o outro lado aceita a conexão e não responde. Sem timeout, a thread ou a conexão do pool fica presa; sob carga, o pool esgota e o serviço inteiro para por causa de uma dependência lenta.

**Correção** — timeout de conexão e de leitura explícitos, sempre. Somados, menores que o timeout de quem chama você — caso contrário o cliente desiste antes e você trabalha para ninguém.

### Estado compartilhado sem proteção

Campo mutável em objeto usado por múltiplas threads, cache global, contador, coleção não sincronizada, lazy init sem guarda.

**Dispara** sob concorrência real — pode passar meses em ambiente de baixo tráfego. Falha não determinística, difícil de reproduzir.

**Correção** — imutabilidade primeiro; sincronização quando o estado precisa mudar; estrutura concorrente própria quando a operação é atômica de fato. `synchronized` em método longo troca corretude por contenção — reduza o escopo do lock.

### Ordem de lock divergente

Dois caminhos que adquirem os mesmos dois locks em ordens diferentes.

**Dispara** com as duas rotas em execução simultânea. Deadlock, não erro — o processo trava sem log.

**Correção** — ordem global de aquisição documentada e seguida. Onde não é viável, timeout na aquisição com falha explícita.

### Verificação separada do uso

`if (exists(path)) open(path)`, checagem de saldo seguida de débito, teste de unicidade antes de inserir.

**Dispara** quando algo muda entre a checagem e o uso. Em arquivo é vetor de segurança; em saldo é dinheiro.

**Correção** — operação atômica que já carrega a verificação: insert com restrição de unicidade e tratamento do conflito, update condicional, `compare-and-swap`. Nunca dois passos onde o banco oferece um.

### Consulta que cresce com o resultado

Laço que consulta dentro da iteração, associação carregada item a item, chamada de API por elemento de lista.

**Dispara** quando o volume cresce. Rápido com 10 registros, timeout com 10 mil — e o teste usou 3.

**Correção** — busque o conjunto em uma operação: join, projeção, batch, `IN`. Se a API não oferece batch, paralelize com limite de concorrência.

### Recurso sem liberação garantida

Arquivo, conexão, lock, socket fechado no caminho felizmente linear.

**Dispara** quando há retorno antecipado ou exceção no meio. Vazamento acumulativo: o serviço degrada ao longo de horas.

**Correção** — construção da linguagem que garante liberação (`with`, `defer`, `try-with-resources`, `using`), não fechamento manual no fim do bloco.

### Unbounded

Coleção que só cresce, fila sem limite, cache sem expiração, upload sem tamanho máximo, paginação ausente.

**Dispara** com uso sustentado. Termina em falta de memória.

**Correção** — limite explícito e política ao atingi-lo: rejeitar, descartar o mais antigo, aplicar contrapressão. Escolher a política é decisão de produto — se não estiver clara, pergunte.

---

## Design — funciona, custa depois

### Efeito colateral capturado do ambiente

Leitura direta de relógio, aleatório, variável de ambiente, sistema de arquivos ou rede no meio da regra de negócio.

**Custo** — a regra só é testável subindo o ambiente. Teste de regra pura vira teste de integração: lento, instável, e por isso ninguém roda.

**Correção** — injete a fonte do efeito. O relógio é parâmetro, não chamada global.

### Invariante duplicada

Mesma validação em duas ou mais camadas, com risco de divergir.

**Custo** — uma cópia é atualizada, a outra não. O bug aparece no caminho que usa a cópia velha.

**Correção** — invariante em um lugar: no tipo, no construtor, na entidade. Validação de borda existe para rejeitar entrada malformada cedo, não para reimplementar a regra.

### Abstração vazada

Interface cujo contrato só faz sentido para uma implementação: parâmetro que é detalhe do banco, exceção específica de driver atravessando a porta, método `flush` em repositório.

**Custo** — a abstração não isola nada, mas cobra o preço da indireção. Trocar a implementação exige mudar o contrato.

**Correção** — defina a porta pelo que o domínio precisa, não pelo que a tecnologia oferece. Porta que só delega uma chamada é cerimônia — vale dizer isso explicitamente.

### Dependência para dentro invertida

Política de negócio importando detalhe de infraestrutura.

**Custo** — o núcleo não compila sem o framework, não testa sem o banco, e migração de tecnologia toca regra de negócio.

**Correção** — inverta com interface possuída pelo domínio. Implementação na borda, injetada.

### Função com mais de uma razão para mudar

Método que valida, transforma, persiste e notifica.

**Custo** — cada motivo de mudança toca o mesmo bloco; teste precisa preparar tudo para verificar uma parte.

**Correção** — separe por motivo de mudança, não por número de linhas. Função de 60 linhas com uma responsabilidade é melhor que seis de 10 acopladas por estado compartilhado.

### Booleano de configuração em assinatura

`process(data, true, false)`.

**Custo** — ilegível na chamada, e cada flag dobra os caminhos a testar.

**Correção** — enum nomeado, ou funções separadas. Duas funções claras vencem uma parametrizada.

---

## Estilo — legibilidade

- **Nome que engana** é pior que nome vago: `getUser` que cria usuário, `isValid` que lança, `list` que é mapa. Corrija o nome ou o comportamento.
- **Comentário que descreve o que o código faz** duplica e envelhece. Comentário útil explica *por quê* — a decisão, a restrição externa, o motivo da escolha não óbvia.
- **Aninhamento profundo** geralmente é guard-clause ausente. Trate o caso excepcional e saia cedo.
- **Número mágico** sem nome: constante nomeada, especialmente se aparece duas vezes.
- **Inconsistência com o arquivo ao redor** — se o resto usa um padrão, seguir o padrão vale mais que a preferência pessoal. Divergência local custa atenção em toda leitura futura.
