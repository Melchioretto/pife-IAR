import random

class Carta:
    naipes = {"♣": "preto", "♥": "vermelho", "♦": "vermelho", "♠": "preto"}
    valores = {"1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"}

    def __init__(self, valor, naipe):
        if valor in Carta.valores and naipe in Carta.naipes:
            self.valor = valor
            self.naipe = naipe
            self.cor = Carta.naipes[naipe]  # Define a cor da carta com base no naipe
        else:
            raise ValueError("Valor ou naipe inválido.")

    def __repr__(self):
        if self.cor == "vermelho":
            return f"\033[91m{self.valor}{self.naipe}\033[0m"  # Texto vermelho
        else:
            return f"\033[97m{self.valor}{self.naipe}\033[0m"  # Texto branco (simulando preto)


class Baralho:
    def __init__(self):
        self.cartas = []
        self.coringas = []
        self.monte_descarte = []  # Monte de descarte
        self.criar_baralho()

    def criar_baralho(self):
        for _ in range(2):  
            for naipe in Carta.naipes:  
                for valor in Carta.valores:  
                    self.cartas.append(Carta(valor, naipe))  

    def definir_coringa(self):
        if not self.cartas:
            return

        # Remove uma carta aleatória do baralho e define o coringa baseado nela
        carta_sorteada = random.choice(self.cartas)
        self.cartas.remove(carta_sorteada)

        print(f"Carta sorteada: {carta_sorteada} (Esta carta será inutilizada)")

        # Identificar as cartas seguintes de mesmo naipe e cor
        valor = carta_sorteada.valor
        cor = carta_sorteada.cor

        try:
            proximo_valor = str(int(valor) + 1) if valor.isdigit() else None
        except ValueError:
            proximo_valor = None

        # Selecionar as cartas que serão os coringas
        for carta in self.cartas:
            if carta.valor == proximo_valor and carta.cor == cor:
                self.coringas.append(carta)

        print(f"As cartas coringas são: {', '.join(str(carta) for carta in self.coringas)}")

    def embaralhar(self):
        random.shuffle(self.cartas)

    def puxar_carta(self):
        return self.cartas.pop() if self.cartas else None

    def adicionar_ao_monte_descarte(self, carta):
        self.monte_descarte.append(carta)

    def puxar_carta_do_monte_descarte(self):
        return self.monte_descarte.pop() if self.monte_descarte else None

    def __len__(self):
        return len(self.cartas) + len(self.monte_descarte)  # Contar o monte de descarte também

    def verificar_se_coringa(self, carta):
        return carta in self.coringas

    def mostrar_monte_compra(self):
        if self.cartas:
            print("Monte de compra:")
            for carta in self.cartas:
                print(carta, end=" ")
            print()
        else:
            print("O monte de compra está vazio.")


class Jogador:
    def __init__(self, nome, is_humano=True):
        self.nome = nome
        self.is_humano = is_humano
        self.mao = []
        self.trincas = []  # Lista de trincas feitas

    def receber_carta(self, carta):
        self.mao.append(carta)

    def jogar_carta(self, index):
        if 0 <= index < len(self.mao):
            return self.mao.pop(index)
        return None

    def mostrar_mao(self):
        return ', '.join([str(carta) for carta in self.mao])

    def escolher_trinca(self, indices):
        trinca = [self.mao[i] for i in indices if 0 <= i < len(self.mao)]
        return trinca

    def adicionar_trinca(self, trinca):
        if self.validar_trinca(trinca):
            self.trincas.append(trinca)
            for carta in trinca:
                self.mao.remove(carta)  # Remove as cartas da mão ao formar a trinca
            print(f"Trinca formada: {', '.join([str(carta) for carta in trinca])}")
        else:
            print("A trinca escolhida é inválida!")

    def remover_trinca(self, index):
        if 0 <= index < len(self.trincas):
            trinca = self.trincas.pop(index)
            self.mao.extend(trinca)  # Devolve as cartas da trinca para a mão
            print(f"Trinca removida: {', '.join([str(carta) for carta in trinca])}")
        else:
            print("Trinca inválida!")

    def validar_trinca(self, trinca):
        if len(trinca) != 3:
            return False

        valores = [carta.valor for carta in trinca if not baralho.verificar_se_coringa(carta)]
        naipes = [carta.naipe for carta in trinca if not baralho.verificar_se_coringa(carta)]

        # Verifica se todas as cartas (ou coringas) têm o mesmo valor e naipes diferentes
        if len(set(valores)) == 1 and len(set(naipes)) == len(trinca):
            return True

        # Verifica se há uma sequência válida (mesmo naipe e valores consecutivos)
        if len(set(naipes)) == 1:
            valores_ordenados = sorted([int(carta.valor) for carta in trinca if carta.valor.isdigit()] + [int(carta.valor) for carta in trinca if carta.valor in {"J", "Q", "K"}])
            if len(valores_ordenados) == 2:  # Se tiver dois valores, coringa completa a sequência
                return valores_ordenados[1] - valores_ordenados[0] == 1
            elif len(valores_ordenados) == 3:
                return valores_ordenados[2] - valores_ordenados[1] == 1 and valores_ordenados[1] - valores_ordenados[0] == 1

        return False

    def mostrar_trincas(self):
        if self.trincas:
            for i, trinca in enumerate(self.trincas, 1):
                print(f"Trinca {i}: {', '.join([str(carta) for carta in trinca])}")
        else:
            print("Nenhuma trinca formada.")


