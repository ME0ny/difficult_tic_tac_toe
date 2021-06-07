import pygame
from pygame.constants import CONTROLLER_BUTTON_LEFTSTICK
from pygame.scrap import put

def check_win(field):
    for i in range(4):
        if (sum(field[i]) == -4 or sum(field[i]) == 4):
            return (field[i][0])
    for i in range(4):
        summ = sum([field[j][i] for j in range(4)])
        if (summ == -4 or summ == 4):
            return (summ // 4)
    summ = sum([field[j][j] for j in range(4)])
    if (summ == -4 or summ == 4):
        return (summ // 4)
    summ = sum([field[j][3 - j] for j in range(4)])
    if (summ == -4 or summ == 4):
        return (summ // 4)
    return (0)

def score_count(field):
    scores = [0, 0]
    for i in range(4):
        for j in range(4):
            if (j < 2):
                if (field[i][j] == -1 and field[i][j + 1] == -1 and field[i][j + 2] == -1):
                    scores[1] += 1
                if (field[i][j] == 1 and field[i][j + 1] == 1 and field[i][j + 2] == 1):
                    scores[0] += 1
            if (i < 2):
                if (field[i][j] == -1 and field[i + 1][j] == -1 and field[i + 2][j] == -1):
                    scores[1] += 1
                if (field[i][j] == 1 and field[i + 1][j] == 1 and field[i + 2][j] == 1):
                    scores[0] += 1
            if (j < 2 and i < 2):
                if (field[i][j] == -1 and field[i + 1][j + 1] == -1 and field[i + 2][j + 2] == -1):
                    scores[1] += 1
                if (field[i][j] == 1 and field[i + 1][j + 1] == 1 and field[i + 2][j + 2] == 1):
                    scores[0] += 1
            if (j > 1 and i < 2):
                if (field[i][j] == -1 and field[i + 1][j - 1] == -1 and field[i + 2][j - 2] == -1):
                    scores[1] += 1
                if (field[i][j] == 1 and field[i + 1][j - 1] == 1 and field[i + 2][j - 2] == 1):
                    scores[0] += 1
    return (scores)

def init(caption):
    pygame.init()
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption(caption)
    clock = pygame.time.Clock()
    return screen, clock

WIN_WIDTH = 500
WIN_HEIGHT = 500
FPS = 30
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (200, 200, 200)

screen, clock = init('Гонки')
start_image = pygame.image.load("wallpaper.png").convert()
field_image = pygame.image.load("field.png").convert()
tic = pygame.image.load("Tic.png").convert_alpha()
tac = pygame.image.load("Tac.png").convert_alpha()
run = True
player = pygame.Rect(58, 58, 94, 94)
mouse_pos = [0, 0]
field = [[0, 0, 0, 0] for i in range(4)]
field_pos = [0, 0]
click_flag = False
turn = 1
turn_count = 0
basic_font = pygame.font.SysFont(None, 36)
result = 0
while run:
    screen.fill(WHITE)
    screen.blit(start_image, (0, 0))
    # обработка событий мыши  клавиатуры:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = event.pos
        if event.type == pygame.MOUSEBUTTONDOWN and click_flag == False:
            click_flag = True
        if event.type == pygame.MOUSEBUTTONUP:
            click_flag = False
 
    if (mouse_pos[0] >= 58 and mouse_pos[0] <= 442 and mouse_pos[1] >= 58 and mouse_pos[1] <= 442 and result == 0):
        field_pos = [(mouse_pos[0] - 58) // 98, (mouse_pos[1] - 58) // 98]
        if (click_flag == True):
            if (field[field_pos[1]][field_pos[0]] == 0):
                field[field_pos[1]][field_pos[0]] = int(turn)
                player.x = field_pos[0] * 98  + 58 - field_pos[0]
                player.y = field_pos[1] * 98  + 58 - field_pos[1]
                turn /= -1
                turn_count += 1

    if (result == 0):
        result = check_win(field)
    if (turn_count == 16 and result == 0):
        scores = score_count(field)
        if (scores[0] > scores[1]):
            result = 1
        elif (scores[0] < scores[1]):
            result = -1
        else:
            result = -2
        turn_count += 1
    if (result == -1):
        winner = "Победил игрок Нолик"
    elif (result == 1):
        winner = "Победил игрок Крестик"
    elif (result == -2):
        winner = "Ничья"
    if (result != 0):
        text = basic_font.render(winner, True, WHITE, BLUE)
        text_pos = (100, 10)
        screen.blit(text, text_pos)
    for i in range(5):
        pygame.draw.line(screen, BLACK, (56 + 97 * i, 55), (56 + 97 * i, 445), 3)
    for i in range(5):
        pygame.draw.line(screen, BLACK, (55, 56 + 97 * i), (445, 56 + 97 * i), 3)
    for i in range(4):
        for j in range(4):
            if field[i][j] == 1:
                screen.blit(tac, (j * 98  + 58 - j + 12, i * 98  + 58 - i + 10))
            elif field[i][j] == -1:
                screen.blit(tic, (j * 98  + 58 - j + 15, i * 98  + 58 - i + 14))
    # конец прорисовки окна
    pygame.display.update()
    clock.tick(10)