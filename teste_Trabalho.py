import random
import time

class Carta:
    naipes = ["♣": "preto", "♥": "vermelho", "♦": "vermelho", "♠": "preto"]
    valores = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

    def __init__(self, valor, naipe):
        if valor in Carta.valores and naipe in Carta.naipes:
            self.valor = valor
            self.naipe = naipe
        else:
            raise ValueError("Valor ou naipe inválido.")

    def __repr__(self):
        return f"{self.valor}{self.naipe}"

class Baralho:
    def __init__(self):
        self.cartas = []
        self.criar_baralho()

    def criar_baralho(self):
        for _ in range(2):  # Dois baralhos
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

    def ordenar_mao(self):
        self.mao.sort(key=lambda c: (Carta.valores.index(c.valor), Carta.naipes.index(c.naipe)))

    def verificar_vitoria(self):
        self.ordenar_mao()
        grupos = self.encontrar_grupos()
        return len(grupos) == 3 and all(len(grupo) >= 3 for grupo in grupos)

    def encontrar_grupos(self):
        grupos = []
        mao_temp = self.mao.copy()
        
        # Procurar por trincas
        valores = set(carta.valor for carta in mao_temp)
        for valor in valores:
            trinca = [carta for carta in mao_temp if carta.valor == valor]
            if len(trinca) >= 3:
                grupos.append(trinca)
                mao_temp = [carta for carta in mao_temp if carta not in trinca]
        
        # Procurar por sequências
        for naipe in Carta.naipes:
            cartas_naipe = [carta for carta in mao_temp if carta.naipe == naipe]
            cartas_naipe.sort(key=lambda c: Carta.valores.index(c.valor))
            i = 0
            while i < len(cartas_naipe):
                sequencia = [cartas_naipe[i]]
                for j in range(i + 1, len(cartas_naipe)):
                    if Carta.valores.index(cartas_naipe[j].valor) == Carta.valores.index(sequencia[-1].valor) + 1:
                        sequencia.append(cartas_naipe[j])
                    else:
                        break
                if len(sequencia) >= 3:
                    grupos.append(sequencia)
                    mao_temp = [carta for carta in mao_temp if carta not in sequencia]
                    i = 0
                else:
                    i += 1
        
        return grupos

    def jogar_como_maquina(self, carta_descartada):
        self.ordenar_mao()
        grupos = self.encontrar_grupos()

        # Verificar se a carta descartada pode formar um grupo
        if carta_descartada:
            for grupo in grupos:
                if len(grupo) == 2 and (carta_descartada.valor == grupo[0].valor or
                   (carta_descartada.naipe == grupo[0].naipe and
                    abs(Carta.valores.index(carta_descartada.valor) - Carta.valores.index(grupo[-1].valor)) == 1)):
                    return carta_descartada, None

        # Se não puder formar um grupo, descartar a carta menos útil
        if self.mao:
            cartas_unicas = [carta for carta in self.mao if sum(1 for c in self.mao if c.valor == carta.valor) == 1]
            if cartas_unicas:
                carta_para_descartar = max(cartas_unicas, key=lambda c: Carta.valores.index(c.valor))
            else:
                carta_para_descartar = self.mao[-1]
            return None, self.jogar_carta(self.mao.index(carta_para_descartar))

        return None, None

