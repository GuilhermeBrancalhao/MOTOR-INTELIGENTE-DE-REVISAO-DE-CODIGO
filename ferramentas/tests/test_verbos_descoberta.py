"""Os verbos que dão SAÍDA ao portão da descoberta, pela CLI de verdade.

O gate de `DESCOBERTA -> ANALISE` já existia e já recusava a transição imprimindo as
perguntas. O que não existia era um verbo para respondê-las: `descoberta.registrar` e
`descoberta.responder` eram API Python, e a skill não chama Python solto. Portão sem
saída — e portão sem saída não é portão, é parede.

Cada teste nomeia, na docstring, a mutação que o derrubaria. Cinco coisas são cobradas:

1. `descoberta <pedido>` registra e classifica;
2. `descoberta status` mostra intenção, bloqueantes (com a **pergunta inteira**) e
   assumíveis;
3. `descoberta responder <ID> <resposta>` fecha uma lacuna;
4. intenção indeterminada **pergunta** em vez de escolher;
5. o ciclo completo — registrar, responder todas, `fase ANALISE` sai **0**.

Tudo por subprocesso, como a skill usa: é o único jeito de medir código de saída de
verdade, e código de saída é o que a skill lê para saber se o passo deu certo.
"""
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

RAIZ_PLUGIN = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ_PLUGIN))

from ferramentas import descoberta, estado  # noqa: E402

#: Pedido com sinal de intenção inequívoco ("sistema novo" é termo de confiança ALTA de
#: MATERIALIZAR). Ele existe para que os testes que **não** são sobre classificação não
#: dependam do classificador: quem quer exercitar a indeterminação usa os pedidos ambíguos
#: mais abaixo, de propósito.
PEDIDO = "construir um sistema novo que soma dois numeros"

#: Teto do laço de respostas. Responder pode ativar outras lacunas (é B1 trabalhando),
#: então o número de voltas não é fixo — mas laço de teste sem teto vira suíte pendurada.
LIMITE_DE_VOLTAS = 40


def _cli(raiz: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(RAIZ_PLUGIN / "ferramentas" / "cli.py"), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        cwd=str(raiz),
        env={**os.environ, "ENGINE_RAIZ": str(raiz)},
    )


def _ligar(raiz: Path) -> None:
    assert _cli(raiz, "ligar", "somar dois numeros").returncode == 0


def _impressao_digital(raiz: Path) -> str:
    """SHA-256 dos BYTES do estado — reordenação de chave e carimbo novo também contam."""
    return hashlib.sha256(estado.caminho(raiz).read_bytes()).hexdigest()


def _ids_bloqueantes(saida: str) -> list[str]:
    """Os ids listados na seção BLOQUEANTES da saída, e só dela.

    Lê o que o usuário lê, em vez de consultar o estado: um `status` que imprimisse a
    seção errada (ou trocasse bloqueante por assumível no texto) passaria despercebido se
    o teste fosse buscar a verdade pela API. O corte é pelo cabeçalho em CAIXA ALTA —
    a linha de contagem usa "Bloqueantes abertas:", com caixa diferente, e por isso não
    colide.
    """
    if "BLOQUEANTES" not in saida:
        return []
    depois = saida.split("BLOQUEANTES", 1)[1]
    secao = depois.split("DECISÕES ABERTAS", 1)[0]
    return re.findall(r"^- \[([^\]]+)\]", secao, flags=re.MULTILINE)


