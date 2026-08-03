"""Gera `volumes/prontos/` a partir de `acervo/` — a cópia que o plugin carrega.

Por que este módulo existe, e por que ele não é conveniência
------------------------------------------------------------
O acervo (`acervo/`) é quem PRODUZ os volumes de conhecimento; o motor é um
plugin que se instala em outros projetos e, depois de instalado, é uma cópia
isolada — ele precisa levar os volumes consigo, porque o projeto hospedeiro não
tem o acervo. Até aqui, essa cópia era feita **à mão**, e o resultado foi o
previsível:

- `31-TESTING` estava em `volumes/prontos/` marcado `status: PRONTO`, enquanto a
  fonte dizia `RASCUNHO`. A cópia mentia sobre prontidão, e o detector de
  volumes (`hooks/volume_detector.py`) carregava o volume no cartão de contexto
  como se fosse consultável.
- `03-DISCOVERY`, esse sim `PRONTO` na fonte, nunca chegou na cópia.
- Nos volumes que existiam dos dois lados, o conteúdo já tinha derivado.

A regra que este módulo estabelece: **`volumes/prontos/` é artefato derivado.**
Ninguém edita nada lá dentro. Quem quiser mudar um volume muda em `acervo/` e
roda a sincronização. `--verificar` transforma isso em porta: o teste
`test_sincronizar.py` reprova a suíte se a cópia divergir da fonte, que é o
único jeito de a deriva ser barrada em vez de descoberta meses depois.

O critério de inclusão é o `status` do `_VOLUME.yml` da FONTE, e só ele. Volume
em `RASCUNHO` não viaja no plugin: um rascunho carregado no contexto como
conhecimento pronto é pior que volume ausente, porque quem lê não tem como
saber que está lendo rascunho.

Uso:

    py "${CLAUDE_PLUGIN_ROOT}/ferramentas/sincronizar.py"             # aplica
    py "${CLAUDE_PLUGIN_ROOT}/ferramentas/sincronizar.py" --verificar # só checa
    python -m ferramentas.sincronizar --verificar                     # da raiz
"""
from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

if not __package__:  # executado como script: a raiz do plugin não está no sys.path
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ferramentas.validar import ler_metadados  # noqa: E402

#: Diretório-fonte dentro da raiz do repositório unificado.
PASTA_ACERVO = "acervo"
#: Destino derivado, lido por `hooks/volume_detector.py` e por `ferramentas/validar.py`.
PASTA_DESTINO = ("volumes", "prontos")
#: Único status que viaja no plugin.
STATUS_CONSULTAVEL = "PRONTO"
#: Nome de diretório de volume: dois dígitos, hífen, nome. `00-INTRODUCAO` casa
#: com o padrão mas não é volume (é o contrato do acervo) e não tem `_VOLUME.yml`,
#: então cai fora sozinho por não ter status.
PADRAO_VOLUME = re.compile(r"^\d{2}-")
#: Lixo de execução que nunca deve entrar no artefato.
IGNORADOS = ("__pycache__", ".pytest_cache")


def raiz_padrao() -> Path:
    """Raiz do repositório (o pai de `ferramentas/`)."""
    return Path(__file__).resolve().parent.parent


def _relevante(caminho: Path) -> bool:
    if any(parte in IGNORADOS for parte in caminho.parts):
        return False
    return caminho.suffix != ".pyc"


def arquivos_do_volume(pasta: Path) -> dict[str, Path]:
    """Arquivos de um volume, indexados pelo caminho relativo (em POSIX, para a
    comparação não depender do separador do sistema)."""
    encontrados: dict[str, Path] = {}
    for arquivo in sorted(pasta.rglob("*")):
        if not arquivo.is_file():
            continue
        relativo = arquivo.relative_to(pasta)
        if not _relevante(relativo):
            continue
        encontrados[relativo.as_posix()] = arquivo
    return encontrados


def volumes_consultaveis(acervo: Path) -> dict[str, Path]:
    """Volumes da fonte cujo `_VOLUME.yml` declara `status: PRONTO`.

    Indexados pelo nome do diretório (ex.: `07-PROMPT-ENGINE`), que é o nome que
    o detector mostra no cartão de contexto.
    """
    prontos: dict[str, Path] = {}
    if not acervo.is_dir():
        return prontos
    for item in sorted(acervo.iterdir()):
        if not item.is_dir() or not PADRAO_VOLUME.match(item.name):
            continue
        metadados = ler_metadados(item / "_VOLUME.yml")
        if metadados.get("status") == STATUS_CONSULTAVEL:
            prontos[item.name] = item
    return prontos


