import pygame
import sys
import math
import os

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GROUND_HEIGHT = SCREEN_HEIGHT - 100
PLATFORM_HEIGHT = 100
PLATFORM_WIDTH = 100
RED = (255, 0, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ultra Crush Siblings (intento)")

clock = pygame.time.Clock()

player_x = SCREEN_WIDTH // 2
player_y = GROUND_HEIGHT - 50
player_width = 100
player_height = 100
collision_width = 50
collision_height = 20
player_speed = 7
velocity_y = 0
gravity = 1
jump_power = -17
on_ground = False
frame_index = 0
player_frames = []

try:
    for i in range(1, 11):
        frame_path = os.path.join(os.path.dirname(__file__), f"frame{i}.png")
        frame = pygame.image.load(frame_path)
        frame = pygame.transform.scale(frame, (player_width, player_height))
        player_frames.append(frame)
except pygame.error as e:
    print(f"Error: no s'ha pogut carregar el personatge {e}")

bullet_list = []
bullet_speed = 15
bullet_size = (50, 100)
try:
    bullet_image = pygame.image.load('bullets_image.png')
    bullet_image = pygame.transform.scale(bullet_image, bullet_size)
except pygame.error as e:
    print(f"Error: no s'ha pogut carregar la imatge de la bala {e}")
    bullet_image = None

platforms = [(150, GROUND_HEIGHT - PLATFORM_HEIGHT), (500, GROUND_HEIGHT - PLATFORM_HEIGHT)]

try:
    background = pygame.image.load('background_image.jpg')
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
except pygame.error as e:
    print(f"Error: no s'ha pogut carregar la imatge de fons {e}")
    background = None

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
    bullet_x = player_x + player_width // 2
    bullet_y = player_y + player_height // 2
    bullet_list.append([bullet_x, bullet_y, dx, dy, player_angle])

running = True
shooting = False
direction = 'right'
player_angle = 0 
frame_delay = 10
frame_counter = 0
moving = False

while running:
    screen.fill(WHITE)

    if background:
        screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z and not shooting:
                shoot_bullet()
                shooting = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_z:
                shooting = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player_angle = 180
        player_x -= player_speed
        moving = True
        if direction != 'left':
            direction = 'left'
    elif keys[pygame.K_RIGHT]:
        player_angle = 0 
        player_x += player_speed
        moving = True
        if direction != 'right':
            direction = 'right'
    else:
        moving = False
    
    if keys[pygame.K_UP]:
        player_angle = 270

    if keys[pygame.K_DOWN]:
        player_angle = 90
        player_y += player_speed

    if keys[pygame.K_x] and on_ground:
        velocity_y = jump_power
        on_ground = False

    player_rect = pygame.Rect(player_x + (player_width - collision_width) // 2, 
                              player_y + (player_height - collision_height), 
                              collision_width, collision_height)

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

    if player_frames:
        if moving:
            if frame_counter >= frame_delay:
                frame_index = (frame_index + 1) % len(player_frames)
                frame_counter = 0
            frame_counter += 1
        else:
            frame_index = 0

        if direction == 'left':
            frame = pygame.transform.flip(player_frames[frame_index], True, False)
        else:
            frame = player_frames[frame_index]
        
        screen.blit(frame, (player_x, player_y))

    for platform in platforms:
        pygame.draw.rect(screen, (0, 255, 0), (platform[0], platform[1], PLATFORM_WIDTH, 20))

    for bullet in bullet_list[:]:
        bullet[0] += bullet[2]
        bullet[1] += bullet[3]
        if bullet[0] < 0 or bullet[0] > SCREEN_WIDTH or bullet[1] < 0 or bullet[1] > SCREEN_HEIGHT:
            bullet_list.remove(bullet)

        if bullet_image:
            rotated_bullet = pygame.transform.rotate(bullet_image, -bullet[4])
            bullet_rect = rotated_bullet.get_rect(center=(bullet[0], bullet[1]))
            screen.blit(rotated_bullet, bullet_rect.topleft)
        else:
            pygame.draw.rect(screen, RED, (bullet[0], bullet[1], bullet_size[0], bullet_size[1]))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