def _responder_tudo_pela_cli(raiz: Path) -> list[str]:
    """Responde as bloqueantes uma a uma, relendo `status` entre cada resposta.

    Reler é obrigatório e não é preciosismo: B3 muda o veredito das outras lacunas
    conforme as partes do critério de aceite são cobertas, e B1 pode ativar lacunas que
    não existiam quando o laço começou. Responder a lista inicial de uma vez deixaria
    bloqueante nova aberta.
    """
    respondidas: list[str] = []
    for _ in range(LIMITE_DE_VOLTAS):
        status = _cli(raiz, "descoberta", "status")
        assert status.returncode == 0, status.stdout + status.stderr
        abertas = _ids_bloqueantes(status.stdout)
        if not abertas:
            return respondidas
        alvo = abertas[0]
        resposta = _cli(raiz, "descoberta", "responder", alvo, f"resposta para {alvo}")
        assert resposta.returncode == 0, resposta.stdout + resposta.stderr
        respondidas.append(alvo)
    raise AssertionError(f"{LIMITE_DE_VOLTAS} respostas e ainda há bloqueante aberta")


# --- 1. registrar ---------------------------------------------------------------------


def test_registrar_grava_o_bloco_e_classifica_a_intencao(tmp_path):
    """Cai se o verbo sumir, se sair 1 no caminho feliz, ou se registrar sem classificar.

    É o primeiro degrau da saída do portão: sem bloco registrado, `avaliar` responde
    `registrada=False` e o gate recusa para sempre — que era o estado anterior a este
    ciclo, com a diferença de que agora existe comando para sair dele.
    """
    _ligar(tmp_path)

    saida = _cli(tmp_path, "descoberta", PEDIDO)

    assert saida.returncode == 0, saida.stdout + saida.stderr
    bloco = estado.carregar(tmp_path)[descoberta.CHAVE]
    assert bloco["pedido"] == PEDIDO
    assert bloco["intencao"] == "MATERIALIZAR"
    assert "MATERIALIZAR" in saida.stdout


def test_registrar_aceita_a_intencao_explicita(tmp_path):
    """Cai se `--intencao` for ignorado e o texto reclassificado por cima.

    É a forma de responder a pergunta de desempate: sem ela, um pedido ambíguo não teria
    como ser registrado nunca, e a desambiguação seria uma pergunta sem resposta possível
    — o mesmo defeito do portão sem saída, um andar acima.
    """
    _ligar(tmp_path)

    saida = _cli(tmp_path, "descoberta", "revisar e otimizar", "--intencao", "REVISAR")

    assert saida.returncode == 0, saida.stdout + saida.stderr
    assert estado.carregar(tmp_path)[descoberta.CHAVE]["intencao"] == "REVISAR"


def test_registrar_aceita_a_forma_com_igual(tmp_path):
    """Cai se só uma das duas grafias de `--intencao` for aceita.

    `--intencao=X` e `--intencao X` são igualmente naturais para quem digita; recusar uma
    delas é erro de uso onde não havia ambiguidade nenhuma.
    """
    _ligar(tmp_path)

    saida = _cli(tmp_path, "descoberta", "revisar e otimizar", "--intencao=OTIMIZAR")

    assert saida.returncode == 0, saida.stdout + saida.stderr
    assert estado.carregar(tmp_path)[descoberta.CHAVE]["intencao"] == "OTIMIZAR"


def test_o_sinalizador_nao_vira_parte_do_pedido(tmp_path):
    """Cai se `--intencao` e o valor dele forem concatenados no texto do pedido.

    O pedido é o texto sobre o qual a entrevista inteira é montada e que volta na tela
    para o usuário conferir. Ter `--intencao MATERIALIZAR` grudado nele faria o registro
    parecer certo e o pedido sair errado.
    """
    _ligar(tmp_path)

    _cli(tmp_path, "descoberta", PEDIDO, "--intencao", "MATERIALIZAR")

    assert estado.carregar(tmp_path)[descoberta.CHAVE]["pedido"] == PEDIDO


def test_registrar_sem_ciclo_ligado_recusa_sem_traceback(tmp_path):
    """Cai se `DescobertaAusente` (um `KeyError`) escapar como traceback.

    Descoberta sem ciclo não tem a quem bloquear, e a mensagem tem de dizer isso. A CLI
    proíbe traceback no topo do próprio arquivo: é esta saída que a skill lê.
    """
    saida = _cli(tmp_path, "descoberta", PEDIDO)

    assert saida.returncode == 1
    assert "Traceback" not in saida.stderr + saida.stdout
    assert "ligue o ENGINE" in saida.stdout
    assert not estado.caminho(tmp_path).is_file()


