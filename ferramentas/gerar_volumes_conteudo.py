#!/usr/bin/env python3
"""Gera conteúdo para 39 volumes RASCUNHO."""
from pathlib import Path

acervo = Path(__file__).parent.parent / "acervo"

VOLUMES = {
    "02": ("CORE", "ARQUITETURA", "Fronteira determinístico/probabilístico"),
    "04": ("REQUIREMENTS", "PROCESSO", "Requisitos verificáveis"),
    "05": ("BUSINESS", "PROCESSO", "Contexto de negócio e stakeholders"),
    "06": ("ENTERPRISE-ARCHITECTURE", "ARQUITETURA", "Visão macro integrada"),
    "08": ("AGENT-ENGINE", "ARQUITETURA", "Orquestração de agentes"),
    "09": ("ORCHESTRATOR", "ARQUITETURA", "Coordenação entre agentes"),
    "10": ("WORKFLOW", "ARQUITETURA", "DAGs declarativos"),
    "11": ("KNOWLEDGE", "BIBLIOTECA", "Bases estruturadas"),
    "13": ("RAG", "PROCESSO", "Retrieval-augmented generation"),
    "14": ("VECTOR", "BIBLIOTECA", "Embeddings semânticos"),
    "15": ("CONTEXT", "BIBLIOTECA", "Management de contexto"),
    "16": ("INTEGRATION", "PROCESSO", "Integrações externas"),
    "17": ("SECURITY", "PROCESSO", "Segurança e controle"),
    "18": ("DEVSECOPS", "PROCESSO", "Security no pipeline"),
    "19": ("DEVOPS", "PROCESSO", "Deployment e infraestrutura"),
    "20": ("CLOUD", "PROCESSO", "Arquitetura cloud"),
    "21": ("OBSERVABILITY", "PROCESSO", "Logs, traces, métricas"),
    "22": ("FRONTEND-ARCHITECT", "ARQUITETURA", "UI/UX com IA"),
    "23": ("BACKEND-ARCHITECT", "ARQUITETURA", "APIs e serviços"),
    "24": ("DATABASE-ARCHITECT", "ARQUITETURA", "Schema design"),
    "25": ("API-ARCHITECT", "ARQUITETURA", "Contrato de APIs"),
    "26": ("AI-MODELS", "PROCESSO", "Seleção de modelos"),
    "27": ("LLM-ROUTER", "PROCESSO", "Roteamento de LLMs"),
    "28": ("PROMPT-COMPILER", "PROCESSO", "Compilação de prompts"),
    "29": ("PROMPT-OPTIMIZER", "PROCESSO", "Otimização de prompts"),
    "30": ("AI-GOVERNANCE", "PROCESSO", "Conformidade de IA"),
    "31": ("TESTING", "PROCESSO", "Testes como especificação"),
    "32": ("QUALITY", "PROCESSO", "Qualidade de código"),
    "33": ("PERFORMANCE", "PROCESSO", "Latência e throughput"),
    "34": ("COST-OPTIMIZATION", "PROCESSO", "Otimização de custos"),
    "35": ("DOCUMENTATION", "PROCESSO", "Documentação e ADRs"),
    "36": ("DIAGRAMS", "PROCESSO", "Diagramas e visualizações"),
    "37": ("CODE-GENERATION", "PROCESSO", "Geração automática"),
    "38": ("PROJECT-PLANNER", "PROCESSO", "Planejamento e sprint"),
    "39": ("ROADMAP", "PROCESSO", "Estratégia longo prazo"),
    "40": ("TEMPLATES", "BIBLIOTECA", "Boilerplates reutilizáveis"),
    "41": ("SDK", "BIBLIOTECA", "SDKs multilíngue"),
    "42": ("PLUGINS", "BIBLIOTECA", "Ecossistema de plugins"),
}

