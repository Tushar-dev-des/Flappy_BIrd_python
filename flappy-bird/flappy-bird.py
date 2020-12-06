import pygame
import sys
import random

pygame.init()
screen = pygame.display.set_mode((570, 1018))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19__.ttf', 40)

# Game variables

gravity = 0.25
bird_movement = 0
game_active = False
score = 0
high_score = 0

# Game variables

bg_surface = pygame.image.load('./images/background-day.png').convert()
bg_surface = pygame.transform.scale2x(bg_surface)
bg_x_pos = 0

floor_surface = pygame.image.load('images/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0


bird_upflap = pygame.transform.scale2x(pygame.image.load(
    'images/bluebird-upflap.png').convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load(
    'images/bluebird-midflap.png').convert_alpha())
bird_downflap = pygame.transform.scale2x(pygame.image.load(
    'images/bluebird-downflap.png').convert_alpha())
bird_frames = [bird_upflap, bird_midflap, bird_downflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(100, 512))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 100)

# bird_surface = pygame.image.load('images/bluebird-midflap.png').convert_alpha()
# bird_surface = pygame.transform.scale2x(bird_surface)
# bird_rect = bird_surface.get_rect(center=(100, 512))

pipe_surface = pygame.image.load('images/pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1500)

game_over_surface = pygame.transform.scale2x(
    pygame.image.load('images/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center=(288, 512))


def move_background():
    screen.blit(bg_surface, (bg_x_pos, 0))
    screen.blit(bg_surface, (bg_x_pos + 576, 0))


def draw_floor():

    screen.blit(floor_surface, (floor_x_pos, 900))
    screen.blit(floor_surface, (floor_x_pos + 576, 900))


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(700, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(700, random_pipe_pos - 300))

    return bottom_pipe, top_pipe


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 4

    return pipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1024:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False

    if bird_rect.top <= -100 or bird_rect.bottom >= 900:
        return False

    return True


def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement*3, 1)

    return new_bird


def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))

    return new_bird, new_bird_rect


def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(
            str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(288, 100))
        screen.blit(score_surface, score_rect)

    if game_state == 'game_over':
        score_surface = game_font.render(
            f'Score : {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(288, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(
            f'High_score : {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(288, 850))
        screen.blit(high_score_surface, high_score_rect)


def update_score(score, high_score):
    if score >= high_score:
        high_score = score

    return high_score


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active == True:
                bird_movement = 0
                bird_movement -= 9
                score += 1

            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 512)
                bird_movement = 0
                score = 0

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0

            bird_surface, bird_rect = bird_animation()

    # background movement ---
    move_background()
    bg_x_pos -= 0.3
    if bg_x_pos <= -576:
        bg_x_pos = 0

    # background movement ---

    # floor movement ---
    draw_floor()
    floor_x_pos -= 3

    if floor_x_pos <= -576:
        floor_x_pos = 0

    # floor movement ---
    pipe_height = [400, 500, 600, 700, 800]
    if game_active:
        # bird movement ---

        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)

        # bird movement ---

        # pipe movement ---

        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        # pipe movement ---

        score_display('main_game')

    else:
        high_score = update_score(score, high_score)
        score_display('game_over')
        screen.blit(game_over_surface, game_over_rect)

    pygame.display.update()
    clock.tick(120)
