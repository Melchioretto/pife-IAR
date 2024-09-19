from random import shuffle
from itertools import combinations_with_replacement

# Função para realizar a jogada
def realizar_jogada(entrada_jogador, pecas_jogador):
    # Caso o jogador escolha 0 e o estoque esteja vazio
    if int(entrada_jogador) == 0 and len(estoque_pecas) == 0:
        return None

    # Caso o jogador escolha 0 e ainda tenha peças no estoque, ele pega uma peça
    elif int(entrada_jogador) == 0 & len(estoque_pecas) > 0:
        pecas_jogador.append(estoque_pecas[-1])  # Adiciona a última peça do estoque às peças do jogador
        estoque_pecas.remove(estoque_pecas[-1])  # Remove essa peça do estoque
        return None

    # Jogada à direita: adicionar a peça ao final da cobra
    if int(entrada_jogador) > 0:
        # Pegar a peça do jogador ou do computador
        peca_final = pecas_jogador[int(entrada_jogador) - 1]
        # Inverter a peça se necessário
        if peca_final[1] == cobra[-1][-1]:
            peca_final.reverse()
        # Colocar a peça no final da cobra
        cobra.append(peca_final)
        # Remover a peça do jogador ou do computador
        pecas_jogador.remove(pecas_jogador[int(entrada_jogador) - 1])

    # Jogada à esquerda: adicionar a peça ao início da cobra
    else:
        # Pegar a peça do jogador ou do computador
        peca_inicial = pecas_jogador[-int(entrada_jogador) - 1]
        # Inverter a peça se necessário
        if peca_inicial[0] == cobra[0][0]:
            peca_inicial.reverse()
        # Colocar a peça no início da cobra
        cobra.insert(0, peca_inicial)
        # Remover a peça do jogador ou do computador
        pecas_jogador.remove(pecas_jogador[-int(entrada_jogador) - 1])

# Função para verificar se a cobra é vencedora
def verificar_vitoria(cobra_atual):
    if cobra_atual[0][0] == cobra_atual[-1][-1] and sum(x.count(cobra_atual[0][0]) for x in cobra_atual) == 8:
        return True
    return False

# Definir a lista de dominós
dominoes = list(combinations_with_replacement(range(0, 7), 2))

# Converter a lista de tuplas em lista de listas
dominoes = [list(x) for x in dominoes]

# Embaralhar os dominós
shuffle(dominoes)

# Definir o coeficiente igual à metade do número total de dominós
coeficiente = len(dominoes) // 2

# Separar o baralho: estoque, peças do computador e peças do jogador
estoque_pecas = dominoes[:coeficiente]
pecas_computador = dominoes[coeficiente:int(coeficiente * 1.5)]
pecas_jogador = dominoes[int(coeficiente * 1.5):]

# Encontrar a cobra (o maior dominó duplo)
cobra = [max([[x, y] for x, y in pecas_computador + pecas_jogador if x == y])]

# Remover a cobra das peças do computador ou do jogador
pecas_computador.remove(cobra[0]) if cobra[0] in pecas_computador else pecas_jogador.remove(cobra[0])

# Definir as mensagens para o jogador
vez_jogador = "Sua vez de jogar. Digite seu comando."
vez_computador = "O computador vai jogar. Pressione Enter para continuar..."
jogador_venceu = 'O jogo acabou. Você venceu!'
computador_venceu = 'O jogo acabou. O computador venceu!'

# Definir quem joga primeiro
numero_vez = 0 if len(pecas_jogador) > len(pecas_computador) else 1

# Iniciar o jogo
while True:
    # Mostrar o estoque, as peças do jogador e do computador
    print('=' * 70)
    print('Tamanho do estoque:', len(estoque_pecas))
    print('Peças do computador:', len(pecas_computador), '\n')
    print(*cobra, '\n', sep='') if len(cobra) <= 6 else print(*cobra[:3], '...', *cobra[-3:], '\n', sep='')
    print("Suas peças:")
    for num, peca in enumerate(pecas_jogador):
        print(f"{num + 1}: {peca}")

    # Condição de vitória do jogador se não houver mais peças
    if len(pecas_jogador) == 0:
        print("\nStatus:", jogador_venceu)
        break

    # Condição de vitória do computador se não houver mais peças
    if len(pecas_computador) == 0:
        print("\nStatus:", computador_venceu)
        break

    # Condição de vitória do jogador se a cobra for vencedora
    if verificar_vitoria(cobra) and numero_vez == 0:
        print("\nStatus:", jogador_venceu)
        break

    # Condição de vitória do computador se a cobra for vencedora
    if verificar_vitoria(cobra) and numero_vez == 1:
        print("\nStatus:", computador_venceu)
        break

    # Definir as extremidades da cobra
    chaves_conexao = [cobra[0][0], cobra[-1][-1]]

    # Condição de empate
    if len(estoque_pecas) == 0 and any([peca[1] for peca in pecas_jogador + pecas_computador if peca[0] in chaves_conexao]):
        print("\nStatus: O jogo acabou. Empate!")
        break

    # Vez do jogador
    if numero_vez % 2 == 0:
        numero_vez += 1  # Contar o turno do jogador
        print("\nStatus:", vez_jogador)
        entrada_usuario = input()  # Capturar a entrada do jogador

        # Verificar se a entrada do jogador é válida
        if entrada_usuario.lstrip("-").isdigit() and int(entrada_usuario) in range(-len(pecas_jogador), len(pecas_jogador) + 1):
            # Realizar a jogada do jogador
            if int(entrada_usuario) == 0:
                realizar_jogada(entrada_usuario, pecas_jogador)
                continue

            # Definir a peça atual
            peca_atual = pecas_jogador[int(entrada_usuario) - 1] if int(entrada_usuario) > 0 else pecas_jogador[-int(entrada_usuario) - 1]

            # Verificar se a peça é válida
            if chaves_conexao[-1] in peca_atual and int(entrada_usuario) > 0 or chaves_conexao[0] in peca_atual and int(entrada_usuario) < 0:
                realizar_jogada(entrada_usuario, pecas_jogador)
            else:
                print("Jogada inválida. Por favor, tente novamente.")
                numero_vez -= 1
                continue
        else:
            print("Entrada inválida. Por favor, tente novamente.")
            numero_vez -= 1
            continue

    # Vez do computador
    else:
        numero_vez += 1  # Contar o turno do computador
        print("\nStatus:", vez_computador)
        input()  # Aguardar a confirmação do jogador

        # Realizar a jogada do computador
        for peca in pecas_computador:
            # Verificar como conectar a cobra
            if peca[0] == chaves_conexao[-1]:
                realizar_jogada(str(pecas_computador.index(peca) + 1), pecas_computador)
                break
            elif peca[1] == chaves_conexao[0]:
                realizar_jogada(str(-pecas_computador.index(peca) - 1), pecas_computador)
                break
        # Comprar uma peça se não houver jogada válida
        else:
            realizar_jogada('0', pecas_computador)
