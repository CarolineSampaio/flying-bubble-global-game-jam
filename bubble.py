import pygame
import random

# inicializacao do pygame
pygame.init()

# inicializar o sistema de áudio
pygame.mixer.init()

# configuracoes da tela
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 700  # aumentei a altura da tela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("bubble fly")

# cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (135, 206, 250)
DARK_BLUE = (25, 25, 112)
GREEN = (34, 139, 34)

# clock
clock = pygame.time.Clock()
FPS = 60

# funcao para desenhar texto centralizado
def draw_text(text, font, color, surface, y_offset=0):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + y_offset)
    surface.blit(textobj, textrect)

# classe da bolha
class Bubble(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # carrega a imagem da bolha
        self.image = pygame.image.load("gallery/sprites/bubble.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))  # Redimensionar para 30x30 pixels
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 2 // 3))  # posição no 1/3 inferior
        self.fixed_position = True  # a bolha começa fixa no 1/3 inferior

    def burst(self):
        # carrega a imagem da bolha estourada
        self.image = pygame.image.load("gallery/sprites/bubble_burst.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 40))
        
        # animacao de desaparecimento
        for i in range(255, 0, -5):
            self.image.set_alpha(i)
            screen.fill(BLUE)
            all_sprites.draw(screen)
            pygame.display.flip()
            pygame.time.delay(10)

    def immunity(self):
        # carrega a imagem da bolha com imunidade
        self.image = pygame.image.load("gallery/sprites/bubble_immunity.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (35, 35))
        all_sprites.draw(screen)
        pygame.display.flip()

    def remove_immunity(self):
        # carrega a imagem da bolha normal
        self.image = pygame.image.load("gallery/sprites/bubble.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        all_sprites.draw(screen)
        pygame.display.flip()

    def update(self):
        # controles laterais
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += 5

# classe de obstaculos
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        # carrega a imagem do obstaculo
        self.image = pygame.image.load("gallery/sprites/obstacle.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))  # Ajustar o tamanho para o tamanho do obstáculo
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, speed):
        self.rect.y += speed  # velocidade de descida
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

# classe da bolinha de imunidade (amarela e sem fundo preto)
class ImmunityBubble(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("gallery/sprites/immunity.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))  # redimensionar para 30x30 pixels
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - 30)
        self.rect.y = random.randint(-100, -30)  # inicia fora da tela
        self.speed_y = 2 # velocidade de descida da bolinha

    def update(self):
        self.rect.y += self.speed_y  # a bolinha desce
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()  # remove a bolinha quando sair da tela

# funcao para gerar obstaculos com boa distribuicao na tela
def generate_obstacle():
    # garantir que os obstaculos nao fiquem muito proximos na horizontal
    x = random.randint(0, SCREEN_WIDTH - 80)  # ajuste para garantir que nao fiquem grudados horizontalmente

    # ajuste no espacamento vertical entre obstaculos
    y = random.randint(-150, -50)  # alterei a faixa para evitar grandes espacos em branco

    # altura fixa do obstaculo (ex: 20 pixels)
    width = random.randint(60, 100)  # largura variavel
    height = 60  # altura fixa

    # verificar se o novo obstaculo vai se sobrepor a algum ja existente
    for obstacle in obstacles:
        if (x < obstacle.rect.x + obstacle.rect.width and
            x + width > obstacle.rect.x and
            y < obstacle.rect.y + obstacle.rect.height and
            y + height > obstacle.rect.y):
            return  # nao gera o obstaculo se sobrepuser com algum ja existente

    # criar o obstaculo e adiciona-lo aos grupos
    obstacle = Obstacle(x, y, width, height)
    all_sprites.add(obstacle)
    obstacles.add(obstacle)

# configuracao inicial
all_sprites = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
immunity_bubbles = pygame.sprite.Group()

bubble = Bubble()
all_sprites.add(bubble)

# contador de altura
height = 0

# velocidades iniciais
obstacle_speed = 2  # ajustei a velocidade para um valor intermediario
scroll_speed = 1  # a velocidade de metros foi diminuida ainda mais

# geracao inicial de obstaculos
for _ in range(5):
    generate_obstacle()

# funcao para tela de "game over"
def game_over():
    font = pygame.font.Font(None, 36)
    draw_text("Game Over", font, WHITE, screen)
    draw_text("Pressione Espaço para", font, WHITE, screen, 50)
    draw_text("Jogar Novamente", font, WHITE, screen, 90)

# funcao para tela inicial
def start_screen():
    font = pygame.font.Font(None, 36)
    draw_text("Bubble Fly", font, WHITE, screen)
    draw_text("Pressione Espaço para Jogar", font, WHITE, screen, 50)

# carregar o áudio
pygame.mixer.music.load("gallery/audio/flying.mp3")
die_sound = pygame.mixer.Sound("gallery/audio/die.mp3")  # carregar o som de game over

# jogo principal
running = True
game_state = 'start'  # pode ser 'start', 'playing', ou 'game_over'
immunity_time = 0  # marca o tempo da imunidade
immunity_duration = 0  # duracao da imunidade

while running:
    screen.fill(BLUE)

    if game_state == 'start':
        start_screen()  # tela inicial
        pygame.mixer.music.stop()  # Para o som no estado inicial
    elif game_state == 'playing':
        # Tocar o som apenas se ainda não estiver tocando
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(-1)  # Reproduzir o som em loop

        # atualizacao dos sprites
        bubble.update()  # atualiza apenas a bolha
        obstacles.update(obstacle_speed)  # atualiza os obstaculos com a velocidade
        immunity_bubbles.update()  # atualiza as bolinhas de imunidade

        # checagem de colisao com a bolha
        if pygame.sprite.spritecollide(bubble, obstacles, False, pygame.sprite.collide_rect_ratio(0.9)) and not immunity_time:  # colisao mais precisa
            die_sound.play() # toca o som de game over
            bubble.burst() # animacao de estouro

            pygame.time.delay(500)
            game_state = 'game_over'  # vai para a tela de game over
            pygame.mixer.music.stop()  # Para o som no game over  

        # checagem de colisao com a bolinha de imunidade
        if pygame.sprite.spritecollide(bubble, immunity_bubbles, True):
            immunity_time = pygame.time.get_ticks()  # marca o tempo da colisao
            immunity_duration = 10000  # 10 segundos de imunidade
            bubble.immunity()  # animacao de imunidade

        # geracao de obstaculos continua com espacamento
        if random.randint(1, 60) == 1:  # aproximadamente 1 por segundo
            generate_obstacle()

        # geracao de bolinhas de imunidade com menos frequencia
        if random.randint(1, 1000) == 1:  # diminui chance de aparecer a bolinha de imunidade
            immunity_bubble = ImmunityBubble()
            all_sprites.add(immunity_bubble)
            immunity_bubbles.add(immunity_bubble)

        # atualizacao da altura
        if bubble.fixed_position:  # atualiza apenas depois que a bolha estiver fixa
            height += scroll_speed
            if int(height) % 50 == 0:  # a cada 50 metros, aumenta a dificuldade
                obstacle_speed += 0.1
                generate_obstacle()

        # mudanca de cenario com base na altura
        if height < 500:
            screen.fill(BLUE)
        elif height < 1000:
            # transicao gradual do azul para azul escuro
            ratio = (height - 500) / 500
            transition_color = (
            int(BLUE[0] + (DARK_BLUE[0] - BLUE[0]) * ratio),
            int(BLUE[1] + (DARK_BLUE[1] - BLUE[1]) * ratio),
            int(BLUE[2] + (DARK_BLUE[2] - BLUE[2]) * ratio)
            )
            screen.fill(transition_color)
        else:
            # transicao gradual do azul escuro para preto
            ratio = (height - 1000) / 500
            if ratio < 1:
                transition_color = (
                int(DARK_BLUE[0] + (BLACK[0] - DARK_BLUE[0]) * ratio),
                int(DARK_BLUE[1] + (BLACK[1] - DARK_BLUE[1]) * ratio),
                int(DARK_BLUE[2] + (BLACK[2] - DARK_BLUE[2]) * ratio)
                )
                screen.fill(transition_color)
            else:
                screen.fill(BLACK)

        # mostrar pontuacao
        font = pygame.font.Font(None, 36)
        text = font.render(f"{int(height)}m", True, WHITE)  # mostra altura como numero inteiro
        screen.blit(text, (10, 10))

        # carrega a imagem do icon de imunidade
        immunity_icon = pygame.image.load("gallery/sprites/immunity.png").convert_alpha()
        immunity_icon = pygame.transform.scale(immunity_icon, (25, 25))

        # mostrar tempo de imunidade
        if immunity_time:
            remaining_time = (pygame.time.get_ticks() - immunity_time)
            if remaining_time < immunity_duration:
                immunity_text = font.render(f'{int((immunity_duration - remaining_time) / 1000)}s', True, WHITE)
                
                # exibe icone e texto do tempo ao lado
                screen.blit(immunity_icon, (SCREEN_WIDTH - immunity_icon.get_width() - immunity_text.get_width() - 10, 10))  # icon
                screen.blit(immunity_text, (SCREEN_WIDTH - immunity_text.get_width() - 10, 10))  # tempo
            else:
                immunity_time = 0  # reinicia a imunidade apos o tempo expirar
                bubble.remove_immunity()  # remove a imunidade

        # desenho dos sprites
        all_sprites.draw(screen)

    elif game_state == 'game_over':
        game_over()  # tela de game over

    # atualizar a tela
    pygame.display.flip()

    # processar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if game_state == 'start' and event.key == pygame.K_SPACE:
                # iniciar o jogo ao pressionar espaco
                game_state = 'playing'
                height = 0
                obstacle_speed = 2  # velocidade intermediaria
                scroll_speed = 0.3 # mais devagar
                # limpar obstaculos e bolinhas antigos
                obstacles.empty()
                immunity_bubbles.empty()
                all_sprites.empty()  # limpar todos os sprites, incluindo a bolha
                bubble = Bubble()  # recriar a bolha
                all_sprites.add(bubble)
                for _ in range(5):
                    generate_obstacle()
            elif game_state == 'game_over' and event.key == pygame.K_SPACE:
                # reiniciar o jogo ao pressionar espaco
                game_state = 'playing'
                height = 0
                obstacle_speed = 2  # velocidade intermediaria
                scroll_speed = 0.3  # mais devagar
                # limpar obstaculos e bolinhas antigos
                obstacles.empty()
                immunity_bubbles.empty()
                all_sprites.empty()  # limpar todos os sprites, incluindo a bolha
                bubble = Bubble()  # recriar a bolha
                all_sprites.add(bubble)
                for _ in range(5):
                    generate_obstacle()

    clock.tick(FPS)

pygame.quit()