class Plays:
    def __init__(self, jogador, baralho):
        self.jogador = jogador
        self.baralho = baralho

    def analisar_mao(self):
        valores = {}
        naipes = {}
        for carta in self.jogador.mao:
            if carta.valor not in valores:
                valores[carta.valor] = []
            valores[carta.valor].append(carta)

            if carta.naipe not in naipes:
                naipes[carta.naipe] = []
            naipes[carta.naipe].append(carta)

        return valores, naipes

    def verificar_trinca(self, valores):
        for valor, cartas in valores.items():
            if len(cartas) >= 3:
                return True
        return False

    def verificar_sequencia(self, naipes):
        for naipe, cartas in naipes.items():
            valores_ordenados = sorted([int(carta.valor) for carta in cartas if carta.valor.isdigit()])
            for i in range(len(valores_ordenados) - 2):
                if valores_ordenados[i] + 1 == valores_ordenados[i + 1] == valores_ordenados[i + 2] - 1:
                    return True
        return False

    def escolher_carta_para_descartar(self):
        valores, naipes = self.analisar_mao()

        if self.verificar_trinca(valores) or self.verificar_sequencia(naipes):
            for carta in self.jogador.mao:
                if len(valores[carta.valor]) < 3 and len(naipes[carta.naipe]) < 3:
                    return self.jogador.mao.index(carta)
        return 0

    def jogar(self):
        index = self.escolher_carta_para_descartar()
        return self.jogador.jogar_carta(index)


# Exemplo de uso
baralho = Baralho()
baralho.embaralhar()
baralho.definir_coringa()  # Define o coringa

jogador_humano = Jogador("Humano")

# Distribui cartas
for _ in range(9): 
    jogador_humano.receber_carta(baralho.puxar_carta())

# Loop para formar trincas e sequências
while True:
    print(f"Mão do {jogador_humano.nome}: {jogador_humano.mostrar_mao()}")

    acao = input("Escolha uma ação: (f)azer trinca, (r)emover trinca, (m)ostrar trincas, (c)omprar cartas, (s)air: ").lower()

    if acao == 'f':
        indices = input("Escolha as cartas para formar uma trinca ou sequência (ex: 0,1,2): ").split(',')
        indices = [int(i) for i in indices]
        trinca = jogador_humano.escolher_trinca(indices)
        jogador_humano.adicionar_trinca(trinca)

    elif acao == 'r':
        jogador_humano.mostrar_trincas()
        indice = int(input("Escolha o índice da trinca para remover: ")) - 1
        jogador_humano.remover_trinca(indice)

    elif acao == 'm':
        jogador_humano.mostrar_trincas()

    elif acao == 'c':
        carta_nova = baralho.puxar_carta()
        if carta_nova:
            jogador_humano.receber_carta(carta_nova)
            print(f"Você pegou uma carta do topo: {carta_nova}")
        else:
            print("O baralho está vazio!")
            continue
    elif acao == 'mo':
        baralho.mostrar_monte_compra()
    elif acao == 's':
        break

    else:
        print("Ação inválida.")
