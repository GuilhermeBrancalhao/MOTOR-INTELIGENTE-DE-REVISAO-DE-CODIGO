---
volume: "20"
volume_nome: CLOUD
tipo: ARQUITETURA
secao: 11-Implementacao
status: PRONTO
atualizado_em: 2026-08-04
---

# Implementação

<!-- exemplo: exemplos/20-cloud/infraestrutura.py -->

`infraestrutura.py`, citado acima, formaliza N1-N6: `Recurso` recusa criação sem `dono` (N3);
`validar_config_sem_segredo` rejeita chaves que carregam segredo em texto plano antes de qualquer
recurso ser aceito (N5); `PlanoDeInfraestrutura.verificar_redundancia` reporta recursos sem
redundância para um alvo que a exige (N2); `PlanoDeInfraestrutura.aplicar_mudanca` recusa mudança
cujo ambiente não corresponde ao do recurso alvo (N4); `detectar_drift` compara declarado contra
real e retorna divergências explícitas, nunca um booleano (N6). N1 (declaração antes de
existência) é uma garantia estrutural do próprio modelo: não há caminho de código que crie um
recurso reconhecido pelo sistema fora de uma declaração validada.


`estado_real`, o parâmetro de `detectar_drift`, é intencionalmente um dicionário simples em vez
de um tipo próprio — o exemplo não assume nenhum formato específico de resposta de provedor de
nuvem, deixando essa tradução para a camada de integração real que consultaria a API do provedor
em questão. O modelo central permanece agnóstico a qualquer fornecedor específico.


A assinatura de `aplicar_mudanca` recebe o recurso já atualizado e o ambiente alvo separadamente,
em vez de inferir o ambiente a partir do recurso — essa separação explícita é o que torna possível
testar o caso de descompasso entre os dois sem precisar simular um cenário de erro de configuração
mais complexo do que o necessário para provar a regra.