import pytest
from io import StringIO
from unittest.mock import patch
from trabalho import Carta, Baralho, Jogador, Jogo # type: ignore

def test_carta_creation():
    carta = Carta("A", "♠")
    assert str(carta) == "A♠"
    
    with pytest.raises(ValueError):
        Carta("Z", "♠")
    
    with pytest.raises(ValueError):
        Carta("A", "X")

def test_baralho_creation():
    baralho = Baralho()
    assert len(baralho) == 104  # 52 cards * 2 decks

def test_baralho_puxar_carta():
    baralho = Baralho()
    carta = baralho.puxar_carta()
    assert isinstance(carta, Carta)
    assert len(baralho) == 103

def test_jogador_receber_carta():
    jogador = Jogador("Test")
    carta = Carta("A", "♠")
    jogador.receber_carta(carta)
    assert len(jogador.mao) == 1
    assert jogador.mao[0] == carta

def test_jogador_jogar_carta():
    jogador = Jogador("Test")
    carta1 = Carta("A", "♠")
    carta2 = Carta("K", "♥")
    jogador.receber_carta(carta1)
    jogador.receber_carta(carta2)
    
    jogada = jogador.jogar_carta(0)
    assert jogada == carta1
    assert len(jogador.mao) == 1
    assert jogador.mao[0] == carta2

def test_jogador_ordenar_mao():
    jogador = Jogador("Test")
    jogador.receber_carta(Carta("K", "♠"))
    jogador.receber_carta(Carta("A", "♥"))
    jogador.receber_carta(Carta("Q", "♦"))
    
    jogador.ordenar_mao()
    assert str(jogador.mao[0]) == "A♥"
    assert str(jogador.mao[1]) == "Q♦"
    assert str(jogador.mao[2]) == "K♠"

def test_jogador_verificar_vitoria():
    jogador = Jogador("Test")
    # Create a winning hand (three sets of three)
    jogador.mao = [
        Carta("A", "♠"), Carta("A", "♥"), Carta("A", "♦"),
        Carta("2", "♠"), Carta("3", "♠"), Carta("4", "♠"),
        Carta("5", "♥"), Carta("6", "♥"), Carta("7", "♥")
    ]
    assert jogador.verificar_vitoria() == True

    # Create a non-winning hand
    jogador.mao = [
        Carta("A", "♠"), Carta("A", "♥"), Carta("K", "♦"),
        Carta("2", "♠"), Carta("3", "♠"), Carta("4", "♠"),
        Carta("5", "♥"), Carta("6", "♥"), Carta("7", "♥")
    ]
    assert jogador.verificar_vitoria() == False

def test_jogador_jogar_como_maquina():
    jogador = Jogador("Máquina", is_humano=False)
    jogador.mao = [
        Carta("A", "♠"), Carta("A", "♥"), Carta("K", "♦"),
        Carta("2", "♠"), Carta("3", "♠"), Carta("4", "♠"),
        Carta("5", "♥"), Carta("6", "♥"), Carta("7", "♥")
    ]
    
    carta_descartada = Carta("A", "♦")
    carta_pegar, carta_descartar = jogador.jogar_como_maquina(carta_descartada)
    
    assert carta_pegar == carta_descartada
    assert carta_descartar is None

    carta_descartada = Carta("Q", "♣")
    carta_pegar, carta_descartar = jogador.jogar_como_maquina(carta_descartada)
    
    assert carta_pegar is None
    assert isinstance(carta_descartar, Carta)

def test_jogo_iniciar():
    jogo = Jogo()
    jogo.iniciar_jogo()
    
    assert len(jogo.jogador_humano.mao) == 9
    assert len(jogo.jogador_maquina.mao) == 9
    assert len(jogo.baralho) == 86  # 104 - (9 * 2)

@patch('builtins.input', side_effect=['1', '1'])
def test_jogada_humano(mock_input):
    jogo = Jogo()
    jogo.iniciar_jogo()
    jogo.carta_descartada = Carta("Q", "♣")
    
    with patch('sys.stdout', new=StringIO()) as fake_out:
        jogo.jogada_humano(False)
        output = fake_out.getvalue()
    
    assert "Nova carta puxada do baralho" in output
    assert "Carta descartada:" in output
    assert len(jogo.jogador_humano.mao) == 9

def test_jogada_maquina():
    jogo = Jogo()
    jogo.iniciar_jogo()
    jogo.carta_descartada = Carta("Q", "♣")
    
    with patch('sys.stdout', new=StringIO()) as fake_out:
        jogo.jogada_maquina()
        output = fake_out.getvalue()
    
    assert "Jogada da máquina concluída" in output
    assert len(jogo.jogador_maquina.mao) == 9

def test_verificar_fim_jogo():
    jogo = Jogo()
    jogo.iniciar_jogo()
    
    assert jogo.verificar_fim_jogo() is None
    
    # Simulate winning condition for human player
    jogo.jogador_humano.mao = [
        Carta("A", "♠"), Carta("A", "♥"), Carta("A", "♦"),
        Carta("2", "♠"), Carta("3", "♠"), Carta("4", "♠"),
        Carta("5", "♥"), Carta("6", "♥"), Carta("7", "♥")
    ]
    assert jogo.verificar_fim_jogo() == "humano"
    
    # Simulate winning condition for machine player
    jogo.jogador_humano.mao = []  # Reset human player's hand
    jogo.jogador_maquina.mao = [
        Carta("A", "♠"), Carta("A", "♥"), Carta("A", "♦"),
        Carta("2", "♠"), Carta("3", "♠"), Carta("4", "♠"),
        Carta("5", "♥"), Carta("6", "♥"), Carta("7", "♥")
    ]
    assert jogo.verificar_fim_jogo() == "maquina"
    
    # Simulate draw condition
    jogo.baralho.cartas = []
    assert jogo.verificar_fim_jogo() == "empate"
    
def test_jogador_sem_cartas():
    jogador = Jogador("Test")
    assert len(jogador.mao) == 0
    
def test_jogador_jogar_carta_invalida():
    jogador = Jogador("Test")
    with pytest.raises(IndexError):
        jogador.jogar_carta(0)  # Tentar jogar sem cartas

def test_jogador_vitoria_especifica():
    jogador = Jogador("Test")
    jogador.mao = [
        Carta("A", "♠"), Carta("A", "♥"), Carta("A", "♦"),
        Carta("K", "♠"), Carta("K", "♥"), Carta("K", "♦"),
        Carta("Q", "♠"), Carta("Q", "♥"), Carta("Q", "♦")
    ]
    assert jogador.verificar_vitoria() == True

@patch('builtins.input', side_effect=['2'])
def test_jogada_humano_puxando_descartada(mock_input):
    jogo = Jogo()
    jogo.iniciar_jogo()
    jogo.carta_descartada = Carta("Q", "♣")
    
    with patch('sys.stdout', new=StringIO()) as fake_out:
        jogo.jogada_humano(False)
        output = fake_out.getvalue()
    
    assert "Você pegou a carta descartada" in output

if __name__ == "__main__":
    pytest.main()
    