#!/usr/bin/env python3
"""Testes unitários para volume_detector.py."""
import sys
import tempfile
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "hooks"))

from volume_detector import DetectorVolumesAoVivo


def criar_volume_teste(raiz: Path, nome: str, com_readme: bool = True):
    """Cria um volume fake para teste."""
    vol_dir = raiz / "volumes" / "prontos" / nome
    vol_dir.mkdir(parents=True, exist_ok=True)

    if com_readme:
        readme = vol_dir / "README.md"
        readme.write_text(f"# {nome}\n\nDescrição do volume {nome}")
    else:
        # Criar arquivo markdown alternativo
        cap = vol_dir / "01-introducao.md"
        cap.write_text(f"# Introdução\n\nCapítulo do {nome}")

    return vol_dir


def test_detectar_volume_unico():
    """Detecta um volume único com README."""
    with tempfile.TemporaryDirectory() as tmpdir:
        raiz = Path(tmpdir)
        criar_volume_teste(raiz, "10-VOLUME-A", com_readme=True)

        detector = DetectorVolumesAoVivo()
        volumes = detector.detectar_volumes(raiz)

        assert len(volumes) == 1
        assert volumes[0][0] == "10-VOLUME-A"
        assert "VOLUME-A" in volumes[0][1]
        print("✅ test_detectar_volume_unico PASSOU")


def test_detectar_multiplos_volumes():
    """Detecta múltiplos volumes."""
    with tempfile.TemporaryDirectory() as tmpdir:
        raiz = Path(tmpdir)
        criar_volume_teste(raiz, "07-PROMPT-ENGINE")
        criar_volume_teste(raiz, "12-MEMORY")
        criar_volume_teste(raiz, "31-TESTING")

        detector = DetectorVolumesAoVivo()
        volumes = detector.detectar_volumes(raiz)

        assert len(volumes) == 3
        nomes = [v[0] for v in volumes]
        assert "07-PROMPT-ENGINE" in nomes
        assert "12-MEMORY" in nomes
        assert "31-TESTING" in nomes
        print("✅ test_detectar_multiplos_volumes PASSOU")


def test_detectar_volume_sem_readme():
    """Detecta volume sem README mas com capítulos."""
    with tempfile.TemporaryDirectory() as tmpdir:
        raiz = Path(tmpdir)
        criar_volume_teste(raiz, "50-VOLUME-B", com_readme=False)

        detector = DetectorVolumesAoVivo()
        volumes = detector.detectar_volumes(raiz)

        assert len(volumes) == 1
        assert volumes[0][0] == "50-VOLUME-B"
        print("✅ test_detectar_volume_sem_readme PASSOU")


def test_cache_funciona():
    """Valida que cache funciona."""
    with tempfile.TemporaryDirectory() as tmpdir:
        raiz = Path(tmpdir)
        criar_volume_teste(raiz, "15-VOL-CACHE")

        detector = DetectorVolumesAoVivo(cache_ttl_segundos=3600)

        # Primeira chamada
        vols1 = detector.detectar_volumes(raiz)
        assert len(vols1) == 1

        # Segunda chamada (deve vir do cache)
        vols2 = detector.detectar_volumes(raiz)
        assert vols1 == vols2
        assert "volumes_" + str(raiz) in detector.cache
        print("✅ test_cache_funciona PASSOU")


def test_invalidar_cache():
    """Valida invalidação de cache."""
    with tempfile.TemporaryDirectory() as tmpdir:
        raiz = Path(tmpdir)
        criar_volume_teste(raiz, "20-VOL-INV")

        detector = DetectorVolumesAoVivo(cache_ttl_segundos=3600)

        # Preencher cache
        vols1 = detector.detectar_volumes(raiz)
        assert len(detector.cache) > 0

        # Invalidar
        detector.invalidar_cache(raiz)
        assert len(detector.cache) == 0
        print("✅ test_invalidar_cache PASSOU")


def test_nao_detecta_diretorio_vazio():
    """Não detecta diretório sem arquivo válido."""
    with tempfile.TemporaryDirectory() as tmpdir:
        raiz = Path(tmpdir)
        # Criar diretório vazio
        (raiz / "volumes" / "prontos" / "vazio").mkdir(parents=True)

        detector = DetectorVolumesAoVivo()
        volumes = detector.detectar_volumes(raiz)

        assert len(volumes) == 0
        print("✅ test_nao_detecta_diretorio_vazio PASSOU")


def test_ordem_alfabetica():
    """Detecta volumes em ordem alfabética."""
    with tempfile.TemporaryDirectory() as tmpdir:
        raiz = Path(tmpdir)
        # Criar em ordem invertida
        criar_volume_teste(raiz, "Z-VOLUME")
        criar_volume_teste(raiz, "A-VOLUME")
        criar_volume_teste(raiz, "M-VOLUME")

        detector = DetectorVolumesAoVivo()
        volumes = detector.detectar_volumes(raiz)

        nomes = [v[0] for v in volumes]
        assert nomes == sorted(nomes), f"Esperado {sorted(nomes)}, obteve {nomes}"
        print("✅ test_ordem_alfabetica PASSOU")


def test_resumo_truncado():
    """Valida que resumo é truncado a 100 chars."""
    with tempfile.TemporaryDirectory() as tmpdir:
        raiz = Path(tmpdir)
        vol_dir = raiz / "volumes" / "prontos" / "LONG-VOL"
        vol_dir.mkdir(parents=True)

        # Criar README com descrição muito longa
        readme = vol_dir / "README.md"
        long_text = "x" * 200
        readme.write_text(f"# LONG-VOL\n\n{long_text}")

        detector = DetectorVolumesAoVivo()
        volumes = detector.detectar_volumes(raiz)

        assert len(volumes) == 1
        resumo = volumes[0][1]
        assert len(resumo) <= 100, f"Resumo tem {len(resumo)} chars, máx 100"
        print("✅ test_resumo_truncado PASSOU")


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("TESTES UNITÁRIOS: Volume Detector")
    print("=" * 80)

    test_detectar_volume_unico()
    test_detectar_multiplos_volumes()
    test_detectar_volume_sem_readme()
    test_cache_funciona()
    test_invalidar_cache()
    test_nao_detecta_diretorio_vazio()
    test_ordem_alfabetica()
    test_resumo_truncado()

    print("\n" + "=" * 80)
    print("✅ TODOS OS TESTES PASSARAM")
    print("=" * 80)