def test_registrar_sem_pedido_reclama(tmp_path):
    """Cai se um pedido vazio for aceito. Bloco com pedido em branco classifica sobre
    nada, e a entrevista inteira sairia montada sobre um texto que ninguém escreveu."""
    _ligar(tmp_path)

    saida = _cli(tmp_path, "descoberta", "--intencao", "MATERIALIZAR")

    assert saida.returncode == 1
    assert descoberta.CHAVE not in estado.carregar(tmp_path)


def test_intencao_sem_valor_depois_nao_engole_o_pedido(tmp_path):
    """Cai se `--intencao` no fim da linha consumir o argumento seguinte (não há nenhum)
    ou for silenciosamente ignorado. Ignorado, o pedido seria reclassificado pelo texto —
    e a intenção que a pessoa quis declarar sumiria sem aviso."""
    _ligar(tmp_path)

    saida = _cli(tmp_path, "descoberta", PEDIDO, "--intencao")

    assert saida.returncode == 1
    assert "--intencao" in saida.stdout
    assert descoberta.CHAVE not in estado.carregar(tmp_path)


def test_intencao_fora_da_taxonomia_lista_as_conhecidas(tmp_path):
    """Cai se o `ValueError` de `Intencao("XPTO")` virar traceback, ou se a mensagem não
    disser quais valores existem — quem digitou errado precisa da lista, não do erro."""
    _ligar(tmp_path)

    saida = _cli(tmp_path, "descoberta", PEDIDO, "--intencao", "XPTO")

    assert saida.returncode == 1
    assert "Traceback" not in saida.stderr + saida.stdout
    assert "MATERIALIZAR" in saida.stdout and "CONSTRUIR_IA" in saida.stdout
    assert descoberta.CHAVE not in estado.carregar(tmp_path)


def test_registrar_por_cima_de_entrevista_respondida_recusa(tmp_path):
    """Cai se a guarda de sobrescrita sumir: `registrar` reescreve o bloco INTEIRO.

    Repetir o verbo para corrigir uma palavra do pedido é o motivo mais natural de
    chamá-lo duas vezes, e sem a guarda ele apagaria em silêncio tudo o que já foi
    respondido — com o agravante de que a pessoa lembra de ter respondido.
    """
    _ligar(tmp_path)
    assert _cli(tmp_path, "descoberta", PEDIDO).returncode == 0
    assert _cli(tmp_path, "descoberta", "responder", "problema", "somar sem erro").returncode == 0
    antes = _impressao_digital(tmp_path)

    saida = _cli(tmp_path, "descoberta", PEDIDO + " corrigido")

    assert saida.returncode == 1
    assert "--forcar" in saida.stdout
    assert _impressao_digital(tmp_path) == antes, "a recusa gravou no estado"


def test_forcar_recomeca_a_entrevista(tmp_path):
    """Cai se `--forcar` deixar de existir — aí a guarda acima vira parede, e corrigir o
    pedido exigiria religar o ciclo inteiro. É o par obrigatório da guarda."""
    _ligar(tmp_path)
    _cli(tmp_path, "descoberta", PEDIDO)
    _cli(tmp_path, "descoberta", "responder", "problema", "somar sem erro")

    saida = _cli(tmp_path, "descoberta", PEDIDO + " corrigido", "--forcar")

    assert saida.returncode == 0, saida.stdout + saida.stderr
    bloco = estado.carregar(tmp_path)[descoberta.CHAVE]
    assert bloco["pedido"].endswith("corrigido")
    assert bloco["respostas"] == {}


# --- 2. status ------------------------------------------------------------------------


