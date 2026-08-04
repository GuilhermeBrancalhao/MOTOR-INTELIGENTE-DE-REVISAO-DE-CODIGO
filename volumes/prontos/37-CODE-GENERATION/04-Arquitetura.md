---
volume: "37"
volume_nome: CODE-GENERATION
tipo: ENGINE
secao: 04-Arquitetura
status: PRONTO
atualizado_em: 2026-08-04
---

# Arquitetura

`EspecificacaoDeGeracao.__post_init__` recusa criação sem `prompt_ou_fonte`, `versao` ou
`escopo_declarado` preenchidos — a especificação que produz código gerado nunca existe sem
rastreabilidade e escopo declarados desde o início.

`aceitar_codigo_gerado` é o portão único que todo código gerado atravessa antes de ser
considerado pronto: recusa código não marcado como gerado (`marcado_como_gerado=False`), recusa
código sem resultado de validação, recusa código cuja validação falhou (não compilou ou não
passou teste), e recusa código sem revisão humana registrada — as quatro verificações precisam
passar juntas, nenhuma substitui as outras.

`editar_codigo_gerado` recusa qualquer tentativa de edição direta sobre código marcado como
gerado — a mudança precisa ir para a especificação, nunca para o arquivo de saída diretamente.

A função `gerar` é determinística por construção: recebe a especificação e uma função geradora
injetada, e o resultado depende exclusivamente desses dois insumos — sem estado externo
influenciando a saída, a mesma especificação com o mesmo gerador sempre produz o mesmo
`CodigoGerado`.


As quatro verificações de `aceitar_codigo_gerado` acontecem em sequência fixa e nenhuma é
opcional — código sem marcação nunca chega a ser avaliado quanto à validação, e código com
validação falha nunca chega a ser avaliado quanto à revisão humana, porque cada verificação
anterior já é suficiente para bloquear, tornando o restante do processo desnecessário até a
causa raiz ser corrigida.