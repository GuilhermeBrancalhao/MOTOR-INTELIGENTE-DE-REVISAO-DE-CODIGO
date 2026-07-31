---
volume: "31"
volume_nome: TESTING
tipo: PROCESSO
secao: 10-Anti-Patterns
status: PRONTO
atualizado_em: 2026-07-30
---

# Anti-Patterns

1. **Depender de `time.sleep()` ou de relógio real sem controle.** Um teste que dorme
   um segundo para simular passagem de tempo custa um segundo real a cada execução, e
   fica sujeito a atraso de máquina sob carga -- a asserção que dependia de um tempo
   mínimo passa a falhar de forma intermitente, sem que o comportamento tenha mudado.
2. **Testar só o caminho "normal" de uma fórmula de checksum.** Um validador de CPF
   testado apenas com números plausíveis passaria mesmo removendo a checagem de dígitos
   repetidos -- o defeito só aparece em produção, quando um número que a fórmula
   "confirma" por coincidência aritmética é aceito como válido.
3. **Mock universal: framework de duplo para toda dependência, mesmo interface
   trivial.** Configurar expectativa de chamada para um método de uma linha gasta mais
   código de configuração do que a implementação de um fake economizaria em execução, e
   ainda acopla o teste à sintaxe do framework em vez de ao comportamento do
   colaborador.
4. **Verificar interação quando só o estado devolvido importa.** Assertar que um método
   interno foi chamado exatamente uma vez, quando o teste já teria a resposta certa
   pelo valor de retorno, prende o teste a um detalhe de implementação -- uma
   refatoração que não muda nenhum comportamento observável passa a quebrar o teste.
5. **Nomear teste por número de caso (`test_caso_1`, `test_caso_2`).** Quando esse teste
   falha, o nome não diz qual regra quebrou -- quem lê o relatório de CI precisa abrir o
   corpo do teste antes de saber se o problema é grave ou cosmético.
6. **Copiar e colar o mesmo teste trocando só o valor de entrada.** Quatro cópias do
   mesmo teste, uma por CPF sintético, escondem que é a mesma regra sendo verificada
   quatro vezes -- e uma correção na regra que esqueça de atualizar uma das quatro
   cópias produz um teste desatualizado que ninguém nota estar testando a versão
   antiga.
7. **Testar só o caminho feliz da validação de parâmetro.** Verificar que um custo
   positivo funciona, sem verificar que custo zero ou negativo levanta, deixa sem
   cobertura exatamente o caso em que um parâmetro de chamador externo chega errado.
8. **O teste "pia de cozinha": muitas asserções não relacionadas no mesmo corpo.**
   Quando esse teste falha, o relatório não diz qual das cinco asserções foi a causa --
   isolar exige rodar o teste em depurador, o que anula a vantagem de ter uma suíte
   automatizada em primeiro lugar.
9. **Deixar marcador de trabalho inacabado na prosa em vez de registrar a pendência
   onde ela tem lugar próprio.** Escrever `TODO` (entre acentos graves, para não
   disparar a própria regra `marcador-proibido` que esta frase descreve) direto na
   seção de implementação, em vez de em `16-Roadmap.md`, é a razão pela qual a
   plataforma reprova esse padrão de forma automática: pendência sem lugar fixo se perde
   na primeira leitura apressada.