def test_status_mostra_intencao_bloqueantes_inteiras_e_assumiveis(tmp_path):
    """Cai se o status virar contagem ("6 bloqueantes") ou listar só os ids.

    Sem a pergunta inteira, quem leu o status não sabe o que responder e volta a perguntar
    ao modelo — que é o motivo de `DecisaoAberta` carregar a pergunta em vez de um rótulo.
    As assumíveis entram pelo motivo oposto: é a lista do que o motor escolheu **não**
    perguntar, e ela existe para que a escolha fique escrita em vez de ficar em silêncio.
    """
    _ligar(tmp_path)
    _cli(tmp_path, "descoberta", PEDIDO)
    avaliacao = descoberta.avaliar_do_disco(tmp_path)
    assert avaliacao.bloqueantes and avaliacao.assumiveis, "o preparo precisa das duas listas"

    saida = _cli(tmp_path, "descoberta", "status")

    assert saida.returncode == 0, saida.stdout + saida.stderr
    assert "MATERIALIZAR" in saida.stdout
    for decisao in avaliacao.bloqueantes:
        assert decisao.id in saida.stdout
        assert decisao.pergunta in saida.stdout
    for decisao in avaliacao.assumiveis:
        assert decisao.id in saida.stdout
        assert decisao.pergunta in saida.stdout


def test_status_separa_bloqueante_de_assumivel(tmp_path):
    """Cai se as duas listas forem impressas juntas, ou trocadas.

    Misturadas, o usuário responde as três assumíveis achando que destrava o plano e o
    gate continua fechado — e a lista de assumíveis, que existe para ser transparência,
    viraria interrogatório.
    """
    _ligar(tmp_path)
    _cli(tmp_path, "descoberta", PEDIDO)
    avaliacao = descoberta.avaliar_do_disco(tmp_path)

    saida = _cli(tmp_path, "descoberta", "status")

    listados = _ids_bloqueantes(saida.stdout)
    assert listados == [decisao.id for decisao in avaliacao.bloqueantes]
    for decisao in avaliacao.assumiveis:
        assert decisao.id not in listados


def test_status_diz_o_predicado_que_travou_cada_bloqueante(tmp_path):
    """Cai se o motivo B1/B2/B3 sumir da saída.

    "Bloqueado porque sim" não sobrevive a uma pessoa com pressa: o motivo é o que separa
    um portão defensável de um obstáculo, e é ele que sustenta, por escrito, a diferença
    entre bloqueante e assumível.
    """
    _ligar(tmp_path)
    _cli(tmp_path, "descoberta", PEDIDO)

    saida = _cli(tmp_path, "descoberta", "status")

    assert "porque " in saida.stdout
    assert "sem gatilho" in saida.stdout or "muda quais outras perguntas" in saida.stdout


def test_status_sem_descoberta_registrada_sai_1_sem_traceback(tmp_path):
    """Cai se a ausência de bloco virar `KeyError`, ou se sair 0 dizendo "tudo certo".

    "Não sei quais lacunas existem" e "não há lacuna" são frases opostas — é a mesma
    confusão que o gate falha fechado para não cometer.
    """
    _ligar(tmp_path)

    saida = _cli(tmp_path, "descoberta", "status")

    assert saida.returncode == 1
    assert "Traceback" not in saida.stderr + saida.stdout
    assert "nenhuma descoberta registrada" in saida.stdout


def test_status_nao_grava_nada(tmp_path):
    """Cai se `status` carimbar data, migrar bloco ou normalizar campo ao ler.

    Verbo de leitura que escreve é o defeito que faz duas sessões brigarem pelo cadeado
    sem ninguém ter pedido mudança nenhuma.
    """
    _ligar(tmp_path)
    _cli(tmp_path, "descoberta", PEDIDO)
    antes = _impressao_digital(tmp_path)

    assert _cli(tmp_path, "descoberta", "status").returncode == 0

    assert _impressao_digital(tmp_path) == antes


