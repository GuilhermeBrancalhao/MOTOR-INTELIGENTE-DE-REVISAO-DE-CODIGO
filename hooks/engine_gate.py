#!/usr/bin/env python3
"""Hook Stop do ENGINE.

Contrato (confirmado na documentação oficial do Claude Code, hooks.md, via
subagente `claude-code-guide`): o evento chega em JSON no STDIN com, entre
outras chaves, `session_id`, `prompt_id`, `transcript_path`, `cwd`,
`permission_mode`, `hook_event_name` ("Stop"), `last_assistant_message` e
`stop_hook_active` (booleano). Saída 2 BLOQUEIA a parada — o stderr vira
feedback direto para o Claude continuar trabalhando (via essa rota, não pela
alternativa JSON `decision: "block"`, que é equivalente mas mais verbosa e
diferente do padrão já usado pelos outros hooks deste plugin). Saída 0 deixa a
parada seguir normalmente.

`stop_hook_active=true` significa que um Stop hook (deste ou de outro plugin)
já bloqueou a parada NESTE turno — o Claude Code usa esse campo para evitar um
laço onde o hook barra a parada, o Claude responde, o Stop dispara nele de
novo, e assim por diante sem fim. Por contrato, essa checagem é a PRIMEIRA
coisa que este hook faz: `true` sai 0 imediatamente, sem sequer carregar o
estado do motor.

Isso por si só não basta para "cobrar uma vez por fase": `stop_hook_active`
descreve o turno corrente, não sobrevive entre invocações separadas do hook em
sessões diferentes (nem entre reinícios do Claude Code). A segunda camada —
e a mais importante desta tarefa — é o contador `cobrancas_por_fase` GRAVADO NO
ESTADO EM DISCO: incrementado e persistido ANTES de imprimir a cobrança e sair
2. Da próxima vez que o Stop disparar nessa mesma fase, o contador já mostra
`>= 1` e o hook sai 0 sem cobrar de novo — é isso que impede o laço infinito
de re-invocação, não `stop_hook_active`. (O Claude Code também tem um teto
próprio de bloqueios consecutivos por turno; esta camada garante "uma cobrança
por fase" independente dele.)

**Ação do próprio motor não conta como evidência.** A única forma de entrar em
BUILD/TESTE/REVISAO é rodar `ferramentas/cli.py fase <DESTINO>` por um comando de
shell — e esse comando dispara o `PostToolUse`, que gravava na trilha uma linha já
carimbada com a fase NOVA. O gate então achava "ação da fase" na primeira consulta
e nunca cobrava nada em operação real (os testes que passavam mudavam a fase pela
API, não pela CLI, e por isso não viam o buraco). Por isso `engine_trilha.py`
marca essas linhas com `do_motor: true` e o gate as IGNORA: a evidência de uma fase
não pode ser satisfeita pela própria chamada que mudou para essa fase.

Cobra evidência quando, e só quando: o motor está ligado, a fase atual é
BUILD, TESTE ou REVISAO, a trilha não tem nenhuma ação registrada daquela
fase (fora as do próprio motor), e o contador da fase ainda está em zero.
Qualquer outra situação —
motor desligado, fase fora da lista, trilha já tem ação da fase, contador
já em 1 ou mais, evento malformado, qualquer exceção — sai 0 sem cobrar.
Nunca bloqueia por erro: ao contrário do PreToolUse (`engine_risco.py`), aqui
a falha segura é NÃO travar a saída do Claude, porque um Stop preso por bug
interno é pior do que um Stop que deixa passar sem evidência.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from _comum import forcar_utf8, raiz_do_ciclo  # noqa: E402

# Ver `_comum.forcar_utf8`: sem isso, acento na cobrança sai como mojibake no
# console do Windows.
forcar_utf8()

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ferramentas import estado, trilha  # noqa: E402

#: Fases que exigem evidência de trabalho na trilha antes de a sessão parar.
_FASES_QUE_EXIGEM_EVIDENCIA = frozenset({"BUILD", "TESTE", "REVISAO"})


def principal() -> int:
    # Rede de segurança de nível externo: qualquer falha não prevista sai 0 —
    # este hook nunca deve travar a saída do Claude por causa de um bug seu.
    try:
        try:
            evento = json.load(sys.stdin)
        except Exception:  # noqa: BLE001
            return 0

        if not isinstance(evento, dict):
            return 0

        # Primeira checagem, por contrato: evita o laço "Stop bloqueia -> Claude
        # responde -> Stop dispara de novo" dentro do mesmo turno, antes mesmo
        # de tocar no estado do motor.
        if evento.get("stop_hook_active"):
            return 0

        raiz = raiz_do_ciclo(Path(evento.get("cwd") or "."))

        dados = estado.carregar(raiz)
        if not dados or not dados.get("ativo"):
            return 0

        fase = dados.get("fase")
        if fase not in _FASES_QUE_EXIGEM_EVIDENCIA:
            return 0

        cobrancas = dados.get("cobrancas_por_fase")
        if not isinstance(cobrancas, dict):
            cobrancas = {}
        if cobrancas.get(fase, 0) >= 1:
            return 0

        trilha_dados = trilha.ler(raiz)
        linhas = trilha_dados.get("linhas", [])
        tem_acao_da_fase = any(
            isinstance(linha, dict)
            and linha.get("fase") == fase
            and not linha.get("do_motor")
            for linha in linhas
        )
        if tem_acao_da_fase:
            return 0

        # O contador é o requisito central desta tarefa: grava ANTES de cobrar,
        # para que a segunda invocação do Stop nesta fase (mesmo em outra
        # sessão) já ache `>= 1` e não cobre de novo.
        cobrancas[fase] = cobrancas.get(fase, 0) + 1
        dados["cobrancas_por_fase"] = cobrancas
        try:
            estado.gravar(raiz, dados)
        except Exception:  # noqa: BLE001
            # Não conseguiu persistir o contador: cobrar agora arriscaria um
            # laço (a próxima invocação não veria o incremento), então melhor
            # deixar passar desta vez.
            return 0

        print(
            f"ENGINE [{fase}]: nenhuma ação desta fase está registrada na trilha "
            f"(.engine/trilha.jsonl). Antes de encerrar, mostre a evidência do "
            f"trabalho da fase {fase} (rodar os testes, aplicar a mudança, "
            f"registrar a revisão) ou volte ao trabalho da fase. Esta cobrança "
            f"só acontece uma vez por fase.",
            file=sys.stderr,
        )
        return 2
    except Exception:  # noqa: BLE001
        return 0


if __name__ == "__main__":
    sys.exit(principal())
