# Convenções — o contrato do acervo-controladoria

Este acervo é irmão de `acervo/` (a plataforma AI-ENGINEERING-OS, subtree público), não filho
dele. Os dois usam a mesma máquina — `ferramentas/contrato.py`, `ferramentas/validar.py`, o
mesmo parser de front-matter — apontada para raízes diferentes via `--raiz`, mas os `_VOLUME.yml`
e o `contrato.json` são independentes. Motivo da separação: `acervo/` trava por teste
(`test_os_42_volumes_estao_declarados`) em exatamente os ids `01`–`42`, e é sincronizado por
`git subtree` com um repositório público que não fala de contabilidade. Estender aquele contrato
para 54 divergiria do upstream a cada `git subtree pull`. Registrar Controladoria aqui, com
contrato próprio, evita as duas coisas.

As regras abaixo são as mesmas do `acervo/` — front-matter de seis campos, 18 seções por tipo,
substância mínima, marcadores proibidos, diagrama Mermaid com descrição, exemplo citado com
teste, link relativo resolvível — porque não há razão para inventar uma segunda gramática só
porque o assunto mudou. O que muda é o conteúdo dos `volumes` e a numeração: aqui os ids vão de
`43` a `54`, contínuos com onde `acervo/` para.

## Tipos usados nestes 12 volumes

| Tipo | Volumes | Por quê |
|---|---|---|
| `ENGINE` | 43, 45, 48, 52 | Têm estado, regras de transição e código executável citável (GL como motor de partidas dobradas, conciliação como motor de casamento, custeio ABC como motor de alocação, consolidação como motor de eliminação) |
| `PROCESSO` | 44, 46, 47, 49, 51 | O fluxo de cálculo/apresentação importa mais que um modelo de dados rígido |
| `GOVERNANCA` | 50, 53 | Política e controle regulatório; exigem matriz de controles em `07-Regras` |
| `ARQUITETURA` | 54 | Camada de integração externa, sem ciclo de vida próprio |

## Definição de PRONTO

Idêntica à do `acervo/`, por design — não existe motivo para um selo de qualidade mais frouxo
só porque o assunto é contabilidade e não IA:

1. `python -m ferramentas.validar 45 --raiz ../acervo-controladoria` (executado de dentro de
   `acervo/`, que é onde o pacote `ferramentas` mora) retorna exit 0.
2. `python -m pytest exemplos/45-conciliacao-contas -q` (executado de dentro de
   `acervo-controladoria/`) passa.
3. Auditoria por outro modelo com média maior ou igual a 8,0, nenhuma seção abaixo de 6,
   registrada em `auditorias/`.
4. Resultado registrado em `CHANGELOG.md` com a data do dia.

Um volume com os gates 1 e 2 verdes e sem o critério 3 permanece `RASCUNHO` no front-matter —
gate mecânico verde não é auditoria de qualidade, é só a ausência de defeito estrutural. Gravar
`PRONTO` com o critério 3 pendente mentiria sobre o estado do acervo, que é exatamente o defeito
que motivou construir esta máquina em vez de gerar prosa solta.

## O que ainda não passou pela máquina

Os 11 volumes além do 45 (43, 44, 46 a 54) têm `_VOLUME.yml` registrado e conteúdo herdado de
uma geração em lote anterior, que não cumpre o mínimo de substância nem o front-matter de seis
campos — rodar `python -m ferramentas.validar --tudo --raiz ../acervo-controladoria` contra eles
hoje reporta violação real, e é isso mesmo: eles ainda não foram reescritos. A reescrita segue o
mesmo processo do 45, um volume por vez, priorizando os que têm material de produção para
espelhar antes dos que exigem autoria do zero.
