---
volume: "40"
volume_nome: TEMPLATES
tipo: BIBLIOTECA
secao: 12-Exemplos
status: PRONTO
atualizado_em: 2026-08-04
---

# Exemplos

## Caso 1 — template completo, aceito e renderizado com sucesso

Um `Template` com versão, escopo, e corpo neutro de domínio é aceito no catálogo. Renderizado com
todas as variáveis obrigatórias fornecidas, produz saída sem ressalva.

## Caso 2 — template com conteúdo de domínio é rejeitado

Um template cujo corpo menciona um termo do conjunto proibido (por exemplo, nome de sistema de
projeto irmão) é rejeitado antes de entrar no catálogo — nunca fica disponível para reutilização
acidental fora do contexto original.

## Caso 3 — renderização sem variável obrigatória é rejeitada

Uma tentativa de renderizar um template sem fornecer todas as variáveis declaradas como
obrigatórias falha explicitamente, nomeando exatamente quais variáveis estão faltando.

## Caso 4 — depreciação sem motivo é rejeitada

Uma tentativa de marcar um template como depreciado sem declarar o motivo é rejeitada — a
depreciação precisa vir acompanhada de explicação desde o momento em que é declarada.

## Caso 5 — verificação de compatibilidade detecta versão divergente

Um conteúdo gerado pela versão `1.0` de um template, comparado contra a versão atual `2.0`, é
sinalizado como incompatível — a mudança de versão nunca é presumida transparente.


Os cinco casos cobrem, juntos, as seis regras completas — o Caso 2 é o mais didático porque
mostra exatamente o tipo de vazamento que a verificação de domínio neutro deste acervo existe
para capturar, aplicado especificamente ao corpo de um template antes de ele se tornar
reutilizável por qualquer pessoa que consulte o catálogo.

Os demais casos cobrem as rejeições específicas de cada regra individual, complementando a cobertura conjunta que os testes da seção seguinte confirmam de forma exaustiva.