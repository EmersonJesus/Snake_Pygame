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
branco = (255, 255, 255)

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
        self.localizacao = (aleatorio_x, aleatorio_y)
    
    def desenha(self):
        quadrado = pygame.Rect(self.localizacao, (tamanho_grade, tamanho_grade))
        pygame.draw.rect(tela, vermelho, quadrado)
    
# Classe Cobra -------------------------------------------------------
class Cobra:
    def __init__(self):
        self.corpo = [(largura / 2, altura / 2)]
        self.direcao = direita
        self.cabeca = self.corpo[0]
        
    
    def virar(self, direcao):
        # Faz a cobra virar ----------------------------------
        if len(self.corpo) == 1:
            self.direcao = direcao
        else:
            # Impede a cobra de virar na direção contraria
            if direcao == esquerda or direcao == direita:
                if self.corpo[0][1] != self.corpo[1][1]:
                    self.direcao = direcao
            
            # Impede a cobra de virar na direção contraria
            if direcao == cima or direcao == baixo:
                if self.corpo[0][0] != self.corpo[1][0]:
                    self.direcao = direcao
    
    def andar(self):
        # Determina o movimento
        x, y = self.direcao
        proximo_x = (self.cabeca[0] + x * tamanho_grade)
        proximo_y = (self.cabeca[1] + y * tamanho_grade)
        
        # Passa a parede -----------------------------------------------
        proximo_x = proximo_x % largura
        proximo_y = proximo_y % altura
        proxima_localizacao = (proximo_x, proximo_y)
        
        # Adiciona nova cabeça no inicio da lista -----------------------
        self.corpo.insert(0, proxima_localizacao)
        self.cabeca = self.corpo[0]
        
        # Checa se a comida está na mesma posição da cabeça -------------
        if comida.localizacao == self.cabeca:
            # Move a comida para outra localização ----------------------
            comida.posicao_aleatoria()
            # Faz com que a proxima localização não seja onde a cobra está
            while comida.localizacao in self.corpo:
                comida.posicao_aleatoria()   
        else:
            # Remove a ultima parte do corpo da lista --------------------
            self.corpo.pop()
    
    def checa_colisao(self):
        # Checa se a cobra bateu no proprio corpo ------------------------
        if self.cabeca in self.corpo[1:]:
            return True
        else:
            return False
    
    def desenha(self):
        for parte_corpo in self.corpo:
            quadrado = pygame.Rect(parte_corpo, (tamanho_grade, tamanho_grade))
            pygame.draw.rect(tela, azul, quadrado)
            pygame.draw.rect(tela, branco, quadrado, 1)

# Criando a comida ---------------------------------------------------
comida = Comida()
# Criando a Cobra ----------------------------------------------------
cobra = Cobra()


# Loop do Jogo -------------------------------------------------------
rodando = True
while rodando:
    relogio.tick(fps)
    pontos = len(cobra.corpo) - 1
    # Checa os eventos -----------------------------------------------
    for evento in pygame.event.get():
        if evento.type == QUIT:
            rodando = False
        elif evento.type == KEYDOWN:
            # Vira a cobra com as teclas -----------------------------
            if evento.key == K_UP:
                cobra.virar(cima)
            elif evento.key == K_DOWN:
                cobra.virar(baixo)
            elif evento.key == K_RIGHT:
                cobra.virar(direita)
            elif evento.key == K_LEFT:
                cobra.virar(esquerda)
            
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
    
    # Move a Cobra ----------------------------------------------------
    cobra.andar()
    # Desenha a Cobra --------------------------------------------------
    cobra.desenha()
    
    # Mostra os pontos -------------------------------------------------
    fonte = pygame.font.Font(pygame.font.get_default_font(), 16)
    texto = fonte.render(f"Pontos: {pontos}", 1, preto)
    tela.blit(texto, (5, 10))
    
    # Checa colisão -----------------------------------------------------
    batida = cobra.checa_colisao()
    if batida:
        fim_de_jogo = True
        
    # Fim de Jogo --------------------------------------------------------
    while fim_de_jogo:
        relogio.tick(fps)
        # Desenha tela de fim de jogo ------------------------------------
        pygame.draw.rect(tela, preto, (0, largura / 2 - 50, altura, 100))
        texto = fonte.render("Fim de Jogo! Aperte ESPAÇO para jogar de novo!", 1, branco)
        texto_rect = texto.get_rect()
        texto_rect.center = (largura / 2, altura / 2)
        tela.blit(texto, texto_rect)
        pygame.display.update()
        
        # Checa se o jogador apertou o espaço ------------------------------
        for evento in pygame.event.get():
            if evento.type == QUIT:
                fim_de_jogo = False
                rodando = False
            elif evento.type == KEYDOWN and evento.key == K_SPACE:
                # Reseta o jogo ----------------------------------------------
                fim_de_jogo = False
                pontos = 0
                cobra.corpo = [(largura / 2, altura / 2)]
                cobra.direcao = direita
                cobra.cabeca = cobra.corpo[0]
                comida.posicao_aleatoria()
                
                    
    
    pygame.display.update()
    
pygame.quit()