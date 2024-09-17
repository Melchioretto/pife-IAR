import random
from abc import ABC, abstractmethod

class Carta:
    NAIPES = ["♠", "♥", "♦", "♣"]
    VALORES = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

    def __init__(self, valor, naipe):
        if valor in self.VALORES and naipe in self.NAIPES:
            self.valor = valor
            self.naipe = naipe
        else:
            raise ValueError("Valor ou naipe inválido.")

    def __repr__(self):
        return f"{self.valor}{self.naipe}"

class Baralho:
    def __init__(self):
        self.cartas = [Carta(valor, naipe) for _ in range(2) for naipe in Carta.NAIPES for valor in Carta.VALORES]
        self.embaralhar()

    def embaralhar(self):
        random.shuffle(self.cartas)

    def puxar_carta(self):
        return self.cartas.pop() if self.cartas else None

    def __len__(self):
        return len(self.cartas)

class Jogador(ABC):
    def __init__(self, nome):
        self.nome = nome
        self.mao = []

    def receber_carta(self, carta):
        self.mao.append(carta)

    def jogar_carta(self, index):
        return self.mao.pop(index) if 0 <= index < len(self.mao) else None

    def mostrar_mao(self):
        return ', '.join(map(str, self.mao))

    def ordenar_mao(self):
        self.mao.sort(key=lambda c: (Carta.VALORES.index(c.valor), Carta.NAIPES.index(c.naipe)))

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
        for naipe in Carta.NAIPES:
            cartas_naipe = [carta for carta in mao_temp if carta.naipe == naipe]
            cartas_naipe.sort(key=lambda c: Carta.VALORES.index(c.valor))
            i = 0
            while i < len(cartas_naipe):
                sequencia = [cartas_naipe[i]]
                for j in range(i + 1, len(cartas_naipe)):
                    if Carta.VALORES.index(cartas_naipe[j].valor) == Carta.VALORES.index(sequencia[-1].valor) + 1:
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

    @abstractmethod
    def fazer_jogada(self, carta_descartada):
        pass

class JogadorHumano(Jogador):
    def fazer_jogada(self, carta_descartada):
        self.ordenar_mao()
        return self.interface.obter_jogada_humano(self, carta_descartada)

class JogadorMaquina(Jogador):
    def fazer_jogada(self, carta_descartada):
        self.ordenar_mao()
        grupos = self.encontrar_grupos()

        # Verificar se a carta descartada pode formar um grupo
        if carta_descartada:
            for grupo in grupos:
                if len(grupo) == 2 and (carta_descartada.valor == grupo[0].valor or
                   (carta_descartada.naipe == grupo[0].naipe and
                    abs(Carta.VALORES.index(carta_descartada.valor) - Carta.VALORES.index(grupo[-1].valor)) == 1)):
                    return carta_descartada, None

        # Se não puder formar um grupo, descartar a carta menos útil
        if self.mao:
            cartas_unicas = [carta for carta in self.mao if sum(1 for c in self.mao if c.valor == carta.valor) == 1]
            if cartas_unicas:
                carta_para_descartar = max(cartas_unicas, key=lambda c: Carta.VALORES.index(c.valor))
            else:
                carta_para_descartar = self.mao[-1]
            return None, self.jogar_carta(self.mao.index(carta_para_descartar))

        return None, None
    
class Interface(ABC):
    @abstractmethod
    def exibir_estado_jogo(self, jogo):
        pass

    @abstractmethod
    def obter_jogada_humano(self, jogador, carta_descartada):
        pass

    @abstractmethod
    def exibir_mensagem(self, mensagem):
        pass
    
