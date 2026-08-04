---
volume: "35"
volume_nome: DOCUMENTATION
tipo: GOVERNANCA
secao: 07-Regras
status: PRONTO
atualizado_em: 2026-08-04
---

# Regras

**W1 — Toda decisão arquitetural com consequência duradoura é registrada como ADR — contexto,
decisão e consequência explícitos.** *Consequência:* nenhuma decisão importante existe apenas
como julgamento implícito na memória de quem a tomou.

**W2 — ADR aceito é imutável; decisão que muda gera um novo ADR que substitui o anterior, nunca
uma edição que apaga o registro original.** *Consequência:* o contexto original permanece
disponível mesmo depois de a decisão mudar, permitindo entender por que a decisão anterior fazia
sentido no momento em que foi tomada.

**W3 — Documentação vive em controle de versão junto do código que descreve.**
*Consequência:* documentação nunca fica desconectada do histórico de mudança que altera o
comportamento que ela documenta.

**W4 — Vigência de documentação é verificada explicitamente; documento desatualizado nunca é
tratado como se ainda fosse verdadeiro.** *Consequência:* a lacuna entre o que o documento afirma
e o que o código realmente faz é detectável, não descoberta por acidente meses depois.

**W5 — Conteúdo gerado automaticamente de uma fonte de verdade única nunca é editado
manualmente.** *Consequência:* nenhuma edição é silenciosamente perdida na próxima geração — a
mudança sempre vai para a fonte de verdade correta.

**W6 — Documentação para usuário e documentação para mantenedor são mantidas estruturalmente
distintas, nunca misturadas no mesmo documento.** *Consequência:* cada documento serve seu
público específico sem comprometer clareza tentando servir os dois ao mesmo tempo.
