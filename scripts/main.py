import pygame
import random
import sys

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Economize Água")

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

clock = pygame.time.Clock()
FPS = 60

class Torneira:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vazando = False
        self.img_normal = pygame.image.load("./assets/torneira.png")
        self.img_vazando = pygame.image.load("./assets/torneira_vazando.png")
        self.img_normal = pygame.transform.scale(self.img_normal, (150, 200))
        self.img_vazando = pygame.transform.scale(self.img_vazando, (150, 200))
        self.rect = self.img_normal.get_rect(topleft=(x, y))

    def desenhar(self):
        if self.vazando:
            screen.blit(self.img_vazando, (self.x, self.y))
        else:
            screen.blit(self.img_normal, (self.x, self.y))

    def ativar_vazamento(self):
        self.vazando = True

    def fechar_vazamento(self):
        self.vazando = False

def mostrar_mensagem_fase(fase):
    fonte = pygame.font.Font(None, 72)
    mensagem = f"Você passou de fase {fase}!"
    texto = fonte.render(mensagem, True, (0, 0, 0))
    screen.blit(texto, (SCREEN_WIDTH // 2 - texto.get_width() // 2, SCREEN_HEIGHT // 2 - texto.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(2000) 


def main():
    
    torneiras = [Torneira(200, 250), Torneira(400, 250), Torneira(600, 250)]

    
    pontuacao = 0
    tempo_para_proximo_vazamento = 2000  
    ultimo_vazamento = pygame.time.get_ticks()
    fase = 1

    rodando = True
    while rodando:
        screen.fill(WHITE)

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for torneira in torneiras:
                    if torneira.rect.collidepoint(event.pos) and torneira.vazando:
                        torneira.fechar_vazamento()
                        pontuacao += 10

        
        agora = pygame.time.get_ticks()
        if agora - ultimo_vazamento > tempo_para_proximo_vazamento:
            ultima_torneira = random.choice(torneiras)
            ultima_torneira.ativar_vazamento()
            ultimo_vazamento = agora

        
        for torneira in torneiras:
            if torneira.vazando:
                pontuacao -= 0.1  

    
        for torneira in torneiras:
            torneira.desenhar()

        
        if pontuacao >= 100 and fase == 1:
            fase = 2
            tempo_para_proximo_vazamento = 1500
            mostrar_mensagem_fase(fase)  
        if pontuacao >= 200 and fase == 2:
            fase = 3
            tempo_para_proximo_vazamento = 1000
            mostrar_mensagem_fase(fase)  

        
        fonte = pygame.font.Font(None, 36)
        texto_pontuacao = fonte.render(f"Pontuação: {int(pontuacao)}", True, (0, 0, 0))
        texto_fase = fonte.render(f"Fase: {fase}", True, (0, 0, 0))
        screen.blit(texto_pontuacao, (10, 10))
        screen.blit(texto_fase, (10, 50))

    
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