def test_status_com_bloco_em_versao_desconhecida_falha_fechado(tmp_path):
    """Cai se `DescobertaInvalida` for tratada como "sem descoberta" — que é liberação
    disfarçada de diagnóstico. Bloco de versão futura lido por motor antigo produz
    avaliação plausível sobre campos que mudaram de significado."""
    _ligar(tmp_path)
    _cli(tmp_path, "descoberta", PEDIDO)

    def _envelhecer(dados):
        dados[descoberta.CHAVE]["versao"] = descoberta.VERSAO_BLOCO + 99
        return dados

    estado.atualizar(tmp_path, _envelhecer)

    saida = _cli(tmp_path, "descoberta", "status")

    assert saida.returncode == 1
    assert "Traceback" not in saida.stderr + saida.stdout
    assert "ilegível" in saida.stdout


# --- 3. responder ---------------------------------------------------------------------


def test_responder_fecha_a_lacuna_e_ela_sai_das_bloqueantes(tmp_path):
    """Cai se a resposta for aceita e não gravada, ou gravada em outra chave.

    É o verbo que o portão exige e não tinha: sem ele, a única saída era editar o
    `.engine/estado.json` à mão — exatamente o que a mensagem de recusa manda não fazer.
    """
    _ligar(tmp_path)
    _cli(tmp_path, "descoberta", PEDIDO)
    antes = _ids_bloqueantes(_cli(tmp_path, "descoberta", "status").stdout)
    assert "problema" in antes

    saida = _cli(tmp_path, "descoberta", "responder", "problema", "somar sem erro de digitacao")

    assert saida.returncode == 0, saida.stdout + saida.stderr
    respostas = estado.carregar(tmp_path)[descoberta.CHAVE]["respostas"]
    assert respostas["problema"]["valor"] == "somar sem erro de digitacao"
    assert "problema" not in _ids_bloqueantes(_cli(tmp_path, "descoberta", "status").stdout)


def test_responder_junta_a_resposta_de_varias_palavras(tmp_path):
    """Cai se só a primeira palavra da resposta for gravada.

    Resposta de entrevista é frase, não símbolo. Guardar "somar" no lugar de "somar sem
    erro de digitacao" é perda silenciosa: a lacuna fecha e o conteúdo some.
    """
    _ligar(tmp_path)
    _cli(tmp_path, "descoberta", PEDIDO)

    _cli(tmp_path, "descoberta", "responder", "usuario", "o", "time", "de", "fiscal")

    respostas = estado.carregar(tmp_path)[descoberta.CHAVE]["respostas"]
    assert respostas["usuario"]["valor"] == "o time de fiscal"


def test_responder_id_desconhecido_recusa_sem_gravar(tmp_path):
    """Cai se `LacunaDesconhecida` for engolida: a resposta iria para um balde que
    ninguém lê, a lacuna verdadeira continuaria aberta e a pessoa lembraria de ter
    respondido. O estado sai byte-idêntico."""
    _ligar(tmp_path)
    _cli(tmp_path, "descoberta", PEDIDO)
    antes = _impressao_digital(tmp_path)

    saida = _cli(tmp_path, "descoberta", "responder", "lacuna_que_nao_existe", "qualquer coisa")

    assert saida.returncode == 1
    assert "Traceback" not in saida.stderr + saida.stdout
    assert "não está ativa" in saida.stdout
    assert _impressao_digital(tmp_path) == antes


def test_responder_sem_descoberta_registrada_recusa(tmp_path):
    """Cai se responder criar o bloco na hora — criar exigiria inventar o pedido e a
    intenção, e intenção inventada escolhe quais perguntas existem."""
    _ligar(tmp_path)

    saida = _cli(tmp_path, "descoberta", "responder", "problema", "qualquer coisa")

    assert saida.returncode == 1
    assert "Traceback" not in saida.stderr + saida.stdout
    assert descoberta.CHAVE not in estado.carregar(tmp_path)


