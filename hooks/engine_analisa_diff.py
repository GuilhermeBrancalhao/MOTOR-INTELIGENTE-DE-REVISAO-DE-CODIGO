#!/usr/bin/env python3
"""FASE 3: Analisador de diff para sugestão automática de motor.

Hook PreToolUse que analisa mudanças do usuário e sugere motor apropriado.
Padrões classificados: revisar, otimizar, arquitetar, materializar, diagramar.
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
        self.sugestoes = []
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
        """Gera texto de sugestão formatado."""
        if motor not in self.PADROES:
            return ""

        config = self.PADROES[motor]
        confianca_pct = int(
            (self.confianca.get(motor, 0) / max(self.confianca.values() or [1]))
            * 100
        )

        return f"💡 Sugestão de motor: {motor} ({confianca_pct}%)\n   {config['descricao']}"


def processar_evento_hook(evento: dict) -> Optional[str]:
    """Processa evento PreToolUse e retorna sugestão."""
    # Extrair diff do evento
    # Formato esperado: evento["tool_use_input"] pode conter diffs de mudanças
    diffs = evento.get("diffs", "")
    if not diffs:
        # Tentar extrair de caminho se houver mudanças locais
        cwd = evento.get("cwd", "")
        diffs = _extrair_diffs_locais(cwd)

    if not diffs:
        return None

    analisador = AnalisadorDiff()
    motor = analisador.analisar_diff(diffs)

    if motor:
        return analisador.gerar_sugestao(motor)

    return None


def _extrair_diffs_locais(cwd: str) -> str:
    """Tenta extrair diffs de mudanças locais (stub para teste)."""
    # Em produção, isso rodaria 'git diff' no cwd
    # Por enquanto, retorna vazio
    return ""


if __name__ == "__main__":
    # Modo teste: ler evento do stdin
    try:
        evento = json.loads(sys.stdin.read())
        resultado = processar_evento_hook(evento)

        if resultado:
            print(resultado)
        sys.exit(0)
    except Exception as e:
        print(f"ERRO: {e}", file=sys.stderr)
        sys.exit(1)
