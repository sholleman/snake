import pygame as pg
from random import randrange

from pygame.color import THECOLORS

WINDOW = 900
TILE_SIZE = 50
RANGE = (TILE_SIZE // 2, WINDOW - TILE_SIZE // 2, TILE_SIZE)

UP = (0, -TILE_SIZE)
DOWN = (0, TILE_SIZE)
LEFT = (-TILE_SIZE, 0)
RIGHT = (TILE_SIZE, 0)

get_random_position = lambda: [randrange(*RANGE), randrange(*RANGE)]

snake = pg.rect.Rect([0, 0, TILE_SIZE - 2, TILE_SIZE - 2])
snake.center = get_random_position()
length = 1
segments = [snake.copy()]
snake_dir = (0, 0)

food = snake.copy()
food.center = get_random_position()

time, time_step = 0, 110

screen = pg.display.set_mode([WINDOW, WINDOW])
clock = pg.time.Clock()

pg.font.init() # you have to call this at the start,
                   # if you want to use this module.
comic_sans = pg.font.SysFont('Comic Sans MS', 30)


def draw_snake(color = None):
    color = color or "green"
    [pg.draw.rect(screen, color, segment) for segment in segments]


while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()
        if event.type == pg.KEYDOWN:
            if event.key in (pg.K_w, pg.K_UP) and snake_dir != DOWN:
                snake_dir = UP
            elif event.key in (pg.K_s, pg.K_DOWN) and snake_dir != UP:
                snake_dir = DOWN
            elif event.key in (pg.K_a, pg.K_LEFT) and snake_dir != RIGHT:
                snake_dir = LEFT
            elif event.key in (pg.K_d, pg.K_RIGHT) and snake_dir != LEFT:
                snake_dir = RIGHT

    screen.fill("black")
    length_counter = comic_sans.render(f"{length}", True, "white")
    screen.blit(length_counter, (10, 10))

    out_of_bounds = snake.left < 0 or snake.right > WINDOW or snake.top < 0 or snake.bottom > WINDOW

    self_eating = pg.Rect.collidelist(snake, segments[:-1]) != -1

    if out_of_bounds or self_eating:
        for _ in range(length):
            screen.fill("black")

            for _ in range(5):
                color = list(THECOLORS.keys())[randrange(len(THECOLORS))]
                draw_snake(color)
                pg.display.flip()
                pg.time.wait(50)

            length -= 1
            segments = segments[-length:]

        snake.center, food.center = get_random_position(), get_random_position()
        length, snake_dir = 1, (0, 0)
        segments = [snake.copy()]

    # check food
    if snake.center == food.center:
        food.center = get_random_position()
        length += 1

    # draw food
    pg.draw.rect(screen, "red", food)

    # draw snake
    draw_snake()

    # move snake
    time_now = pg.time.get_ticks()
    if time_now - time > time_step:
        time = time_now
        snake.move_ip(snake_dir)
        segments.append(snake.copy())
        segments = segments[-length:]

    pg.display.flip()
    clock.tick(60)
