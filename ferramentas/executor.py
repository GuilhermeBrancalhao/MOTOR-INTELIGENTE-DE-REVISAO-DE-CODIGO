"""Executor de critério de aceite do ENGINE: roda o comando, captura a evidência e
devolve veredito estruturado.

Até aqui o aceite de um ciclo era **digitado** (`programa aceite C1 ok`). Nada rodava o
critério declarado, nada lia saída nenhuma: "concluído" era afirmação do modelo. Isto é
exatamente o que a invariante 1 do motor proíbe — nunca afirmar sucesso sem ter olhado.
Este módulo existe para tirar o veredito das mãos de quem escreve o código.

Quatro decisões de desenho, e o porquê de cada uma:

**1. Veredito não existe sem evidência.** `Veredito` é um dataclass congelado cujo campo
`codigo_saida` não tem default: quem tenta construir um veredito sem ele leva `TypeError`
na hora da construção, não um aviso no relatório. E `__post_init__` recusa as três formas
de burlar isso por dentro — `codigo_saida` de tipo errado, `codigo_saida=None` num
veredito APROVADO, e veredito que **contradiz** o código capturado. A regra é estrutural
de propósito: por convenção, ela dura até o primeiro chamador apressado.

**2. Só o código de saída decide.** `julgar` olha um número e mais nada. Nenhuma
heurística sobre o texto — nada de procurar "FAILED", "error", "0 passed". Interpretar
texto reintroduz exatamente o julgamento do modelo que este módulo existe para eliminar:
um dia "passed" aparece dentro de um nome de teste, no outro a suíte muda o formato da
linha de resumo, e o veredito volta a depender de quem lê. Um comando que sai 0 imprimindo
"FAILED" é um comando mal escrito — e consertar o comando é trabalho de quem declara o
aceite, não do executor. Ninguém precisa confiar no executor para conferir isso: o campo
`saida` fica no veredito e na trilha.

**3. A ausência de código também é evidência — e só reprova.** Comando que estoura o
tempo, comando recusado pela política de risco e comando que nem chega a nascer não têm
código de saída. Nesses casos `codigo_saida` é `None`, o `motivo` é obrigatório e o
resultado só pode ser REPROVADO. Falha FECHADA: o que não foi verificado nunca aprova.

**4. Risco antes de execução.** O comando de aceite passa por `ferramentas.risco` antes de
rodar, com a mesma política de qualquer comando de shell do motor — e **comando de shell
nunca é `livre` neste projeto**. `travado` não executa: devolve REPROVADO dizendo qual
família recusou. Autonomia de processo não é autonomia de risco; um plano-mestre não
ganha o direito de rodar `rm -rf` só porque a palavra "aceite" está no campo.

Sobre o teto de saída: um veredito é lido DENTRO do contexto do modelo, e `relatorio.py`
já documenta o preço de esquecer isso (uma trilha de 50 mil linhas virava 3,1 MB
impressos). A saída é cortada em `TETO_SAIDA` caracteres, mantendo o começo **e** o fim —
o começo tem a primeira falha, o fim tem a linha de resumo; cortar só o rabo jogaria fora
a conclusão. O corte anuncia quantos caracteres ficaram de fora.

Sobre a redação: a saída é redigida (`trilha.redigir`) ANTES de ser cortada, e essa ordem
é a correção de um furo real e não zelo teórico. Cortando primeiro, uma credencial que
cai em cima da fronteira do corte perde o rabo, deixa de casar o padrão que a reconhece, e
o pedaço que sobrou vai em claro para o disco. Redigir primeiro fecha isso. O que fica no
campo `saida` do veredito já é o texto redigido, e não uma segunda cópia crua.

Só biblioteca padrão. `subprocess` basta.
"""
from __future__ import annotations

import math
import os
import signal
import subprocess
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from ferramentas import config, risco, trilha

APROVADO = "APROVADO"
REPROVADO = "REPROVADO"

#: Os dois únicos vereditos possíveis. Não existe "PARCIAL", não existe "INCONCLUSIVO":
#: um critério de aceite ou foi satisfeito ou não foi, e um terceiro valor viraria a
#: gaveta onde o caso duvidoso é guardado sem ninguém decidir nada.
RESULTADOS: tuple[str, ...] = (APROVADO, REPROVADO)

