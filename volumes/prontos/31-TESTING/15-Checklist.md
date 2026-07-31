---
volume: "31"
volume_nome: TESTING
tipo: PROCESSO
secao: 15-Checklist
status: PRONTO
atualizado_em: 2026-07-30
---

# Checklist

Conferência antes de aprovar um pull request que adiciona ou altera teste. Cada item se
marca com evidência nomeada, não com impressão de quem revisa.

- [ ] Nenhum teste novo chama `time.sleep` nem lê relógio real sem injeção -- evidência:
  busca por `time.sleep`, `datetime.now` e `time.monotonic` fora de um parâmetro
  nomeado `agora` ou equivalente.
- [ ] O nome de cada função de teste descreve a regra travada, não o método chamado --
  evidência: ler o nome sem abrir o corpo e conseguir dizer o que quebraria se a
  asserção fosse removida.
- [ ] Todo parâmetro de validação de entrada tem caso de teste no caminho de erro, não
  só no caminho válido -- evidência: para cada `raise` no código de produção, existe
  pelo menos um `pytest.raises` correspondente.
- [ ] Dublê de teste escrito à mão para interface de um ou dois métodos; framework de
  mock reservado a interface grande ou instável -- evidência: contagem de linhas do
  dublê contra a configuração que um framework exigiria.
- [ ] Nenhuma função de teste mistura asserção de interação e asserção de estado
  redundantes entre si na mesma função -- evidência: para cada asserção, confirmar que
  ela prova um fato que nenhuma outra asserção da mesma função já provaria; uma função
  que só verifica interação (porque é o único jeito de observar o efeito, como
  `test_registrar_envia_mensagem_formatada_ao_destinatario`) não viola este item.
- [ ] Classe de equivalência coberta por `@pytest.mark.parametrize`, não por cópia do
  mesmo teste com valor diferente -- evidência: nenhuma função de teste repete o corpo
  de outra a menos de um literal.
- [ ] `python -m pytest exemplos/<vol> -q` passa localmente antes de abrir o pull
  request -- evidência: saída colada na descrição do PR, não a afirmação "deve passar".
- [ ] Nenhum marcador de pendência (`TODO`, `FIXME`, `PENDENTE`) fora de code span na
  prosa nem dentro do código de exemplo -- evidência: `python -m ferramentas.validar
  NN` limpo na regra `marcador-proibido`.
- [ ] Todo trecho de código citado pelo comentário de exemplo (a tag HTML que aponta
  para um arquivo em `exemplos/`) tem teste correspondente em `tests/test_<arquivo>.py`
  -- evidência: mesmo gate, regra `exemplo-sem-teste`.
