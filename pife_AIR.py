from modelos import Carta, Baralho, Jogador, JogadorHumano, JogadorMaquina

class Jogo:
    def __init__(self, interface):
        self.interface = interface
        self.baralho = Baralho()
        self.jogador_humano = JogadorHumano("Humano")
        self.jogador_humano.interface = interface
        self.jogador_maquina = JogadorMaquina("Máquina")
        self.carta_descartada = None

    def iniciar_jogo(self):
        for _ in range(9):
            self.jogador_humano.receber_carta(self.baralho.puxar_carta())
            self.jogador_maquina.receber_carta(self.baralho.puxar_carta())
        self.jogador_humano.ordenar_mao()
        self.jogador_maquina.ordenar_mao()

    def jogada(self, jogador):
        self.interface.exibir_mensagem(f"\nVez do jogador {jogador.nome}...")
        carta_pegar, carta_descartar = jogador.fazer_jogada(self.carta_descartada)

        if carta_pegar:
            jogador.receber_carta(self.carta_descartada)
            self.carta_descartada = None
            self.interface.exibir_mensagem(f"{jogador.nome} pegou a carta descartada.")
        elif isinstance(jogador, JogadorHumano):
            nova_carta = self.baralho.puxar_carta()
            if nova_carta:
                jogador.receber_carta(nova_carta)
                self.interface.exibir_mensagem(f"{jogador.nome} puxou uma nova carta do baralho: {nova_carta}")
        else:
            nova_carta = self.baralho.puxar_carta()
            if nova_carta:
                jogador.receber_carta(nova_carta)
                self.interface.exibir_mensagem(f"{jogador.nome} puxou uma nova carta do baralho.")

        if carta_descartar:
            self.carta_descartada = carta_descartar
            self.interface.exibir_mensagem(f"{jogador.nome} descartou: {carta_descartar}")
        elif len(jogador.mao) > 9:
            self.carta_descartada = jogador.jogar_carta(-1)
            self.interface.exibir_mensagem(f"{jogador.nome} descartou carta extra: {self.carta_descartada}")

        jogador.ordenar_mao()

    def verificar_fim_jogo(self):
        if len(self.baralho) == 0:
            return "empate"
        if self.jogador_humano.verificar_vitoria():
            return "humano"
        if self.jogador_maquina.verificar_vitoria():
            return "maquina"
        return None

    def executar(self):
        self.iniciar_jogo()
        self.interface.executar()
        rodada = 1
        while True:
            self.interface.exibir_mensagem(f"\n--- Rodada {rodada} ---")
            self.interface.exibir_estado_jogo(self)

            # Jogada do humano
            self.jogada(self.jogador_humano)

            # Verificar fim de jogo após jogada do humano
            resultado = self.verificar_fim_jogo()
            if resultado:
                self.finalizar_jogo(resultado)
                break

            # Jogada da máquina
            self.jogada(self.jogador_maquina)

            # Verificar fim de jogo após jogada da máquina
            resultado = self.verificar_fim_jogo()
            if resultado:
                self.finalizar_jogo(resultado)
                break

            rodada += 1
            input("Pressione Enter para continuar para a próxima rodada...")

    def finalizar_jogo(self, resultado):
        self.interface.exibir_estado_jogo(self)
        if resultado == "empate":
            self.interface.exibir_mensagem("O baralho acabou! O jogo terminou em empate.")
        elif resultado == "humano":
            self.interface.exibir_mensagem("Parabéns! Você venceu!")
        else:
            self.interface.exibir_mensagem("A máquina venceu. Tente novamente!")

def main():
    from interface_grafica import InterfaceGrafica
    interface = InterfaceGrafica()
    jogo = Jogo(interface)
    interface.jogo = jogo
    jogo.executar()

if __name__ == "__main__":
    main()
    