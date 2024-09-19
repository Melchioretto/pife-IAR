import random
from typing import List, Tuple

# Tipos personalizados
Peca = Tuple[int, int]
Cobra = List[Peca]

def criar_pecas() -> List[Peca]:
    return [(i, j) for i in range(7) for j in range(i, 7)]

def distribuir_pecas(pecas: List[Peca]) -> Tuple[List[Peca], List[Peca], List[Peca]]:
    random.shuffle(pecas)
    return pecas[:14], pecas[14:21], pecas[21:]

def encontrar_cobra_inicial(pecas_computador: List[Peca], pecas_jogador: List[Peca]) -> Peca:
    todas_pecas = pecas_computador + pecas_jogador
    peca_inicial = max((peca for peca in todas_pecas if peca[0] == peca[1]), key=lambda x: x[0], default=None)
    if peca_inicial is None:
        peca_inicial = max(todas_pecas, key=lambda x: x[0] + x[1])
    
    if peca_inicial in pecas_computador:
        pecas_computador.remove(peca_inicial)
    else:
        pecas_jogador.remove(peca_inicial)
    return peca_inicial

def pode_conectar(peca: Peca, cobra: Cobra) -> bool:
    return peca[0] in (cobra[0][0], cobra[-1][1]) or peca[1] in (cobra[0][0], cobra[-1][1])

def conectar_peca(peca: Peca, cobra: Cobra) -> None:
    if peca[1] == cobra[0][0]:
        cobra.insert(0, peca)
    elif peca[0] == cobra[-1][1]:
        cobra.append(peca)
    elif peca[0] == cobra[0][0]:
        cobra.insert(0, peca[::-1])
    else:
        cobra.append(peca[::-1])

def realizar_jogada(jogador: str, pecas: List[Peca], cobra: Cobra, estoque: List[Peca]) -> bool:
    if jogador == "computador":
        for peca in pecas:
            if pode_conectar(peca, cobra):
                conectar_peca(peca, cobra)
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
                if pode_conectar(peca, cobra):
                    conectar_peca(peca, cobra)
                    pecas.pop(indice)
                    return True
                else:
                    print("Essa peça não pode ser conectada. Tente novamente.")
            except (ValueError, IndexError):
                print("Entrada inválida. Tente novamente.")

def verificar_vitoria(cobra: Cobra) -> bool:
    return cobra[0][0] == cobra[-1][1] and sum(peca.count(cobra[0][0]) for peca in cobra) == 8

def exibir_estado_jogo(estoque: List[Peca], pecas_computador: List[Peca], cobra: Cobra):
    print('=' * 70)
    print(f'Tamanho do estoque: {len(estoque)}')
    print(f'Peças do computador: {len(pecas_computador)}\n')
    print(' '.join(str(peca) for peca in cobra) + '\n')

def jogar_domino():
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
        if not estoque and not any(pode_conectar(p, cobra) for p in pecas_jogador + pecas_computador):
            print("Empate! Ninguém pode jogar.")
            break

        if vez_jogador:
            print("\nSua vez de jogar.")
            realizar_jogada("jogador", pecas_jogador, cobra, estoque)
        else:
            print("\nVez do computador. Pressione Enter para continuar...")
            input()
            realizar_jogada("computador", pecas_computador, cobra, estoque)

        vez_jogador = not vez_jogador

if __name__ == "__main__":
    jogar_domino()
    
    
# ======================================================================
# Tamanho do estoque: 14
# Peças do computador: 6

# (6, 6)


# Sua vez de jogar.

# Suas peças:
# 1: (3, 6)
# 2: (3, 5)
# 3: (0, 3)
# 4: (0, 6)
# 5: (0, 5)
# 6: (4, 5)
# 7: (0, 1)
# Escolha uma peça (número) ou 0 para comprar do estoque: 4
# ======================================================================
# Tamanho do estoque: 14
# Peças do computador: 6

# (0, 6) (6, 6)


# Vez do computador. Pressione Enter para continuar...