def test_responder_sem_resposta_recusa(tmp_path):
    """Cai se `responder <ID>` sem texto gravar valor vazio.

    Lacuna com resposta em branco está fechada para o gate e aberta para a realidade: o
    plano passa e a pergunta continua sem resposta, que é o defeito exato que a
    elicitação existe para não ter.
    """
    _ligar(tmp_path)
    _cli(tmp_path, "descoberta", PEDIDO)
    antes = _impressao_digital(tmp_path)

    saida = _cli(tmp_path, "descoberta", "responder", "problema")

    assert saida.returncode == 1
    assert _impressao_digital(tmp_path) == antes


def test_responder_com_espacos_em_branco_recusa(tmp_path):
    """Cai se a resposta for testada por comprimento em vez de conteúdo: "   " tem três
    caracteres e nenhuma informação."""
    _ligar(tmp_path)
    _cli(tmp_path, "descoberta", PEDIDO)
    antes = _impressao_digital(tmp_path)

    saida = _cli(tmp_path, "descoberta", "responder", "problema", "   ")

    assert saida.returncode == 1
    assert _impressao_digital(tmp_path) == antes


def test_responder_de_novo_o_mesmo_id_corrige(tmp_path):
    """Cai se a segunda resposta ao mesmo id for recusada.

    Correção é normal em entrevista, e recusá-la deixaria uma resposta errada gravada para
    sempre, com o ciclo inteiro construído em cima dela.
    """
    _ligar(tmp_path)
    _cli(tmp_path, "descoberta", PEDIDO)
    _cli(tmp_path, "descoberta", "responder", "problema", "primeira versao")

    saida = _cli(tmp_path, "descoberta", "responder", "problema", "versao corrigida")

    assert saida.returncode == 0, saida.stdout + saida.stderr
    respostas = estado.carregar(tmp_path)[descoberta.CHAVE]["respostas"]
    assert respostas["problema"]["valor"] == "versao corrigida"


def test_responder_preserva_o_resto_do_estado(tmp_path):
    """Cai se a gravação da resposta montar um estado novo em vez de mutar o do disco.

    O bloco de descoberta mora dentro do `estado.json`, ao lado de `ciclo`, `cartoes` e
    `fases_concluidas`. Um mutador que devolvesse dicionário novo apagaria o ciclo inteiro
    para gravar uma resposta.
    """
    _ligar(tmp_path)
    _cli(tmp_path, "descoberta", PEDIDO)
    antes = json.loads(json.dumps(estado.carregar(tmp_path)["ciclo"]))

    _cli(tmp_path, "descoberta", "responder", "problema", "somar sem erro")

    assert estado.carregar(tmp_path)["ciclo"] == antes


# --- 4. intenção indeterminada: perguntar, nunca escolher -------------------------------


def test_intencao_empatada_pede_desambiguacao_e_nao_grava(tmp_path):
    """Cai se a CLI escolher a primeira candidata do placar.

    É a regra "sem evidência é pendência, não palpite" aplicada onde ela custa mais caro:
    a intenção decide QUAIS perguntas existem, e a errada não produz uma pergunta ruim —
    produz uma entrevista inteira sobre outro trabalho, respondida até o fim antes de
    alguém notar.
    """
    _ligar(tmp_path)

    saida = _cli(tmp_path, "descoberta", "revisar e otimizar")

    assert saida.returncode == 1
    assert "Traceback" not in saida.stderr + saida.stdout
    assert "REVISAR" in saida.stdout and "OTIMIZAR" in saida.stdout
    assert "--intencao" in saida.stdout
    assert descoberta.CHAVE not in estado.carregar(tmp_path), "gravou apesar da dúvida"


