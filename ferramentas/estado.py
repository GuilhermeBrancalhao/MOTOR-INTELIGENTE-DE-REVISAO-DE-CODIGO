"""Estado do ENGINE: persistência em disco e máquina de fases.

O estado vive em `<projeto>/.engine/estado.json`. É disco, não contexto — é isso que
faz o modo sobreviver à compactação.

Arquivo único, várias sessões
-----------------------------
`.engine/estado.json` é um arquivo só, e o Claude Code pode ter mais de uma sessão
aberta na mesma pasta. Toda mutação aqui é **ler → alterar → gravar**, e duas
sessões fazendo isso ao mesmo tempo produziam *lost update*: a segunda lia antes de
a primeira gravar, e a gravação da segunda apagava a transição que a primeira já
tinha confirmado ao usuário. Não era corrupção — `gravar` sempre foi atômico — era
pior: sumiço silencioso de trabalho confirmado.

A trava é o `cadeado`: um arquivo `.engine/estado.lock` criado com `O_EXCL`, que
serializa a seção crítica inteira (a leitura E a gravação), não só a gravação.
Quem muta estado usa `atualizar()`, nunca `gravar()` direto — e
`test_nenhum_gravar_fora_do_estado` trava essa regra contra reintrodução.
"""
from __future__ import annotations

import json
import os
import re
import time
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Callable, Iterator

FASES: tuple[str, ...] = (
    "DESCOBERTA",
    "ANALISE",
    "EVOLUCAO",
    "PLANO",
    "BUILD",
    "TESTE",
    "REVISAO",
    "DOC",
    "ENTREGA",
)

TRANSICOES: dict[str, tuple[str, ...]] = {
    "DESCOBERTA": ("ANALISE",),
    "ANALISE": ("EVOLUCAO", "PLANO"),
    "EVOLUCAO": ("PLANO",),
    "PLANO": ("BUILD",),
    "BUILD": ("TESTE",),
    "TESTE": ("BUILD", "REVISAO"),
    "REVISAO": ("BUILD", "DOC"),
    "DOC": ("ENTREGA",),
    "ENTREGA": (),
}

VERSAO = 1


class TransicaoInvalida(Exception):
    """Passagem de fase que não existe no grafo da especificação."""


class EstadoCorrompido(Exception):
    """O arquivo de estado existe, mas não é JSON válido ou não é um objeto.

    Sobrescrever nesse caso apagaria um ciclo em andamento sem ninguém perceber —
    por isso é um erro explícito, não um `None` silencioso.
    """


class CicloJaAtivo(Exception):
    """Já existe um ciclo ativo; `novo_ciclo` recusa sobrescrevê-lo sem `forcar=True`."""


class EstadoOcupado(Exception):
    """Outra sessão segurou o cadeado do estado além da espera máxima.

    Quem chama decide o que fazer. A CLI reclama e sai 1 (o humano está olhando);
    hook engole e segue (nunca pode derrubar o turno). O que nenhum dos dois pode
    fazer é gravar assim mesmo: seria exatamente o *lost update* que o cadeado
    existe para impedir.
    """


def caminho(raiz: Path) -> Path:
    return Path(raiz) / ".engine" / "estado.json"


# ---------------------------------------------------------------------------
# Cadeado entre sessões
# ---------------------------------------------------------------------------

#: Nome do cadeado, ao lado do estado. `.engine/` inteiro é ignorado pelo git.
NOME_CADEADO = "estado.lock"

#: Espera máxima por padrão. Curta de propósito: hook que trava é hook que atrapalha
#: o turno, e a contenção real aqui é de milissegundos (a seção crítica é ler um JSON
#: pequeno, mexer num dicionário e trocar o arquivo).
ESPERA_PADRAO = 2.0

#: Acima desta idade o cadeado é considerado abandonado — o dono morreu sem soltar
#: (sessão fechada no meio, processo morto). Sem isso, um cadeado órfão travaria o
#: motor para sempre naquele projeto, que é um modo de falhar pior do que a corrida
#: que ele previne.
IDADE_MAXIMA_CADEADO = 30.0

_INTERVALO_TENTATIVA = 0.005


