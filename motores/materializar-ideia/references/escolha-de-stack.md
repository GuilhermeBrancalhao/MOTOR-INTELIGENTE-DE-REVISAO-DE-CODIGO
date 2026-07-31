# Escolha de stack — matriz de decisão

Referência do motor `materializar-ideia`. Cada opção traz o que ela custa e **o sinal de que ela deixou de servir** — porque a decisão errada normalmente não é a escolha inicial, é a insistência nela depois que o requisito mudou.

---

## O eixo que decide

Não é "qual framework". É **onde o estado vive**:

| Estado vive em | Stack mínima | Complexidade |
|---|---|---|
| Nenhum lugar (cálculo puro) | HTML + JS, arquivo único | Trivial |
| Memória da aba | idem, com estado em JS | Trivial |
| Navegador do usuário | idem + `localStorage`/IndexedDB | Baixa |
| Arquivo que o usuário controla | idem + import/export | Baixa |
| Servidor, um usuário | backend + SQLite | Média |
| Servidor, vários usuários | backend + Postgres + auth | Alta |
| Vários usuários simultâneos no mesmo dado | tudo acima + tempo real + resolução de conflito | Muito alta |

**Desça esta tabela apenas quando o requisito empurrar.** Cada linha adiciona modo de falha: rede, migração, sessão, concorrência. Pular direto para a última "porque um dia vai precisar" paga o custo hoje por um benefício hipotético.

O sinal honesto de que precisa de backend: **dois dispositivos diferentes precisam ver o mesmo dado**, ou existe segredo que o cliente não pode conhecer. Fora disso, provavelmente não precisa.

---

## Arquivo único (HTML + CSS + JS inline)

**Serve para** — calculadora, conversor, visualização de dado colado, gerador, simulador, protótipo de interface, ferramenta interna de uso pessoal.

**Ganha porque** — zero build, zero dependência, zero deploy. Abre com duplo clique, funciona offline, sobrevive a dez anos de bit rot. Manda por e-mail e funciona.

**Custa** — sem sistema de módulo, o arquivo fica grande. Acima de ~1500 linhas a navegação piora.

**Deixou de servir quando** — precisa persistir entre dispositivos, precisa esconder chave de API, ou passou de três telas com estado compartilhado entre elas.

**Como fazer bem** — seções comentadas na ordem: tokens de estilo, estilo, marcação, modelo, casos de uso, render, inicialização. Módulo ES via `<script type="module">` funciona em arquivo local moderno.

---

## Framework de componente com build

**Serve para** — interface com muito estado derivado, formulário complexo com validação interdependente, navegação real, tabela com ordenação e filtro e paginação simultâneos.

**Ganha porque** — estado derivado deixa de ser sincronizado à mão. É exatamente aí que a manipulação direta de DOM começa a produzir bug de atualização parcial.

**Custa** — cadeia de build, `node_modules`, versão de runtime, e o projeto deixa de abrir com duplo clique.

**Deixou de servir quando** — nunca, para app real. Mas **nunca serviu** se o projeto era uma calculadora: aí o custo de build foi pago por nada.

**Sinal de que era necessário desde o início** — você escreveu a terceira função que atualiza dois pedaços da tela para manter um valor consistente.

---

## Backend

**Só entra quando** pelo menos uma for verdadeira:

- Dado compartilhado entre dispositivos ou pessoas
- Segredo que o cliente não pode ver (chave de API de terceiro, regra de precificação)
- Regra que o cliente não pode burlar (autorização, limite, cobrança)
- Trabalho longo que não pode depender da aba aberta

**Se nenhuma for verdadeira, backend é custo puro.**

### Banco

| Escolha | Quando | Cuidado |
|---|---|---|
| SQLite (arquivo) | Um processo, leitura predominante, ferramenta local | Escrita concorrente serializa; não use com múltiplas instâncias |
| Postgres | Padrão para qualquer coisa multiusuário | Precisa de infra; use container em desenvolvimento |
| Chave-valor | Cache, sessão, fila simples | Não é fonte de verdade; assuma que pode perder |
| Documento | Schema genuinamente irregular por documento | Sem transação entre coleções na maioria dos casos; sem migração, o schema irregular vira dívida silenciosa |

**Padrão razoável:** Postgres. Se a resposta a "por que não Postgres" for "não sei", é Postgres.

**Regra sem exceção:** schema versionado por migração desde a primeira tabela. Geração automática de schema em ambiente que não é descartável é defeito, não conveniência — porque o dia em que você precisa reverter é o dia em que não há como.

---

## Decisões que dependem da restrição dura

**"Precisa rodar offline"** → arquivo único ou app com service worker. Elimina backend como caminho crítico. Se há sincronização, ela é oportunista, e você precisa de estratégia de conflito antes de escrever a primeira linha.

**"Não posso instalar nada"** → arquivo único, ou linguagem já presente na máquina. Em Windows corporativo, PowerShell costuma estar disponível quando Node não está.

**"Dado sensível / LGPD"** → o dado não sai do cliente sem necessidade demonstrada. Se sair: em trânsito cifrado, mínimo necessário coletado, retenção definida, log sem PII. Isso é decisão de arquitetura, não de configuração — muda onde o processamento acontece.

**"Preciso mostrar amanhã"** → uma vertical completa e polida. Cinco telas mockadas impressionam menos que uma que funciona, e não sobrevivem à primeira pergunta da plateia.

**"Vai integrar com sistema X"** → descubra o contrato real de X **antes** de escolher a stack. Se X só fala SOAP ou só tem driver para uma linguagem, isso decide mais que qualquer preferência.

---

## Armadilhas

**Escolher pelo currículo.** A stack certa é a que atende o requisito com menos peça móvel — não a mais interessante de aprender. Se o usuário quer aprender algo específico, ele diz.

**Microserviço sem organização para sustentar.** Serviço separado exige que alguém opere o que está entre eles: rede, versão de contrato, observabilidade distribuída, transação que virou eventual. Monolito modular entrega o mesmo isolamento lógico sem a conta operacional. Comece monolito com fronteira clara; separe quando houver motivo nomeável — equipe independente ou perfil de escala genuinamente diferente.

**Autenticação artesanal.** Nunca implemente hash de senha, fluxo de token ou reset por conta própria. Use o que o ecossistema já auditou. Este é o caso em que dependência nova é obrigatoriamente mais barata que código próprio.

**ORM sem entender o SQL gerado.** Ganha velocidade no começo e cobra em consulta que multiplica com o volume. Saiba qual SQL sai; onde não souber, escreva o SQL.

**Otimizar antes de medir.** Cache, índice e assincronismo adicionados por antecipação escondem o gargalo real e adicionam invalidação — que é uma classe de bug nova. Meça primeiro, sempre.
