---
volume: "17"
volume_nome: SECURITY
tipo: GOVERNANCA
secao: 07-Regras
status: PRONTO
atualizado_em: 2026-08-03
---

# Regras

## Invariantes

**O default para ação de risco não enumerável é inverso: comprovadamente inócuo executa,
qualquer outra coisa trava ou é rastreada.** Nunca o contrário — uma lista de proibições que
tenta enumerar todo comportamento perigoso perde contra adversário adaptativo, porque cada
lista fechada é uma lista de contornos já conhecidos, não de todos os contornos possíveis.

**Dado processado de origem não confiável nunca é concatenado à instrução do operador sem
distinção estrutural.** A distinção precisa sobreviver ao processamento pelo modelo — se o
modelo não consegue diferenciar "isto é instrução" de "isto é dado", a defesa não existe, mesmo
que a intenção de separação estivesse presente antes da chamada ao modelo.

**Toda chamada de ferramenta que envia dado para fora do sistema é auditada contra uma lista de
destinos autorizados**, nunca liberada por assumir que o conteúdo é inócuo. Ausência de destino
na lista autorizada é motivo de travamento, não de aviso ignorável.

**Execução de código ou comando gerado pelo modelo nunca é liberada sem verificação
estruturalmente comprovada.** Comando de shell, especificamente, nunca é classificado como
"livre" (execução sem verificação) — só operação de arquivo simples atinge esse nível, porque
comando de shell é uma linguagem com superfície de contorno grande demais para enumerar.

**Toda mudança na política de segurança é registrada com o vetor específico que a motivou.** Um
controle novo sem vetor documentado não pode ser avaliado quanto a se ainda é necessário quando o
sistema evoluir — o vetor é o que permite julgar, no futuro, se a condição que motivou o controle
ainda existe.

## Matriz de controles

| Controle | Risco mitigado | Como é verificado |
|---|---|---|
| Isolamento estrutural de dado processado e instrução do operador | Prompt injection através de documento, e-mail, resultado de busca ou saída de ferramenta anterior | Teste que injeta instrução dentro de dado processado e verifica que o sistema não executa a ação injetada sem confirmação explícita |
| Lista de destinos autorizados para toda chamada de ferramenta com efeito de saída de dado | Exfiltração de dado sensível via ferramenta legítima usada para fim não autorizado | Teste que tenta uma chamada de ferramenta com destino fora da lista autorizada e verifica travamento |
| Nenhuma categoria de comando de shell classificada como execução livre | Execução insegura de comando gerado por IA, incluindo contorno via aspas, substituição ou variante de plataforma | Teste (`test_nenhum_comando_de_shell_e_livre`, real neste próprio motor) que trava a política contra reintrodução acidental de exceção |
| Registro do vetor específico por família de controle de segurança | Controle mantido ou removido sem entender o risco original que o motivou | Revisão de `README.md`/changelog de segurança exigindo vetor nomeado por família (R1 a R12, no caso do motor ENGINE) |
