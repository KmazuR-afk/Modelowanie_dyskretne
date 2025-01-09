import pygame
import sys
from pygame import mouse
from PIL import Image

import db_con
from Environment import Environment
from Hunters import Hunter
def lock_obj(board):
    rows,cols=board.shape
    hunters=[]
    exits=[]
    id=0
    for y in range(rows):
        for x in range(cols):
            if(board[y][x]==3):
                hunters.append((id,x,y))
                id+=1
            elif(board[y][x]==5):
                exits.append((x,y))
    print(hunters)
    return hunters,exits
WIDTH, HEIGHT = 800, 800
LEGEND = 200
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LINE_COL = (200, 200, 200)
TEXT_COLOR = (0, 0, 0)
DEFAULT = (200, 200, 200)
ACTIVE = (100, 100, 100)

ALIVE = (218, 165, 32)
DEAD = (100,100,0)
HUNTER=(255,0,0)
EXIT=(0,255,0)


font = None
screen = None

patterns = {
    "1x1": [[1]],
    "3x3": [[1, 1, 1], [1, 1, 1], [1, 1, 1]],
    "blank": [[0]],
    "escapee": [[2]],
    "hunter":[[3]],
    "exit":[[5]],
}

pressed = None

# Slider variables for controlling simulation speed
slider_rect = pygame.Rect(WIDTH + 50, 180, 100, 10)  # Position of slider
slider_knob = pygame.Rect(WIDTH + 100, 175, 10, 20)  # Knob for the slider
slider_value = 1  # Slider value
speed_factor = 1  # Factor to control speed of simulation

def add_pattern(board, pattern, top_left_row, top_left_col):
    for i, row in enumerate(pattern):
        for j, cell in enumerate(row):
            if 0 <= top_left_row + i < len(board) and 0 <= top_left_col + j < len(board[0]):
                board[top_left_row + i][top_left_col + j] = cell
    return board

def draw_slider():
    pygame.draw.rect(screen, LINE_COL, slider_rect)  # Draw slider track
    pygame.draw.rect(screen, BLACK, slider_knob)  # Draw the knob on the slider

def draw_board(board, plane_size):
    screen.fill(WHITE)
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == 1:
                color = BLACK
            elif board[row][col]==2:
                color=ALIVE
            elif board[row][col] == 3:
                color = HUNTER
            elif board[row][col]==4:
                color=DEAD
            elif board[row][col] == 5:
                color = EXIT
            else:  color=WHITE
            pygame.draw.rect(screen, color, (col * plane_size, row * plane_size, plane_size, plane_size))
    #for row in range(len(board) + 1):
        #pygame.draw.line(screen, LINE_COL, (0, row * plane_size), (WIDTH, row * plane_size), 2)
    #for col in range(len(board[0]) + 1):
        #pygame.draw.line(screen, LINE_COL, (col * plane_size, 0), (col * plane_size, HEIGHT), 2)

def draw_legend():
    legend_x = WIDTH + 20
    lines = [
        "Legenda klawiszy:",
        "0 - rysowanie ścian 1x1",
        "1 - rysowanie 3x3",
        "2 - usuwanie ścian",
        "4 - łowca",
        "5 - exit",
        "Backspace - wyczyszczenie planszy",
        "Enter - uruchomienie gry"
    ]
    y = 20
    for line in lines:
        text_surface = font.render(line, True, TEXT_COLOR)
        screen.blit(text_surface, (legend_x, y))
        y += 30

    pygame.draw.rect(screen, ACTIVE if pressed == "Save" else DEFAULT, (legend_x, y, 150, 50))
    p_text = font.render("Save", True, TEXT_COLOR)
    screen.blit(p_text, (legend_x + 20, y + 10))


