import random
from typing import List, Tuple

# Tipos personalizados
Peca = Tuple[int, int]
Cobra = List[Peca]

def criar_pecas() -> List[Peca]:
    """
    Cria todas as peças possíveis do jogo de dominó.
    :return: Lista de todas as peças de dominó.
    """
    return [(i, j) for i in range(7) for j in range(i, 7)]

def distribuir_pecas(pecas: List[Peca]) -> Tuple[List[Peca], List[Peca], List[Peca]]:
    """
    Distribui as peças entre o jogador, o computador e o estoque.
    :param pecas: Lista de todas as peças do jogo.
    :return: Tupla contendo as peças do jogador, do computador e do estoque.
    """
    random.shuffle(pecas)
    return pecas[:14], pecas[14:21], pecas[21:]

def encontrar_cobra_inicial(pecas_computador: List[Peca], pecas_jogador: List[Peca]) -> Peca:
    """
    Encontra a peça inicial para começar o jogo.
    :param pecas_computador: Peças do computador.
    :param pecas_jogador: Peças do jogador.
    :return: A peça inicial do jogo.
    """
    todas_pecas = pecas_computador + pecas_jogador
    peca_inicial = max((peca for peca in todas_pecas if peca[0] == peca[1]), key=lambda x: x[0], default=None)
    if peca_inicial is None:
        peca_inicial = max(todas_pecas, key=lambda x: x[0] + x[1])

    if peca_inicial in pecas_computador:
        pecas_computador.remove(peca_inicial)
    else:
        pecas_jogador.remove(peca_inicial)
    return peca_inicial

def pode_conectar(peca: Peca, cobra: Cobra, posicao: str) -> bool:
    """
    Verifica se uma peça pode ser conectada à cobra na posição especificada.
    :param peca: A peça a ser verificada.
    :param cobra: A cobra atual do jogo.
    :param posicao: A posição onde a peça seria conectada ('inicio' ou 'fim').
    :return: True se a peça pode ser conectada, False caso contrário.
    """
    if posicao == 'inicio':
        return peca[0] == cobra[0][0] or peca[1] == cobra[0][0]
    else:  # fim
        return peca[0] == cobra[-1][1] or peca[1] == cobra[-1][1]

def conectar_peca(peca: Peca, cobra: Cobra, posicao: str) -> None:
    """
    Conecta uma peça à cobra na posição especificada.
    :param peca: A peça a ser conectada.
    :param cobra: A cobra atual do jogo.
    :param posicao: A posição onde a peça será conectada ('inicio' ou 'fim').
    """
    if posicao == 'inicio':
        if peca[1] == cobra[0][0]:
            cobra.insert(0, peca)
        else:
            cobra.insert(0, peca[::-1])
    else:  # fim
        if peca[0] == cobra[-1][1]:
            cobra.append(peca)
        else:
            cobra.append(peca[::-1])

def calcular_pontos(pecas: List[Peca]) -> int:
    """
    Calcula a pontuação total de um conjunto de peças.
    :param pecas: Lista de peças.
    :return: A soma dos pontos de todas as peças.
    """
    return sum(sum(peca) for peca in pecas)

def estrategia_computador(pecas: List[Peca], cobra: Cobra, dificuldade: str) -> Tuple[Peca, str]:
    """
    Determina a jogada do computador com base na dificuldade escolhida.
    :param pecas: Peças do computador.
    :param cobra: A cobra atual do jogo.
    :param dificuldade: Nível de dificuldade do jogo.
    :return: A peça escolhida e a posição onde será jogada, ou (None, '') se não houver jogada possível.
    """
    pecas_validas = [(peca, 'inicio') for peca in pecas if pode_conectar(peca, cobra, 'inicio')] + \
                    [(peca, 'fim') for peca in pecas if pode_conectar(peca, cobra, 'fim')]
    
    if not pecas_validas:
        return None, ''

    if dificuldade == "fácil":
        return random.choice(pecas_validas)
    elif dificuldade == "médio":
        return max(pecas_validas, key=lambda p: p[0][0] + p[0][1])
    else:  # difícil
        contagem = {i: sum(p.count(i) for p in cobra + pecas) for i in range(7)}
        return max(pecas_validas, key=lambda p: contagem[p[0][0]] + contagem[p[0][1]])

