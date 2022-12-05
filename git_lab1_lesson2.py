import pygame
from copy import deepcopy

class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, scr):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == 1:
                    scr.fill((0, 255, 0), [self.left + self.cell_size * j,
                                           self.top + self.cell_size * i,
                                           self.cell_size, self.cell_size])
                else:
                    scr.fill((0, 0, 0), [self.left + self.cell_size * j,
                                           self.top + self.cell_size * i,
                                           self.cell_size, self.cell_size])
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                pygame.draw.rect(scr, (255, 255, 255), (self.left + self.cell_size * j,
                                                        self.top + self.cell_size * i,
                                                        self.cell_size, self.cell_size), 1)

class Life(Board):
    def __init__(self, width, height):
        super().__init__(width, height)

    def left_mouse_check(self, pos, scr):
        if pos[0] > self.width * self.cell_size + self.left or pos[0] < self.left or \
                pos[1] > self.height * self.cell_size + self.top or pos[1] < self.top:
            return None
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.left + self.cell_size * j <= pos[0] <= self.left + self.cell_size * (j + 1) and \
                        self.top + self.cell_size * i <= pos[1] <= self.top + self.cell_size * (i + 1):
                    if self.board[i][j] == 0:
                        scr.fill((0, 255, 0), [self.left + self.cell_size * j,
                                               self.top + self.cell_size * i,
                                               self.cell_size, self.cell_size])
                        self.board[i][j] = 1
        pygame.display.flip()

    def game_move(self):
        current_board = deepcopy(self.board)
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                count = 0
                if i + 1 != 25 and self.board[i + 1][j] == 1:
                    count += 1
                if i - 1 != -1 and self.board[i - 1][j] == 1:
                    count += 1
                if j + 1 != 25 and self.board[i][j + 1] == 1:
                    count += 1
                if j - 1 != -1 and self.board[i][j - 1] == 1:
                    count += 1
                if i + 1 != 25 and j + 1 != 25 and self.board[i + 1][j + 1] == 1:
                    count += 1
                if i - 1 != -1 and j - 1 != -1 and self.board[i - 1][j - 1] == 1:
                    count += 1
                if i + 1 != 25 and j - 1 != -1 and self.board[i + 1][j - 1] == 1:
                    count += 1
                if i - 1 != -1 and j + 1 != 25 and self.board[i - 1][j + 1] == 1:
                    count += 1
                print(count)
                if self.board[i][j] == 1:
                    if count > 3 or count < 2:
                        current_board[i][j] = 0
                elif self.board[i][j] == 0:
                    if count == 3:
                        current_board[i][j] = 1
        self.board = deepcopy(current_board)

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Игра «Жизнь»')
    size = width, height = 800, 800
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    fps = 15

    life = Life(25, 25)
    running = True
    game_start = False
    left_btn = True
    screen.fill((0, 0, 0))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not game_start:
                    life.left_mouse_check(event.pos, screen)
                elif event.button == 3 and left_btn:
                    left_btn = False
                    game_start = True
            if event.type == pygame.MOUSEWHEEL:
                fps += event.y * 2
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    left_btn = False
                    game_start = not game_start
            if event.type == pygame.QUIT:
                running = False
        if game_start:
            life.game_move()
        clock.tick(fps)
        life.render(screen)
        pygame.display.flip()

    pygame.quit()