#: Tempo máximo padrão de um comando de aceite, em segundos. Generoso porque uma suíte
#: real leva minutos (a deste projeto leva ~112 s), mas finito porque comando que trava
#: não pode travar o programa inteiro.
TIMEOUT_PADRAO = 600.0

#: Teto de caracteres da saída guardada. Em CARACTERES e não em linhas: o custo que
#: importa é o de contexto, e uma única linha de log pode ter megabytes.
TETO_SAIDA = 8000

#: Quanto se espera pela saída parcial depois de matar um comando estourado. Curto: a
#: essa altura o veredito já está decidido (REPROVADO por tempo), e a saída parcial é
#: um bônus de diagnóstico — nunca uma razão para continuar preso.
_ESPERA_APOS_MATAR = 5.0

#: Ferramenta com que o executor assina suas linhas na trilha.
FERRAMENTA_TRILHA = "executor"


class VereditoSemEvidencia(Exception):
    """Tentativa de montar um veredito que não se sustenta na evidência capturada.

    Cobre os quatro casos: código de saída de tipo errado, booleano no lugar de código,
    ausência de código num veredito que não é REPROVADO fundamentado, e veredito que
    contradiz o código capturado (APROVADO com código diferente de zero, ou REPROVADO
    com zero).
    """


class TimeoutObrigatorio(ValueError):
    """Chamada sem prazo utilizável (`None`, zero, negativo, infinito ou não numérico).

    Herda de `ValueError` para que quem já trata erro de argumento continue tratando —
    o que não pode acontecer é o executor assumir um prazo "razoável" no lugar de quem
    chamou e ficar preso para sempre num comando que não termina.
    """


@dataclass(frozen=True)
class Veredito:
    """Resultado de um critério de aceite, com a evidência que o sustenta.

    `codigo_saida` não tem valor default: é o que torna a regra estrutural. Um veredito
    sem código de saída não é um veredito otimista, é um objeto que não chega a existir.

    `saida` e `comando` já vêm redigidos e cortados — ver o docstring do módulo.
    """

    resultado: str
    codigo_saida: int | None
    comando: str
    saida: str = ""
    motivo: str = ""
    duracao_s: float = 0.0

    def __post_init__(self) -> None:
        if self.resultado not in RESULTADOS:
            raise VereditoSemEvidencia(
                f"resultado {self.resultado!r} não é um veredito; use um de: "
                + ", ".join(RESULTADOS)
            )
        codigo = self.codigo_saida
        if isinstance(codigo, bool):
            # `bool` é `int` em Python, e sem esta linha `codigo_saida=True` passaria
            # como se fosse o código 1 e `False` como o código 0 — um veredito APROVADO
            # construído a partir de um "deu certo?" booleano, que é a opinião que este
            # módulo existe para não aceitar.
            raise VereditoSemEvidencia(
                "codigo_saida booleano: um veredito se apoia no código de saída do "
                "processo, não num 'deu certo' de quem chamou"
            )
        if codigo is not None and not isinstance(codigo, int):
            raise VereditoSemEvidencia(
                f"codigo_saida precisa ser inteiro ou None (comando não executado); "
                f"veio {type(codigo).__name__}"
            )
        if codigo is None:
            # Ausência de código é evidência de que o comando NÃO terminou. Ela reprova,
            # e nunca aprova — e precisa dizer por quê, senão o relatório fica com um
            # REPROVADO órfão que ninguém sabe reabrir.
            if self.resultado != REPROVADO:
                raise VereditoSemEvidencia(
                    "sem código de saída capturado só existe veredito REPROVADO: "
                    "o que não foi verificado não pode aprovar"
                )
            if not (self.motivo or "").strip():
                raise VereditoSemEvidencia(
                    "veredito sem código de saída exige motivo explícito (tempo "
                    "esgotado, recusa por risco, falha ao iniciar)"
                )
            return
        esperado = julgar(codigo)
        if self.resultado != esperado:
            raise VereditoSemEvidencia(
                f"veredito {self.resultado} contradiz o código de saída {codigo} "
                f"(código {codigo} é {esperado}); só o código de saída decide"
            )

    @property
    def aprovado(self) -> bool:
        return self.resultado == APROVADO

    @property
    def houve_execucao(self) -> bool:
        """Diz se o comando chegou a terminar e produzir código de saída."""
        return self.codigo_saida is not None


