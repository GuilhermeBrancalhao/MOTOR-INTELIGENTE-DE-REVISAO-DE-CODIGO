#!/usr/bin/env python3
"""Classificador de diff que sugere um motor — MÓDULO, não hook.

Apesar de morar em `hooks/`, isto **não é um hook**: não está em
`hooks/hooks.json` e o Claude Code nunca o executa. Quem o usa é
`hooks/engine_contexto.py` (UserPromptSubmit), que o importa para montar a linha
de sugestão do cartão. A docstring antiga o anunciava como "Hook PreToolUse", o
que é um convite a registrá-lo — e registrá-lo seria um defeito de segurança:
o bloco `__main__` abaixo sai com **código 1**, e o contrato deste repositório
(ver `hooks/engine.sh` e `hooks/engine_risco.py`) é explícito em que 1 não
bloqueia nada e, num hook de decisão, equivale a liberar a ação.

O `__main__` existe só para inspeção manual (`echo '{...}' | py
hooks/engine_analisa_diff.py`), e por isso pode sair 1: é uma ferramenta de
linha de comando, não um caminho de decisão.

Padrões classificados: revisar, otimizar, arquitetar, materializar, diagramar.
A classificação é heurística por contagem de palavra-chave e extensão — serve
para sugerir, nunca para decidir.
"""
import json
import re
import sys
from pathlib import Path
from typing import Optional


class AnalisadorDiff:
    """Analisa diff e sugere motor."""

    # Padrões de mudança por tipo
    PADROES = {
        "revisar-codigo": {
            "palavras_chave": [
                "try",
                "except",
                "null",
                "None",
                "injection",
                "sql",
                "xss",
                "csrf",
                "deadlock",
                "race",
                "timeout",
                "encoding",
                "utf",
                "memory",
                "leak",
            ],
            "extensoes": [".py", ".java", ".js", ".ts", ".go", ".rs", ".cpp"],
            "descricao": "Detectou código com padrões de segurança/confiabilidade",
        },
        "otimizar-performance": {
            "palavras_chave": [
                "query",
                "select",
                "join",
                "index",
                "cache",
                "buffer",
                "algorithm",
                "loop",
                "O(n)",
                "sort",
                "memory",
                "cpu",
                "latency",
                "throughput",
            ],
            "extensoes": [".py", ".java", ".sql", ".go"],
            "descricao": "Detectou código com foco em performance/otimização",
        },
        "arquitetar-sistema": {
            "palavras_chave": [
                "abstract",
                "interface",
                "pattern",
                "architecture",
                "module",
                "package",
                "boundary",
                "dependency",
                "refactor",
                "design",
                "extends",
                "implements",
                "inheritance",
            ],
            "extensoes": [".py", ".java", ".ts", ".go", ".rs"],
            "descricao": "Detectou refatoração arquitetural ou design patterns",
        },
        "materializar-ideia": {
            "palavras_chave": [
                "def",
                "function",
                "endpoint",
                "handler",
                "controller",
                "service",
                "api",
                "test",
                "assert",
                "mock",
            ],
            "extensoes": [".py", ".java", ".js", ".ts", ".go"],
            "descricao": "Detectou implementação de nova feature/função",
        },
        "diagramar": {
            "palavras_chave": [
                "flow",
                "sequence",
                "er",
                "entity",
                "relationship",
                "diagram",
                "model",
                "schema",
            ],
            "extensoes": [".md", ".txt", ".yaml", ".yml"],
            "descricao": "Detectou mudança em documentação/modelos",
        },
    }

    def __init__(self):
        #: Pontuação por motor, preenchida por `analisar_diff` e lida por
        #: `gerar_sugestao`. Um analisador serve a UM diff: reaproveitá-lo soma a
        #: pontuação de diffs diferentes e falseia a participação.
        self.confianca = {}

    def analisar_diff(self, diff_texto: str) -> Optional[str]:
        """Analisa diff e retorna sugestão de motor (mais confiante)."""
        if not diff_texto or not diff_texto.strip():
            return None

        # Contar ocorrências de cada motor
        for motor, config in self.PADROES.items():
            score = self._calcular_score(diff_texto, config)
            if score > 0:
                self.confianca[motor] = score

        if not self.confianca:
            return None

        # Retornar motor com maior confiança
        motor_sugerido = max(self.confianca.items(), key=lambda x: x[1])
        return motor_sugerido[0]

    def _calcular_score(self, diff_texto: str, config: dict) -> int:
        """Calcula score de confiança para um motor."""
        score = 0
        diff_lower = diff_texto.lower()

        # Pontos por palavras-chave (word boundaries para evitar falsos positivos)
        for palavra in config["palavras_chave"]:
            # Usar regex com word boundaries
            pattern = r"\b" + re.escape(palavra.lower()) + r"\b"
            count = len(re.findall(pattern, diff_lower))

            # Peso diferenciado para certas palavras
            peso = 3
            if palavra in ["abstract", "interface", "pattern"]:
                peso = 4  # Mais peso para arquitetura
            elif palavra in ["query", "join", "index"]:
                peso = 4  # Mais peso para otimização
            elif palavra in ["try", "except"]:
                peso = 4  # Mais peso para review

            score += count * peso

        # Bônus significativo por extensões (peso grande)
        for ext in config["extensoes"]:
            if ext in diff_texto:
                score += 15

        return score

    def gerar_sugestao(self, motor: str) -> str:
        """Texto da sugestão, com a **participação** do motor no total de pontos.

        O percentual antigo dividia o score do vencedor pelo MAIOR score — e o
        vencedor é o maior por construção, então o cartão dizia `(100%)` sempre,
        para qualquer diff. Um número constante disfarçado de medida é pior que
        número nenhum: ele vai para o contexto do modelo a cada turno afirmando
        uma certeza que ninguém apurou.

        A participação no total, sim, varia e diz algo: quatro candidatos
        empatados dão ~25% (o diff não separa nada), um vencedor isolado dá um
        número alto (a evidência aponta para um lado só).
        """
        if motor not in self.PADROES:
            return ""

        config = self.PADROES[motor]
        total = sum(self.confianca.values())
        participacao = int((self.confianca.get(motor, 0) / total) * 100) if total else 0

        return f"💡 Sugestão de motor: {motor} ({participacao}%)\n   {config['descricao']}"