# ======================================================================
# Tamanho do estoque: 14
# Peças do computador: 5

# (0, 6) (6, 6) (6, 4)


# Sua vez de jogar.

# Suas peças:
# 1: (3, 6)
# 2: (3, 5)
# 3: (0, 3)
# 4: (0, 5)
# 5: (4, 5)
# 6: (0, 1)
# Escolha uma peça (número) ou 0 para comprar do estoque: 3
# ======================================================================
# Tamanho do estoque: 14
# Peças do computador: 5

# (3, 0) (0, 6) (6, 6) (6, 4)


# Vez do computador. Pressione Enter para continuar...

# ======================================================================
# Tamanho do estoque: 14
# Peças do computador: 4

# (3, 0) (0, 6) (6, 6) (6, 4) (4, 0)


# Sua vez de jogar.

# Suas peças:
# 1: (3, 6)
# 2: (3, 5)
# 3: (0, 5)
# 4: (4, 5)
# 5: (0, 1)
# Escolha uma peça (número) ou 0 para comprar do estoque: 2
# ======================================================================
# Tamanho do estoque: 14
# Peças do computador: 4

# (5, 3) (3, 0) (0, 6) (6, 6) (6, 4) (4, 0)


# Vez do computador. Pressione Enter para continuar...

# ======================================================================
# Tamanho do estoque: 14
# Peças do computador: 3

# (6, 5) (5, 3) (3, 0) (0, 6) (6, 6) (6, 4) (4, 0)


# Sua vez de jogar.

# Suas peças:
# 1: (3, 6)
# 2: (0, 5)
# 3: (4, 5)
# 4: (0, 1)
# Escolha uma peça (número) ou 0 para comprar do estoque: 2
# ======================================================================
# Tamanho do estoque: 14
# Peças do computador: 3

# (6, 5) (5, 3) (3, 0) (0, 6) (6, 6) (6, 4) (4, 0) (0, 5)


# Vez do computador. Pressione Enter para continuar...

# ======================================================================
# Tamanho do estoque: 13
# Peças do computador: 4

# (6, 5) (5, 3) (3, 0) (0, 6) (6, 6) (6, 4) (4, 0) (0, 5)


# Sua vez de jogar.

# Suas peças:
# 1: (3, 6)
# 2: (4, 5)
# 3: (0, 1)
# Escolha uma peça (número) ou 0 para comprar do estoque: 1
# ======================================================================
# Tamanho do estoque: 13
# Peças do computador: 4

# (3, 6) (6, 5) (5, 3) (3, 0) (0, 6) (6, 6) (6, 4) (4, 0) (0, 5)


# Vez do computador. Pressione Enter para continuar...

# ======================================================================
# Tamanho do estoque: 12
# Peças do computador: 5

# (3, 6) (6, 5) (5, 3) (3, 0) (0, 6) (6, 6) (6, 4) (4, 0) (0, 5)


# Sua vez de jogar.

# Suas peças:
# 1: (4, 5)
# 2: (0, 1)
# Escolha uma peça (número) ou 0 para comprar do estoque: 1
# ======================================================================
# Tamanho do estoque: 12
# Peças do computador: 5

# (3, 6) (6, 5) (5, 3) (3, 0) (0, 6) (6, 6) (6, 4) (4, 0) (0, 5) (5, 4)


# Vez do computador. Pressione Enter para continuar...

# ======================================================================
# Tamanho do estoque: 12
# Peças do computador: 4

# (3, 6) (6, 5) (5, 3) (3, 0) (0, 6) (6, 6) (6, 4) (4, 0) (0, 5) (5, 4) (4, 1)


# Sua vez de jogar.

# Suas peças:
# 1: (0, 1)
# Escolha uma peça (número) ou 0 para comprar do estoque: 1
# ======================================================================
# Tamanho do estoque: 12
# Peças do computador: 4

# (3, 6) (6, 5) (5, 3) (3, 0) (0, 6) (6, 6) (6, 4) (4, 0) (0, 5) (5, 4) (4, 1) (1, 0)

# Você venceu!