def julgar(codigo_saida: int) -> str:
    """Traduz código de saída em veredito: 0 é APROVADO, qualquer outro é REPROVADO.

    Uma linha, de propósito. Toda a tentação de sofisticação (ignorar o código 5 de
    "nenhum teste coletado", perdoar aviso de deprecação, ler o texto) é a mesma
    tentação: devolver a decisão para quem interpreta. O contrato com quem declara o
    aceite é o contrato universal de processo — saiu 0, passou.
    """
    return APROVADO if codigo_saida == 0 else REPROVADO


def preparar_saida(bruta: str, teto: int = TETO_SAIDA) -> str:
    """Redige credencial e corta no teto — **nesta ordem**, que é o ponto.

    Cortar antes de redigir deixa passar a credencial que cai em cima da fronteira: o
    pedaço que sobra não casa mais o padrão que a reconhece e vai em claro para a
    trilha. Redigir primeiro elimina o caso.

    O corte guarda o começo e o fim, com um aviso no meio dizendo quantos caracteres
    ficaram de fora. O começo costuma trazer a primeira falha e o fim a linha de
    resumo; cortar só pelo fim jogaria a conclusão fora. O aviso não conta contra o
    teto — ele é o recibo do corte, não conteúdo.
    """
    if teto <= 0:
        raise ValueError(f"teto de saída precisa ser positivo; veio {teto!r}")
    texto = trilha.redigir(bruta if isinstance(bruta, str) else str(bruta))
    if len(texto) <= teto:
        return texto
    inicio = teto // 2
    fim = teto - inicio
    omitidos = len(texto) - teto
    aviso = (
        f"\n... [{omitidos} caractere(s) de saída omitido(s) pelo teto de "
        f"{teto}] ...\n"
    )
    return texto[:inicio] + aviso + texto[len(texto) - fim :]


def executar(
    comando: str,
    *,
    raiz: Path,
    timeout_s: float = TIMEOUT_PADRAO,
    teto_saida: int = TETO_SAIDA,
    config_efetiva: dict | None = None,
    fase: str = "PROGRAMA",
    ciclo: str = "",
    quando: str | None = None,
    registrar_na_trilha: bool = True,
) -> Veredito:
    """Roda o comando de aceite e devolve o veredito com a evidência.

    Ordem fixa, e cada passo existe por um motivo:

    1. **valida o prazo** — sem prazo utilizável nada roda (`TimeoutObrigatorio`);
    2. **classifica o risco** com `ferramentas.risco`, exatamente como qualquer comando
       de shell do motor;
    3. **recusa sem executar** o que a política travou, ou o comando vazio;
    4. **executa** dentro de `raiz`, capturando saída e código;
    5. **registra na trilha** a linha com comando, veredito, código e saída redigida.

    O passo 2 vem antes do 4 e não há caminho que pule dele para o 4 — é o que impede
    que "o plano-mestre mandou" vire licença para qualquer comando.

    A saída de erro é fundida na saída padrão (`stderr=STDOUT`): o diagnóstico de uma
    suíte que quebra costuma sair pelos dois canos, e dois campos separados só fariam
    quem lê o relatório reconstruir a ordem dos eventos na cabeça.

    Sempre devolve um `Veredito`. Erro de infraestrutura (diretório inexistente,
    executável ausente, permissão) vira REPROVADO com motivo — nunca exceção que sobe
    até o chamador e nunca, em hipótese alguma, um APROVADO por omissão.
    """
    tempo_limite = _exigir_timeout(timeout_s)
    if teto_saida <= 0:
        raise ValueError(f"teto de saída precisa ser positivo; veio {teto_saida!r}")

    raiz = Path(raiz)
    texto_comando = comando if isinstance(comando, str) else ""
    cfg = config_efetiva if config_efetiva is not None else config.carregar(raiz)
    classificacao = risco.classificar(
        "Bash", {"command": texto_comando}, raiz=raiz, config=cfg
    )

    if classificacao.nivel == risco.TRAVADO:
        veredito = Veredito(
            resultado=REPROVADO,
            codigo_saida=None,
            comando=trilha.redigir(texto_comando),
            saida="",
            motivo=(
                f"recusado pela política de risco ({classificacao.regra or 'sem regra'}): "
                f"{classificacao.motivo} — comando NÃO executado"
            ),
        )
        _registrar(veredito, classificacao, raiz, fase, ciclo, quando, registrar_na_trilha)
        return veredito

    if not texto_comando.strip():
        veredito = Veredito(
            resultado=REPROVADO,
            codigo_saida=None,
            comando="",
            saida="",
            motivo=(
                "critério de aceite sem comando executável: não há o que rodar, e um "
                "veredito sem evidência é opinião"
            ),
        )
        _registrar(veredito, classificacao, raiz, fase, ciclo, quando, registrar_na_trilha)
        return veredito

    inicio = time.monotonic()
    codigo, saida_bruta, falha = _rodar(texto_comando, raiz, tempo_limite)
    duracao = round(time.monotonic() - inicio, 3)

    if codigo is None:
        veredito = Veredito(
            resultado=REPROVADO,
            codigo_saida=None,
            comando=trilha.redigir(texto_comando),
            saida=preparar_saida(saida_bruta, teto_saida),
            motivo=falha or "comando não produziu código de saída",
            duracao_s=duracao,
        )
    else:
        veredito = Veredito(
            resultado=julgar(codigo),
            codigo_saida=codigo,
            comando=trilha.redigir(texto_comando),
            saida=preparar_saida(saida_bruta, teto_saida),
            motivo=f"código de saída {codigo}",
            duracao_s=duracao,
        )
    _registrar(veredito, classificacao, raiz, fase, ciclo, quando, registrar_na_trilha)
    return veredito