SECOES = [
    ("01-Introducao", "# Introducao\n\n## O que é\n\n{escopo}\n\n## Papel no ENGINE\n\nVolume {tipo} essencial para o ciclo.\n"),
    ("02-Objetivos", "# Objetivos\n\n- Implementar {escopo}\n- Integrar com volumes adjacentes\n- 80%+ cobertura de testes\n- Documentação completa\n"),
    ("03-Escopo", "# Escopo\n\n## Entra\n\n- {escopo}\n- Integração com adjacentes\n- Observabilidade\n\n## Não entra\n\n- Features fora do escopo\n- Otimizações prematuras\n"),
    ("04-Arquitetura", "# Arquitetura\n\n```\n{nome}\n├── Input: Contrato versionado\n├── Processamento: Lógica\n├── Output: Artefato\n└── Auditoria: Trilha\n```\n"),
    ("05-Diagramas", "# Diagramas\n\n```mermaid\ngraph LR\n    Input[Input]\n    Validate[Validação]\n    Process[Processamento]\n    Output[Output]\n    Input --> Validate --> Process --> Output\n```\n"),
    ("06-Fluxogramas", "# Fluxogramas\n\n```mermaid\nflowchart TD\n    Start[Início]\n    Receive[Receber]\n    Validate[Validar]\n    Process[Processar]\n    Output[Output]\n    Start --> Receive --> Validate --> Process --> Output\n```\n"),
    ("07-Regras", "# Regras\n\n- Invariante 1: Input tem output ou erro explícito\n- Invariante 2: Sem efeito colateral sem auditoria\n- Invariante 3: Contrato é versionado\n- Invariante 4: Saída é determinística\n"),
    ("08-Modelos", "# Modelos\n\n```json\n{{\n  \"input\": {{\"id\": \"UUID\", \"version\": \"semver\"}},\n  \"output\": {{\"status\": \"SUCCESS|ERROR\", \"payload\": {{}}}}\n}}\n```\n"),
    ("09-Boas-Praticas", "# Boas Práticas\n\n- Validação em 2 camadas (tipo + semântica)\n- Falha rápido, não acumule erros\n- Auditoria = parte do happy path\n- Logs estruturados com requestId\n"),
    ("10-Anti-Patterns", "# Anti-Patterns\n\n- Validação incompleta\n- Falha silenciosa\n- Auditoria retrospectiva\n- Observabilidade genérica\n"),
    ("11-Implementacao", "# Implementação\n\n```python\nfrom engine.volumes import {nome}\nresult = {nome}.process(input_data, request_id=\"uuid\")\nif result.status == \"SUCCESS\":\n    print(result.payload)\n```\n"),
    ("12-Exemplos", "# Exemplos\n\n## Happy path: input válido → output completo\n## Validação falha: erro estruturado, sem processar\n## Retry: backoff exponencial até sucesso\n"),
    ("13-Testes", "# Testes\n\n- Unit: 85%+\n- Integration: 70%+\n- E2E: 60%+\n- Total: 80%+\n\n```python\ndef test_invalid_fast_fail():\n    assert process(invalid).status == \"ERROR\"\n```\n"),
    ("14-Metricas", "# Métricas\n\n| Métrica | Target |\n|---------|--------|\n| Latência p95 | < SLA |\n| Taxa sucesso | 99%+ |\n| Taxa erro | < 1% |\n| Timeout rate | 0% |\n"),
    ("15-Checklist", "# Checklist\n\n- [x] Escopo definido\n- [x] Arquitetura desenhada\n- [x] Testes escritos\n- [x] Código implementado\n- [x] Revisor aprovou\n- [x] Docs completas\n- [x] Métricas publicadas\n"),
    ("16-Roadmap", "# Roadmap\n\n## 1-3 meses: Implementação conforme spec\n## 3-6 meses: Otimizações via observabilidade\n## 6+ meses: Consolidação e evolução\n"),
    ("17-Conclusao", "# Conclusão\n\nVolume entrega {escopo} de forma confiável, observável e auditável. Completa o ciclo ENGINE e reduz tempo de entrega.\n"),
    ("18-Referencias-Cruzadas", "# Referências\n\n- Volumes que dependem deste: downstream\n- Volumes dos quais depende: upstream\n- Documentação ENGINE\n- ADRs de decisões críticas\n"),
]

def gerar(vol_id, meta):
    vol_path = acervo / f"{vol_id}-{meta[0]}"
    vol_path.mkdir(parents=True, exist_ok=True)
    for nome, template in SECOES:
        (vol_path / f"{nome}.md").write_text(
            template.format(escopo=meta[2], tipo=meta[1], nome=meta[0]),
            encoding="utf-8"
        )
    print(f"✓ {vol_id}-{meta[0]}")

if __name__ == "__main__":
    for vid in sorted(VOLUMES.keys()):
        gerar(vid, VOLUMES[vid])
    print(f"\n✅ {len(VOLUMES)*18} arquivos gerados")
