#!/usr/bin/env python3
"""FASE 5: Validador de plugin - verifica estrutura e metadados.

Valida:
1. plugin.json tem schema correto
2. Arquivos referenciados existem
3. Versionamento semântico
4. Documentação completa
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

if sys.platform == "win32":
    for _fluxo in (sys.stdout, sys.stderr):
        try:
            _fluxo.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass


class ValidadorPlugin:
    """Valida estrutura de plugin."""

    def __init__(self, repo_dir: Path):
        self.repo_dir = repo_dir
        self.plugin_dir = repo_dir / ".claude-plugin"
        self.plugin_json_path = self.plugin_dir / "plugin.json"
        self.erros = []
        self.avisos = []

    def validar_tudo(self) -> bool:
        """Executa todas validações."""
        print("\n" + "=" * 80)
        print("VALIDADOR DE PLUGIN - ENGINE")
        print("=" * 80)

        # 1. Arquivo plugin.json
        if not self._validar_plugin_json():
            return False

        # 2. Estrutura de diretórios
        self._validar_estrutura_diretorios()

        # 3. Versionamento
        self._validar_versionamento()

        # 4. Documentação
        self._validar_documentacao()

        # 5. Motores
        self._validar_motores()

        # 6. Volumes
        self._validar_volumes()

        # 7. Wiring real dos hooks (o que o Claude Code de fato lê)
        self._validar_hooks_json()

        # Reportar
        return self._relatar()

    def _validar_plugin_json(self) -> bool:
        """Valida plugin.json."""
        print("\n--- plugin.json ---")

        if not self.plugin_json_path.exists():
            self.erros.append("plugin.json não encontrado")
            print("❌ plugin.json não existe")
            return False

        try:
            with open(self.plugin_json_path) as f:
                plugin = json.load(f)
            print("✓ JSON válido")
        except json.JSONDecodeError as e:
            self.erros.append(f"JSON inválido: {e}")
            print(f"❌ Erro de JSON: {e}")
            return False

        # Campos obrigatórios
        required = ["name", "displayName", "version", "description"]
        for campo in required:
            if campo not in plugin:
                self.erros.append(f"Campo obrigatório faltando: {campo}")
                print(f"❌ Falta: {campo}")
            else:
                print(f"✓ {campo}: {plugin[campo]}")

        # Validar versionamento
        if "version" in plugin:
            if not self._eh_semver(plugin["version"]):
                self.avisos.append(
                    f"Versão {plugin['version']} não segue semver"
                )
                print(f"⚠️  Versão não é semver: {plugin['version']}")

        return len(self.erros) == 0

    def _eh_semver(self, version: str) -> bool:
        """Valida se versão é semver (X.Y.Z)."""
        parts = version.split(".")
        if len(parts) != 3:
            return False
        try:
            return all(p.isdigit() for p in parts)
        except Exception:
            return False

    def _validar_estrutura_diretorios(self):
        """Valida estrutura de diretórios."""
        print("\n--- Estrutura de Diretórios ---")

        dirs_obrigatorios = [
            "hooks",
            "motores",
            "volumes/prontos",
            ".claude-plugin",
        ]

        for dir_name in dirs_obrigatorios:
            dir_path = self.repo_dir / dir_name
            if dir_path.exists():
                print(f"✓ {dir_name}/")
            else:
                self.erros.append(f"Diretório faltando: {dir_name}")
                print(f"❌ Falta: {dir_name}/")

    def _validar_versionamento(self):
        """Valida versionamento semântico."""
        print("\n--- Versionamento ---")

        # Ler version de plugin.json
        try:
            with open(self.plugin_json_path) as f:
                plugin = json.load(f)
            version = plugin.get("version", "0.0.0")
            print(f"✓ Versão: {version}")

            if not self._eh_semver(version):
                self.avisos.append(f"Versão inválida: {version}")
                print(f"⚠️  Semver inválido: {version}")
            else:
                print(f"✓ Semver válido")
        except Exception as e:
            self.erros.append(f"Erro lendo versão: {e}")

    def _validar_documentacao(self):
        """Valida documentação."""
        print("\n--- Documentação ---")

        docs_obrigatorios = [
            ("PLUGIN-README.md", "README do plugin"),
            ("CHANGELOG.md", "Histórico de mudanças"),
        ]

        for arquivo, desc in docs_obrigatorios:
            path = self.repo_dir / arquivo
            if path.exists():
                tamanho = path.stat().st_size
                print(f"✓ {arquivo} ({tamanho} bytes) - {desc}")
            else:
                self.avisos.append(f"Documentação faltando: {arquivo}")
                print(f"⚠️  Falta: {arquivo}")

    def _validar_motores(self):
        """Valida motores."""
        print("\n--- Motores (Skills) ---")

        motores_esperados = [
            "revisar-codigo",
            "otimizar-performance",
            "arquitetar-sistema",
            "materializar-ideia",
            "diagramar",
        ]

        for motor in motores_esperados:
            path = self.repo_dir / "motores" / motor
            if path.exists() and (path / "SKILL.md").exists():
                print(f"✓ {motor}/")
            else:
                self.erros.append(f"Motor incompleto: {motor}")
                print(f"❌ Falta: {motor}/SKILL.md")

    def _validar_volumes(self):
        """Valida volumes.

        A convenção real é `_VOLUME.yml` com `status: PRONTO` (lida também por
        `ferramentas/validar.py`/`status.py`) — os volumes deste repositório usam
        capítulos numerados (`01-*.md` etc.), não `README.md`. Checar README.md
        aqui reprovava os 3 volumes reais mesmo com o plugin correto.
        """
        print("\n--- Volumes Consultáveis ---")

        volumes_base = [
            "07-PROMPT-ENGINE",
            "12-MEMORY",
            "31-TESTING",
        ]

        found = 0
        for vol in volumes_base:
            path = self.repo_dir / "volumes" / "prontos" / vol
            status = self._ler_status_volume(path)
            if path.exists() and status == "PRONTO":
                print(f"✓ {vol}/ (status: PRONTO)")
                found += 1
            elif path.exists() and status is not None:
                self.avisos.append(f"Volume {vol} existe mas status é '{status}', não PRONTO")
                print(f"⚠️  {vol}/ status é '{status}', não PRONTO")
            else:
                self.avisos.append(f"Volume faltando ou sem _VOLUME.yml: {vol}")
                print(f"⚠️  Falta: {vol}/_VOLUME.yml")

        print(f"\n  Total: {found}/3 volumes base encontrados")

    def _ler_status_volume(self, volume_path: Path) -> str | None:
        """Lê o campo `status` de `_VOLUME.yml` (parser mínimo, sem depender de PyYAML)."""
        caminho = volume_path / "_VOLUME.yml"
        if not caminho.exists():
            return None
        try:
            for linha in caminho.read_text(encoding="utf-8").split("\n"):
                linha = linha.strip()
                if linha.startswith("status:"):
                    return linha.split(":", 1)[1].strip().strip('"').strip("'")
        except Exception:
            pass
        return None

    def _validar_hooks_json(self):
        """Valida `hooks/hooks.json` — a única fonte que o Claude Code lê para
        decidir quais scripts rodam em cada evento (`plugin.json` não declara hooks;
        um bloco assim é ignorado pelo Claude Code, então validá-lo aqui não prova
        nada sobre o que roda de verdade)."""
        print("\n--- hooks/hooks.json (wiring real) ---")

        caminho = self.repo_dir / "hooks" / "hooks.json"
        if not caminho.exists():
            self.erros.append("hooks/hooks.json não encontrado")
            print("❌ hooks/hooks.json não existe")
            return

        try:
            with open(caminho, encoding="utf-8") as f:
                config_hooks = json.load(f)
        except json.JSONDecodeError as e:
            self.erros.append(f"hooks.json inválido: {e}")
            print(f"❌ Erro de JSON: {e}")
            return

        eventos = config_hooks.get("hooks", {})
        if not eventos:
            self.avisos.append("hooks.json não declara nenhum evento")
            print("⚠️  Nenhum evento declarado")
            return

        for evento, entradas in eventos.items():
            for entrada in entradas:
                for hook in entrada.get("hooks", []):
                    args = hook.get("args", [])
                    for arg in args:
                        if not arg.endswith(".py"):
                            continue
                        # ${CLAUDE_PLUGIN_ROOT} é expandido pelo Claude Code em tempo
                        # de execução — aqui o plugin é a própria raiz do repo.
                        relativo = arg.replace("${CLAUDE_PLUGIN_ROOT}/", "")
                        script = self.repo_dir / relativo
                        if script.exists():
                            print(f"✓ {evento} → {relativo}")
                        else:
                            self.erros.append(
                                f"hooks.json declara {evento} → {relativo}, mas o arquivo não existe"
                            )
                            print(f"❌ {evento} → {relativo} (arquivo não existe)")

    def _relatar(self) -> bool:
        """Relata resultados."""
        print("\n" + "=" * 80)
        print("RESULTADO DA VALIDAÇÃO")
        print("=" * 80)

        if self.erros:
            print(f"\n❌ {len(self.erros)} ERRO(S):")
            for erro in self.erros:
                print(f"  - {erro}")

        if self.avisos:
            print(f"\n⚠️  {len(self.avisos)} AVISO(S):")
            for aviso in self.avisos:
                print(f"  - {aviso}")

        if not self.erros:
            print("\n✅ PLUGIN VÁLIDO - PRONTO PARA PUBLICAÇÃO")
            return True
        else:
            print("\n❌ PLUGIN COM ERROS - CORRIJA ANTES DE PUBLICAR")
            return False


if __name__ == "__main__":
    repo_dir = Path(__file__).resolve().parent
    validador = ValidadorPlugin(repo_dir)

    if validador.validar_tudo():
        sys.exit(0)
    else:
        sys.exit(1)