def test_a_desambiguacao_diz_como_responder(tmp_path):
    """Cai se a mensagem listar as candidatas e não disser o comando.

    É o mesmo defeito do portão sem saída em miniatura: a pessoa sabe o que falta decidir
    e não tem como informar a decisão.
    """
    _ligar(tmp_path)

    saida = _cli(tmp_path, "descoberta", "revisar e otimizar")

    assert 'descoberta "revisar e otimizar" --intencao' in saida.stdout


def test_a_desambiguacao_e_aceita_pela_propria_cli(tmp_path):
    """Cai se o comando sugerido na mensagem não funcionar como está escrito.

    Sugestão que não roda é pior que sugestão nenhuma: a pessoa a executa, recebe outro
    erro e conclui que o motor está quebrado.
    """
    _ligar(tmp_path)
    recusa = _cli(tmp_path, "descoberta", "revisar e otimizar")
    assert recusa.returncode == 1

    saida = _cli(tmp_path, "descoberta", "revisar e otimizar", "--intencao", "REVISAR")

    assert saida.returncode == 0, saida.stdout + saida.stderr
    assert estado.carregar(tmp_path)[descoberta.CHAVE]["intencao"] == "REVISAR"


def test_pedido_sem_sinal_nenhum_tambem_pergunta(tmp_path):
    """Cai se a ausência de sinal cair num ramo diferente do empate e escolher um padrão.

    São os dois casos de `IntencaoIndeterminada`, e nenhum dos dois autoriza escolher: sem
    candidata, a pergunta é aberta, e a lista de intenções conhecidas é o que a torna
    respondível.
    """
    _ligar(tmp_path)

    saida = _cli(tmp_path, "descoberta", "faz a coisa la do jeito que voce achar melhor")

    assert saida.returncode == 1
    assert "Nenhuma candidata" in saida.stdout
    assert "MATERIALIZAR" in saida.stdout and "CONSTRUIR_IA" in saida.stdout
    assert descoberta.CHAVE not in estado.carregar(tmp_path)


def test_a_desambiguacao_nao_e_recusa_de_estado(tmp_path):
    """Cai se a indeterminação for reportada como erro de estado.

    São diagnósticos opostos: um se conserta dizendo qual é a intenção, o outro mexendo no
    ciclo. Trocá-los manda a pessoa consertar o que não está quebrado.
    """
    _ligar(tmp_path)

    saida = _cli(tmp_path, "descoberta", "revisar e otimizar")

    assert "Nada foi gravado no estado." in saida.stdout
    assert "ligue o ENGINE" not in saida.stdout


# --- 5. o ciclo completo: registrar -> responder tudo -> `fase ANALISE` sai 0 -----------


def test_ciclo_completo_so_pela_cli_abre_o_portao(tmp_path):
    """O teste que prova que o portão tem saída. Cai se qualquer degrau exigir Python.

    Antes deste ciclo, esta sequência era impossível sem `python -c`: o gate recusava e
    não havia verbo para responder. Se algum dia `registrar`, `status` ou `responder`
    deixar de existir — ou o gate parar de reconhecer o que eles gravam —, é aqui que
    aparece, e aparece como o motor travado na primeira fase.
    """
    _ligar(tmp_path)
    assert _cli(tmp_path, "descoberta", PEDIDO).returncode == 0
    assert _cli(tmp_path, "fase", "ANALISE").returncode == 1, "o gate tem de estar fechado"

    respondidas = _responder_tudo_pela_cli(tmp_path)

    assert respondidas, "o preparo precisa de pelo menos uma bloqueante"
    saida = _cli(tmp_path, "fase", "ANALISE")
    assert saida.returncode == 0, saida.stdout + saida.stderr
    dados = estado.carregar(tmp_path)
    assert dados["fase"] == "ANALISE"
    assert dados["fases_concluidas"] == ["DESCOBERTA"]


