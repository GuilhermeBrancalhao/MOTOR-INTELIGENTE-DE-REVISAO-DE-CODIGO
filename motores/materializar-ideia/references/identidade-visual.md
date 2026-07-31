# Identidade visual — método

Referência do motor `materializar-ideia`. O objetivo não é "deixar bonito": é fazer a interface **derivar do assunto**, para que ela pareça feita para aquele problema e não um template com as cores trocadas.

---

## Antes de escolher qualquer cor

**1. Existe sistema visual no projeto?** Procure `CLAUDE.md`, arquivo de tokens ou tema, estilo de componente existente. Se existir, ele manda — o que está aqui só preenche lacuna.

**Precedência, sempre:** palavra do usuário > sistema existente no projeto > sua escolha.

**2. Qual é o assunto, concretamente?** O vocabulário do domínio é a fonte das decisões distintivas. Painel de fechamento contábil, ferramenta de conciliação, app de treino e catálogo de vinho não podem compartilhar a mesma cara. Instrumentos, materiais e jargão do assunto é onde mora a escolha específica.

**3. É documento ou é ferramenta?** Muda tudo:

- **Documento** — lido de cima a baixo. O trabalho é tipografia: hierarquia, medida de linha, respiro.
- **Ferramenta** — escaneada e operada. O trabalho é design de informação: resumo antes do detalhe, estado legível de relance, o que é clicável parece clicável.

---

## Calibre o tratamento

Nem tudo pede tratamento editorial. A maioria dos pedidos internos pede **utilitário polido**: hierarquia real, espaçamento pensado, paleta escolhida — sem herói gigante, sem floreio.

Tratamento editorial (identidade forte, um risco estético deliberado) cabe em vitrine, apresentação para cliente, algo que a pessoa vai guardar ou compartilhar.

Página bem composta nunca é resposta errada. Página superdesenhada às vezes é.

---

## Paleta

**Não use cinza neutro puro.** Cinza médio exato lê como não-escolhido. Puxe o cinza levemente na direção do acento — a diferença é quase imperceptível item a item e muito perceptível no conjunto.

Estrutura mínima: fundo, superfície, borda, texto, texto secundário, um acento. Semântico (bom/atenção/crítico) é **separado do acento** e não conta como ele.

**Gaste ousadia em um lugar só** e mantenha o resto quieto. Se o acento briga com o fundo, reduza a saturação ou mova para análogo — não troque por outra cor forte.

Branco puro e quase-preto são fundos legítimos quando servem ao assunto. O ponto é que a escolha foi feita, não herdada.

---

## Tipografia

Carrega a página mesmo quando a página não é sobre tipografia.

- **Duas famílias com papéis distintos** — uma de display usada com parcimônia, uma de texto. Uma terceira monoespaçada se houver dado ou código.
- **CDN de fonte é bloqueado em artifact.** `@font-face` com fonte embutida em data URI, ou stack de sistema. Nunca link de webfont que falha em silêncio e cai para fallback sem você ver.
- Texto corrido perto de **65 caracteres** por linha.
- Escala de tamanho definida e respeitada. Tamanho ad hoc a cada bloco é o que faz a página parecer montada às pressas.
- `text-wrap: balance` em título. `letter-spacing` leve em rótulo em caixa alta.
- `font-variant-numeric: tabular-nums` em qualquer coluna de número — sem isso, os dígitos dançam e a coluna fica ilegível. Obrigatório em tabela financeira.

---

## Repertório a evitar

O visual que hoje denuncia geração automática:

- Creme `#F4F1EA` com serifada de display e acento terracota
- Quase-preto com um único verde-ácido ou vermelhão de destaque
- Fios de hairline estilo jornal com colunas densas
- Gradiente roxo-para-azul no herói sobre branco
- Inter ou Space Grotesk como escolha "segura"
- Emoji marcando seção
- Tudo centralizado
- `border-radius` médio uniforme em tudo
- Cartão arredondado com barrinha de acento à esquerda
- Marcador numerado `01 / 02 / 03` em conteúdo que **não é sequência**

O último merece nota: numeração, divisória e rótulo devem codificar algo verdadeiro sobre o conteúdo. Numerar itens que não têm ordem é decoração fingindo ser estrutura.

**Se o usuário pediu uma dessas direções, faça exatamente ela.** A palavra dele vence.

---

## Tema claro e escuro

A página abre no tema de quem olha. Faça no nível de token:

```css
:root { --bg: #fff; --fg: #18181b; --accent: #0d6e6e; }

@media (prefers-color-scheme: dark) {
  :root { --bg: #101014; --fg: #e8e8ea; --accent: #4fd1c5; }
}

:root[data-theme="dark"]  { --bg: #101014; --fg: #e8e8ea; --accent: #4fd1c5; }
:root[data-theme="light"] { --bg: #fff;    --fg: #18181b; --accent: #0d6e6e; }
```

Regras:

- Componente estiliza **pelo token**, nunca dentro do bloco de media query. Estilo direto na media query não é sobrescrito pelo toggle e o tema quebra em uma das direções.
- `:root[data-theme]` precisa vencer a media query nos dois sentidos.
- **Não inverta ingenuamente.** O acento que funciona no claro costuma sumir no escuro; ajuste luminosidade e saturação em cada tema.
- Tema único é aceitável quando é escolha declarada (terminal, impresso, arcade). Não quando é esquecimento.

---

## Layout

- Espaçamento por `flex`/`grid` + `gap`, não por margem em cada elemento. Margem irmã colapsa ou dobra em silêncio.
- Conteúdo largo — tabela, código, diagrama — em contêiner próprio com `overflow-x: auto`. **O corpo da página nunca rola na horizontal.**
- Unidade relativa, `max-width: 100%` em imagem.
- Verifique em largura estreita antes de entregar.

---

## Interface de ferramenta

Quando é painel e não documento:

- **Resumo antes do detalhe.** O número que importa aparece antes da tabela que o origina.
- **Estado na forma, não só no número** — pílula, chip, faixa de severidade. O que precisa de atenção deve ser visível de relance, sem leitura.
- Gráfico e sparkline com o mesmo cuidado do texto: preenchimento de área, grade discreta, ponto final destacado.
- Foco de teclado com estado visível. `prefers-reduced-motion` respeitado.

---

## Texto da interface

Palavra é material de design.

- Nomeie pelo que a pessoa reconhece, não pela implementação. Ela gerencia *notificações*, não *configuração de webhook*.
- Voz ativa. O botão diz o que acontece: "Publicar" → aviso "Publicado".
- Erro diz o que falhou e como resolver. Sem desculpa, sem vago.
- Específico vence esperto.

---

## Bugs visuais silenciosos

- Especificidade de seletor em conflito — classe de seção brigando com classe de componente por `padding`. Estruture a cascata para não desfazer o próprio espaçamento.
- Fonte que caiu para fallback sem aviso.
- Elemento sobreposto por `z-index` acidental.
- Atributo sem aspas, elemento não fechado.
- Para gráfico gerado ou decorativo, prefira Canvas a `path` de SVG escrito à mão — SVG longo à mão é onde nascem erros invisíveis.
