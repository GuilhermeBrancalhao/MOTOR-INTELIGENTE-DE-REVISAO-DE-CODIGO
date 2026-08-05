"""Camada de PROGRAMA: a sequência de ciclos que constrói um sistema inteiro.

O ciclo (`estado.py`) conduz UM trabalho de engenharia, do DESCOBERTA ao ENTREGA.
Um sistema de alta complexidade não é um ciclo — é uma sequência deles, com
dependências. Até a Fase 3 essa sequência vivia fora da máquina: na cabeça do
usuário, que religava o motor a cada etapa. Nada auditava a decomposição, nada
sabia dizer "o sistema está pronto", e a parada obrigatória do PLANO acontecia N
vezes para aprovar uma arquitetura já aprovada na primeira.

Este módulo é a camada de cima. Ele **não altera o ciclo**: mesmo grafo, mesmas
fases, mesmos gates. Ele liga ciclos, verifica o aceite de cada um contra a
evidência, e decide o próximo.

Três propriedades foram herdadas de `estado.py` de propósito, e não reescritas:

- **cadeado entre processos** (`estado.cadeado`), porque programa e ciclo vivem na
  mesma pasta `.engine/` e duas sessões podem mexer nos dois ao mesmo tempo;
- **escrita atômica**, para que um hook interrompido não deixe o programa ilegível;
- **estado é função apenas do disco**, que é o que faz o programa sobreviver a
  compactação e a sessão nova — a mesma razão pela qual o cartão sobrevive.

O arquivo é separado (`programa.json`) por decisão P3: um `desligar` de ciclo não
pode destruir o programa que o contém.

**O critério de aceite de cada ciclo é comando, e não só prosa.** `validar_plano` exigia
um `aceite` não-vazio e aceitava qualquer frase; frase não se executa, então o veredito
do ciclo continuava saindo de alguém digitar `programa aceite C1 ok`. Desde este ciclo
todo ciclo do plano-mestre declara também `comando_de_aceite` — a linha de comando que
`ferramentas.executor` roda para decidir o veredito pelo código de saída. A exigência
vive só no caminho de escrita (`validar_plano`), e a leitura (`comando_de_aceite`) é
tolerante: `programa.json` gravado antes disto continua carregando inteiro.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Callable

from . import estado

#: Estados do programa. Não confundir com as FASES do ciclo — são máquinas distintas.
ESTADOS: tuple[str, ...] = (
    "CONCEPCAO",
    "PLANO_MESTRE",
    "EXECUCAO",
    "DESVIO",
    "ACEITE_SISTEMA",
    "CONCLUIDO",
    "ABORTADO",
)

#: O grafo. `PLANO_MESTRE -> EXECUCAO` é a porta P1: existe no grafo, mas só
#: `aprovar()` a atravessa, e `aprovar()` é o único verbo que o modelo não pode
#: executar por conta própria.
#:
#: **`ABORTADO` é um terminal próprio, e não `CONCLUIDO` reusado.** Antes, o verbo
#: `abortar` da CLI escrevia `estado = "CONCLUIDO"` na mão, por fora de
#: `transicionar`: funcionava a partir de qualquer estado, não deixava rastro, e
#: produzia um programa cujo desfecho gravado ("concluído") mentia sobre o que tinha
#: acontecido — inclusive para `novo()`, que passava a abrir outro por cima sem
#: reclamar. Fim VERIFICADO (aceite de sistema verde) e fim DECLARADO por fiat são
#: desfechos diferentes e precisam de nomes diferentes; com dois terminais, quem lê o
#: `programa.json` seis meses depois distingue os dois sem consultar a trilha.
#:
#: Toda origem não-terminal tem aresta para `ABORTADO`: desistir é legítimo em
#: qualquer ponto vivo do programa. O que não é legítimo é desistir **sem passar pela
#: máquina** — e a única maneira de garantir isso é a aresta existir.
TRANSICOES: dict[str, tuple[str, ...]] = {
    "CONCEPCAO": ("PLANO_MESTRE", "ABORTADO"),
    "PLANO_MESTRE": ("EXECUCAO", "ABORTADO"),
    "EXECUCAO": ("DESVIO", "ACEITE_SISTEMA", "ABORTADO"),
    "DESVIO": ("EXECUCAO", "PLANO_MESTRE", "ABORTADO"),
    "ACEITE_SISTEMA": ("EXECUCAO", "CONCLUIDO", "ABORTADO"),
    "CONCLUIDO": (),
    "ABORTADO": (),
}

#: Terminais: nada sai deles. Derivado do grafo, e não escrito à mão, para que a
#: adição de um terceiro desfecho não deixe esta lista para trás.
TERMINAIS: tuple[str, ...] = tuple(
    origem for origem, destinos in TRANSICOES.items() if not destinos
)

#: Os estados em que o motor abre um programa novo por cima do anterior **sem** o
#: usuário pedir `--forcar`.
#:
#: Só `CONCLUIDO` está aqui, e `ABORTADO` está de fora de propósito. A regra é: a
#: pasta se libera sozinha quando o fim foi **verificado** — `CONCLUIDO` só existe
#: depois de um aceite de sistema verde, que é um veredito que a máquina conferiu.
#: `ABORTADO` é fim **declarado**: alguém disse que acabou, e ninguém provou nada.
#: Liberar por declaração daria um segundo caminho, mais silencioso, para o que
#: `--forcar` já faz em voz alta — bastaria `abortar` seguido de `programa <objetivo>`
#: para descartar um plano-mestre que o usuário tinha aprovado na porta P1, sem que a
#: palavra "forçar" aparecesse em lugar nenhum. Descartar o registro de um programa
#: continua sendo uma decisão explícita, tomada no momento em que se descarta.
ESTADOS_QUE_LIBERAM_A_PASTA: tuple[str, ...] = ("CONCLUIDO",)

#: Status de um ciclo dentro do programa.
STATUS_CICLO: tuple[str, ...] = ("PENDENTE", "ATIVO", "CONCLUIDO", "REPROVADO")

#: Onde mora o comando executável do critério de aceite de um ciclo.
#:
#: **Campo NOVO, ao lado de `aceite`, e não `aceite` virando objeto
#: `{descricao, comando}`.** As duas formas guardam a mesma informação; o que as separa é
#: o que acontece com os arquivos que já estão no disco.
#:
#: - `aceite` continua sendo **string** em todo `programa.json` já gravado. Nenhum leitor
#:   precisa saber que este campo passou a existir: `resumo`, `proximo_elegivel`,
#:   `_prog_imprimir` e o `programa proximo` da CLI seguem lendo `aceite` como sempre
#:   leram. Um objeto no lugar da string quebraria os quatro no mesmo instante, com
#:   `TypeError` em cima de um arquivo que ninguém tocou.
#: - `VERSAO` continua 1 **porque não há nada a migrar**. Subir a versão obrigaria a
#:   escrever uma função de migração, e uma migração que ninguém escreveu é uma migração
#:   que roda na cabeça de quem lê o arquivo. Campo ausente já tem significado exato aqui
#:   (plano anterior a este ciclo), e esse significado é lido por `comando_de_aceite`.
#: - A separação também é honesta quanto ao conteúdo: a **prosa** diz o que está sendo
#:   afirmado (o enunciado falsificável do volume 04), o **comando** diz como se
#:   verifica. Fundir os dois numa string só foi exatamente o defeito que este ciclo
#:   corrige — o plano trazia a frase e ninguém tinha o que rodar.
CAMPO_COMANDO = "comando_de_aceite"

#: Motivos que autorizam parar a execução e perguntar (P2). Fechado de propósito:
#: parada que acontece por qualquer coisa deixa de ser sinal — a mesma lição do
#: falso positivo de R8, em que travar demais treina a aprovar no automático.
MOTIVOS_DESVIO: tuple[str, ...] = (
    "stack-fora-do-plano",
    "dependencia-nao-prevista",
    "aceite-inalcancavel",
    "escopo-fora-do-declarado",
)

VERSAO = 1

NOME_CADEADO = "programa.lock"


class ProgramaCorrompido(Exception):
    """O arquivo existe, mas não é JSON válido ou não é um objeto."""


class ProgramaJaAtivo(Exception):
    """Já existe um programa em andamento; `novo` recusa sobrescrevê-lo."""


class TransicaoInvalida(Exception):
    """Passagem de estado que não existe no grafo."""


class PlanoInvalido(Exception):
    """A decomposição não passa na validação (DAG, aceite ausente, id repetido)."""


class DescobertaIncompleta(PlanoInvalido):
    """A macro-DESCOBERTA do programa não está fechada: `CONCEPCAO -> PLANO_MESTRE` recusada.

    **Exceção nova, e não `PlanoInvalido` reusada.** As duas recusam a mesma transição,
    mas dizem coisas opostas sobre o que fazer em seguida: `PlanoInvalido` significa "a
    decomposição está errada, reescreva o JSON"; esta significa "a decomposição pode até
    estar certa, mas ninguém sabe ainda o que o sistema tem de fazer — vá responder as
    lacunas". Fundir as duas obrigaria quem lê a recusa a distinguir pelo texto da
    mensagem, e texto não é contrato.

    **Herda de `PlanoInvalido` de propósito.** Todo chamador que já escrevia
    `except programa.PlanoInvalido` continua recusando a transição sem alteração — e é
    isso que faz a falha ser FECHADA por construção: um caminho que ainda não conhece a
    exceção nova não passa a liberar o plano, ele continua barrando. Se fosse uma
    hierarquia paralela, cada `except` esquecido viraria um vazamento silencioso, que é
    exatamente o modo de falhar que este ciclo existe para fechar.

    A mensagem carrega a lista de lacunas bloqueantes **com a pergunta inteira** (o
    `resumo()` da avaliação da descoberta), pela mesma razão que a recusa do gate de
    fase carrega: quem leu "bloqueado" e não sabe o que responder volta a perguntar ao
    modelo, e a elicitação inteira perde o sentido.
    """


class PortaNaoAtravessada(Exception):
    """Tentativa de executar sem o plano-mestre ter sido aprovado pelo usuário."""


class SemCicloElegivel(Exception):
    """Nenhum ciclo com dependências satisfeitas — ou acabaram, ou há reprovado."""


class DesvioInvalido(Exception):
    """Motivo de desvio fora do conjunto fechado de `MOTIVOS_DESVIO`."""


def caminho(raiz: Path) -> Path:
    return Path(raiz) / ".engine" / "programa.json"


def caminho_cadeado(raiz: Path) -> Path:
    return Path(raiz) / ".engine" / NOME_CADEADO


# ---------------------------------------------------------------------------
# Persistência
# ---------------------------------------------------------------------------


def carregar(raiz: Path) -> dict | None:
    """Tolerante: `None` para inexistente E para ilegível. Para hooks."""
    alvo = caminho(raiz)
    if not alvo.is_file():
        return None
    try:
        return json.loads(alvo.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError, UnicodeDecodeError):
        return None


def carregar_estrito(raiz: Path) -> dict | None:
    """Distingue "não existe" de "existe e está quebrado".

    Quem grava por cima precisa da diferença: sobrescrever um programa ilegível
    apagaria a decomposição inteira de um sistema sem ninguém perceber.
    """
    alvo = caminho(raiz)
    if not alvo.is_file():
        return None
    try:
        dados = json.loads(alvo.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError, UnicodeDecodeError) as erro:
        raise ProgramaCorrompido(f"programa ilegível em {alvo}: {erro}") from erro
    if not isinstance(dados, dict):
        raise ProgramaCorrompido(f"programa em {alvo} não é um objeto JSON")
    return dados


def gravar(raiz: Path, dados: dict) -> None:
    """Escrita atômica, com o pid no temporário — mesmo motivo de `estado.gravar`.

    Nome fixo de temporário faz dois processos disputarem o mesmo arquivo
    intermediário; no Windows isso estoura `PermissionError` dentro do hook em vez
    de degradar em perda silenciosa.
    """
    alvo = caminho(raiz)
    alvo.parent.mkdir(parents=True, exist_ok=True)
    temporario = alvo.with_name(f"{alvo.name}.{os.getpid()}.tmp")
    try:
        temporario.write_text(
            json.dumps(dados, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        os.replace(temporario, alvo)
    except BaseException:
        try:
            temporario.unlink()
        except OSError:
            pass
        raise


def _cadeado(raiz: Path, espera: float = estado.ESPERA_PADRAO):
    """Cadeado próprio do programa, com o mecanismo de `estado.cadeado`.

    Arquivo de cadeado separado porque as seções críticas são independentes: uma
    transição de fase do ciclo não precisa esperar uma atualização do programa, e
    o contrário também não. Compartilhar o cadeado do estado acoplaria os dois sem
    necessidade — e como o cadeado não é reentrante, o orquestrador (que mexe nos
    dois) travaria contra si mesmo.
    """
    return estado.cadeado(
        raiz,
        espera=espera,
        idade_maxima=estado.IDADE_MAXIMA_CADEADO,
        nome=NOME_CADEADO,
    )


def atualizar(
    raiz: Path,
    mutador: Callable[[dict | None], dict | None],
    *,
    espera: float = estado.ESPERA_PADRAO,
) -> dict | None:
    """Ler → alterar → gravar como uma operação só, sob cadeado.

    O mutador recebe o programa relido de DENTRO da seção crítica. É esse relê que
    mata o *lost update*: com cadeado só na gravação, a segunda sessão gravaria por
    cima com dados velhos.
    """
    with _cadeado(raiz, espera=espera):
        resultado = mutador(carregar_estrito(raiz))
        if resultado is None:
            return None
        gravar(raiz, resultado)
        return resultado


# ---------------------------------------------------------------------------
# Validação do plano-mestre
# ---------------------------------------------------------------------------


def comando_de_aceite(ciclo: dict) -> str:
    """O comando executável do aceite de um ciclo, ou `""` quando não há.

    **Leitura tolerante, de propósito, e é aqui que mora a retrocompatibilidade.** Todo
    ciclo gravado antes deste ciclo do motor não tem o campo, e nada que apenas *lê* um
    programa pode quebrar por causa disso: `programa status`, `programa relatorio`,
    `proximo_elegivel` e os hooks continuam funcionando sobre um `programa.json` antigo.
    Valor de tipo errado também vira `""` em vez de estourar — quem lê um arquivo velho
    não é quem pode consertá-lo, e traceback no terminal do usuário é o formato de erro
    que a CLI proíbe.

    Devolver `""` é o valor certo para "não sei": `executor.executar` recusa comando
    vazio com REPROVADO fundamentado, e nunca aprova por omissão. A tolerância na leitura
    não afrouxa nada — a exigência vive em `validar_plano`, do lado da escrita.
    """
    valor = ciclo.get(CAMPO_COMANDO)
    return valor.strip() if isinstance(valor, str) else ""


def _texto_do_plano(ciclo: dict, campo: str, cid: str) -> str:
    """Lê um campo de texto do plano **estritamente**: tipo errado é plano inválido.

    Na escrita a tolerância seria dano: um `comando_de_aceite` que veio como lista ou
    dicionário no JSON passaria pela validação (não é vazio) e só apareceria lá na
    frente, quando `executor.executar` recebesse algo que não é comando. Recusar aqui
    devolve o erro a quem ainda está escrevendo o plano.
    """
    valor = ciclo.get(campo)
    if valor is None:
        return ""
    if not isinstance(valor, str):
        raise PlanoInvalido(
            f"ciclo {cid!r}: campo {campo!r} precisa ser texto; veio "
            f"{type(valor).__name__}"
        )
    return valor.strip()


def validar_plano(ciclos: list[dict]) -> None:
    """Recusa uma decomposição que não pode ser executada. Roda ANTES da porta.

    Seis condições, todas verificáveis. Elas existem porque cada uma, se passasse,
    produziria uma falha tardia e obscura:

    - lista vazia: um programa sem ciclos "conclui" sozinho sem construir nada;
    - id repetido: o encadeamento não saberia qual ciclo marcar como concluído;
    - `depende_de` apontando para id inexistente: o ciclo nunca fica elegível, e o
      programa trava sem mensagem;
    - **ciclo no grafo de dependências**: mesma coisa, mas pior de diagnosticar —
      é a mesma regra que o acervo aplica a `depende_de` de volume;
    - aceite ausente ou vazio: sem critério falsificável o encadeamento não tem
      como decidir se o ciclo passou, e "concluído" viraria opinião do modelo.
      É o volume 04 aplicado à decomposição: requisito é enunciado que pode ser falso;
    - **`comando_de_aceite` ausente ou vazio**: um critério em prosa é falsificável em
      tese e inexecutável na prática. `executor.executar` (P2C1) sabe rodar comando e
      ler código de saída; não sabe rodar frase. Enquanto o plano só trouxer a frase, o
      veredito continua saindo da boca de quem escreveu o código — que é o defeito que
      o programa 2 inteiro existe para fechar.

    **Onde fica a fronteira da retrocompatibilidade, e por que ela é exatamente aqui.**
    Plano velho (sem comando) precisa continuar carregando; plano novo precisa ser
    recusado sem comando. Não é preciso inventar bandeira, flag de versão nem parâmetro
    `estrito=`: a fronteira já é estrutural, porque **esta função só é chamada no caminho
    de ESCRITA**. Quem a chama é `propor_plano`, e mais ninguém — carregar, resumir,
    imprimir e encadear nunca revalidam. Um `programa.json` gravado em julho passa por
    `carregar` e por `comando_de_aceite`, jamais por aqui; o plano que alguém acabou de
    escrever passa por aqui obrigatoriamente, porque a única porta para PLANO_MESTRE é
    `propor_plano`. Colocar a exigência na validação, e não na leitura, é o que faz "o
    arquivo antigo continua legível" e "o plano novo é recusado" conviverem sem
    migração, sem `VERSAO` nova e sem um segundo modo de validar que alguém pudesse
    desligar por engano. Um parâmetro para relaxar a checagem seria o mesmo defeito que
    `propor_plano` já documenta: predicado que libera portão e pode ser omitido não é
    gate, é sugestão.

    **Por que NÃO se classifica o risco do comando aqui.** A tentação é óbvia — descobrir
    na hora de planejar que `ferramentas.risco` vai travar o comando é melhor do que
    descobrir na hora de rodar. Foi considerado e recusado, por três razões, em ordem de
    peso:

    1. *O veredito de risco não é propriedade do plano; é propriedade do projeto no
       instante da execução.* `risco.classificar` precisa de `raiz` e da configuração
       efetiva (`engine.config.json`, cujas famílias o projeto ajusta). O mesmo plano
       classificado hoje aqui e amanhã ali dá respostas diferentes, e com razão. Um
       "aprovado pelo risco" carimbado no PLANO_MESTRE seria um carimbo que vence sozinho
       — e carimbo vencido é pior que carimbo nenhum, porque convida o executor a confiar
       nele em vez de reclassificar.
    2. *Custaria a pureza deste módulo.* `programa.py` não tem `raiz`, não abre arquivo e
       não toma cadeado, e a suíte inteira depende disso (há teste textual guardando).
       Trazer `risco` para cá arrastaria `raiz` e `config` para dentro de uma função pura,
       ou faria a checagem depender de um argumento opcional — de novo, gate que se pode
       omitir.
    3. *Não há furo a fechar.* `executor.executar` classifica o risco ANTES de executar e
       recusa o comando travado com REPROVADO fundamentado, sem rodar nada. A falha já é
       FECHADA no ponto em que ela importa. O preço de só descobrir na execução é um
       ciclo REPROVADO com o motivo escrito na trilha — que é diagnóstico, não vazamento.

    Pelo mesmo motivo não há aqui nenhuma heurística sobre o TEXTO do comando (procurar
    `pytest`, exigir um executável conhecido, adivinhar se "aquilo parece prosa"):
    interpretar texto é o julgamento do modelo que o executor documenta ter eliminado, e
    reintroduzi-lo do lado do plano o traria de volta pela porta dos fundos. O que esta
    função garante é estrutural e verificável — **existe um comando não-vazio, e ele é
    texto**. Se o comando prova a coisa certa, quem decide é o humano na porta P1, lendo
    a prosa do `aceite` ao lado do comando que a verifica. É para isso que os dois campos
    são dois.
    """
    if not ciclos:
        raise PlanoInvalido("plano-mestre sem nenhum ciclo — nada a construir")

    vistos: set[str] = set()
    for c in ciclos:
        cid = c.get("id")
        if not cid:
            raise PlanoInvalido(f"ciclo sem id: {c!r}")
        if cid in vistos:
            raise PlanoInvalido(f"id de ciclo repetido: {cid!r}")
        vistos.add(cid)
        if not _texto_do_plano(c, "objetivo", cid):
            raise PlanoInvalido(f"ciclo {cid!r} sem objetivo")
        if not _texto_do_plano(c, "aceite", cid):
            raise PlanoInvalido(
                f"ciclo {cid!r} sem critério de aceite — sem ele o encadeamento "
                "não tem como decidir se o ciclo passou"
            )
        if not _texto_do_plano(c, CAMPO_COMANDO, cid):
            raise PlanoInvalido(
                f"ciclo {cid!r} sem comando executável de aceite: declare "
                f"{CAMPO_COMANDO!r} com a linha de comando que verifica o critério "
                f"(quem decide o veredito é o código de saída dela, não a prosa do "
                f"campo 'aceite')"
            )

    for c in ciclos:
        for dep in c.get("depende_de", []):
            if dep not in vistos:
                raise PlanoInvalido(
                    f"ciclo {c['id']!r} depende de {dep!r}, que não existe no plano"
                )

    _recusar_ciclo_no_grafo(ciclos)


def _recusar_ciclo_no_grafo(ciclos: list[dict]) -> None:
    """Busca em profundidade com marcação temporária (detecção clássica de ciclo).

    Reporta o caminho fechado, não só "há um ciclo": quem escreveu a decomposição
    precisa saber ONDE, e num plano de 20 ciclos procurar à mão é inviável.
    """
    dependencias = {c["id"]: list(c.get("depende_de", [])) for c in ciclos}
    PERMANENTE, TEMPORARIO = 2, 1
    marca: dict[str, int] = {}

    def visitar(no: str, caminho_atual: list[str]) -> None:
        estado_no = marca.get(no)
        if estado_no == PERMANENTE:
            return
        if estado_no == TEMPORARIO:
            fecho = caminho_atual[caminho_atual.index(no) :] + [no]
            raise PlanoInvalido(
                "dependência cíclica entre ciclos: " + " -> ".join(fecho)
            )
        marca[no] = TEMPORARIO
        for dep in dependencias.get(no, []):
            visitar(dep, caminho_atual + [no])
        marca[no] = PERMANENTE

    for cid in dependencias:
        visitar(cid, [])


# ---------------------------------------------------------------------------
# Ciclo de vida do programa
# ---------------------------------------------------------------------------


def novo(raiz: Path, objetivo: str, agora: str, forcar: bool = False) -> dict:
    """Abre um programa novo em CONCEPCAO.

    Sob cadeado: a checagem de "já existe" e a gravação são uma operação só, senão
    duas sessões abrindo ao mesmo tempo passariam ambas pela checagem.
    """
    with _cadeado(raiz):
        existente = carregar_estrito(raiz)
        if (
            existente is not None
            and existente.get("estado") not in ESTADOS_QUE_LIBERAM_A_PASTA
            and not forcar
        ):
            raise ProgramaJaAtivo(
                f"já existe um programa neste projeto (objetivo: "
                f"{existente.get('objetivo', '?')!r}, estado: "
                f"{existente.get('estado', '?')}); use forcar=True para descartá-lo"
            )
        dados = {
            "versao": VERSAO,
            "programa": _novo_id(existente, agora),
            "objetivo": objetivo,
            "estado": "CONCEPCAO",
            "iniciado_em": agora,
            "aceite_de_sistema": "",
            "ciclos": [],
            "desvio": None,
            "historico": _historico_com(existente, agora),
        }
        gravar(raiz, dados)
        return dados


def _novo_id(existente: dict | None, agora: str) -> str:
    dia = agora[:10]
    anteriores = list((existente or {}).get("historico", []))
    numero = sum(1 for i in anteriores if i.startswith(f"{dia}-")) + 1
    return f"{dia}-{numero}"


def _historico_com(existente: dict | None, agora: str) -> list[str]:
    historico = list((existente or {}).get("historico", []))
    historico.append(_novo_id(existente, agora))
    return historico


def transicionar(dados: dict, destino: str) -> dict:
    atual = dados["estado"]
    if destino not in TRANSICOES.get(atual, ()):
        permitidos = ", ".join(TRANSICOES.get(atual, ())) or "nenhum"
        raise TransicaoInvalida(
            f"{atual} -> {destino} não existe no grafo do programa; "
            f"a partir de {atual} só: {permitidos}"
        )
    novo_estado = dict(dados)
    novo_estado["estado"] = destino
    return novo_estado


def propor_plano(dados: dict, ciclos: list[dict], aceite_de_sistema: str) -> dict:
    """Registra a decomposição e vai para PLANO_MESTRE. **Não** aprova nada.

    Validar aqui, e não em `aprovar`, é deliberado: o usuário deve ver na porta um
    plano que já se sabe executável. Pedir aprovação de um plano com dependência
    cíclica seria pedir que ele valide o que a máquina consegue conferir sozinha.

    O `aceite_de_sistema` é exigido aqui e não no fim porque, declarado no fim, ele
    seria escrito depois de se saber o que o sistema faz — e passaria sempre. É o
    mesmo motivo pelo qual um teste precisa poder ficar vermelho.

    **Onde mora o gate da macro-DESCOBERTA, e por que não é aqui.** A spec da Fase 4
    diz que `CONCEPCAO` *é* a macro-DESCOBERTA, conduzida pelo papel `descobridor`.
    Verificar isso exige o veredito da entrevista, que mora no `.engine/estado.json` —
    e esta função é **pura sobre dicionário**: não conhece `raiz`, não abre arquivo,
    não toma cadeado. Três opções foram consideradas e duas foram descartadas:

    - *ler o disco daqui dentro* (receber `raiz`) destrói a pureza da qual a suíte
      inteira depende — 29 testes chamam esta função sobre dicionário montado à mão,
      sem projeto nenhum em disco — e repete o defeito que o C4 travou por teste
      textual: leitura de disco por fora do cadeado dá veredito sobre retrato velho;
    - *receber a avaliação como argumento opcional* mantém a pureza, mas o gate ficaria
      **opcional**: chamar com três argumentos (que é como toda a suíte chama, e como
      qualquer chamador novo chamaria por descuido) transicionaria sem gate nenhum.
      Predicado que libera portão e pode ser omitido não é gate, é sugestão.
    - *cobrar no chamador* é o que vale, e é o que está feito: `cli.py`, no sub-verbo
      `programa plano`, exige a descoberta fechada **antes** de chamar esta função,
      levantando `DescobertaIncompleta` pelo mesmo predicado e com a mesma mensagem do
      gate de fase (`cli._gate_descoberta`). Como a recusa acontece antes, esta função
      nem é chamada: nada transiciona, e `programa.json` não é tocado.

    Isto não deixa esta função "sem gate": `DescobertaIncompleta` herda de
    `PlanoInvalido`, e quem chama a máquina por API e já trata `PlanoInvalido` recusa a
    transição do mesmo jeito. O que faz a obrigatoriedade valer no caminho real é o
    teste textual de `ferramentas/tests/test_gate_programa.py`, que lê o `cli.py` e
    reprova se o gate deixar de vir antes desta chamada — a mesma tática que o C4 usa
    para impedir que o gate de fase volte a ler o disco por fora do cadeado.

    **Duas arestas entram em PLANO_MESTRE, e as duas são cobradas.** `CONCEPCAO` é a
    primeira; `DESVIO` é a segunda, e é o replanejamento. Durante um bom tempo o gate
    do chamador olhava só a primeira, e o resultado era o gate desligado exatamente
    onde ele mais vale: os quatro `MOTIVOS_DESVIO` descrevem, um a um, situações em que
    a descoberta original ficou obsoleta (stack que não serve, dependência que ninguém
    previu, aceite inalcançável, escopo fora do declarado). Replanejar sem reabrir a
    entrevista é assinar o mesmo plano com outro nome. O chamador deriva as origens
    protegidas do próprio `TRANSICOES`, e não de uma lista escrita à mão: uma terceira
    aresta para PLANO_MESTRE nasce com gate.
    """
    if not (aceite_de_sistema or "").strip():
        raise PlanoInvalido(
            "programa sem aceite de sistema — sem ele, N ciclos verdes não provam "
            "que o sistema funciona, apenas que os pedaços passaram nos próprios testes"
        )
    validar_plano(ciclos)

    novo_estado = transicionar(dados, "PLANO_MESTRE")
    novo_estado["aceite_de_sistema"] = aceite_de_sistema
    anteriores = {c["id"]: c for c in dados.get("ciclos", [])}
    novo_estado["ciclos"] = [_reaproveitar(c, anteriores.get(c["id"])) for c in ciclos]
    # Replanejar É a resposta ao desvio: o motivo que parou a execução deixa de estar
    # aberto no instante em que o plano novo é proposto. Sem esta limpeza, o registro
    # do desvio sobreviveria à aprovação e o programa seguiria em EXECUCAO exibindo
    # para sempre um conflito já resolvido — ruído que treina a ignorar o campo, que é
    # o oposto do que a parada por exceção (P2) existe para produzir. Vindo de
    # CONCEPCAO o campo já é `None`, então a atribuição é inócua nesse caminho.
    novo_estado["desvio"] = None
    return novo_estado


def _reaproveitar(novo_ciclo: dict, anterior: dict | None) -> dict:
    """Monta o ciclo do plano novo **preservando o veredito já dado**, quando cabe.

    Antes, todo ciclo nascia `PENDENTE`. Isso era inofensivo enquanto a única aresta
    de entrada em PLANO_MESTRE fosse `CONCEPCAO -> PLANO_MESTRE`, onde não há ciclo
    nenhum para perder. Pela segunda aresta (`DESVIO -> PLANO_MESTRE`, o
    replanejamento) o efeito era outro: reconstruir do zero apagava em silêncio o
    `CONCLUIDO` de todo ciclo já aceito e o `REPROVADO` de todo ciclo já reprovado, e
    o `programa.json` passava a afirmar que nada tinha sido feito. Replanejar não
    desfaz trabalho aceito, e muito menos absolve trabalho reprovado.

    **A chave da preservação é o critério de aceite, não o id.** O id é rótulo; o
    aceite é o enunciado falsificável que decidiu o veredito. Se o plano novo mantém o
    id mas reescreve o aceite, o `CONCLUIDO` antigo é prova sobre uma afirmação que
    não está mais no plano — e carimbá-lo no critério novo seria dar por satisfeito um
    requisito que ninguém verificou. Nesse caso o ciclo volta a `PENDENTE`, junto com
    a amarração ao ciclo real (`ciclo_do_estado`), porque o trabalho vai ser refeito.
    A falha, quando há dúvida, é para o lado de refazer.

    **E o critério agora são DOIS campos: a prosa e o comando.** Mudar só o comando, com
    a frase intacta, muda o critério tanto quanto reescrever a frase — passou a ser outra
    verificação. Comparar apenas a prosa deixaria um `CONCLUIDO` de pé sob um comando que
    ninguém rodou, que é a mesma mentira do parágrafo anterior escrita no campo novo.

    O caso mais comum disso é a **primeira** migração de um plano antigo: o ciclo no
    disco não tem comando, o plano novo tem, o critério difere, e todo ciclo já fechado
    volta a `PENDENTE`. É deliberado, e o preço é menor do que parece — refazer aqui
    quer dizer *rodar o comando uma vez*. Se o trabalho estava mesmo pronto, o comando
    sai 0 e o ciclo fecha de novo em segundos, agora com a evidência que faltava. A
    alternativa (herdar o verde de um veredito digitado para dentro de um critério que
    exige execução) seria carimbar como verificado exatamente o que nunca foi.
    """
    base = {
        "id": novo_ciclo["id"],
        "objetivo": novo_ciclo["objetivo"],
        "depende_de": list(novo_ciclo.get("depende_de", [])),
        "aceite": novo_ciclo["aceite"],
        CAMPO_COMANDO: comando_de_aceite(novo_ciclo),
        "status": "PENDENTE",
        "ciclo_do_estado": None,
    }
    if anterior is None:
        return base
    if _criterio(anterior) != _criterio(novo_ciclo):
        return base
    base["status"] = anterior.get("status", "PENDENTE")
    base["ciclo_do_estado"] = anterior.get("ciclo_do_estado")
    return base


def _criterio(ciclo: dict) -> tuple[str, str]:
    """O par que decide o veredito: a afirmação e o comando que a verifica.

    Tolerante a tipo (o `anterior` vem do disco, e disco velho tem de tudo): campo que
    não é texto vira `""`, e `""` nunca é igual a um critério de verdade — o ciclo cai
    para o lado de refazer, que é o lado seguro.
    """
    aceite = ciclo.get("aceite")
    return (
        aceite.strip() if isinstance(aceite, str) else "",
        comando_de_aceite(ciclo),
    )


def aprovar(dados: dict, agora: str) -> dict:
    """A porta P1. Só o usuário roda o verbo que chama isto.

    É o único ponto do motor em que a autonomia para por decisão de desenho, e não
    por risco. A razão está na spec: arquitetura errada executada com disciplina
    perfeita continua sendo sistema errado — e o custo de descobrir isso só no
    ACEITE_SISTEMA é o programa inteiro.
    """
    if dados["estado"] != "PLANO_MESTRE":
        raise TransicaoInvalida(
            f"aprovar só vale a partir de PLANO_MESTRE; o programa está em "
            f"{dados['estado']}"
        )
    novo_estado = transicionar(dados, "EXECUCAO")
    novo_estado["aprovado_em"] = agora
    return novo_estado


# ---------------------------------------------------------------------------
# Encadeamento
# ---------------------------------------------------------------------------


def concluidos(dados: dict) -> set[str]:
    return {c["id"] for c in dados["ciclos"] if c["status"] == "CONCLUIDO"}


def proximo_elegivel(dados: dict) -> dict | None:
    """Primeiro ciclo PENDENTE cujas dependências estão todas CONCLUIDO.

    Ordem estável (a do plano) de propósito: com N ciclos elegíveis ao mesmo tempo,
    escolher sempre o primeiro torna a execução reproduzível. Um critério
    "inteligente" aqui tornaria duas execuções do mesmo plano divergentes, e o
    diagnóstico de uma falha dependeria de adivinhar qual caminho foi tomado.
    """
    prontos = concluidos(dados)
    for c in dados["ciclos"]:
        if c["status"] == "PENDENTE" and all(d in prontos for d in c["depende_de"]):
            return c
    return None


def iniciar_ciclo(dados: dict, id_ciclo: str, id_do_estado: str) -> dict:
    """Marca um ciclo como ATIVO e amarra-o ao id do ciclo real em `estado.json`.

    A amarração é o que permite auditar depois qual execução de ciclo produziu qual
    entrega — sem ela, a trilha e o programa contariam histórias paralelas.
    """
    if dados["estado"] != "EXECUCAO":
        raise PortaNaoAtravessada(
            f"o programa está em {dados['estado']}; ciclos só ligam em EXECUCAO "
            "(o plano-mestre precisa ter sido aprovado)"
        )
    novo_estado = _com_ciclo(dados, id_ciclo, status="ATIVO", ciclo_do_estado=id_do_estado)
    return novo_estado


def registrar_aceite(dados: dict, id_ciclo: str, passou: bool) -> dict:
    """Fecha um ciclo com o veredito do seu critério de aceite.

    `passou=False` marca REPROVADO e **não** libera os dependentes — é o coração de
    A2. Quem chama decide o que fazer (reabrir em BUILD, ou desviar); o que este
    módulo garante é que um ciclo vermelho nunca conta como pré-requisito satisfeito.
    """
    return _com_ciclo(
        dados, id_ciclo, status="CONCLUIDO" if passou else "REPROVADO"
    )


def reabrir(dados: dict, id_ciclo: str) -> dict:
    """Devolve um ciclo REPROVADO para PENDENTE, para nova tentativa.

    Existe para que o caminho de recuperação seja explícito no estado, e não uma
    edição manual do JSON — a mesma razão pela qual `TESTE -> BUILD` está no grafo
    do ciclo em vez de ser um "volte e conserte" informal.
    """
    alvo = _achar(dados, id_ciclo)
    if alvo["status"] != "REPROVADO":
        raise TransicaoInvalida(
            f"só um ciclo REPROVADO pode ser reaberto; {id_ciclo!r} está "
            f"{alvo['status']}"
        )
    return _com_ciclo(dados, id_ciclo, status="PENDENTE")


def _achar(dados: dict, id_ciclo: str) -> dict:
    for c in dados["ciclos"]:
        if c["id"] == id_ciclo:
            return c
    raise KeyError(f"ciclo {id_ciclo!r} não existe neste programa")


def _com_ciclo(dados: dict, id_ciclo: str, **campos) -> dict:
    _achar(dados, id_ciclo)  # levanta se não existe, antes de copiar
    novo_estado = dict(dados)
    novo_estado["ciclos"] = [
        {**c, **campos} if c["id"] == id_ciclo else dict(c) for c in dados["ciclos"]
    ]
    return novo_estado


# ---------------------------------------------------------------------------
# Desvio e aceite de sistema
# ---------------------------------------------------------------------------


def desviar(dados: dict, motivo: str, detalhe: str) -> dict:
    """Para a execução e registra por que o plano aprovado não serve mais.

    O conjunto de motivos é fechado (P2). Um motivo livre transformaria "desvio" em
    "qualquer coisa que o modelo achar estranho", e a parada por exceção viraria
    parada por etapa — exatamente o que a porta única foi desenhada para eliminar.
    """
    if motivo not in MOTIVOS_DESVIO:
        raise DesvioInvalido(
            f"motivo {motivo!r} não é um desvio válido; use um de: "
            + ", ".join(MOTIVOS_DESVIO)
        )
    novo_estado = transicionar(dados, "DESVIO")
    novo_estado["desvio"] = {"motivo": motivo, "detalhe": detalhe}
    return novo_estado


def retomar_apos_desvio(dados: dict) -> dict:
    if dados["estado"] != "DESVIO":
        raise TransicaoInvalida(
            f"retomar só vale a partir de DESVIO; o programa está em {dados['estado']}"
        )
    novo_estado = transicionar(dados, "EXECUCAO")
    novo_estado["desvio"] = None
    return novo_estado


def pronto_para_aceite(dados: dict) -> bool:
    return bool(dados["ciclos"]) and all(
        c["status"] == "CONCLUIDO" for c in dados["ciclos"]
    )


def entrar_em_aceite(dados: dict) -> dict:
    """Só entra quando TODOS os ciclos estão CONCLUIDO.

    Sem essa checagem o programa poderia declarar aceite com ciclos pendentes ou
    reprovados — a versão em escala do defeito que a auditoria de 2026-08-03
    encontrou no acervo: peças marcadas como entregues que não estavam.
    """
    if not pronto_para_aceite(dados):
        faltam = [c["id"] for c in dados["ciclos"] if c["status"] != "CONCLUIDO"]
        raise TransicaoInvalida(
            "ACEITE_SISTEMA exige todos os ciclos CONCLUIDO; faltam: "
            + (", ".join(faltam) or "nenhum, mas o plano está vazio")
        )
    return transicionar(dados, "ACEITE_SISTEMA")


def concluir(dados: dict, passou: bool, agora: str) -> dict:
    """Fecha o programa — ou o devolve para EXECUCAO se o aceite reprovou.

    Aceite vermelho **não** conclui. É A7: sem isso, o programa terminaria verde com
    o sistema quebrado, que é o único desfecho que a Fase 4 inteira existe para
    tornar impossível.
    """
    if dados["estado"] != "ACEITE_SISTEMA":
        raise TransicaoInvalida(
            f"concluir só vale a partir de ACEITE_SISTEMA; o programa está em "
            f"{dados['estado']}"
        )
    if not passou:
        return transicionar(dados, "EXECUCAO")
    novo_estado = transicionar(dados, "CONCLUIDO")
    novo_estado["concluido_em"] = agora
    return novo_estado


def abortar(dados: dict, agora: str) -> dict:
    """Encerra o programa por decisão, sem aceite — o terminal `ABORTADO`.

    É o verbo mais destrutivo da camada: desfaz um programa inteiro, inclusive um
    plano-mestre que o usuário aprovou na porta P1. Antes ele nem existia aqui — a CLI
    escrevia `estado = "CONCLUIDO"` direto no dicionário, por fora de `transicionar`.
    Três coisas vinham junto com esse atalho, e as três morrem com esta função:

    - **funcionava a partir de qualquer estado**, inclusive de um programa já fechado,
      porque não havia grafo nenhum a consultar;
    - **gravava o desfecho errado**: "CONCLUIDO" é a palavra reservada para aceite de
      sistema verde, e passou a nomear também a desistência. Quem lesse o arquivo
      depois não teria como saber qual dos dois aconteceu;
    - **abria a porta de trás de `novo()`**, que libera a pasta quando o estado é
      `CONCLUIDO`: abortar e abrir outro por cima virava uma sequência de dois verbos
      sem a palavra "forçar" em lugar nenhum.

    Recusar a partir dos terminais é deliberado e não é purismo de grafo: `abortar` de
    um programa já `CONCLUIDO` reescreveria um desfecho verificado como desistência,
    que é perda de informação — e `abortar` de um `ABORTADO` só mexeria no carimbo.
    Nos dois casos não há o que encerrar, e dizer isso é mais útil do que obedecer.
    """
    atual = dados["estado"]
    if atual in TERMINAIS:
        raise TransicaoInvalida(
            f"o programa já terminou em {atual}; não há o que abortar "
            "(abrir outro programa por cima exige `--forcar`)"
        )
    novo_estado = transicionar(dados, "ABORTADO")
    novo_estado["abortado_em"] = agora
    return novo_estado


def resumo(dados: dict) -> dict:
    """Números do programa, para status e relatório."""
    total = len(dados["ciclos"])
    por_status = {s: 0 for s in STATUS_CICLO}
    for c in dados["ciclos"]:
        por_status[c["status"]] = por_status.get(c["status"], 0) + 1
    return {
        "programa": dados.get("programa"),
        "objetivo": dados.get("objetivo"),
        "estado": dados.get("estado"),
        "total": total,
        "concluidos": por_status["CONCLUIDO"],
        "por_status": por_status,
        "proximo": (proximo_elegivel(dados) or {}).get("id"),
        "desvio": dados.get("desvio"),
    }
