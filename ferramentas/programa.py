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
)

#: O grafo. `PLANO_MESTRE -> EXECUCAO` é a porta P1: existe no grafo, mas só
#: `aprovar()` a atravessa, e `aprovar()` é o único verbo que o modelo não pode
#: executar por conta própria.
TRANSICOES: dict[str, tuple[str, ...]] = {
    "CONCEPCAO": ("PLANO_MESTRE",),
    "PLANO_MESTRE": ("EXECUCAO",),
    "EXECUCAO": ("DESVIO", "ACEITE_SISTEMA"),
    "DESVIO": ("EXECUCAO", "PLANO_MESTRE"),
    "ACEITE_SISTEMA": ("EXECUCAO", "CONCLUIDO"),
    "CONCLUIDO": (),
}

#: Status de um ciclo dentro do programa.
STATUS_CICLO: tuple[str, ...] = ("PENDENTE", "ATIVO", "CONCLUIDO", "REPROVADO")

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


def validar_plano(ciclos: list[dict]) -> None:
    """Recusa uma decomposição que não pode ser executada. Roda ANTES da porta.

    Cinco condições, todas verificáveis. Elas existem porque cada uma, se passasse,
    produziria uma falha tardia e obscura:

    - lista vazia: um programa sem ciclos "conclui" sozinho sem construir nada;
    - id repetido: o encadeamento não saberia qual ciclo marcar como concluído;
    - `depende_de` apontando para id inexistente: o ciclo nunca fica elegível, e o
      programa trava sem mensagem;
    - **ciclo no grafo de dependências**: mesma coisa, mas pior de diagnosticar —
      é a mesma regra que o acervo aplica a `depende_de` de volume;
    - aceite ausente ou vazio: sem critério falsificável o encadeamento não tem
      como decidir se o ciclo passou, e "concluído" viraria opinião do modelo.
      É o volume 04 aplicado à decomposição: requisito é enunciado que pode ser falso.
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
        if not (c.get("objetivo") or "").strip():
            raise PlanoInvalido(f"ciclo {cid!r} sem objetivo")
        if not (c.get("aceite") or "").strip():
            raise PlanoInvalido(
                f"ciclo {cid!r} sem critério de aceite — sem ele o encadeamento "
                "não tem como decidir se o ciclo passou"
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
        if existente is not None and existente.get("estado") != "CONCLUIDO" and not forcar:
            raise ProgramaJaAtivo(
                f"já existe um programa em andamento (objetivo: "
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
    """
    if not (aceite_de_sistema or "").strip():
        raise PlanoInvalido(
            "programa sem aceite de sistema — sem ele, N ciclos verdes não provam "
            "que o sistema funciona, apenas que os pedaços passaram nos próprios testes"
        )
    validar_plano(ciclos)

    novo_estado = transicionar(dados, "PLANO_MESTRE")
    novo_estado["aceite_de_sistema"] = aceite_de_sistema
    novo_estado["ciclos"] = [
        {
            "id": c["id"],
            "objetivo": c["objetivo"],
            "depende_de": list(c.get("depende_de", [])),
            "aceite": c["aceite"],
            "status": "PENDENTE",
            "ciclo_do_estado": None,
        }
        for c in ciclos
    ]
    return novo_estado


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
