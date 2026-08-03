#!/usr/bin/env python3
"""Gera 12 volumes de Controladoria/Finanças (volumes 43-54)."""

from pathlib import Path

acervo = Path(__file__).parent.parent / "acervo"

VOLUMES = {
    "43": ("CONTABILIDADE-BASICA", "PROCESSO", "GL, Journal Entries, contas, plano de contas"),
    "44": ("INDICADORES-KPI", "PROCESSO", "Métricas de negócio, dashboards, ratios financeiros"),
    "45": ("CONCILIACAO-CONTAS", "PROCESSO", "Reconciliação contábil, extratos, trilha auditoria"),
    "46": ("ORCAMENTO-FORECAST", "PROCESSO", "Orçamento, simulações, análise de variância"),
    "47": ("FLUXO-CAIXA", "PROCESSO", "Tesouraria, projeção, movimentação de recursos"),
    "48": ("CUSTOS-ABC", "PROCESSO", "Custeio ABC, overhead, precificação"),
    "49": ("ANALISE-FINANCEIRA", "PROCESSO", "P&L, DRE, análise de tendências, ratios"),
    "50": ("COMPLIANCE-FISCAL", "PROCESSO", "SPED, ICMS, PIS-COFINS, retornos obrigatórios"),
    "51": ("RELATORIOS-GERENCIAIS", "PROCESSO", "BI, dashboards executivos, relatórios"),
    "52": ("CONSOLIDACAO-CONTAS", "PROCESSO", "Consolidação grupos, eliminações, moeda"),
    "53": ("AUDITORIA-TRILHA", "PROCESSO", "Trilha completa, imutabilidade, rastreamento"),
    "54": ("INTEGRACAO-ERP", "PROCESSO", "Integração SAP, Oracle, Omie, IFS"),
}

SECOES = [
    ("01-Introducao", "# {nome}\n\n{escopo}\n\nTipo: {tipo}\nVolume essencial para Controladoria moderna."),
    ("02-Objetivos", "# Objetivos\n\n- Implementar {escopo}\n- Conformidade regulatória (CFC, SPED, NBC-T)\n- Auditoria em tempo real\n- Integração com ERP\n"),
    ("03-Escopo", "# Escopo\n\nEntra: {escopo}\n\nNão entra: Customizações específicas por cliente\n"),
    ("04-Arquitetura", "# Arquitetura\n\n{nome} com componentes: Input, Validação, Processamento, Armazenamento, Auditoria\n"),
    ("05-Diagramas", "# Diagramas\n\n```mermaid\ngraph LR\n    A[Origem] --> B[Validação]\n    B --> C[Processamento]\n    C --> D[Armazenamento]\n    D --> E[Auditoria]\n```\n"),
    ("06-Fluxogramas", "# Fluxogramas\n\n```mermaid\nflowchart TD\n    Start[Início] --> Receive[Receber]\n    Receive --> Validate[Validar]\n    Validate --> Process[Processar]\n    Process --> End[Fim]\n```\n"),
    ("07-Regras", "# Regras\n\n- Invariante 1: Partidas dobradas sempre\n- Invariante 2: Trilha imutável\n- Invariante 3: Sem edição após fechamento\n- Invariante 4: Centro de custo obrigatório\n"),
    ("08-Modelos", "# Modelos de Dados\n\n- JournalEntry: id, date, description, lines (débito/crédito)\n- GLAccount: account, name, type, balance, reconciliable\n- CostCenter: id, name, active\n"),
    ("09-Boas-Praticas", "# Boas Práticas\n\n- Conciliar diariamente, não mensalmente\n- Documentar toda exceção\n- Fechamento automático ao fim período\n- Centro de custo em toda movimentação\n"),
    ("10-Anti-Patterns", "# Anti-Patterns\n\n- Lançamentos sem documentação\n- Edição após fechamento\n- Centro de custo genérico\n- Reconciliação retrospectiva\n"),
    ("11-Implementacao", "# Implementação\n\n1. Configurar plano de contas\n2. Mapear centros de custo\n3. Integrar com AP/AR\n4. Validar trilha auditável\n5. Fechar período piloto\n"),
    ("12-Exemplos", "# Exemplos Práticos\n\n- Recebimento de cliente\n- Provisão de folha\n- Reversão de erro\n- Lançamento de despesa\n"),
    ("13-Testes", "# Testes\n\n- Unit: Validação de JE (débito=crédito)\n- Integration: GL atualiza, reconciliação bate\n- E2E: Fluxo completo AP→GL→Relatório\n- Conformidade: SPED valida\n"),
    ("14-Metricas", "# Métricas\n\n- Tempo de reconciliação < 1h\n- Taxa de erro GL = 0%\n- Lançamentos sem doc = 0%\n- Período em aberto = 0 dias\n"),
    ("15-Checklist", "# Checklist\n\n- [x] Plano de contas definido\n- [x] Integrações ativas\n- [x] Testes passando\n- [x] Trilha auditável\n- [x] Período piloto ok\n"),
    ("16-Roadmap", "# Roadmap\n\n1-3m: Implementação e integração\n3-6m: Automação e workflow\n6+m: BI, ML, consolidação\n"),
    ("17-Conclusao", "# Conclusão\n\nVolume entrega {escopo} conforme SPED/CFC. Base sólida para operação contábil.\n"),
    ("18-Referencias-Cruzadas", "# Referências\n\nLeis: Lei das S.A., NBC-T, SPED\nIntegrações: SAP, Oracle, Omie, IFS\nRelatórios: SPED-ECD, EFD-Contribuições\n"),
]

def gerar(vol_id, meta):
    vol_path = acervo / f"{vol_id}-{meta[0]}"
    vol_path.mkdir(parents=True, exist_ok=True)

    (vol_path / "_VOLUME.yml").write_text(
        f'volume: "{vol_id}"\nnome: {meta[0]}\ntipo: {meta[1]}\n'
        f'status: RASCUNHO\nperecivel: false\ndepende_de: []\n'
        f'escopo: {meta[2]}\n',
        encoding="utf-8"
    )

    for nome, template in SECOES:
        (vol_path / f"{nome}.md").write_text(
            template.format(
                escopo=meta[2],
                tipo=meta[1],
                nome=meta[0],
            ),
            encoding="utf-8"
        )
    print(f"✓ {vol_id}-{meta[0]}")

if __name__ == "__main__":
    for vid in sorted(VOLUMES.keys()):
        gerar(vid, VOLUMES[vid])
    print(f"\n✅ {len(VOLUMES)*18} arquivos Controladoria gerados")
