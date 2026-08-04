---
volume: "24"
volume_nome: DATABASE-ARCHITECT
tipo: ARQUITETURA
secao: 17-Conclusao
status: PRONTO
atualizado_em: 2026-08-04
---

# Conclusão

Persistência para um sistema com componente de IA carrega uma exigência que persistência
tradicional às vezes trata como opcional: saber não apenas o que foi gravado, mas o que produziu
aquilo, e detectar quando duas escritas concorrentes disputam o mesmo registro sem deixar isso
silenciosamente resolvido pela ordem de chegada. As seis regras deste volume convergem para uma
ideia central: schema, proveniência e concorrência deveriam ser tratados com o mesmo rigor que se
espera de qualquer sistema de persistência crítico, mesmo — ou principalmente — quando parte do
conteúdo vem de um modelo cujo comportamento pode mudar entre uma versão e a próxima sem aviso.

A regra mais fácil de negligenciar quando o prazo aperta é A2 — proveniência. Parece dado
acessório até o momento em que dois resultados que deveriam ser idênticos divergem, e sem saber
qual modelo produziu cada um, a única explicação disponível é "bug", quando a explicação real
pode ser simplesmente que o modelo mudou.