def realizar_jogada(jogador: str, pecas: List[Peca], cobra: Cobra, estoque: List[Peca], dificuldade: str) -> bool:
    """
    Realiza uma jogada para o jogador especificado.
    :param jogador: 'computador' ou 'jogador'.
    :param pecas: Peças do jogador atual.
    :param cobra: A cobra atual do jogo.
    :param estoque: O estoque de peças.
    :param dificuldade: Nível de dificuldade do jogo (usado para o computador).
    :return: True se uma jogada foi realizada, False se comprou do estoque ou não pôde jogar.
    """
    if jogador == "computador":
        peca, posicao = estrategia_computador(pecas, cobra, dificuldade)
        if peca:
            conectar_peca(peca, cobra, posicao)
            pecas.remove(peca)
            return True
        if estoque:
            pecas.append(estoque.pop())
        return False
    else:
        while True:
            print("\nSuas peças:")
            for i, peca in enumerate(pecas, 1):
                print(f"{i}: {peca}")
            entrada = input("Escolha uma peça (número) ou 0 para comprar do estoque: ")
            if entrada == "0":
                if estoque:
                    pecas.append(estoque.pop())
                return False
            try:
                indice = int(entrada) - 1
                peca = pecas[indice]
                if pode_conectar(peca, cobra, 'inicio') or pode_conectar(peca, cobra, 'fim'):
                    while True:
                        posicao = input("Escolha a posição (i para início, f para fim): ").lower()
                        if posicao in ['i', 'f']:
                            posicao_completa = 'inicio' if posicao == 'i' else 'fim'
                            if pode_conectar(peca, cobra, posicao_completa):
                                conectar_peca(peca, cobra, posicao_completa)
                                pecas.pop(indice)
                                return True
                            else:
                                print("Essa jogada não é permitida. Escolha outra posição ou outra peça.")
                                break
                        else:
                            print("Posição inválida. Digite 'i' para início ou 'f' para fim.")
                else:
                    print("Essa peça não pode ser conectada. Tente novamente.")
            except (ValueError, IndexError):
                print("Entrada inválida. Tente novamente.")

def verificar_vitoria(cobra: Cobra) -> bool:
    """
    Verifica se o jogo terminou em vitória.
    :param cobra: A cobra atual do jogo.
    :return: True se o jogo terminou em vitória, False caso contrário.
    """
    return cobra[0][0] == cobra[-1][1] and sum(peca.count(cobra[0][0]) for peca in cobra) == 8

def exibir_estado_jogo(estoque: List[Peca], pecas_computador: List[Peca], cobra: Cobra):
    """
    Exibe o estado atual do jogo.
    :param estoque: O estoque de peças.
    :param pecas_computador: Peças do computador.
    :param cobra: A cobra atual do jogo.
    """
    print('=' * 70)
    print(f'Tamanho do estoque: {len(estoque)}')
    print(f'Peças do computador: {len(pecas_computador)}\n')
    print(' '.join(str(peca) for peca in cobra) + '\n')

def escolher_dificuldade() -> str:
    """
    Permite ao jogador escolher o nível de dificuldade do jogo.
    :return: O nível de dificuldade escolhido.
    """
    while True:
        escolha = input("Escolha a dificuldade (1 para fácil, 2 para médio, 3 para difícil): ")
        if escolha in ['1', '2', '3']:
            return ['fácil', 'médio', 'difícil'][int(escolha) - 1]
        print("Escolha inválida. Por favor, digite 1, 2 ou 3.")

def jogar_novamente() -> bool:
    """
    Pergunta ao jogador se deseja jogar novamente.
    :return: True se o jogador quiser jogar novamente, False caso contrário.
    """
    while True:
        escolha = input("Deseja jogar novamente? (s/n): ").lower()
        if escolha in ['s', 'n']:
            return escolha == 's'
        print("Escolha inválida. Por favor, digite 's' para sim ou 'n' para não.")

def jogar_domino():
    """
    Função principal que controla o fluxo do jogo de dominó.
    """
    while True:
        dificuldade = escolher_dificuldade()
        pecas = criar_pecas()
        estoque, pecas_computador, pecas_jogador = distribuir_pecas(pecas)
        cobra = [encontrar_cobra_inicial(pecas_computador, pecas_jogador)]
        vez_jogador = len(pecas_jogador) > len(pecas_computador)

        while True:
            exibir_estado_jogo(estoque, pecas_computador, cobra)

            if not pecas_jogador:
                print("Você venceu!")
                break
            if not pecas_computador:
                print("O computador venceu!")
                break
            if verificar_vitoria(cobra):
                print("O jogador venceu!" if vez_jogador else "O computador venceu!")
                break
            if not estoque and not any(pode_conectar(p, cobra, 'inicio') or pode_conectar(p, cobra, 'fim') for p in pecas_jogador + pecas_computador):
                print("Empate! Ninguém pode jogar.")
                break

            if vez_jogador:
                print("\nSua vez de jogar.")
                realizar_jogada("jogador", pecas_jogador, cobra, estoque, dificuldade)
            else:
                print("\nVez do computador. Pressione Enter para continuar...")
                input()
                realizar_jogada("computador", pecas_computador, cobra, estoque, dificuldade)

            vez_jogador = not vez_jogador

        if not jogar_novamente():
            print("Obrigado por jogar! Até a próxima!")
            break

if __name__ == "__main__":
    jogar_domino()

