"""Modelo mínimo de disciplina de ecossistema de plugin.

Formaliza AD1-AD6 do volume 42-PLUGINS: contrato de extensão versionado,
isolamento de falha (exceção de plugin nunca propaga ao host), permissão
declarada explicitamente, registro explícito de ativação, desativação sem
efeito residual, e evolução do contrato seguindo a mesma disciplina de
versionamento semântico de 41-SDK.
"""

from dataclasses import dataclass, field


class ContratoIncompativel(Exception):
    """AD1 — plugin com contrato alvo incompatível ao contrato do host."""


class CapacidadeNaoDeclarada(Exception):
    """AD3 — plugin tenta acessar capacidade não declarada na ativação."""


class RegistroImplicito(Exception):
    """AD4 — declaração de plugin sem ponto de entrada explícito."""


class PluginNaoEncontrado(Exception):
    """Operação sobre plugin que não está ativo no host."""


class QuebraDeContratoSemMajorBump(Exception):
    """AD6 — mudança que quebra hook sem incrementar versão maior do contrato."""


@dataclass(frozen=True)
class VersaoDeContrato:
    major: int
    minor: int

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}"


@dataclass(frozen=True)
class ContratoDeExtensao:
    versao: VersaoDeContrato
    hooks: frozenset = frozenset()


@dataclass(frozen=True)
class DeclaracaoDePlugin:
    nome: str
    versao_do_contrato_alvo: VersaoDeContrato
    ponto_de_entrada: str = ""
    capacidades_solicitadas: frozenset = frozenset()

    def __post_init__(self) -> None:
        if not self.ponto_de_entrada:
            raise RegistroImplicito(
                f"plugin '{self.nome}' declarado sem ponto de entrada explicito (AD4)"
            )


def ativar_plugin(
    contrato_do_host: ContratoDeExtensao, declaracao: DeclaracaoDePlugin
) -> None:
    """AD1 — plugin com contrato alvo incompatível é rejeitado antes da ativação."""
    if declaracao.versao_do_contrato_alvo.major != contrato_do_host.versao.major:
        raise ContratoIncompativel(
            f"plugin '{declaracao.nome}' alvo contrato "
            f"{declaracao.versao_do_contrato_alvo} incompativel com contrato do "
            f"host {contrato_do_host.versao} (AD1)"
        )


def acessar_capacidade(declaracao: DeclaracaoDePlugin, capacidade: str) -> None:
    """AD3 — capacidade não declarada na ativação é negada."""
    if capacidade not in declaracao.capacidades_solicitadas:
        raise CapacidadeNaoDeclarada(
            f"plugin '{declaracao.nome}' tentou acessar capacidade '{capacidade}' "
            f"nao declarada na ativacao (AD3)"
        )


@dataclass(frozen=True)
class ResultadoDeHook:
    nome_plugin: str
    sucesso: bool
    valor: object = None
    erro: str = ""


def executar_hook_isolado(nome_plugin: str, hook, *args) -> ResultadoDeHook:
    """AD2 — exceção lançada dentro do hook do plugin nunca propaga ao host."""
    try:
        valor = hook(*args)
        return ResultadoDeHook(nome_plugin=nome_plugin, sucesso=True, valor=valor)
    except Exception as erro:
        return ResultadoDeHook(nome_plugin=nome_plugin, sucesso=False, erro=str(erro))


@dataclass
class EstadoDoHost:
    plugins_ativos: dict = field(default_factory=dict)
    recursos_por_plugin: dict = field(default_factory=dict)

    def ativar(self, declaracao: DeclaracaoDePlugin, recursos=None) -> None:
        self.plugins_ativos[declaracao.nome] = declaracao
        self.recursos_por_plugin[declaracao.nome] = list(recursos or [])

    def desativar(self, nome: str) -> None:
        """AD5 — desativação libera todo recurso associado, sem efeito residual."""
        if nome not in self.plugins_ativos:
            raise PluginNaoEncontrado(f"plugin '{nome}' nao esta ativo")
        del self.plugins_ativos[nome]
        del self.recursos_por_plugin[nome]


def evoluir_contrato(
    contrato_atual: ContratoDeExtensao,
    contrato_novo: ContratoDeExtensao,
    quebra_hook: bool,
) -> None:
    """AD6 — mudança que quebra hook exige versão maior nova do próprio contrato."""
    if quebra_hook and contrato_novo.versao.major == contrato_atual.versao.major:
        raise QuebraDeContratoSemMajorBump(
            f"mudanca de contrato quebra hook existente mas versao maior nao "
            f"mudou ({contrato_atual.versao} -> {contrato_novo.versao}) (AD6)"
        )
