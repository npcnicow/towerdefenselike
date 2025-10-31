import pygame
import math
import random

pygame.init()

# --- Fenêtre ---
screen_width, screen_height = 1280, 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Crystal Defender")
clock = pygame.time.Clock()

# --- Fond ---
fond = pygame.image.load("res/map.png").convert()
fond = pygame.transform.scale(fond, (screen_width, screen_height))

# --- Joueur ---
char_img = pygame.image.load("res/char.png").convert_alpha()
char = pygame.transform.scale(char_img, (85, 85))
char_rect = char.get_rect(center=(screen_width // 2, screen_height // 2))

# --- Projectile (feather) ---
feather_img = pygame.image.load("res/feather.png").convert_alpha()
feather_img = pygame.transform.scale(feather_img, (60, 30))
projectiles = []  # [x, y, vx, vy, angle]

# --- Ennemis ---
enemy_img = pygame.image.load("res/enemy.png").convert_alpha()
enemy_img = pygame.transform.scale(enemy_img, (60, 60))
enemies = []
enemy_speed = 2
max_enemies = 5

# --- Timer difficulté ---
TIMER_EVENT_spawn_next_phase_of_monsters = pygame.USEREVENT + 1
pygame.time.set_timer(TIMER_EVENT_spawn_next_phase_of_monsters, 60000)
difficulty = 0

# --- Score ---
score = 0
font = pygame.font.SysFont(None, 50)

# --- Game over flag ---
game_over = False

# --- Boucle principale ---
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if not game_over:
            # Timer pour activer les ennemis
            if event.type == TIMER_EVENT_spawn_next_phase_of_monsters:
                difficulty = 1

            # Clic souris → créer un projectile
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click_x, click_y = event.pos
                dx = click_x - char_rect.centerx
                dy = click_y - char_rect.centery
                angle = math.atan2(dy, dx)
                speed = 12
                vx = math.cos(angle) * speed
                vy = math.sin(angle) * speed
                projectiles.append([char_rect.centerx, char_rect.centery, vx, vy, angle])

    if not game_over:
        # --- Spawn ennemis ---
        if difficulty == 1:
            while len(enemies) < max_enemies:
                x = random.randint(0, screen_width)
                y = random.randint(0, screen_height)
                enemy_rect = enemy_img.get_rect(center=(x, y))
                enemies.append(enemy_rect)

        # --- Déplacement ennemis vers joueur ---
        for enemy_rect in enemies:
            dx = char_rect.centerx - enemy_rect.centerx
            dy = char_rect.centery - enemy_rect.centery
            distance = math.hypot(dx, dy)
            if distance != 0:
                dx /= distance
                dy /= distance
            enemy_rect.x += dx * enemy_speed
            enemy_rect.y += dy * enemy_speed

            # --- Collision joueur → game over ---
            if char_rect.colliderect(enemy_rect):
                game_over = True

        # --- Déplacement projectiles ---
        for p in projectiles:
            p[0] += p[2]
            p[1] += p[3]

        # Supprimer projectiles hors écran
        projectiles = [p for p in projectiles if 0 < p[0] < screen_width and 0 < p[1] < screen_height]

        # --- Collision projectile → ennemis ---
        for p in projectiles[:]:  # copier la liste pour pouvoir supprimer
            p_rect = pygame.Rect(p[0]-15, p[1]-15, 30, 30)  # petite approximation
            for enemy_rect in enemies[:]:
                if p_rect.colliderect(enemy_rect):
                    enemies.remove(enemy_rect)  # tuer l'ennemi
                    projectiles.remove(p)       # supprimer le projectile
                    score += 1                  # augmenter score
                    break

    # --- Dessin ---
    screen.blit(fond, (0, 0))

    if not game_over:
        screen.blit(char, char_rect)

        # Dessiner projectiles
        for p in projectiles:
            rotated = pygame.transform.rotate(feather_img, -math.degrees(p[4]))
            rect = rotated.get_rect(center=(p[0], p[1]))
            screen.blit(rotated, rect.topleft)

        # Dessiner ennemis
        for enemy_rect in enemies:
            screen.blit(enemy_img, enemy_rect)

        # Afficher le score
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
    else:
        # --- Écran de fin ---
        end_text = font.render(f"GAME OVER ! Score: {score}", True, (255, 0, 0))
        screen.blit(end_text, (screen_width//2 - end_text.get_width()//2,
                               screen_height//2 - end_text.get_height()//2))

    pygame.display.flip()
    clock.tick(60)


