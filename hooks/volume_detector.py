#!/usr/bin/env python3
"""FASE 4: Detector dinâmico de volumes PRONTO.

Detecta automaticamente volumes em volumes/prontos/ sem hardcoding.
Usa cache com invalidação inteligente para performance.
"""
import json
from pathlib import Path
from typing import Optional, List
from datetime import datetime, timedelta


class DetectorVolumesAoVivo:
    """Detecta volumes PRONTO dinamicamente."""

    def __init__(self, cache_ttl_segundos: int = 300):
        self.cache_ttl = timedelta(seconds=cache_ttl_segundos)
        self.cache = {}
        self.ultima_atualizacao = {}

    def _caminho_volumes(self, raiz: Path) -> Path:
        """Retorna caminho para volumes/prontos."""
        return raiz / "volumes" / "prontos"

    def _esta_cache_valido(self, chave: str) -> bool:
        """Verifica se cache ainda é válido."""
        if chave not in self.ultima_atualizacao:
            return False
        tempo_decorrido = datetime.now() - self.ultima_atualizacao[chave]
        return tempo_decorrido < self.cache_ttl

    def _ler_resumo_volume(self, volume_path: Path) -> Optional[str]:
        """Lê resumo do volume de seu README.md."""
        try:
            readme = volume_path / "README.md"
            if readme.exists():
                conteudo = readme.read_text(encoding="utf-8")
                # Primeira linha não-vazia (sem #)
                for linha in conteudo.split("\n"):
                    if linha.strip() and not linha.startswith("#"):
                        # Cortar a 100 caracteres
                        texto = " ".join(linha.strip().split())
                        return texto if len(texto) <= 100 else texto[:97] + "…"
        except Exception:
            pass
        return None

    def detectar_volumes(self, raiz: Path) -> List[tuple[str, str]]:
        """
        Detecta volumes PRONTO disponíveis.
        Retorna lista de (nome, resumo).
        """
        chave = "volumes_" + str(raiz)

        # Verificar cache
        if self._esta_cache_valido(chave):
            return self.cache.get(chave, [])

        # Detectar volumes
        caminho_volumes = self._caminho_volumes(raiz)
        volumes_encontrados = []

        if caminho_volumes.exists():
            try:
                # Listar diretórios em volumes/prontos/
                for item in sorted(caminho_volumes.iterdir()):
                    if item.is_dir():
                        nome = item.name
                        # Validar que é um volume (tem README ou estrutura)
                        if self._validar_volume(item):
                            resumo = self._ler_resumo_volume(item)
                            if resumo:
                                volumes_encontrados.append((nome, resumo))
                            else:
                                # Fallback: usar nome como resumo
                                volumes_encontrados.append((nome, f"Volume {nome}"))
            except Exception:
                pass

        # Atualizar cache
        self.cache[chave] = volumes_encontrados
        self.ultima_atualizacao[chave] = datetime.now()

        return volumes_encontrados

    def _validar_volume(self, volume_path: Path) -> bool:
        """Valida que diretório é um volume legítimo."""
        # Um volume é legítimo se:
        # 1. Tem README.md ou
        # 2. Tem arquivos .md ou
        # 3. Tem subdiretorios com padrão XX-*.md (volumes)
        try:
            if (volume_path / "README.md").exists():
                return True

            # Verificar se tem arquivos markdown
            md_files = list(volume_path.glob("*.md"))
            if md_files:
                return True

            # Verificar se tem estrutura de capítulos (01-*.md, etc)
            capítulos = list(volume_path.glob("[0-9][0-9]-*.md"))
            if capítulos:
                return True

            return False
        except Exception:
            return False

    def invalidar_cache(self, raiz: Optional[Path] = None):
        """Invalida cache (quando há mudanças)."""
        if raiz is None:
            # Limpar cache global
            self.cache.clear()
            self.ultima_atualizacao.clear()
        else:
            # Limpar cache específico
            chave = "volumes_" + str(raiz)
            if chave in self.cache:
                del self.cache[chave]
            if chave in self.ultima_atualizacao:
                del self.ultima_atualizacao[chave]

    def obter_resumo(self, raiz: Path, volume_nome: str) -> Optional[str]:
        """Obtém resumo de um volume específico."""
        volume_path = self._caminho_volumes(raiz) / volume_nome
        if volume_path.exists():
            return self._ler_resumo_volume(volume_path)
        return None


def detectar_volumes_rapido(raiz: Path) -> List[tuple[str, str]]:
    """Helper rápido para detectar volumes."""
    detector = DetectorVolumesAoVivo()
    return detector.detectar_volumes(raiz)
