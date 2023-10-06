import pygame
from pygame.locals import *
import random

pygame.init()

# Criando a tela do jogo ------------------------------------------
largura = 480
altura = 480
tamanho_tela = (largura, altura)
tela = pygame.display.set_mode(tamanho_tela)
pygame.display.set_caption('Snake')

# Variaveis da grade ----------------------------------------------
tamanho_grade = 20
quantidade_linhas = altura // tamanho_grade
quantidade_colunas = largura // tamanho_grade

# Direções ---------------------------------------------------------
cima = (0, -1)
baixo = (0, 1)
esquerda = (-1, 0)
direita = (1, 0)

# Cores ------------------------------------------------------------
preto = (0, 0, 0)
azul = (25, 103, 181)
verde_claro = (67, 160, 71)
verde_escuro = (129, 199, 132)
vermelho = (200, 0, 0)

# Variaveis do Jogo -------------------------------------------------
pontos = 0
fim_de_jogo = False

# Relogio do jogo ---------------------------------------------------
relogio = pygame.time.Clock()
fps = 10

# Classe Comida ------------------------------------------------------
class Comida:
    def __init__(self):
        self.posicao_aleatoria()
    
    def posicao_aleatoria(self):
        aleatorio_x = random.randint(0, quantidade_colunas - 1) * tamanho_grade
        aleatorio_y = random.randint(0, quantidade_linhas - 1) * tamanho_grade
        self.location = (aleatorio_x, aleatorio_y)
    
    def desenha(self):
        quadrado = pygame.Rect(self.location, (tamanho_grade, tamanho_grade))
        pygame.draw.rect(tela, vermelho, quadrado)
    
# Classe Cobra -------------------------------------------------------
class Cobra:
    def __init__(self):
        self.corpo = [(largura / 2, altura / 2)]
        self.direcao = direita
        self.cabeca = self.body[0]
        
    
    def virar(self, direcao):
        pass
    
    def andar(self):
        pass
    
    def checa_colisao(self):
        pass
    
    def desenha(self):
        pass

# Criando a comida ---------------------------------------------------
comida = Comida()


# Loop do Jogo -------------------------------------------------------
rodando = True
while rodando:
    relogio.tick(fps)
    
    # Checa os eventos -----------------------------------------------
    for evento in pygame.event.get():
        if evento.type == QUIT:
            rodando = False
            
    # Desenha o fundo ------------------------------------------------
    for x in range(quantidade_colunas):
        for y in range(quantidade_linhas):
            # Criando um quadrado na grade ---------------------------
            quadrado = pygame.Rect((x * tamanho_grade, y * tamanho_grade), (tamanho_grade, tamanho_grade))
            
            # Alternando a cor entre os quadrados --------------------
            if (x + y) % 2 == 0:
                pygame.draw.rect(tela, verde_escuro, quadrado)
            else:
                pygame.draw.rect(tela, verde_claro, quadrado)
    
    # Desenhando a comida ---------------------------------------------
    comida.desenha()
    
    pygame.display.update()
    
pygame.quit()