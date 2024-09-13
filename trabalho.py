import random
# crinado a classe de cartas para ter um objeto de cada carta. Isso vai ajudar a manipular 
class Carta:
    naipes = {"paus", "copas", "ouros", "espadas"}
    valores = {"1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"}

    def __init__(self, valor, naipe):
        if valor in Carta.valores and naipe in Carta.naipes:
            self.valor = valor
            self.naipe = naipe
        else:
            raise ValueError("Valor ou naipe inválido.")

    def __repr__(self):
        return f"{self.valor} de {self.naipe}"

class Baralho:
    def __init__(self):
        self.cartas = []
        self.criar_baralho()

    def criar_baralho(self):
        for _ in range(2):  
            for naipe in Carta.naipes:  
                for valor in Carta.valores:  
                    self.cartas.append(Carta(valor, naipe))  

    def embaralhar(self):
        random.shuffle(self.cartas)

    def puxar_carta(self):
        return self.cartas.pop() if self.cartas else None

    def __len__(self):
        return len(self.cartas)

class Jogador:
    def __init__(self, nome, is_humano=True):
        self.nome = nome
        self.is_humano = is_humano  
        self.mao = []

    def receber_carta(self, carta):
        self.mao.append(carta)

    def jogar_carta(self, index):
        if 0 <= index < len(self.mao):
            return self.mao.pop(index)
        return None

    def mostrar_mao(self):
        return ', '.join([str(carta) for carta in self.mao])

    def jogar_como_maquina(self):
        if not self.is_humano and self.mao:
            return self.jogar_carta(0)
        return None

jogador_humano = Jogador("Humano")
jogador_maquina = Jogador("Máquina", is_humano=False)

baralho = Baralho()
baralho.embaralhar()

for _ in range(9): 
    jogador_humano.receber_carta(baralho.puxar_carta())
    jogador_maquina.receber_carta(baralho.puxar_carta())


while True:
    jogador_humano.receber_carta(baralho.puxar_carta())
    print(f"Mão do {jogador_humano.nome}: {jogador_humano.mostrar_mao()}")
    print(f"Mão do {jogador_maquina.nome}: {jogador_maquina.mostrar_mao()}")
    escolha = input()

    if escolha.lower() == 'sair':
        print("Você decidiu encerrar o jogo.")
        break

    try:
        indice = int(escolha) - 1
        if 0 <= indice < len(jogador_humano.mao):
            carta_descartada = jogador_humano.jogar_carta(indice)
            print(f"Você descartou: {carta_descartada}")
        else:
            print("Escolha inválida, tente novamente.")
            continue
    except ValueError:
        print("Entrada inválida, tente novamente.")
        continue

    carta_descartada_maquina = jogador_maquina.jogar_como_maquina()
    print(f"{jogador_maquina.nome} descartou: {carta_descartada_maquina}")

    if len(baralho) == 0:
        print("O baralho acabou! O jogo terminou.")
        break
    
print("Fim do jogo.")
