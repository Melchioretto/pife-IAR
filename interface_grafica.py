import pygame
import sys
from typing import List, Tuple
from modelos import Carta, Baralho, Jogador, JogadorHumano, JogadorMaquina

pygame.init()

# Configurações da tela
LARGURA, ALTURA = 800, 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo de Pife")

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERDE = (0, 128, 0)
VERMELHO = (255, 0, 0)
AZUL = (0, 0, 255)

# Fontes
FONTE_PEQUENA = pygame.font.Font(None, 24)
FONTE_MEDIA = pygame.font.Font(None, 36)
FONTE_GRANDE = pygame.font.Font(None, 48)

class InterfaceGrafica:
    def __init__(self):
        self.jogo = None
        self.carta_selecionada = None
        self.carta_puxada = None
        self.botao_puxar = None
        self.botao_descartar = None
        self.animacoes = []
        self.mensagens = []

    def desenhar_carta(self, carta: Carta, x: int, y: int, selecionada: bool = False):
        largura, altura = 70, 100
        cor = AZUL if selecionada else BRANCO
        pygame.draw.rect(TELA, cor, (x, y, largura, altura))
        pygame.draw.rect(TELA, PRETO, (x, y, largura, altura), 2)
        
        cor_naipe = VERMELHO if carta.naipe in ["♥", "♦"] else PRETO
        
        valor = FONTE_MEDIA.render(carta.valor, True, cor_naipe)
        naipe = FONTE_GRANDE.render(carta.naipe, True, cor_naipe)
        
        TELA.blit(valor, (x + 5, y + 5))
        TELA.blit(naipe, (x + largura//2 - naipe.get_width()//2, y + altura//2 - naipe.get_height()//2))

    def desenhar_mao(self, jogador: Jogador, y: int):
        for i, carta in enumerate(jogador.mao):
            self.desenhar_carta(carta, 50 + i * 80, y, self.carta_selecionada == i)

    def desenhar_botao(self, texto: str, x: int, y: int, largura: int, altura: int) -> pygame.Rect:
        botao = pygame.Rect(x, y, largura, altura)
        pygame.draw.rect(TELA, BRANCO, botao)
        pygame.draw.rect(TELA, PRETO, botao, 2)
        texto_surf = FONTE_MEDIA.render(texto, True, PRETO)
        texto_rect = texto_surf.get_rect(center=botao.center)
        TELA.blit(texto_surf, texto_rect)
        return botao

    def desenhar_tela(self):
        TELA.fill(VERDE)
        self.desenhar_mao(self.jogo.jogador_humano, 450)
        texto_maquina = FONTE_MEDIA.render(f"Cartas da Máquina: {len(self.jogo.jogador_maquina.mao)}", True, BRANCO)
        TELA.blit(texto_maquina, (50, 50))
        
        if self.jogo.carta_descartada:
            self.desenhar_carta(self.jogo.carta_descartada, 365, 250)
            texto_descarte = FONTE_PEQUENA.render("Carta descartada", True, BRANCO)
            TELA.blit(texto_descarte, (350, 220))
        
        texto_baralho = FONTE_MEDIA.render(f"Baralho: {len(self.jogo.baralho)}", True, BRANCO)
        TELA.blit(texto_baralho, (600, 250))
        
        self.botao_puxar = self.desenhar_botao("Puxar do Baralho", 550, 300, 200, 50)
        self.botao_descartar = self.desenhar_botao("Descartar", 550, 360, 200, 50)
        
        # Desenhar mensagens no canto superior
        for i, mensagem in enumerate(self.mensagens[-3:]):
            texto = FONTE_PEQUENA.render(mensagem, True, BRANCO)
            TELA.blit(texto, (10, 10 + i * 30))
        
        # Desenhar animações
        for animacao in self.animacoes:
            animacao.desenhar(TELA)
        
        pygame.display.flip()

    def adicionar_mensagem(self, mensagem: str):
        self.mensagens.append(mensagem)
        if len(self.mensagens) > 5:
            self.mensagens.pop(0)

    def animar_carta(self, carta: Carta, origem: Tuple[int, int], destino: Tuple[int, int], duracao: int):
        animacao = AnimacaoCarta(carta, origem, destino, duracao)
        self.animacoes.append(animacao)

    def atualizar_animacoes(self):
        for animacao in self.animacoes[:]:
            animacao.atualizar()
            if animacao.concluida:
                self.animacoes.remove(animacao)

    def obter_jogada_humano(self, jogador: JogadorHumano, carta_descartada: Carta) -> Tuple[Carta, Carta]:
        self.carta_puxada = None
        self.carta_selecionada = None
        aguardando_escolha = True
        
        while aguardando_escolha:
            self.atualizar_animacoes()
            self.desenhar_tela()
            
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if 50 <= x <= 770 and 450 <= y <= 550:
                        self.carta_selecionada = (x - 50) // 80
                    elif self.botao_puxar.collidepoint(x, y) and not self.carta_puxada:
                        self.carta_puxada = self.jogo.baralho.puxar_carta()
                        if self.carta_puxada:
                            jogador.receber_carta(self.carta_puxada)
                            self.animar_carta(self.carta_puxada, (600, 250), (50 + len(jogador.mao) * 80, 450), 30)
                            self.adicionar_mensagem(f"Você puxou: {self.carta_puxada}")
                            return None, self.carta_puxada
                    elif self.botao_descartar.collidepoint(x, y) and self.carta_selecionada is not None:
                        carta_descartada = jogador.jogar_carta(self.carta_selecionada)
                        self.animar_carta(carta_descartada, (50 + self.carta_selecionada * 80, 450), (365, 250), 30)
                        self.adicionar_mensagem(f"Você descartou: {carta_descartada}")
                        self.carta_selecionada = None
                        return None, carta_descartada
                    elif 365 <= x <= 435 and 250 <= y <= 350 and carta_descartada and not self.carta_puxada:
                        jogador.receber_carta(carta_descartada)
                        self.animar_carta(carta_descartada, (365, 250), (50 + len(jogador.mao) * 80, 450), 30)
                        self.adicionar_mensagem(f"Você pegou a carta descartada: {carta_descartada}")
                        return carta_descartada, None
            
            pygame.time.wait(10)  # Pequena pausa para evitar uso excessivo da CPU

        return None, None

    def exibir_mensagem(self, mensagem: str):
        self.adicionar_mensagem(mensagem)
        self.desenhar_tela()
        pygame.time.wait(1000)

    def executar(self):
        self.jogo.iniciar_jogo()
        rodada = 1
        while True:
            self.exibir_mensagem(f"Rodada {rodada}")
            self.desenhar_tela()

            # Jogada do humano
            self.jogo.jogada(self.jogo.jogador_humano)

            # Verificar fim de jogo após jogada do humano
            resultado = self.jogo.verificar_fim_jogo()
            if resultado:
                self.finalizar_jogo(resultado)
                break

            # Jogada da máquina
            self.jogo.jogada(self.jogo.jogador_maquina)

            # Verificar fim de jogo após jogada da máquina
            resultado = self.jogo.verificar_fim_jogo()
            if resultado:
                self.finalizar_jogo(resultado)
                break

            rodada += 1

    def finalizar_jogo(self, resultado: str):
        self.desenhar_tela()
        if resultado == "empate":
            mensagem = "O jogo terminou em empate!"
        elif resultado == "humano":
            mensagem = "Parabéns! Você venceu!"
        else:
            mensagem = "A máquina venceu. Tente novamente!"
        self.exibir_mensagem(mensagem)
        pygame.time.wait(5000)
        pygame.quit()
        sys.exit()

class AnimacaoCarta:
    def __init__(self, carta: Carta, origem: Tuple[int, int], destino: Tuple[int, int], duracao: int):
        self.carta = carta
        self.origem = origem
        self.destino = destino
        self.duracao = duracao
        self.progresso = 0
        self.concluida = False

    def atualizar(self):
        self.progresso += 1
        if self.progresso >= self.duracao:
            self.concluida = True

    def desenhar(self, tela):
        t = self.progresso / self.duracao
        x = int(self.origem[0] + (self.destino[0] - self.origem[0]) * t)
        y = int(self.origem[1] + (self.destino[1] - self.origem[1]) * t)
        InterfaceGrafica.desenhar_carta(None, self.carta, x, y)