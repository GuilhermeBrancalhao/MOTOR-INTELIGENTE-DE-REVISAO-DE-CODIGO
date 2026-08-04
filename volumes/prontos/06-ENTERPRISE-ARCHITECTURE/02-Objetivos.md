---
volume: "06"
volume_nome: ENTERPRISE-ARCHITECTURE
tipo: ARQUITETURA
secao: 02-Objetivos
status: PRONTO
atualizado_em: 2026-08-04
---

# Objetivos

Depois de ler este volume, o leitor consegue:

**Registrar um sistema no inventário de portfólio** com a dependência explícita (modelo, provedor,
fonte de dado) que ele introduz — não como documentação burocrática, mas como o dado que permite
enxergar duplicação e concentração de risco entre projetos.

**Distinguir decisão de projeto de decisão de portfólio.** A regra prática: se a decisão só afeta
o sistema em questão, é de projeto; se cria consequência que outro projeto herda sem ter
escolhido (contrato de fornecedor, política de dado), é de portfólio.

**Calcular custo total de propriedade agregado**, não por projeto isolado — o mesmo fornecedor
usado por dez projetos pequenos pode custar, somado, mais que um único projeto grande com
fornecedor dedicado, e nenhum dos dez projetos vê isso sozinho.

**Identificar capacidade duplicada entre projetos** — dois times construindo o mesmo tipo de
pipeline de recuperação de conhecimento de forma independente é achado de portfólio, não de
projeto, porque nenhum dos dois projetos tem visibilidade do outro.

**Traçar a fronteira com `02-CORE`**: aquele volume decide onde fica a fronteira
determinístico/probabilístico *dentro* de um sistema; este volume decide onde o sistema inteiro
se encaixa *dentro* da empresa. As duas fronteiras são independentes — um sistema pode ter a
fronteira interna impecável e ainda assim ser uma péssima decisão de portfólio.