def catalogo(prontos: dict[str, Path]) -> str:
    """Texto de `volumes/_catalogo.md` — também derivado, para não virar a
    próxima coisa que alguém atualiza à mão e esquece."""
    linhas = [
        "# Catálogo de Volumes Consultáveis",
        "",
        "Volumes de conhecimento marcados como PRONTO, carregados dinamicamente",
        "no contexto.",
        "",
        "<!-- ARQUIVO GERADO por ferramentas/sincronizar.py a partir de acervo/.",
        "     Não edite à mão: a próxima sincronização sobrescreve. -->",
        "",
    ]
    if not prontos:
        linhas.append("_Nenhum volume PRONTO no acervo._")
    else:
        for nome, pasta in prontos.items():
            metadados = ler_metadados(pasta / "_VOLUME.yml")
            tipo = metadados.get("tipo", "?")
            linhas.append(f"- **{nome}** — tipo {tipo}")
    return "\n".join(linhas) + "\n"


def divergencias(raiz: Path | None = None) -> list[str]:
    """Diferenças entre a fonte e o artefato, em linguagem de gente.

    Lista vazia significa que a cópia do plugin é exatamente o que o acervo diz.
    """
    raiz = raiz or raiz_padrao()
    prontos = volumes_consultaveis(raiz / PASTA_ACERVO)
    destino = raiz.joinpath(*PASTA_DESTINO)

    existentes = (
        {p.name for p in destino.iterdir() if p.is_dir()} if destino.is_dir() else set()
    )
    achados: list[str] = []

    for sobrando in sorted(existentes - set(prontos)):
        achados.append(
            f"{sobrando}: está em volumes/prontos/ mas não é PRONTO no acervo"
        )
    for faltando in sorted(set(prontos) - existentes):
        achados.append(
            f"{faltando}: é PRONTO no acervo mas não está em volumes/prontos/"
        )

    for nome in sorted(set(prontos) & existentes):
        na_fonte = arquivos_do_volume(prontos[nome])
        no_destino = arquivos_do_volume(destino / nome)
        for arquivo in sorted(set(no_destino) - set(na_fonte)):
            achados.append(f"{nome}/{arquivo}: existe na cópia e não na fonte")
        for arquivo in sorted(set(na_fonte) - set(no_destino)):
            achados.append(f"{nome}/{arquivo}: existe na fonte e não na cópia")
        for arquivo in sorted(set(na_fonte) & set(no_destino)):
            if na_fonte[arquivo].read_bytes() != no_destino[arquivo].read_bytes():
                achados.append(f"{nome}/{arquivo}: conteúdo diferente da fonte")

    arquivo_catalogo = raiz / "volumes" / "_catalogo.md"
    esperado = catalogo(prontos)
    atual = (
        arquivo_catalogo.read_text(encoding="utf-8")
        if arquivo_catalogo.exists()
        else ""
    )
    if atual != esperado:
        achados.append("volumes/_catalogo.md: não corresponde aos volumes PRONTO")

    return achados


def sincronizar(raiz: Path | None = None) -> list[str]:
    """Reescreve o artefato a partir da fonte. Devolve o que mudou."""
    raiz = raiz or raiz_padrao()
    prontos = volumes_consultaveis(raiz / PASTA_ACERVO)
    destino = raiz.joinpath(*PASTA_DESTINO)
    destino.mkdir(parents=True, exist_ok=True)

    feito: list[str] = []

    for pasta in sorted(p for p in destino.iterdir() if p.is_dir()):
        if pasta.name not in prontos:
            shutil.rmtree(pasta)
            feito.append(f"removido {pasta.name} (não é PRONTO no acervo)")

    for nome, origem in prontos.items():
        alvo = destino / nome
        # Reescrita completa em vez de cópia incremental: é o que garante que o
        # artefato seja função apenas da fonte. Cópia incremental deixaria para
        # trás arquivo que a fonte apagou — que é uma das formas da deriva.
        if alvo.exists():
            shutil.rmtree(alvo)
        alvo.mkdir(parents=True)
        for relativo, arquivo in arquivos_do_volume(origem).items():
            destino_arquivo = alvo / relativo
            destino_arquivo.parent.mkdir(parents=True, exist_ok=True)
            destino_arquivo.write_bytes(arquivo.read_bytes())
        feito.append(f"sincronizado {nome}")

    (raiz / "volumes" / "_catalogo.md").write_text(catalogo(prontos), encoding="utf-8")
    feito.append("regenerado volumes/_catalogo.md")
    return feito


def main(argumentos: list[str] | None = None) -> int:
    argumentos = list(sys.argv[1:] if argumentos is None else argumentos)
    raiz = raiz_padrao()
    if "--raiz" in argumentos:
        indice = argumentos.index("--raiz")
        raiz = Path(argumentos[indice + 1]).resolve()
        del argumentos[indice : indice + 2]

    if "--verificar" in argumentos:
        achados = divergencias(raiz)
        if not achados:
            print("volumes/prontos/ esta em dia com o acervo.")
            return 0
        print("volumes/prontos/ divergiu do acervo:", file=sys.stderr)
        for achado in achados:
            print(f"  - {achado}", file=sys.stderr)
        print(
            "\nRode `python -m ferramentas.sincronizar` para regenerar.",
            file=sys.stderr,
        )
        return 1

    for linha in sincronizar(raiz):
        print(linha)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