def simulate(board, hunters, escapees, exits, conn):
    global font, screen
    pygame.init()
    font = pygame.font.Font(None, 24)
    screen = pygame.display.set_mode((WIDTH + LEGEND, HEIGHT))
    pygame.display.set_caption('Rysowanie labiryntu')
    global slider_rect,slider_knob,slider_value
    escp_starting_pos = []
    obj_hunters = []
    slider_dragging=False
    for hunter in hunters:
        obj_hunters.append(Hunter(hunter[0], None, hunter[1], hunter[2]))

    env = Environment(board, conn, obj_hunters, escapees, exits)
    for hunter in obj_hunters:
        hunter.environment = env
    for escape in escapees:
        escape.environment = env
        escp_starting_pos.append((escape.pos_x, escape.pos_y))
        escape.print_info()

    running = True
    paused = False
    plane_size = WIDTH // len(board[0])
    clock = pygame.time.Clock()
    old_escapes = escapees.copy()

    while running:
        # Draw the board and slider
        draw_board(env.map, plane_size)
        sim_legend()  # Draw the slider for controlling speed
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # End the game
                    running = False
                    for escp in escapees:
                        db_con.save_q_table(conn, escp.q_table, escp.escapee_id)  # Save Q-tables
                if event.key == pygame.K_SPACE:  # Pause the game
                    paused = not paused
                if event.key == pygame.K_TAB:  # Restart game
                    clear_esp(board)
                    escapees = old_escapes.copy()
                    for escp in escapees:
                        x, y, wtd = place_escapee(board)
                        if wtd:
                            escp.set_state(x, y)
                        else:
                            escapees.remove(escp)
                    env.escapees = escapees
                    old_escapes = escapees.copy()
                if event.key == pygame.K_1:
                    drawing(50,50,env.map)
                    added_hunters,added_exits=lock_obj(env.map)
                    print(len(obj_hunters)-len(added_hunters))
                    dif_h=len(obj_hunters)-len(added_hunters)
                    if dif_h!=0:
                        for i in range (0,dif_h):
                            obj_hunters.append(Hunter(added_hunters[i+len(env.hunters)][0],None,added_hunters[i+len(env.hunters)][1],added_hunters[i+len(env.hunters)][2]))
                            obj_hunters[i+len(obj_hunters)].environment=env
                        env.hunters = obj_hunters


            # Handle slider knob dragging
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if slider_knob.collidepoint(event.pos):
                    slider_dragging = True
            elif event.type == pygame.MOUSEBUTTONUP:
                slider_dragging = False
            elif event.type == pygame.MOUSEMOTION and slider_dragging:
                mouse_x, _ = event.pos
                slider_knob.x = max(min(mouse_x, slider_rect.right - slider_knob.width), slider_rect.left)
                slider_value = int((slider_knob.x - slider_rect.left) / slider_rect.width * 100 - 50)



        # Adjust simulation speed based on slider value
        if not paused:
            env.step()  # Execute one step in the simulation

        clock.tick(51 + slider_value)  # Control the speed with the slider value


def but_usage(mouse_x, mouse_y, l_x=WIDTH + 20, l_y=290):
    global pressed
    if l_x <= mouse_x <= l_x + 150 and l_y <= mouse_y <= l_y + 50:
        pressed = "Save"
        return True
    return False


def save_board(board):
    rows, cols = len(board), len(board[0])
    img = Image.new("RGB", (cols, rows), "white")
    pixels = img.load()
    for row in range(rows):
        for col in range(cols):
            if board[row][col] == 1:
                color = BLACK
            elif board[row][col] == 2:
                color = ALIVE
            elif board[row][col] == 3:
                color = HUNTER
            elif board[row][col] == 4:
                color = DEAD
            elif board[row][col] == 5:
                color = EXIT
            else:
                color = WHITE
            pixels[col, row] = color
    img.save("obrazek.png")
    print("Plansza zapisana jako 'default.png'.")

