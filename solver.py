import pygame, sys
from pygame.locals import *

soduko = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
          [6, 0, 0, 1, 9, 5, 0, 0, 0],
          [0, 9, 8, 0, 0, 0, 0, 6, 0],
          [8, 0, 0, 0, 6, 0, 0, 0, 3],
          [4, 0, 0, 8, 0, 3, 0, 0, 1],
          [7, 0, 0, 0, 2, 0, 0, 0, 6],
          [0, 6, 0, 0, 0, 0, 2, 8, 0],
          [0, 0, 0, 4, 1, 9, 0, 0, 5],
          [0, 0, 0, 0, 8, 0, 0, 7, 9]]

window_multiplier = 10
window_size = 81
window_width = window_size * window_multiplier
window_height = window_size * window_multiplier
square_size = int((window_size * window_multiplier) / 3)
cell_size = int(square_size / 3)
number_size = int(cell_size / 3)

# Set up the colours
black = (0, 0, 0)
white = (255, 255, 255)
light_gray = (200, 200, 200)


def matrix_print(matrix, title="Matrix"):
    print(f"\n {title}:")
    for row in matrix:
        print('     ', ' '.join(map(str, row)))


def draw_grid():
    for i in [cell_size, square_size]:
        for x in range(0, window_width, i):  # draw vertical lines
            pygame.draw.line(display_surface, light_gray if i == cell_size else black, (x, 0), (x, window_height))
        for y in range(0, window_height, i):  # draw horizontal lines
            pygame.draw.line(display_surface, light_gray if i == cell_size else black, (0, y), (window_width, y))

    return None


def initiate_cells():
    grid = {}
    full_cell = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    for xCoord in range(0, 9):
        for yCoord in range(0, 9):
            grid[xCoord, yCoord] = list(full_cell)
    return grid


def display_cells(grid):
    global soduko
    for item in grid:
        data = grid[item]
        for number in data:
            populate_cells(soduko[item[0]][item[1]], (item[1] * cell_size) + number_size,
                           (item[0] * cell_size) + number_size)


def possible(y, x, n):
    global soduko
    for i in range(0, 9):
        if soduko[y][i] == n:
            return False
    for i in range(0, 9):
        if soduko[i][x] == n:
            return False
    x0 = (x // 3) * 3
    y0 = (y // 3) * 3
    for i in range(0, 3):
        for j in range(0, 3):
            if soduko[y0 + i][x0 + j] == n:
                return False
    return True


def solver():
    global currentGrid
    for y in range(9):
        for x in range(9):
            if soduko[y][x] == 0:
                for n in range(1, 10):
                    if possible(y, x, n):
                        soduko[y][x] = n
                        solver()
                        soduko[y][x] = 0
                return
    matrix_print(soduko, "Solved")
    display_surface.fill(white)
    draw_grid()
    display_cells(currentGrid)


def populate_cells(cell, x, y):
    cell_surf = font.render('%s' % cell, True, black)
    cell_rect = cell_surf.get_rect()
    cell_rect.topleft = (x, y)
    display_surface.blit(cell_surf, cell_rect)


def main():
    pygame.init()
    global display_surface, font
    display_surface = pygame.display.set_mode((window_width, window_height))
    font_size = 24
    font = pygame.font.Font('freesansbold.ttf', font_size)

    pygame.display.set_caption('Sudoku Solver')

    matrix_print(soduko)
    solver()
    while True:  # main game loop
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()


if __name__ == '__main__':
    currentGrid = initiate_cells()
    main()
