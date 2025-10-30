import pygame
import math

# Initialisation de Pygame
pygame.init()

# Création de la fenêtre
screen_width, screen_height = 1280, 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Crystal Defender")

clock = pygame.time.Clock()
running = True

# Chargement du fond
fond = pygame.image.load("res/map.png").convert()
fond = pygame.transform.scale(fond, (screen_width, screen_height))

# Chargement du personnage
char_img = pygame.image.load("res/char.png").convert_alpha()
char = pygame.transform.scale(char_img, (85, 85))
char_x = screen_width // 2 - char.get_width() // 2
char_y = screen_height // 2 - char.get_height() // 2

# Chargement du projectile (feather)
feather_img = pygame.image.load("res/feather.png").convert_alpha()
feather_img = pygame.transform.scale(feather_img, (60, 30))  # un peu plus long que haut

# Liste des projectiles : [x, y, vx, vy, angle]
projectiles = []

# Boucle principale
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Clic souris → créer un projectile
        if event.type == pygame.MOUSEBUTTONDOWN:
            click_x, click_y = event.pos
            dx = click_x - (char_x + char.get_width() // 2)
            dy = click_y - (char_y + char.get_height() // 2)
            angle = math.atan2(dy, dx)
            speed = 12
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            # On stocke aussi l’angle pour dessiner la rotation
            projectiles.append([
                char_x + char.get_width() // 2,
                char_y + char.get_height() // 2,
                vx, vy, angle
            ])

    # === MISE À JOUR ===
    for p in projectiles:
        p[0] += p[2]
        p[1] += p[3]

    # Supprimer ceux qui sortent de l’écran
    projectiles = [p for p in projectiles if 0 < p[0] < screen_width and 0 < p[1] < screen_height]

    # === DESSIN ===
    screen.blit(fond, (0, 0))
    screen.blit(char, (char_x, char_y))

    for p in projectiles:
        # On tourne la plume selon l’angle de tir
        # ⚠️ pygame.transform.rotate tourne dans le sens antihoraire et prend les degrés
        # Si tu veux que le "côté gauche" pointe vers la direction du tir :
        # l’image de base doit être tournée vers la droite (0° sur l’axe X)
        rotated = pygame.transform.rotate(feather_img, -math.degrees(p[4]))
        rect = rotated.get_rect(center=(p[0], p[1]))
        screen.blit(rotated, rect.topleft)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

