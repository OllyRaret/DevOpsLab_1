import sys

import pygame
import random


class Tile:
    def __init__(self, number, x, y, speed, size):
        self.number = number
        self.x = x
        self.y = y
        self.speed = speed
        self.size = size
        self.target = [0, 0]
        self.direction = 0
        self.move = False

    def Update(self):
        if self.move and (self.x != self.target[0] or self.y != self.target[1]):
            if self.direction == 0:
                self.y -= self.speed
                if self.y <= self.target[1]:
                    self.y = self.target[1]
                    self.move = False
            elif self.direction == 1:
                self.x -= self.speed
                if self.x <= self.target[0]:
                    self.x = self.target[0]
                    self.move = False
            elif self.direction == 2:
                self.x += self.speed
                if self.x >= self.target[0]:
                    self.x = self.target[0]
                    self.move = False
            else:
                self.y += self.speed
                if self.y >= self.target[1]:
                    self.y = self.target[1]
                    self.move = False


def isWin(matrix, n):
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] != n * n:
                if matrix[i][j] != (i * n + j + 1):
                    return False
    return True


def generateNumbers(matrix, n):
    flags = [False for i in range(n * n)]

    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            matrix[i][j] = random.randint(1, n * n)
            while flags[matrix[i][j] - 1]:
                matrix[i][j] = random.randint(1, n * n)
            flags[matrix[i][j] - 1] = True

    return matrix


GRAY = (100, 100, 100)
WHITE = (255, 255, 255)
RED = (180, 0, 0)

tile_size = 100
tile_speed = 25

indent = 10

n = 4
W = tile_size * n + indent
H = W + 50

gameover = False

fps = 60

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Пятнашки")
clock = pygame.time.Clock()

restart = False

while 1:
    if not gameover:
        restart = False
        numbers = [[0 for j in range(n)] for i in range(n)]

        # num = 1
        # for i in range(n):
        #     for j in range(n):
        #         numbers[i][j] = num
        #         num += 1

        numbers = generateNumbers(numbers, n)

        tiles = []

        for i in range(n):
            for j in range(n):
                if numbers[i][j] == n * n:
                    empty_tile_x = j * tile_size + indent
                    empty_tile_y = i * tile_size + indent
                    empty_tile_i = i
                    empty_tile_j = j
                else:
                    tiles.append(
                        Tile(numbers[i][j], j * tile_size + indent, i * tile_size + indent, tile_speed,
                             tile_size - indent))

    while (not gameover) and (not restart):
        clock.tick(fps)

        screen.fill(WHITE)

        for tile in tiles:
            if tile.number != n * n:
                pygame.draw.rect(screen, GRAY,
                                 (tile.x, tile.y, tile.size, tile.size))

                font = pygame.font.Font(None, 50)
                text = font.render(f"{tile.number}", True, WHITE)
                screen.blit(text, [tile.x, tile.y])

                font = pygame.font.Font(None, 40)
                text = font.render("Esc - начать сначала", True, RED)
                screen.blit(text, [25, H - 40])

        pygame.display.update()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos

                for i in range(len(tiles)):
                    if (not tiles[i].move) and pos[0] > tiles[i].x and pos[1] > tiles[i].y and pos[0] < tiles[i].x + \
                            tiles[i].size and pos[1] < tiles[i].y + tiles[i].size:
                        if tiles[i].x + tile_size == empty_tile_x and tiles[i].y == empty_tile_y:
                            tiles[i].direction = 2
                            tiles[i].move = True

                        elif tiles[i].x - tile_size == empty_tile_x and tiles[i].y == empty_tile_y:
                            tiles[i].direction = 1
                            tiles[i].move = True

                        elif tiles[i].y + tile_size == empty_tile_y and tiles[i].x == empty_tile_x:
                            tiles[i].direction = 3
                            tiles[i].move = True

                        elif tiles[i].y - tile_size == empty_tile_y and tiles[i].x == empty_tile_x:
                            tiles[i].direction = 0
                            tiles[i].move = True

                        if tiles[i].move:
                            tiles[i].target = [empty_tile_x, empty_tile_y]

                            empty_tile_x = tiles[i].x
                            empty_tile_y = tiles[i].y

                            numbers[(tiles[i].x - indent) // tile_size][(tiles[i].y - indent) // tile_size], numbers[empty_tile_i][empty_tile_j] = numbers[empty_tile_i][empty_tile_j], numbers[(tiles[i].x - indent) // tile_size][(tiles[i].y - indent) // tile_size]

                            empty_tile_i, empty_tile_j = (tiles[i].x - indent) // tile_size, (tiles[i].y - indent) // tile_size
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    restart = True

        gameover = isWin(numbers, n)

        for tile in tiles:
            tile.Update()

    if gameover:
        screen.fill(WHITE)

        font = pygame.font.Font(None, W // 10)
        message = font.render('Вы победили!', True, RED, WHITE)
        mes_rect = message.get_rect(center=(W / 2, H / 2))
        screen.blit(message, mes_rect)

        font = pygame.font.Font(None, W // 20)
        message = font.render('Нажмите любую клавишу', True, RED, WHITE)
        mes_rect = message.get_rect(center=(W / 2, H / 2 + H / 3))
        screen.blit(message, mes_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                gameover = False
