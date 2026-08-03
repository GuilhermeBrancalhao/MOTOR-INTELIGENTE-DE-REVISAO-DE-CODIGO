---
volume: "17"
volume_nome: SECURITY
tipo: GOVERNANCA
secao: 09-Boas-Praticas
status: PRONTO
atualizado_em: 2026-08-03
---

# Boas Práticas

**Classificar por comprovação de inocuidade, revisando periodicamente o que foi classificado
como `Livre`.** Uma ação classificada como inócua hoje pode deixar de ser, se o sistema evoluir
(nova ferramenta, novo tipo de dado processado) — a classificação não é permanente por natureza,
precisa de revisão quando o contexto muda.

**Documentar o vetor concreto que motivou cada controle, não só a regra abstrata.** "Comando de
shell nunca é livre" é mais defensável e mais fácil de manter quando acompanhado dos doze
contornos reais que motivaram a inversão de default — sem o vetor, a regra parece arbitrária para
quem chega depois e pode ser relaxada por engano.

**Tratar toda auditoria adversarial que encontra novo contorno como sinal de família de controle
nova, não de patch pontual.** Corrigir só o contorno específico encontrado deixa a classe de
vulnerabilidade aberta para a próxima variação — generalizar o achado numa família (como R9 a
R12 do motor `ENGINE`) é o que fecha a classe, não a instância.

**Preferir travar sobre um comando acima de um teto de tamanho razoável, em vez de analisá-lo.**
Um comando de shell gigante analisado por padrão de regex é vetor de negação de serviço em si —
travar por tamanho excessivo, sem tentar entender o conteúdo, é o lado seguro do erro.

**Nunca deixar a própria infraestrutura de segurança fora do escopo de proteção.** Escrita no
diretório de configuração do sistema de controle de risco precisa ser travada com o mesmo rigor
que qualquer outra ação de alto risco — um sistema que protege tudo exceto seu próprio painel de
controle não se protege de fato.
