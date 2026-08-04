---
volume: "13"
volume_nome: RAG
tipo: ENGINE
secao: 09-Boas-Praticas
status: PRONTO
atualizado_em: 2026-08-04
---

# Boas Práticas

**Recuperar mais candidatos do que o necessário antes de reordenar**, nunca limitar a busca
inicial ao número final desejado. Reordenação por relevância específica só tem material para
trabalhar se a recuperação inicial trouxer variedade suficiente de candidatos.

**Tratar recusa explícita como resultado de sucesso do pipeline, não como falha a ser escondida
ou contornada.** Um sistema que nunca recusa provavelmente está gerando resposta sem fundamento
em algum subconjunto de perguntas — a ausência de recusa não é sinal de qualidade, pode ser sinal
de que a verificação de R4 não está sendo aplicada com rigor suficiente.

**Medir fidelidade em amostra representativa antes de confiar na métrica agregada.** Um número
médio de fidelidade alto pode esconder um subconjunto de perguntas com fidelidade sistematicamente
baixa — a distribuição importa tanto quanto a média.

**Revalidar documento no momento da citação final, não só no momento da recuperação inicial.**
Entre a recuperação e a composição da resposta, especialmente em pipelines com etapas assíncronas,
o estado de validade pode ter mudado.

**Registrar o score de relevância junto com a citação na resposta**, não só internamente. Isso
permite a quem consome a resposta avaliar a força relativa de cada fonte citada, não só a
presença da citação.