class Jogo:
    def __init__(self):
        self.baralho = Baralho()
        self.jogador_humano = Jogador("Humano")
        self.jogador_maquina = Jogador("Máquina", is_humano=False)
        self.carta_descartada = None

    def iniciar_jogo(self):
        self.baralho.embaralhar()
        for _ in range(9):
            self.jogador_humano.receber_carta(self.baralho.puxar_carta())
            self.jogador_maquina.receber_carta(self.baralho.puxar_carta())
        self.jogador_humano.ordenar_mao()
        self.jogador_maquina.ordenar_mao()

    def jogada_humano(self):
        print("\nSua vez de jogar!")
        print(f"Sua mão atual: {self.jogador_humano.mostrar_mao()}")

        # Opção de pegar carta descartada ou puxar do baralho
        if self.carta_descartada:
            while True:
                escolha = input(f"Deseja pegar a carta descartada ({self.carta_descartada})? (s/n): ").lower()
                if escolha in ['s', 'n']:
                    break
                print("Escolha inválida. Digite 's' para sim ou 'n' para não.")

            if escolha == 's':
                self.jogador_humano.receber_carta(self.carta_descartada)
                self.carta_descartada = None
                print("Você pegou a carta descartada.")
            else:
                nova_carta = self.baralho.puxar_carta()
                if nova_carta:
                    self.jogador_humano.receber_carta(nova_carta)
                    print(f"Você puxou {nova_carta} do baralho.")
                else:
                    print("O baralho está vazio!")
                    return False
        else:
            nova_carta = self.baralho.puxar_carta()
            if nova_carta:
                self.jogador_humano.receber_carta(nova_carta)
                print(f"Você puxou {nova_carta} do baralho.")
            else:
                print("O baralho está vazio!")
                return False

        self.jogador_humano.ordenar_mao()
        print(f"Sua mão atualizada: {self.jogador_humano.mostrar_mao()}")

        # Descartar uma carta
        while True:
            try:
                indice = int(input("Escolha uma carta para descartar (1-10): ")) - 1
                if 0 <= indice < len(self.jogador_humano.mao):
                    carta_descartada = self.jogador_humano.jogar_carta(indice)
                    self.carta_descartada = carta_descartada
                    print(f"Você descartou: {carta_descartada}")
                    break
                else:
                    print("Índice inválido. Tente novamente.")
            except ValueError:
                print("Entrada inválida. Por favor, digite um número.")

        return True

    def jogada_maquina(self):
        print("\nVez da Máquina...")
        time.sleep(1)  # Pausa para criar suspense

        carta_pegar, carta_descartar = self.jogador_maquina.jogar_como_maquina(self.carta_descartada)
        if carta_pegar:
            self.jogador_maquina.receber_carta(self.carta_descartada)
            self.carta_descartada = None
            print("A Máquina pegou a carta descartada.")
        else:
            nova_carta = self.baralho.puxar_carta()
            if nova_carta:
                self.jogador_maquina.receber_carta(nova_carta)
                print("A Máquina puxou uma nova carta do baralho.")
            else:
                print("O baralho está vazio!")
                return False

        time.sleep(1)  # Outra pausa para criar suspense

        if carta_descartar:
            self.carta_descartada = carta_descartar
            print(f"A Máquina descartou: {carta_descartar}")
        elif len(self.jogador_maquina.mao) > 9:
            self.carta_descartada = self.jogador_maquina.jogar_carta(-1)
            print(f"A Máquina descartou: {self.carta_descartada}")

        self.jogador_maquina.ordenar_mao()
        return True

    def verificar_fim_jogo(self):
        if len(self.baralho) == 0:
            return "empate"
        if self.jogador_humano.verificar_vitoria():
            return "humano"
        if self.jogador_maquina.verificar_vitoria():
            return "maquina"
        return None

def exibir_estado_jogo(jogo):
    print("\n" + "=" * 50)
    print(f"Sua mão: {jogo.jogador_humano.mostrar_mao()}")
    print(f"Cartas da Máquina: {len(jogo.jogador_maquina.mao)}")
    print(f"Carta descartada: {jogo.carta_descartada}")
    print(f"Cartas no baralho: {len(jogo.baralho)}")
    print("=" * 50)

def main():
    print("Bem-vindo ao Jogo de Pife!")
    print("Objetivo: Forme 3 grupos de 3 ou mais cartas (trincas ou sequências) para vencer.")
    input("Pressione Enter para começar...")

    jogo = Jogo()
    jogo.iniciar_jogo()

    rodada = 1
    while True:
        print(f"\n        ----------- Rodada {rodada} -----------")
        exibir_estado_jogo(jogo)

        # Jogada do humano
        if not jogo.jogada_humano():
            break

        # Verificar fim de jogo após jogada do humano
        resultado = jogo.verificar_fim_jogo()
        if resultado:
            break

        # Jogada da máquina
        if not jogo.jogada_maquina():
            break

        # Verificar fim de jogo após jogada da máquina
        resultado = jogo.verificar_fim_jogo()
        if resultado:
            break

        rodada += 1
        input("Pressione Enter para continuar para a próxima rodada...")

    # Fim do jogo
    exibir_estado_jogo(jogo)
    if resultado == "empate":
        print("O baralho acabou! O jogo terminou em empate.")
    elif resultado == "humano":
        print("Parabéns! Você venceu!")
    else:
        print("A máquina venceu. Tente novamente!")

if __name__ == "__main__":
    main()

