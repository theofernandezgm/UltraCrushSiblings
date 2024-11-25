import pygame
import sys
import math

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
player_angle = 0

# Load the background image from the local directory
background = pygame.image.load('background_image.jpg')  # Replace with your image filename
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Scale to fit the screen

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

def shoot_bullet():
    angle_rad = math.radians(player_angle)
    dx = bullet_speed * math.cos(angle_rad)
    dy = bullet_speed * math.sin(angle_rad)
    bullets.append([player_x + player_width // 2, player_y + player_height // 2, dx, dy])

running = True
while running:
    screen.fill(WHITE)
    
    # Draw the background image
    screen.blit(background, (0, 0))  # Blit the background image at (0, 0)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                shoot_bullet()
    
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player_x -= player_speed
        player_angle = 180
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
        player_angle = 0
    if keys[pygame.K_UP]:
        player_y -= player_speed
        player_angle = 270
    if keys[pygame.K_DOWN]:
        player_y += player_speed
        player_angle = 90

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
        bullet[0] += bullet[2]
        bullet[1] += bullet[3]
        if bullet[0] < 0 or bullet[0] > SCREEN_WIDTH or bullet[1] < 0 or bullet[1] > SCREEN_HEIGHT:
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