def _exigir_timeout(timeout_s) -> float:
    """Recusa prazo ausente, não numérico, não positivo ou infinito.

    `None` é recusado explicitamente porque `subprocess` o entende como "espere para
    sempre" — o valor que transforma um comando travado numa sessão travada. Infinito
    é a mesma coisa escrita com outro tipo.
    """
    if isinstance(timeout_s, bool) or not isinstance(timeout_s, (int, float)):
        raise TimeoutObrigatorio(
            f"timeout obrigatório em segundos; veio {timeout_s!r} — comando que trava "
            "não pode travar o programa"
        )
    valor = float(timeout_s)
    if not math.isfinite(valor) or valor <= 0:
        raise TimeoutObrigatorio(
            f"timeout precisa ser um número finito e positivo; veio {timeout_s!r}"
        )
    return valor


def _kwargs_de_grupo() -> dict:
    """Faz o comando nascer num grupo de processos próprio, quando a plataforma deixa.

    No POSIX isso é o que permite matar a árvore inteira com `killpg`: matar só o filho
    direto deixa o neto vivo segurando o cano da saída, e a leitura seguinte fica
    pendurada — o timeout viraria decorativo. No Windows não existe equivalente aqui
    (o parâmetro é POSIX e levanta `ValueError`), e a árvore é derrubada por
    `taskkill /T` em `_matar_arvore`.
    """
    if os.name == "nt":
        return {}
    return {"start_new_session": True}


def _matar_arvore(processo: subprocess.Popen) -> None:
    """Derruba o comando e tudo que ele gerou. Best-effort, nunca propaga.

    O filho direto quase nunca é o processo que interessa: com `shell=True` o filho é o
    interpretador de comandos, e quem está travado é o neto. Matar só o pai deixaria o
    neto rodando e segurando o cano — o processo que o timeout deveria ter encerrado
    continuaria vivo depois de o veredito sair.
    """
    if os.name == "nt":
        try:
            subprocess.run(
                ["taskkill", "/F", "/T", "/PID", str(processo.pid)],
                capture_output=True,
                timeout=_ESPERA_APOS_MATAR,
            )
        except Exception:  # noqa: BLE001 — matar é best-effort; o veredito já saiu
            pass
    else:
        try:
            os.killpg(os.getpgid(processo.pid), signal.SIGKILL)
        except Exception:  # noqa: BLE001
            pass
    try:
        processo.kill()
    except Exception:  # noqa: BLE001
        pass


