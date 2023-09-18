#Configurações iniciais
import pygame
import random
import sys 

pygame.init()
pygame.display.set_caption("Jogo Snake Python")
largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))
relogio = pygame.time.Clock()

#cores RGB
preta = (0, 0, 0)
branca = (255, 255, 255)
vermelha = (255, 0, 0)
verde = (0, 255, 0)

#parametros da cobrinha
tamanho_quadrado = 20
velocidade_jogo = 10

def gerar_comida():
    comida_x = round(random.randrange(0, largura-tamanho_quadrado) / 20.0) * 20.0
    comida_y = round(random.randrange(0, altura-tamanho_quadrado) / 20.0) * 20.0
    return comida_x, comida_y

def desenhar_comida(tamanho, comida_x, comida_y):
    pygame.draw.rect(tela, verde, [comida_x, comida_y, tamanho, tamanho])

def desenhar_cobra(tamanho, pixels):
    for pixel in pixels:
        pygame.draw.rect(tela, branca, [pixel[0], pixel[1], tamanho, tamanho])

def desenhar_pontuacao(pontuacao):
    fonte = pygame.font.SysFont("Helvetica", 35)
    texto = fonte.render(f'Pontos: {pontuacao}', True, vermelha)
    tela.blit(texto, [1,1])

def selecionar_velocidade(tecla, velocidade_x, velocidade_y):
    if tecla == pygame.K_DOWN and velocidade_y != -tamanho_quadrado:
        velocidade_x = 0
        velocidade_y = tamanho_quadrado
    elif tecla == pygame.K_UP and velocidade_y != tamanho_quadrado:
        velocidade_x = 0
        velocidade_y = -tamanho_quadrado
    elif tecla == pygame.K_RIGHT and velocidade_x != -tamanho_quadrado:
        velocidade_x = tamanho_quadrado
        velocidade_y = 0
    elif tecla == pygame.K_LEFT and velocidade_x != tamanho_quadrado:
        velocidade_x = -tamanho_quadrado
        velocidade_y = 0
    return velocidade_x, velocidade_y

def mostrar_mensagem_perdeu(pontuacao):
    fonte = pygame.font.Font(None, 36)
    texto1 = fonte.render("Você perdeu!", True, vermelha)
    texto_rect1 = texto1.get_rect(center=(largura // 2, altura // 2 - 20))

    texto2 = fonte.render(f'Pontuação: {pontuacao}', True, vermelha)
    texto_rect2 = texto2.get_rect(center=(largura // 2, altura // 2 + 20))

    tela.fill(preta)
    tela.blit(texto1, texto_rect1)
    tela.blit(texto2, texto_rect2)
    pygame.display.update()

    aguardando_clique = True
    while aguardando_clique:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                aguardando_clique = False

def rodar_jogo():
    
    recomecar = True

    x = largura / 2
    y = altura / 2

    velocidade_x = 0
    velocidade_y = 0

    tamanho_cobra = 1
    pixels = []

    comida_x, comida_y = gerar_comida()

    while True:
        tela.fill(preta)
        
        if recomecar:
            tamanho_cobra = 1
            pixels = []
            comida_x, comida_y = gerar_comida()
            x = largura / 2
            y = altura / 2
            direcao_x = tamanho_quadrado
            direcao_y = 0
            recomecar = False   
            
        for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.KEYDOWN:
                    velocidade_x, velocidade_y = selecionar_velocidade(evento.key, velocidade_x, velocidade_y)

        #atualizar a posicao da cobra
        if x >= largura or x < 0 or y >= altura or y < 0:
            mostrar_mensagem_perdeu(tamanho_cobra - 1)
            recomecar = True
        
        x += velocidade_x
        y += velocidade_y

        #desenhar comida
        desenhar_comida(tamanho_quadrado, comida_x, comida_y)
        
        #desenhar cobra
        pixels.append([x, y])
        if len(pixels) > tamanho_cobra:
            del pixels[0]

        #se a cobrinha bateu no proprio corpo   
        for pixel in pixels[:-1]:
            if pixel == [x, y]:
                mostrar_mensagem_perdeu(tamanho_cobra - 1)
                recomecar = True
        desenhar_cobra(tamanho_quadrado, pixels)

        #desenhar pontos
        desenhar_pontuacao(tamanho_cobra-1)

        #atualizacao da tela
        pygame.display.update()

        #criar nova comida
        if x == comida_x and y == comida_y:
            tamanho_cobra += 1
            comida_x, comida_y = gerar_comida()

        relogio.tick(velocidade_jogo)

rodar_jogo()
