import pygame
from pygame.constants import CONTROLLER_BUTTON_LEFTSTICK
from pygame.scrap import put
pygame.init()

class Window():
    def __init__(self, width = 500, height = 500, fps = 30, name = "TicTac"):
        WIN_WIDTH = 500
        WIN_HEIGHT = 500
        FPS = 30
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.start_image = pygame.image.load("wallpaper.png").convert()
        self.field_image = pygame.image.load("field.png").convert()
        self.tic = pygame.image.load("Tic.png").convert_alpha()
        self.tac = pygame.image.load("Tac.png").convert_alpha()
    def pre_render(self):
        self.screen.fill(WHITE)
        self.screen.blit(self.start_image, (0, 0))
    def render_field(self):
        for i in range(5):
            pygame.draw.line(self.screen, BLACK, (56 + 97 * i, 55), (56 + 97 * i, 445), 3)
        for i in range(5):
            pygame.draw.line(self.screen, BLACK, (55, 56 + 97 * i), (445, 56 + 97 * i), 3)
        for i in range(4):
            for j in range(4):
                if field[i][j] == 1:
                    self.screen.blit(self.tac, (j * 98  + 58 - j + 12, i * 98  + 58 - i + 10))
                elif field[i][j] == -1:
                    self.screen.blit(self.tic, (j * 98  + 58 - j + 15, i * 98  + 58 - i + 14))

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

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (200, 200, 200)

run = True
button = pygame.Rect(189, 467, 122, 23)
mouse_pos = [0, 0]
field = [[0, 0, 0, 0] for i in range(4)]
field_pos = [0, 0]
click_flag = False
turn = 1
turn_count = 0
basic_font = pygame.font.SysFont(None, 36)
btn_font = pygame.font.SysFont(None, 12)
result = 0
step = 0
window = Window()
while run:
    window.pre_render()
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
            click_flag = False
            if (field[field_pos[1]][field_pos[0]] == 0):
                if (step < 2):
                    turn = 1
                    field[field_pos[1]][field_pos[0]] = int(turn)
                elif (step < 4):
                    turn = -1
                    field[field_pos[1]][field_pos[0]] = int(turn)
                step += 1
                step %= 4
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
        window.screen.blit(text, text_pos)
    window.render_field()
    # конец прорисовки окна
    pygame.display.update()
    window.clock.tick(10)