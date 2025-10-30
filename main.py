import pygame
from pygame import *

# Initialisation de Pygame
pygame.init()

# Création de la fenêtre
screen_width, screen_height = 1280, 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("crystal defender")

clock = pygame.time.Clock()
running = True

# Chargement et redimensionnement du fond
fond = pygame.image.load("res/map.png").convert()
fond = pygame.transform.scale(fond, (screen_width, screen_height))  # <--- redimensionnement
#Chargement du charachter
charachter_img=pygame.image.load("res/char.png")
charachter=transform.scale(charachter_img,(85,85))
#fixer la charachter x et y

char_x = screen_width // 2 - charachter.get_width() // 2
char_y = screen_height // 2 - charachter.get_height() // 2


# Boucle principale
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #detecter les clicks
        if event.type == pygame.MOUSEBUTTONDOWN:
            
            print("clic détecté à :", event.pos)    
            click_pos_x=event.pos[0]
            click_pos_y=event.pos[1]
            #il faut trianguler la position avec char_x et char y
                
                

    # Dessiner le fond
    screen.blit(fond, (0, 0))
    #dessiner le charachter
    screen.blit(charachter,(char_x,char_y))
    # Mettre à jour l'affichage
    pygame.display.flip()

    # Limiter à 60 FPS
    clock.tick(60)

pygame.quit()
