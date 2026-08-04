---
volume: "20"
volume_nome: CLOUD
tipo: ARQUITETURA
secao: 03-Escopo
status: PRONTO
atualizado_em: 2026-08-04
---

# Escopo

Este volume cobre a infraestrutura que hospeda o sistema em execução: como recursos são
declarados, como redundância é garantida contra um alvo de disponibilidade, como custo é
atribuído, e como divergência de estado é detectada.

**Fronteira com `19-DEVOPS`.** O caminho que uma mudança percorre do commit ao deploy — build,
teste, gate de segurança, rollout — é daquele volume. Este volume trata do que existe do outro
lado desse caminho: a infraestrutura que efetivamente recebe e executa o artefato implantado. Uma
pergunta sobre "como o deploy acontece" pertence ao 19; uma pergunta sobre "o que sustenta o
sistema depois de implantado" pertence a este volume.

**Fronteira com `06-ENTERPRISE-ARCHITECTURE`.** Concentração de fornecedor de infraestrutura
(por exemplo, dependência de um único provedor de nuvem sem alternativa viável) é uma decisão de
portfólio, tratada no 06 — este volume garante que o custo e a redundância de cada recurso
individual são visíveis, o que alimenta essa decisão, mas não a toma.

**Fronteira com `18-DEVSECOPS`.** Controle de acesso e gestão de segredo em infraestrutura tocam
o 17-SECURITY e o 18; este volume garante que segredo nunca é declarado diretamente na
configuração de infraestrutura como texto plano, mas a política de quem pode acessar o quê é
daqueles volumes.

Não cobre dimensionamento de capacidade específico por carga de trabalho, nem escolha de provedor
— este volume garante que, qualquer que seja o provedor escolhido, os mesmos princípios de
declaração, redundância, atribuição de custo e detecção de divergência se aplicam.
