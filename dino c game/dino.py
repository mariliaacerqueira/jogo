from typing import Any
import pygame
from pygame.locals import *
from sys import exit 
import os
from random import randrange, choice

pygame.init() 
pygame.mixer.init()

diretorio_principal = os.path.dirname(_file_)
diretorio_imagens = os.path.join(diretorio_principal, 'imagens')
diretorio_sons = os.path.join(diretorio_principal, 'sons')

largura = 640
altura = 480
FPS = 20
AZUL = (173,216,230)

tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Dinoland')

sprite_sheet = pygame.image.load(os.path.join(diretorio_imagens, 'cogumelo.png')).convert_alpha()
sprite_sol = pygame.image.load(os.path.join(diretorio_imagens, 'sol.png')).convert_alpha()

def load_sound(file_path, volume):
    sound = pygame.mixer.Sound(file_path)
    sound.set_volume(volume)
    return sound

# Load sounds
som_ambiente = load_sound(os.path.join(diretorio_sons, 'bg_music.mp3'), 0.1)
som_colisao = load_sound(os.path.join(diretorio_sons, 'death_sound.wav'), 0.2)
som_pontuacao = load_sound(os.path.join(diretorio_sons, 'score_sound.wav'), 0.2)
som_pontuacao1 = load_sound(os.path.join(diretorio_sons, '1000.wav'), 0.2)
som_pontuacao2 = load_sound(os.path.join(diretorio_sons, '1001.wav'), 0.2)  

colidiu = False

escolha_obstaculo = choice([0, 1])

pontos = 0

velocidade_jogo = 10

som_ambiente.play()

def exibe_mensagem(msg, tamanho, cor):
    fonte = pygame.font.SysFont('comicsansms', tamanho, True, False)
    mensagem = f'{msg}'
    texto_formatado = fonte.render(mensagem, True, cor)
    return texto_formatado

def reiniciar_jogo():
    global pontos, velocidade_jogo, colidiu, escolha_obstaculo
    pontos = 0
    velocidade_jogo = 10
    colidiu = False
    dino.rect.y = altura - 135
    dino.pulo = False
    aviao.rect.x = largura
    cogumelo.rect.x = largura
    escolha_obstaculo = choice([0,1])
    som_ambiente.play()

class Dino(pygame.sprite.Sprite):
    def _init_(self):
        pygame.sprite.Sprite._init_(self)
        self.som_pulo = pygame.mixer.Sound(os.path.join(diretorio_sons, 'jump_sound.wav'))
        self.som_pulo.set_volume(0.2)
        self.imagens_dinossauro = []
        for i in range(3):
            img = sprite_sheet.subsurface((i * 64,0), (64,114))
            img = pygame.transform.scale(img, (64*2,114*2))
            self.imagens_dinossauro.append(img)

        self.index_lista = 0
        self.image = self.imagens_dinossauro[self.index_lista]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.pos_y_inicial = altura - 170
        self.rect.center = (100, altura - 50)
        self.pulo = False
        self.som_pulo.stop()

    def pular(self):
        self.pulo = True
        self.som_pulo.play()
    
    def update(self):
        if self.pulo == True:
            if self.rect.y <=180:
                self.pulo = False
            self.rect.y -= 20
        else:
            if self.rect.y < self.pos_y_inicial:
                self.rect.y += 20
            else: 
                self.rect.y = self.pos_y_inicial

        if self.index_lista > 2:
            self.index_lista = 0
        self.index_lista += 0.25
        self.image = self.imagens_dinossauro[int(self.index_lista)]

class Nuvens(pygame.sprite.Sprite):
    def _init_(self):
        pygame.sprite.Sprite._init_(self)
        self.image = sprite_sheet.subsurface((7*64, 0), (64,114))
        self.image = pygame.transform.scale(self.image, (64*1.5, 114*1.5))
        self.rect = self.image.get_rect()
        self.rect.y = randrange(10, 160, 50)
        self.rect.x = largura - randrange(30, 390, 90)

    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = largura
            self.rect.y = randrange(10, 160, 50)
        self.rect.x -= velocidade_jogo

class Chao(pygame.sprite.Sprite):
    def _init_(self, pos_x):
        pygame.sprite.Sprite._init_(self)
        self.image = sprite_sheet.subsurface((6*64, 0), (64,114))
        self.image = pygame.transform.scale(self.image, (64*1.5, 114*1.5))
        self.rect = self.image.get_rect()
        self.rect.y = altura - 100
        self.rect.x = pos_x * 64

    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = largura
        self.rect.x -= 10

class Cogumelo(pygame.sprite.Sprite):
    def _init_(self):
        pygame.sprite.Sprite._init_(self)
        self.image = sprite_sheet.subsurface((5*64, 0), (64,114))
        self.image = pygame.transform.scale(self.image, (64*1.1, 114*1.1))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.escolha = escolha_obstaculo
        self.rect.center = (largura, altura - 55)
        self.rect.x = largura

    def update(self):
        if self.escolha == 0:
            if self.rect.topright[0] < 0:
                self.rect.x = largura
            self.rect.x -= velocidade_jogo