def _rodar(comando: str, raiz: Path, tempo_limite: float) -> tuple[int | None, str, str]:
    """Executa e devolve `(codigo, saida, falha)`. `codigo=None` quando não houve.

    `shell=True` porque o critério de aceite é declarado como uma linha de comando de
    verdade (`python -m pytest ... -q`), com as formas do shell que o humano escreveu —
    e porque é assim que `ferramentas.risco` já entende e classifica comando neste
    motor. A alternativa (quebrar em lista) mudaria o que roda em relação ao que foi
    classificado, que é a pior combinação possível.

    `errors="replace"` na decodificação: a saída de um comando no Windows nem sempre é
    UTF-8, e um byte estranho no meio de um log não pode virar exceção que derruba o
    veredito de uma suíte que rodou inteira.

    Depois do timeout, a saída parcial é buscada com prazo PRÓPRIO: se um neto
    sobreviveu segurando o cano, o executor desiste da saída — nunca do veredito.
    """
    try:
        processo = subprocess.Popen(  # noqa: S602 — ver docstring
            comando,
            shell=True,
            cwd=str(raiz),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            stdin=subprocess.DEVNULL,
            text=True,
            encoding="utf-8",
            errors="replace",
            **_kwargs_de_grupo(),
        )
    except Exception as erro:  # noqa: BLE001 — falha ao nascer reprova, não estoura
        return None, "", (
            f"falha ao iniciar o comando ({erro.__class__.__name__}): {erro}"
        )

    try:
        saida, _ = processo.communicate(timeout=tempo_limite)
        return processo.returncode, saida or "", ""
    except subprocess.TimeoutExpired:
        _matar_arvore(processo)
        try:
            parcial, _ = processo.communicate(timeout=_ESPERA_APOS_MATAR)
        except Exception:  # noqa: BLE001 — neto segurando o cano; a saída se perde
            parcial = ""
        return None, parcial or "", (
            f"tempo esgotado: o comando passou de {tempo_limite:g}s e foi encerrado "
            "sem produzir código de saída"
        )
    except Exception as erro:  # noqa: BLE001
        _matar_arvore(processo)
        return None, "", (
            f"falha ao capturar a saída ({erro.__class__.__name__}): {erro}"
        )


def _registrar(
    veredito: Veredito,
    classificacao: risco.Classificacao,
    raiz: Path,
    fase: str,
    ciclo: str,
    quando: str | None,
    ligado: bool,
) -> None:
    """Grava a linha do veredito na trilha, com a evidência junto.

    A linha carrega o mesmo esqueleto das demais (`quando`/`fase`/`ferramenta`/`alvo`/
    `risco`/`regra`) para que relatório e leitura da trilha continuem funcionando sem
    caso especial, mais os campos que só um veredito tem: resultado, código de saída,
    duração e a saída redigida.

    `do_motor: True` porque esta linha é escrita pelo próprio motor: sem a marca, o
    gate de fase leria o registro do executor como evidência do trabalho do ciclo — o
    defeito encontrado na revisão de 2026-07-31, aqui em versão pior, porque bastaria
    verificar o aceite para "provar" que houve trabalho.

    `trilha.registrar` nunca propaga exceção, e essa propriedade é herdada de
    propósito: o comando já rodou e o veredito já está decidido; falhar em anotá-lo não
    pode reescrever o que aconteceu.
    """
    if not ligado:
        return
    linha = {
        "quando": quando or datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "fase": fase,
        "ferramenta": FERRAMENTA_TRILHA,
        "alvo": veredito.comando,
        "risco": classificacao.nivel,
        "regra": classificacao.regra,
        "do_motor": True,
        "veredito": veredito.resultado,
        "codigo_saida": veredito.codigo_saida,
        "duracao_s": veredito.duracao_s,
        "motivo": veredito.motivo,
        "saida": veredito.saida,
    }
    if ciclo:
        # Só quando há ciclo de verdade: `relatorio._do_ciclo_corrente` trata linha com
        # `ciclo` vazio como "anterior à separação por ciclo" e a reporta como ignorada.
        linha["ciclo"] = ciclo
    trilha.registrar(raiz, linha)