def test_o_status_anuncia_a_porta_aberta_quando_nao_ha_bloqueante(tmp_path):
    """Cai se o status nunca disser que terminou.

    Sem essa linha, quem responde não sabe quando parar e continua respondendo assumíveis
    — que é o interrogatório de quarenta itens que a regra de bloqueio existe para evitar.
    """
    _ligar(tmp_path)
    _cli(tmp_path, "descoberta", PEDIDO)
    _responder_tudo_pela_cli(tmp_path)

    saida = _cli(tmp_path, "descoberta", "status")

    assert saida.returncode == 0
    assert "ABERTA" in saida.stdout
    assert _ids_bloqueantes(saida.stdout) == []


def test_as_assumiveis_continuam_abertas_depois_da_porta_abrir(tmp_path):
    """Cai se responder as bloqueantes apagar a lista de assumíveis.

    A porta abre com assumível em aberto de propósito — é isso que "não pergunte o que
    você pode decidir" quer dizer aqui. O que não pode é a lista sumir: ela é o registro
    do que o motor escolheu não perguntar.
    """
    _ligar(tmp_path)
    _cli(tmp_path, "descoberta", PEDIDO)
    _responder_tudo_pela_cli(tmp_path)

    avaliacao = descoberta.avaliar_do_disco(tmp_path)

    assert avaliacao.liberado_para_planejar
    assert avaliacao.assumiveis, "as assumíveis não podem sumir quando a porta abre"


# --- nenhum caminho termina em traceback ------------------------------------------------


@pytest.mark.parametrize(
    "argumentos",
    [
        (),
        ("status",),
        ("responder",),
        ("responder", "problema"),
        ("responder", "id_inexistente", "valor"),
        ("--intencao",),
        ("--intencao", "XPTO"),
        ("pedido qualquer", "--intencao", "NAO_EXISTE"),
        ("revisar e otimizar",),
        ("um pedido sem sinal nenhum de intencao",),
    ],
)
def test_nenhum_caminho_do_verbo_termina_em_traceback(tmp_path, argumentos):
    """Cai se alguma exceção nova escapar — `KeyError` do bloco, `ValueError` da
    taxonomia, `DescobertaInvalida`, o que for.

    Traceback no terminal é o formato de erro que a CLI proíbe no topo do próprio arquivo:
    a skill lê esta saída para decidir o que reportar ao usuário.
    """
    _ligar(tmp_path)

    saida = _cli(tmp_path, "descoberta", *argumentos)

    assert "Traceback" not in saida.stderr, saida.stderr
    assert "Traceback" not in saida.stdout, saida.stdout
    assert saida.returncode == 1


def test_o_verbo_aparece_no_uso(tmp_path):
    """Cai se `descoberta` for implementado e não anunciado.

    Verbo que existe e não consta do `uso` é o portão sem saída de novo, agora por
    desconhecimento: quem vê a recusa do gate não descobre o comando que a resolve.
    """
    saida = _cli(tmp_path, "verbo_que_nao_existe")

    assert saida.returncode == 1
    assert "descoberta" in saida.stdout


def test_o_verbo_nao_grava_estado_por_fora_do_cadeado(tmp_path):
    """Cai se alguém trocar `descoberta.registrar`/`responder` por escrita direta.

    A trava geral (`test_nenhum_gravar_fora_do_estado`) varre o arquivo inteiro por texto;
    esta olha o corpo dos verbos novos e cobra o caminho positivo — que a mutação passe
    pelas funções que tomam o cadeado. Uma escrita solta aqui é o *lost update* de volta,
    e ele some em silêncio até duas sessões se atropelarem.
    """
    fonte = (RAIZ_PLUGIN / "ferramentas" / "cli.py").read_text(encoding="utf-8")
    corpo = fonte.split("def _verbo_descoberta")[1].split("\ndef _prog_trilha")[0]
    assert "descoberta.registrar(" in corpo
    assert "descoberta.responder(" in corpo
    assert ".write_text(" not in corpo
    assert "json.dump" not in corpo