class Aviao(pygame.sprite.Sprite):
    def _init_(self):
        pygame.sprite.Sprite._init_(self)
        self.imagens_dinossauro = []
        for i in range(3,5):
            img = sprite_sheet.subsurface((i * 64, 0), (64,114))
            img = pygame.transform.scale(img, (64*1.5,114*1.5))
            self.imagens_dinossauro.append(img)

        self.index_lista = 0
        self.image = self.imagens_dinossauro[self.index_lista]
        self.mask = pygame.mask.from_surface(self.image)
        self.escolha = escolha_obstaculo
        self.rect = self.image.get_rect()
        self.rect.center = (largura, 330)
        self.rect.x = largura

    def update(self):
        if self.escolha == 1:
            if self.rect.topright[0] < 0:
                self.rect.x = largura
            self.rect.x -= velocidade_jogo

            if self.index_lista > 1:    
                self.index_lista = 0
            self.index_lista += 0.25
            self.image = self.imagens_dinossauro[int(self.index_lista)]

class Sol(pygame.sprite.Sprite):
    def _init_(self):
        pygame.sprite.Sprite._init_(self)
        self.image = sprite_sol.subsurface((0, 0), (64, 63))
        self.rect = self.image.get_rect()
        self.rect.y = altura - 420
        self.rect.x = largura - 580
        self.angle = 0
        self.frame_count = 0  # Contador de frames
        self.rotation_interval = 40  # Intervalo de frames para atualizar o ângulo

    def update(self):
        self.frame_count += 1
        if self.frame_count % self.rotation_interval == 0:
            self.angle += 1
            rotated_image = pygame.transform.rotate(self.image, self.angle)
            self.image = rotated_image
            self.rect = self.image.get_rect(center=self.rect.center)

todas_as_sprites = pygame.sprite.Group()
dino = Dino()
todas_as_sprites.add(dino)

for i in range(4):
    nuvem = Nuvens()
    todas_as_sprites.add(nuvem)

for i in range(12):
    chao = Chao(i)
    todas_as_sprites.add(chao)

cogumelo = Cogumelo()
todas_as_sprites.add(cogumelo)

aviao = Aviao()
todas_as_sprites.add(aviao)

sol = Sol()
todas_as_sprites.add(sol)

grupo_obstaculos = pygame.sprite.Group()
grupo_obstaculos.add(cogumelo)
grupo_obstaculos.add(aviao)

relogio = pygame.time.Clock()
while True:
    relogio.tick(FPS)
    tela.fill(AZUL)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                if dino.rect.y != dino.pos_y_inicial:
                    pass
                else:
                    dino.pular()    

            if event.key == K_r and colidiu == True:
                som_colisao.stop()
                reiniciar_jogo()

    if colidiu == True:
        som_pontuacao1.stop()

    colisoes = pygame.sprite.spritecollide(dino, grupo_obstaculos, False, pygame.sprite.collide_mask)                    

    todas_as_sprites.draw(tela)

    if cogumelo.rect.topright[0] <= 0 or aviao.rect.topright[0] <= 0:
        escolha_obstaculo = choice([0,1])
        cogumelo.rect.x = largura
        aviao.rect.x = largura
        cogumelo.escolha = escolha_obstaculo
        aviao.escolha = escolha_obstaculo

    if colisoes and colidiu == False:
        som_colisao.play()
        colidiu = True 

    if colidiu == True:
        if pontos % 100 == 0:
            pontos +=1
        game_over = exibe_mensagem('GAME OVER', 40, (0,0,0))
        tela.blit(game_over, (largura//2, altura//2))
        restart = exibe_mensagem('Pressione r para reiniciar', 25, (0,0,0))
        tela.blit(restart, ((largura//2 - 20), (altura//2) + 35))
        som_ambiente.stop()

    else:
        pontos += 1
        todas_as_sprites.update()
        texto_pontos = exibe_mensagem(pontos, 40, (255,14,93))

    if pontos %500 == 0 and escolha_obstaculo == 1:
        som_pontuacao1.play()
        velocidade_jogo += 3

        if velocidade_jogo >= 35:
            velocidade_jogo = 35
    
    if pontos %500 == 0 and escolha_obstaculo == 0:
        som_pontuacao2.play()
        velocidade_jogo -= 5

    else:
        if pontos % 100 == 0:
            som_pontuacao.play()
            if velocidade_jogo >= 35:
                velocidade_jogo += 0
            else:
                velocidade_jogo += 1          
    
    print(velocidade_jogo)

    tela.blit(texto_pontos, (525,60))

    pygame.display.flip()
