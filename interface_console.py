from modelos import Interface

class InterfaceConsole(Interface):
    def exibir_estado_jogo(self, jogo):
        print("\n" + "=" * 50)
        print(f"Sua mão: {jogo.jogador_humano.mostrar_mao()}")
        print(f"Cartas da Máquina: {len(jogo.jogador_maquina.mao)}")
        print(f"Carta descartada: {jogo.carta_descartada}")
        print(f"Cartas no baralho: {len(jogo.baralho)}")
        print("=" * 50 + "\n")

    def obter_jogada_humano(self, jogador, carta_descartada):
        while True:
            print(f"\nSua mão atual: {jogador.mostrar_mao()}")
            try:
                escolha = int(input("Digite 0 para pegar a carta descartada ou 1 para puxar do baralho: "))
                if escolha in [0, 1]:
                    pegar_descartada = (escolha == 0)
                    if pegar_descartada and not carta_descartada:
                        print("Não há carta descartada para pegar. Você irá puxar do baralho.")
                        pegar_descartada = False

                    if pegar_descartada:
                        return carta_descartada, None
                    else:
                        nova_carta = None
                        if len(jogador.mao) < 10:
                            nova_carta = "Nova carta"  # Placeholder para a nova carta
                            jogador.mao.append(nova_carta)

                        print(f"\nSua mão atual: {', '.join(str(c) for c in jogador.mao)} (Total: {len(jogador.mao)} cartas)")
                        for i, carta in enumerate(jogador.mao, 1):
                            print(f"{i}: {carta}")

                        indice = int(input("Escolha uma carta para descartar (1-10): ")) - 1
                        if 0 <= indice < len(jogador.mao):
                            carta_descartada = jogador.jogar_carta(indice)
                            if carta_descartada == nova_carta:
                                carta_descartada = None  # Descartou a carta que acabou de puxar
                            return None, carta_descartada
                        else:
                            print("Índice inválido. Tente novamente.")
                else:
                    print("Escolha inválida. Digite 0 ou 1.")
            except ValueError:
                print("Entrada inválida. Por favor, digite um número.")

    def exibir_mensagem(self, mensagem):
        print(mensagem)