def processar_evento_hook(evento: dict) -> Optional[str]:
    """Sugere um motor a partir do diff que vier no evento.

    Só serve à inspeção manual pelo `__main__`: quem usa isto em produção é
    `hooks/engine_contexto.py`, que chama `AnalisadorDiff` direto e obtém o diff
    com `git diff` de verdade (`_extrair_diff_local`, com timeout).

    Aqui o diff tem de vir pronto em `evento["diffs"]`. Havia um
    `_extrair_diffs_locais(cwd)` que prometia rodar `git diff` e devolvia string
    vazia em todos os casos — a chamada parecia cobrir o caso "sem `diffs` no
    evento" e não cobria nada. Sem diff, esta função devolve `None`, que é a
    verdade.
    """
    diffs = evento.get("diffs", "")
    if not diffs:
        return None

    analisador = AnalisadorDiff()
    motor = analisador.analisar_diff(diffs)

    if motor:
        return analisador.gerar_sugestao(motor)

    return None


if __name__ == "__main__":
    # Inspeção manual, fora de qualquer caminho de decisão do Claude Code — por
    # isso a saída 1 aqui é legítima (ver o docstring do módulo).
    try:
        evento = json.loads(sys.stdin.read())
        resultado = processar_evento_hook(evento)

        if resultado:
            print(resultado)
        sys.exit(0)
    except Exception as e:
        print(f"ERRO: {e}", file=sys.stderr)
        sys.exit(1)