def draw_legend_escp():
    global slider_rect,slider_knob
    legend_x = WIDTH + 20
    lines = [
        "Legenda klawiszy:",
        "ENTER - zapisanie pozycji ",
        "ESC - zakończ dodawanie"
    ]

    y = 20
    for line in lines:
        text_surface = font.render(line, True, TEXT_COLOR)
        screen.blit(text_surface, (legend_x, y))
        y+=30
def place_escapee(board):
    global font, screen
    pygame.init()
    font = pygame.font.Font(None, 24)
    screen = pygame.display.set_mode((WIDTH + LEGEND, HEIGHT))
    pygame.display.set_caption('Rysowanie labiryntu')
    rows, cols = len(board), len(board[0])
    plane_size = WIDTH // cols  # Rozmiar komórki w pikselach
    selected_pattern = "escapee"
    pen_down = False
    x, y = None, None  # Pozycja w macierzy (kolumna, wiersz)

    while True:
        draw_board(board, plane_size)  #
        draw_legend_escp()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return x, y, True

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if mouse_x < WIDTH and mouse_y < HEIGHT:
                    if x!=None and y!=None:
                        board[y][x] = 0
                    row, col = mouse_y // plane_size, mouse_x // plane_size
                    if board[row][col] == 0:
                        board = add_pattern(board, patterns[selected_pattern], row, col)
                        x, y = col, row

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return x, y, True
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return x, y, False
def drawing(rows=50,cols=50,board=None):
    global font,screen
    pygame.init()
    font = pygame.font.Font(None, 24)
    screen = pygame.display.set_mode((WIDTH + LEGEND, HEIGHT))
    pygame.display.set_caption('Rysowanie labiryntu')
    plane_size = WIDTH // cols
    if board is None:
        board=[[0 for i in range(cols)] for j in range(rows)]
    selected_pattern = "1x1"
    pen_down=False
    while True:
        draw_board(board, plane_size)
        draw_legend()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = mouse.get_pos()
                if mouse_x < WIDTH and mouse_y < HEIGHT:
                    row, col = mouse_y // plane_size, mouse_x // plane_size
                    board = add_pattern(board, patterns[selected_pattern], row, col)
                    pen_down = True
                else:
                    if but_usage(mouse_x, mouse_y):
                        save_board(board)
                        pygame.quit()
            elif event.type == pygame.MOUSEBUTTONUP:
                pen_down=False
            elif event.type == pygame.MOUSEMOTION and pen_down:
                mouse_x, mouse_y = mouse.get_pos()
                if mouse_x < WIDTH and mouse_y <HEIGHT:
                    row, col = mouse_y // plane_size, mouse_x // plane_size
                    board = add_pattern(board, patterns[selected_pattern], row, col)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_0:
                    selected_pattern = "1x1"
                elif event.key == pygame.K_1:
                    selected_pattern = "3x3"
                elif event.key == pygame.K_2:
                    selected_pattern = "blank"

                elif event.key == pygame.K_4:
                    selected_pattern = "hunter"
                elif event.key == pygame.K_5:
                    selected_pattern = "exit"
                elif event.key == pygame.K_BACKSPACE:
                    board = [[1 for i in range(cols)] for j in range(rows)]
                elif event.key == pygame.K_RETURN:
                    return board
                    pygame.quit()


def sim_legend():
    legend_x = WIDTH + 20
    lines = [
        "Legenda klawiszy:",
        "ENTER - zapisanie pozycji i zakończenie gry ",
        "SPACE - zatrzymanie gry/wznowienie gry",
        "TAB - restart",
        "1 - edycja planszy"
    ]

    y = 20
    for line in lines:
        text_surface = font.render(line, True, TEXT_COLOR)
        screen.blit(text_surface, (legend_x, y))
        y += 30
    pygame.draw.rect(screen, LINE_COL, slider_rect)  # Draw slider track
    pygame.draw.rect(screen, BLACK, slider_knob)
def clear_esp(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 2:
                board[i][j] = 0
