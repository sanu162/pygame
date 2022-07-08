import pygame as pg
import random as rd
import os

pg.mixer.init()
pg.init()

white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)

screen_width = 600
screen_height = 600

win = pg.display.set_mode((screen_width, screen_height))
start = pg.image.load('start.jpg')
start = pg.transform.scale(start, (screen_width, screen_height)).convert_alpha()

gameback = pg.image.load('game.jpg')
gameback = pg.transform.scale(gameback, (screen_width, screen_height)).convert_alpha()

overback = pg.image.load('overback.jpg')
overback = pg.transform.scale(overback, (screen_width, screen_height)).convert_alpha()

pg.display.set_caption('My First Game')
clock = pg.time.Clock()
font = pg.font.SysFont(None, 30, italic=True)
pg.display.update()


def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    win.blit(screen_text, [x, y])


def plot_snake(window, color, snk_list, size):
    for x, y in snk_list:
        pg.draw.rect(window, color, [x, y, size, size])


def welcome():
    g_exit = False
    pg.mixer.music.load("audioback.mp3")
    pg.mixer.music.play(-1)
    while not g_exit:
        win.fill(white)
        win.blit(start, (0, 0))
        text_screen("Wecome to Snake Game.", black, 100, 100)
        text_screen("Press Space.", black, 100, 150)
        for i in pg.event.get():
            if i.type == pg.QUIT:
                g_exit = True
            if i.type == pg.KEYDOWN:
                if i.key == pg.K_SPACE:
                    gameloop()

        pg.display.update()
        clock.tick(30)
    pg.quit()
    quit()


def gameloop():
    if not os.path.exists("hiscore.txt"):
        with open("hiscore.txt", "w") as f:
            f.write("0")
    with open('hiscore.txt', 'r') as f:
        hiscore = f.read()
    g_exit = False
    g_over = False
    snake_x = 45
    snake_y = 40
    velocity_x = 0
    velocity_y = 0
    food_x = rd.randint(10, screen_width / 2)
    food_y = rd.randint(10, screen_height / 2)
    init_velocity = 5
    snake_size = 10
    fps = 30
    score = 0

    snk_list = []
    snk_length = 1

    while not g_exit:
        if g_over:
            with open('hiscore.txt', 'w') as f:
                f.write(str(hiscore))
            win.fill(white)
            win.blit(overback, (0, 0))
            text_screen("Press Enter to continue.", white, 180, 480)
            text_screen("High Score: " + str(hiscore), white, 180, 520)
            text_screen("Your Score: " + str(score), white, 180, 540)

            for i in pg.event.get():
                if i.type == pg.QUIT:
                    g_exit = True
                if i.type == pg.KEYDOWN:
                    if i.key == pg.K_RETURN:
                        welcome()
        else:
            for i in pg.event.get():
                if i.type == pg.QUIT:
                    g_exit = True

                if i.type == pg.KEYDOWN:
                    if i.key == pg.K_RIGHT:
                        velocity_x = 5
                        velocity_y = 0
                    if i.key == pg.K_LEFT:
                        velocity_x = -5
                        velocity_y = 0
                    if i.key == pg.K_UP:
                        velocity_x = 0
                        velocity_y = -5
                    if i.key == pg.K_DOWN:
                        velocity_x = 0
                        velocity_y = 5

            snake_x += velocity_x
            snake_y += velocity_y

            if abs(snake_x - food_x) < 12 and abs(snake_y - food_y) < 12:
                score += 10
                pg.mixer.Channel(0).play(pg.mixer.Sound('food.mp3'), maxtime=700)
                food_x = rd.randint(10, screen_width / 2)
                food_y = rd.randint(10, screen_height / 2)
                snk_length += 4
                if score > int(hiscore):
                    hiscore = score

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list) > snk_length:
                del snk_list[0]

            if head in snk_list[:-1]:
                g_over = True
                pg.mixer.music.load("over.mp3")
                pg.mixer.music.play()

            if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
                g_over = True
                pg.mixer.music.load("over.mp3")
                pg.mixer.music.play()

            win.fill(white)
            win.blit(gameback, (0, 0))
            text_screen("Score: " + str(score) + "High score: " + str(hiscore), red, 5, 5)
            pg.draw.rect(win, red, [food_x, food_y, snake_size, snake_size])

            plot_snake(win, black, snk_list, snake_size)

        pg.display.update()
        clock.tick(fps)

    pg.quit()
    quit()


welcome()
