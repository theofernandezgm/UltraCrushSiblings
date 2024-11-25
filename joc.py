import pygame
import sys

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GROUND_HEIGHT = SCREEN_HEIGHT - 50
PLATFORM_HEIGHT = 100
PLATFORM_WIDTH = 200

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ultra Crush Siblings (intento)")

clock = pygame.time.Clock()

player_x = SCREEN_WIDTH // 2
player_y = GROUND_HEIGHT - 50
player_width = 50
player_height = 50
player_speed = 5
velocity_y = 0
gravity = 1
jump_power = -15
on_ground = False

bullets = []
bullet_speed = 10

platforms = [(100, GROUND_HEIGHT - PLATFORM_HEIGHT), (500, GROUND_HEIGHT - PLATFORM_HEIGHT)]

def check_platform_collision(player_rect, platforms):
    global velocity_y, on_ground, player_y
    for platform in platforms:
        platform_rect = pygame.Rect(platform[0], platform[1], PLATFORM_WIDTH, 20)
        if player_rect.colliderect(platform_rect) and velocity_y >= 0:
            on_ground = True
            velocity_y = 0
            player_y = platform_rect.top - player_height
            break
    else:
        on_ground = False

running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullets.append([player_x + player_width // 2 - 5, player_y])
    
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed

    if keys[pygame.K_UP] and on_ground:
        velocity_y = jump_power
        on_ground = False

    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)

    velocity_y += gravity
    player_y += velocity_y

    check_platform_collision(player_rect, platforms)

    if player_y >= GROUND_HEIGHT - player_height:
        player_y = GROUND_HEIGHT - player_height
        on_ground = True
        velocity_y = 0

    if player_x < 0:
        player_x = 0
    if player_x + player_width > SCREEN_WIDTH:
        player_x = SCREEN_WIDTH - player_width

    for bullet in bullets[:]:
        bullet[1] -= bullet_speed
        if bullet[1] < 0:
            bullets.remove(bullet)

    pygame.draw.rect(screen, BLUE, player_rect)

    for platform in platforms:
        pygame.draw.rect(screen, (0, 255, 0), (platform[0], platform[1], PLATFORM_WIDTH, 20))

    for bullet in bullets:
        pygame.draw.rect(screen, RED, (bullet[0], bullet[1], 10, 20))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
