"""Elicitação de requisitos: as 37 lacunas que uma especificação precisa fechar.

**Por que este pacote existe.** O catálogo de lacunas, a detecção de plataforma e
contexto, o controle de entrevista e a geração da especificação viviam inteiros em
`acervo/exemplos/03-discovery/` — como material didático de um volume. Estavam
escritos, testados e provados, e **nenhuma linha de `ferramentas/` os conhecia**:
37 lacunas com pergunta, motivo declarado e peso, desligadas da máquina que conduz
o ciclo. Exemplo não se importa; o que não se importa não roda em projeto nenhum.

Este pacote é a cópia importável desse exemplo. A origem permanece publicada e
intocada — é material do acervo e continua sendo lido como texto —, e a única
diferença entre os dois lados são seis linhas de `import`, que aqui são relativas
porque aqui isto é pacote e lá era um diretório posto no `sys.path` por um
`conftest.py`. Manter a diferença nesse tamanho é deliberado: o port se audita com
um `diff`, e qualquer divergência de comportamento aparece como linha a mais.

**Quatro módulos, não um.** A separação carrega a política de projeto do exemplo e
sobrevive à cópia:

- `catalogo`: o conjunto de lacunas e a condição que torna cada uma relevante. Não
  ordena e não decide o que perguntar.
- `deteccao`: o que se infere da frase inicial, sempre com o trecho que provou.
  Não confirma nada.
- `entrevista`: qual pergunta vem agora e quando para de valer a pena perguntar.
- `especificacao`: o retrato congelado — o decidido, o aberto e o inferido que
  ninguém confirmou.

Trocar a heurística de ordenação sem tocar no conteúdo das perguntas, e revisar o
conteúdo das perguntas sem risco de mudar o comportamento do controle, é o que essa
divisão compra. Juntar os quatro num módulo só devolveria 1466 linhas ilegíveis e
perderia a fronteira.

**Um quinto módulo, este daqui de dentro.** `taxonomia` não veio do exemplo: é o
terceiro eixo, a **intenção** — que trabalho o pedido pede —, e ele mora à parte
justamente para não estragar o `diff` dos outros quatro. Os quatro portados cruzam
plataforma com contexto e, para qualquer pedido, fazem as mesmas trinta e sete
perguntas; `taxonomia` acrescenta as perguntas que só existem porque alguém quer
otimizar em vez de criar, ou evoluir em vez de revisar. Ele lê `catalogo` e reusa o
casamento por termo de `deteccao`, e nenhum dos dois sabe que ele existe.

**Um sexto módulo, também local.** `bloqueio` é a regra que decide o que **trava** o
plano: uma lacuna é bloqueante se responder muda quais outras perguntas existem (B1),
se ela é universal (B2), ou se sem ela não se escreve critério de aceite falsificável
(B3). Todo o resto é assumível — e assumível sai como decisão aberta com a pergunta
inteira, nunca como valor chutado. Ele lê os outros e nenhum deles sabe que ele existe;
a persistência do resultado mora fora do pacote, em `ferramentas/descoberta.py`, porque
aqui dentro não se importa nada além da biblioteca padrão.

**Só biblioteca padrão**, como todo o resto de `ferramentas/`: o plugin se instala
em projeto alheio e não tem licença para arrastar dependência junto. Há teste nesta
suíte varrendo os `import` de topo destes módulos exatamente para que a primeira
tentativa de trazer uma biblioteca de fora falhe na hora, e não na instalação.
"""

from __future__ import annotations

from .bloqueio import (
    MOTIVO_DO_PREDICADO,
    PARTES_DO_ACEITE,
    BloqueioInvalido,
    DecisaoAberta,
    PadraoAssumidoProibido,
    ParteDoAceite,
    Predicado,
    RespostaForaDasOpcoes,
    aplicar_resposta,
    assumiveis_abertas,
    avaliar_lacuna,
    bloqueantes_abertas,
    classificar_lacunas,
    exigir_origem_declarada,
    exigir_resposta_admissivel,
    universo_completo,
    validar_bloqueio,
)
from .catalogo import (
    CATALOGO,
    PESO_MAXIMO_VALIDO,
    PESO_MINIMO_VALIDO,
    CatalogoInvalido,
    Contexto,
    Lacuna,
    Plataforma,
    lacunas_ativas,
    validar_catalogo,
)
from .deteccao import (
    CONFIANCA_ALTA,
    CONFIANCA_BAIXA,
    CONFIANCA_MEDIA,
    Origem,
    Palpite,
    detectar_contextos,
    detectar_plataformas,
)
from .entrevista import (
    PESO_MINIMO_PADRAO,
    Entrevista,
    LacunaDesconhecida,
    PalpiteDesconhecido,
)
from .especificacao import Especificacao, gerar
from .taxonomia import (
    LACUNAS_POR_INTENCAO,
    MOTOR_POR_INTENCAO,
    PONTOS_MINIMOS,
    PONTOS_POR_CONFIANCA,
    Intencao,
    IntencaoDesconhecida,
    IntencaoIndeterminada,
    TaxonomiaInvalida,
    classificar,
    lacunas_da_intencao,
    lacunas_do_pedido,
    sinais_de_intencao,
    validar_taxonomia,
)

__all__ = [
    # bloqueio
    "BloqueioInvalido",
    "DecisaoAberta",
    "MOTIVO_DO_PREDICADO",
    "PARTES_DO_ACEITE",
    "PadraoAssumidoProibido",
    "ParteDoAceite",
    "Predicado",
    "RespostaForaDasOpcoes",
    "aplicar_resposta",
    "assumiveis_abertas",
    "avaliar_lacuna",
    "bloqueantes_abertas",
    "classificar_lacunas",
    "exigir_origem_declarada",
    "exigir_resposta_admissivel",
    "universo_completo",
    "validar_bloqueio",
    # catalogo
    "CATALOGO",
    "CatalogoInvalido",
    "Contexto",
    "Lacuna",
    "PESO_MAXIMO_VALIDO",
    "PESO_MINIMO_VALIDO",
    "Plataforma",
    "lacunas_ativas",
    "validar_catalogo",
    # deteccao
    "CONFIANCA_ALTA",
    "CONFIANCA_BAIXA",
    "CONFIANCA_MEDIA",
    "Origem",
    "Palpite",
    "detectar_contextos",
    "detectar_plataformas",
    # entrevista
    "Entrevista",
    "LacunaDesconhecida",
    "PESO_MINIMO_PADRAO",
    "PalpiteDesconhecido",
    # especificacao
    "Especificacao",
    "gerar",
    # taxonomia
    "Intencao",
    "IntencaoDesconhecida",
    "IntencaoIndeterminada",
    "LACUNAS_POR_INTENCAO",
    "MOTOR_POR_INTENCAO",
    "PONTOS_MINIMOS",
    "PONTOS_POR_CONFIANCA",
    "TaxonomiaInvalida",
    "classificar",
    "lacunas_da_intencao",
    "lacunas_do_pedido",
    "sinais_de_intencao",
    "validar_taxonomia",
]
