---
volume: "36"
volume_nome: DIAGRAMS
tipo: BIBLIOTECA
secao: 11-Implementacao
status: PRONTO
atualizado_em: 2026-08-04
---

# Implementação

<!-- exemplo: exemplos/36-diagrams/catalogo_de_diagramas.py -->

`catalogo_de_diagramas.py`, citado acima, formaliza X1-X6: `TipoDeDiagrama.__post_init__` recusa
`nome` fora do conjunto de tipos reconhecidos (X3) e recusa `proposito`/`quando_usar` vazios (X1);
`Catalogo.registrar` recusa `EntradaDeCatalogo` sem `prosa_explicativa` (X2) ou sem
`fora_de_escopo` (X6); `escolher_tipo_por_necessidade` mapeia necessidade declarada para tipo,
nunca o inverso (X5); `verificar_vigencia_do_diagrama` levanta exceção nomeada quando o diagrama
não reflete mais o sistema real (X4).

`_TIPOS_RECONHECIDOS` e `_MAPA_NECESSIDADE_PARA_TIPO` são as duas únicas fontes de verdade sobre
o vocabulário fechado de quatro tipos — qualquer extensão futura do catálogo, se genuinamente
necessária, precisaria atualizar as duas estruturas de forma consistente, nunca uma sem a outra,
para que a rejeição de tipo não catalogado (X3) e o mapeamento de necessidade (X5) continuem
sincronizados entre si.

Manter as duas estruturas como constantes de módulo, em vez de espalhadas por múltiplas funções, facilita revisar o vocabulário completo do catálogo num único lugar do código.

Isso reduz a chance de uma mudança futura no vocabulário esquecer de atualizar uma das duas
estruturas, um erro que só apareceria em tempo de execução sob condição específica, tarde demais
para ser pego numa simples revisão de código superficial antes do problema afetar produção, ou
pior, antes de afetar diretamente a confiança de quem consulta o catálogo publicado.