def caminho_cadeado(raiz: Path) -> Path:
    return Path(raiz) / ".engine" / NOME_CADEADO


def _abandonado(alvo: Path, idade_maxima: float) -> bool:
    try:
        return (time.time() - alvo.stat().st_mtime) > idade_maxima
    except OSError:
        # Sumiu entre o `O_EXCL` falhar e o `stat` — quem tinha soltou. Não é
        # abandono; a próxima tentativa de criar vai simplesmente funcionar.
        return False


@contextmanager
def cadeado(
    raiz: Path,
    *,
    espera: float = ESPERA_PADRAO,
    idade_maxima: float = IDADE_MAXIMA_CADEADO,
) -> Iterator[Path]:
    """Exclusão mútua entre processos para a seção crítica do estado.

    `os.open(..., O_CREAT | O_EXCL)` é a primitiva porque é a única que funciona
    igual no Windows e no POSIX usando só a biblioteca padrão — `fcntl.flock` não
    existe no Windows e `msvcrt.locking` não existe fora dele, e o motor não pode
    ganhar dependência de runtime nem um ramo por plataforma neste ponto.

    NÃO é reentrante: chamar uma função que pega o cadeado de dentro de outra que
    já o segura trava até o timeout. Por isso as funções públicas deste módulo
    pegam o cadeado e delegam o trabalho a um núcleo `_sem_cadeado`.
    """
    alvo = caminho_cadeado(raiz)
    alvo.parent.mkdir(parents=True, exist_ok=True)
    limite = time.monotonic() + espera
    descritor: int | None = None

    while True:
        try:
            descritor = os.open(alvo, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            break
        except FileExistsError:
            if _abandonado(alvo, idade_maxima):
                try:
                    alvo.unlink()
                except OSError:
                    pass  # outro processo quebrou primeiro; tanto faz quem foi
            if time.monotonic() >= limite:
                raise EstadoOcupado(
                    f"cadeado do estado ({alvo}) ocupado por mais de {espera}s — "
                    "outra sessão do ENGINE está gravando nesta mesma pasta"
                ) from None
            time.sleep(_INTERVALO_TENTATIVA)
        except OSError as erro:
            raise EstadoOcupado(f"não foi possível criar o cadeado {alvo}: {erro}") from erro

    try:
        # Só diagnóstico: quem inspecionar um cadeado preso sabe qual processo olhar.
        try:
            os.write(descritor, f"{os.getpid()}\n".encode("utf-8"))
        except OSError:
            pass
        os.close(descritor)
        descritor = None
        yield alvo
    finally:
        if descritor is not None:
            try:
                os.close(descritor)
            except OSError:
                pass
        try:
            alvo.unlink()
        except OSError:
            pass


def atualizar(
    raiz: Path,
    mutador: Callable[[dict | None], dict | None],
    *,
    espera: float = ESPERA_PADRAO,
) -> dict | None:
    """Ler → alterar → gravar como uma operação só, sob cadeado.

    `mutador` recebe o estado **relido de dentro da seção crítica** (nunca uma
    cópia que quem chamou leu antes) e devolve o que gravar, ou `None` para não
    gravar nada. Exceção levantada pelo mutador sobe sem gravar, e o cadeado é
    solto de qualquer forma.

    É este relê-de-dentro que mata o *lost update*: com o cadeado só na gravação,
    a segunda sessão ainda gravaria por cima com dados velhos.
    """
    with cadeado(raiz, espera=espera):
        resultado = mutador(carregar_estrito(raiz))
        if resultado is None:
            return None
        gravar(raiz, resultado)
        return resultado


def carregar(raiz: Path) -> dict | None:
    """Devolve `None` tanto quando o estado não existe quanto quando está corrompido.

    Usada pelos hooks: falhar ali não pode derrubar o turno do usuário, então os
    dois casos "sem estado" e "estado ilegível" são tratados como equivalentes.
    """
    alvo = caminho(raiz)
    if not alvo.is_file():
        return None
    try:
        return json.loads(alvo.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError, UnicodeDecodeError):
        return None


def carregar_estrito(raiz: Path) -> dict | None:
    """Como `carregar`, mas distingue "não existe" de "existe e está quebrado".

    Devolve `None` só quando o arquivo não existe. Quando existe mas o conteúdo não
    é JSON válido (ou não é um objeto), levanta `EstadoCorrompido` em vez de
    devolver `None` — quem grava por cima do estado precisa saber da diferença para
    não apagar um ciclo em andamento.
    """
    alvo = caminho(raiz)
    if not alvo.is_file():
        return None
    try:
        dados = json.loads(alvo.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError, UnicodeDecodeError) as erro:
        raise EstadoCorrompido(f"estado ilegível em {alvo}: {erro}") from erro
    if not isinstance(dados, dict):
        raise EstadoCorrompido(f"estado em {alvo} não é um objeto JSON")
    return dados


def gravar(raiz: Path, dados: dict) -> None:
    """Escrita atômica: grava num temporário e substitui.

    Um hook interrompido no meio da escrita não pode deixar o estado corrompido —
    seria a única forma de o motor perder o ciclo sem ninguém perceber.

    O temporário leva o pid no nome. Com um nome fixo (`estado.json.tmp`), dois
    processos gravando ao mesmo tempo disputavam o MESMO arquivo intermediário, e
    no Windows isso não degradava em perda de escrita: estourava
    `PermissionError` (`WinError 32`, arquivo em uso) dentro do hook. Foi o que a
    mutação de `test_seis_sessoes_simultaneas_nao_perdem_escrita` mostrou quando
    o cadeado foi removido de propósito. O cadeado de `atualizar` já serializa os
    caminhos de mutação do motor; o pid aqui é a defesa em profundidade, para que
    `gravar` seja seguro por si só.

    Isto NÃO substitui o cadeado: nome único resolve a colisão no temporário, não
    o *lost update* — dois processos ainda leriam o mesmo estado e um sobrescreveria
    o outro, só que sem erro nenhum para denunciar.
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


def novo_ciclo(
    raiz: Path, objetivo: str, agora: str, modo: str = "normal", forcar: bool = False
) -> dict:
    """Abre um ciclo novo, gravando por cima do estado anterior (se houver).

    Sob cadeado: a checagem de "já existe ciclo ativo" e a gravação do ciclo novo
    são uma operação só. Sem isso, duas sessões abrindo ciclo ao mesmo tempo
    passariam as duas pela checagem e a segunda apagaria o ciclo da primeira —
    justamente o caso que `CicloJaAtivo` existe para impedir.
    """
    with cadeado(raiz):
        return _novo_ciclo_sem_cadeado(raiz, objetivo, agora, modo, forcar)


def _novo_ciclo_sem_cadeado(
    raiz: Path, objetivo: str, agora: str, modo: str, forcar: bool
) -> dict:
    """Núcleo de `novo_ciclo`. Pressupõe o cadeado já tomado — não o pega.

    Recusa sobrescrever um ciclo ainda ativo a menos que `forcar=True` — sem essa
    trava, chamar `novo_ciclo` duas vezes perderia silenciosamente o ciclo em
    andamento (cartões, decisões, pendências, diffs pendentes).

    O `id` do ciclo é `<dia>-<n>`, onde `n` conta quantos ciclos já existiram nesse
    dia segundo `historico` — a lista (preservada entre ciclos) de todos os ids já
    usados. Isso evita colisão de id quando dois ciclos abrem no mesmo dia.

    Estado corrompido NUNCA é sobrescrito em silêncio: `carregar_estrito` (não o
    `carregar` tolerante, que devolve `None` tanto para "não existe" quanto para
    "quebrado") distingue os dois casos, e o arquivo ilegível é preservado com o
    mesmo mecanismo de renomeação do `desligar` (`estado.corrompido-<carimbo>.json`)
    ANTES de o ciclo novo ser gravado. O `historico` dentro dele estava ilegível de
    qualquer forma — mas continua recuperável no arquivo preservado.
    """
    try:
        existente = carregar_estrito(raiz)
    except EstadoCorrompido:
        _preservar_estado_corrompido(raiz, agora)
        existente = None
    historico: list[str] = []
    if existente is not None:
        if existente.get("ativo") and not forcar:
            objetivo_ativo = existente.get("ciclo", {}).get("objetivo", "?")
            raise CicloJaAtivo(
                f"já existe um ciclo ativo (objetivo: {objetivo_ativo!r}); "
                "use forcar=True para sobrescrevê-lo"
            )
        historico = list(existente.get("historico", []))

    dia = agora[:10]
    numero = sum(1 for id_usado in historico if id_usado.startswith(f"{dia}-")) + 1
    novo_id = f"{dia}-{numero}"
    historico.append(novo_id)

    dados = {
        "versao": VERSAO,
        "ativo": True,
        "ciclo": {
            "id": novo_id,
            "objetivo": objetivo,
            "iniciado_em": agora,
            "modo": modo,
        },
        "fase": "DESCOBERTA",
        "fases_concluidas": [],
        "cartoes": [],
        "decisoes": [],
        "pendencias": [],
        "diffs_pendentes": [],
        "cobrancas_por_fase": {},
        "historico": historico,
    }
    gravar(raiz, dados)
    return dados


def transicionar(dados: dict, destino: str) -> dict:
    atual = dados["fase"]
    if destino not in TRANSICOES.get(atual, ()):
        permitidas = ", ".join(TRANSICOES.get(atual, ())) or "nenhuma"
        raise TransicaoInvalida(
            f"{atual} -> {destino} não existe no grafo; a partir de {atual} só: {permitidas}"
        )
    if atual not in dados["fases_concluidas"]:
        dados["fases_concluidas"].append(atual)
    dados["fase"] = destino
    return dados


def desligar(raiz: Path, agora: str | None = None) -> dict:
    """Marca o estado como inativo, preservando um estado corrompido em vez de apagá-lo.

    Antes, `carregar(raiz) or {}` tratava "corrompido" igual a "não existe" e
    gravava um dicionário vazio por cima — apagando `ciclo`, `cartoes`, `decisoes`,
    `pendencias` e `diffs_pendentes` de um ciclo em andamento. Agora, se o JSON
    estiver quebrado, o arquivo original é renomeado para
    `estado.corrompido-<carimbo>.json` antes de qualquer gravação nova.

    Sob cadeado, como toda mutação: desligar concorrente com uma transição de fase
    de outra sessão fazia uma das duas sumir.
    """
    with cadeado(raiz):
        try:
            dados = carregar_estrito(raiz)
        except EstadoCorrompido:
            _preservar_estado_corrompido(raiz, agora)
            dados = None
        dados = dados or {}
        dados["ativo"] = False
        gravar(raiz, dados)
        return dados


def _preservar_estado_corrompido(raiz: Path, agora: str | None) -> None:
    carimbo = agora if agora is not None else datetime.now().strftime("%Y%m%d%H%M%S")
    # `agora` pode ser um instante ISO (`2026-07-31T10:00:00`), e `:` é inválido em
    # nome de arquivo no Windows — o carimbo é saneado para caracteres seguros.
    carimbo = re.sub(r"[^0-9A-Za-z._-]", "-", carimbo)
    alvo = caminho(raiz)
    destino = alvo.parent / f"estado.corrompido-{carimbo}.json"
    os.replace(alvo, destino)


def registrar_diff(raiz: Path, caminho_arquivo: str) -> dict:
    """Registra um diff pendente. Levanta `EstadoCorrompido` se o estado existir e
    estiver ilegível — sem estado (arquivo ausente) continua devolvendo `{}` em
    silêncio, porque esse caminho é chamado por hooks que não podem quebrar o turno.

    Sob cadeado, via `atualizar`: era o site de corrida mais provável do motor —
    o PreToolUse dispara a cada ação de ferramenta, então duas sessões trabalhando
    em paralelo perdiam diffs uma da outra o tempo todo.
    """

    def _mutar(dados: dict | None) -> dict | None:
        if dados is None:
            return None
        pendentes = dados.setdefault("diffs_pendentes", [])
        if caminho_arquivo not in pendentes:
            pendentes.append(caminho_arquivo)
        return dados

    return atualizar(raiz, _mutar) or {}
