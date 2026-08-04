"""Catálogo de templates: variável declarada, versionado, validado, neutro de domínio.

As regras AB1-AB6 formalizadas: `Template.__post_init__` exige versão/escopo
(AB1/AB6), exige motivo de depreciação (AB5), e rejeita conteúdo de domínio
(AB4); `renderizar` exige variáveis obrigatórias (AB3);
`verificar_compatibilidade` detecta versão divergente (AB2).
"""

from __future__ import annotations

from dataclasses import dataclass, field

_PALAVRAS_DE_DOMINIO_PROIBIDAS = {"concilia", "controladoria", "omie", "sicoob"}


class TemplateIncompleto(Exception):
    """AB1/AB6: template sem versão ou escopo declarado."""


class DepreciacaoSemMotivo(Exception):
    """AB5: template marcado como depreciado sem motivo declarado."""


class ConteudoDeDominioDetectado(Exception):
    """AB4: corpo do template contém termo específico de domínio proibido."""


class VariavelAusente(Exception):
    """AB3: renderização sem todas as variáveis obrigatórias fornecidas."""


class VersaoDeTemplateIncompativel(Exception):
    """AB2: conteúdo gerado por versão de template diferente da atual."""


@dataclass(frozen=True)
class Template:
    nome: str
    versao: str
    corpo: str
    variaveis_obrigatorias: frozenset
    escopo_declarado: str
    depreciado: bool = False
    motivo_de_depreciacao: str | None = None

    def __post_init__(self) -> None:
        if not self.versao or not self.escopo_declarado:
            raise TemplateIncompleto(f"template '{self.nome}' sem versao ou escopo (AB1/AB6)")
        if self.depreciado and not self.motivo_de_depreciacao:
            raise DepreciacaoSemMotivo(f"template '{self.nome}' depreciado sem motivo (AB5)")
        corpo_lower = self.corpo.lower()
        for palavra in _PALAVRAS_DE_DOMINIO_PROIBIDAS:
            if palavra in corpo_lower:
                raise ConteudoDeDominioDetectado(
                    f"template '{self.nome}' contem conteudo de dominio: '{palavra}' (AB4)"
                )


def renderizar(template: Template, valores: dict) -> str:
    ausentes = template.variaveis_obrigatorias - set(valores.keys())
    if ausentes:
        raise VariavelAusente(
            f"template '{template.nome}' sem variaveis: {sorted(ausentes)} (AB3)"
        )
    return template.corpo.format(**valores)


@dataclass(frozen=True)
class ConteudoGeradoDeTemplate:
    template_nome: str
    template_versao: str
    conteudo: str


def verificar_compatibilidade(conteudo: ConteudoGeradoDeTemplate, template_atual: Template) -> None:
    if conteudo.template_versao != template_atual.versao:
        raise VersaoDeTemplateIncompativel(
            f"conteudo gerado com versao {conteudo.template_versao}, "
            f"template atual e {template_atual.versao} (AB2)"
        )
