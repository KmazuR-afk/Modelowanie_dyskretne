import numpy as np
import pygame
import pygame_gui

from Automaton import Automaton

# Wymiary okna
WIDTH, HEIGHT = 800, 800
panel_width = 200
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LINE_COL = (200, 200, 200)
TEXT_COLOR = (0, 0, 0)
ONE = (0, 255, 0)
TWO = (255, 255, 0)
THREE = (255, 165, 0)
FOUR = (255, 0, 0)

# Inicjalizacja Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH + panel_width, HEIGHT))
font = pygame.font.SysFont(None, 24)
manager = pygame_gui.UIManager((WIDTH + panel_width, HEIGHT))


# Funkcja do rysowania planszy
def draw_board(board, plane_size):
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == 255:
                color = BLACK
            elif board[row][col] == 1:
                color = ONE
            elif board[row][col] == 2:
                color = TWO
            elif board[row][col] == 3:
                color = THREE
            elif board[row][col] == 0:
                color = WHITE  # Jeśli brak wartości, tło białe
            else:
                color = FOUR
            # Rysowanie kwadratu na planszy
            pygame.draw.rect(screen, color, (col * plane_size, row * plane_size, plane_size, plane_size))
def draw_LBM(board, plane_size):
    for row in range(len(board)):
        for col in range(len(board[0])):
            #if not np.array_equal(board[row][col],[255,255,255]):
            pygame.draw.rect(screen, board[row][col], (col * plane_size, row * plane_size, plane_size, plane_size))

def draw_panel(fps_text, probability_text):
    pygame.draw.rect(screen, (50, 50, 50), (WIDTH, 0, panel_width, HEIGHT))  # Rysujemy panel boczny
    y_offset = 10
    labels = [
        ("ONE", ONE),
        ("TWO", TWO),
        ("THREE", THREE),
        ("FOUR", FOUR),
    ]

    for label, color in labels:
        text = font.render(f"{label}", True, color)
        screen.blit(text, (WIDTH + 10, y_offset))
        y_offset += 40


def create_buttons():
    start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WIDTH + 10, 250), (panel_width - 20, 40)),
                                                text='Start', manager=manager)
    stop_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WIDTH + 10, 300), (panel_width - 20, 40)),
                                               text='Stop', manager=manager)
    reset_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WIDTH + 10, 350), (panel_width - 20, 40)),
                                                text='Reset', manager=manager)
    return start_button, stop_button, reset_button


def create_input_fields():
    fps_input = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((WIDTH + 10, 150), (panel_width - 20, 30)),
        manager=manager)
    probability_input = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((WIDTH + 10, 200), (panel_width - 20, 30)),
        manager=manager)
    return fps_input, probability_input


def draw_automaton(board, plane_size,fps_text, probability_text):
    screen.fill(WHITE)
    draw_board(board, plane_size)
    draw_panel(fps_text, probability_text)
    manager.update(pygame.time.get_ticks())  # Update UI manager
    manager.draw_ui(screen)  # Rysowanie UI na ekranie
    pygame.display.flip()

def draw_LBM_Panel(board, plane_size):
    screen.fill(WHITE)
    draw_LBM(board, plane_size)
    manager.update(pygame.time.get_ticks())  # Update UI manager
    manager.draw_ui(screen)  # Rysowanie UI na ekranie
    pygame.display.flip()

def add_pattern(board, top_left_row, top_left_col, choice=0):
    for i in range(-5, 5):
        for j in range(-5, 5):
            row, col = top_left_row + i, top_left_col + j
            if 0 <= row < len(board) and 0 <= col < len(board[0]):
                if board[row][col] == 255:
                    board[row][col] = choice
    return board


def simul(automaton):
    plane_size = WIDTH // automaton.grid_size
    pen_down = False
    running = True
    simulation_running = False  # Flaga informująca, czy symulacja jest w trakcie
    clock = pygame.time.Clock()
    fps = 10
    probability = automaton.particle_prob
    fps_text = f"FPS: {fps}"
    probability_text = f"Prawdopodobieństwo: {probability}%"

    start_button, stop_button, reset_button = create_buttons()
    fps_input, probability_input = create_input_fields()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if mouse_x < WIDTH and mouse_y < HEIGHT:
                    row, col = mouse_y // plane_size, mouse_x // plane_size
                    automaton.state = add_pattern(automaton.state, row, col)
                    pen_down = True
            elif event.type == pygame.MOUSEBUTTONUP:
                pen_down = False
            elif event.type == pygame.MOUSEMOTION and pen_down:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if mouse_x < WIDTH and mouse_y < HEIGHT:
                    row, col = mouse_y // plane_size, mouse_x // plane_size
                    automaton.state = add_pattern(automaton.state, row, col)

            manager.process_events(event)

            if start_button.check_pressed():
                simulation_running = True
            if stop_button.check_pressed():
                simulation_running = False
            if reset_button.check_pressed():
                simulation_running = False
                automaton.reset()
                reset_button.disable()
                reset_button.enable()

            if fps_input.get_text() != fps_text.split(": ")[1]:
                fps_text = f"FPS: {fps_input.get_text()}"
                try:
                    fps = int(fps_input.get_text())
                except ValueError:
                    pass
            if probability_input.get_text() != probability_text.split(": ")[1]:
                probability_text = f"Prawdopodobieństwo: {probability_input.get_text()}"
                try:
                    automaton.particle_prob = float(probability_input.get_text())/100
                except ValueError:
                    pass  # Nie zmieniać prawdopodobieństwa, jeśli tekst nie jest liczbą

        # Jeśli symulacja jest aktywna, przeprowadzamy kroki propagacji i kolizji
        if simulation_running:
            automaton.propagate()
            automaton.collide()

        draw_automaton(automaton.state, plane_size, fps_text, probability_text)
        clock.tick(fps)

    pygame.quit()

def simul_LBM(LBM):
    plane_size = WIDTH // LBM.size
    pen_down = False
    running = True
    simulation_running = False  # Flaga informująca, czy symulacja jest w trakcie
    clock = pygame.time.Clock()
    fps = 10
    fps_text = f"FPS: {fps}"


    start_button, stop_button, reset_button = create_buttons()
    fps_input,_= create_input_fields()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            manager.process_events(event)

            if start_button.check_pressed():
                simulation_running = True
            if stop_button.check_pressed():
                simulation_running = False
            if reset_button.check_pressed():
                simulation_running = False
                LBM.reset()
                reset_button.disable()
                reset_button.enable()

            if fps_input.get_text() != fps_text.split(": ")[1]:
                fps_text = f"FPS: {fps_input.get_text()}"
                try:
                    fps = int(fps_input.get_text())
                except ValueError:
                    pass

        # Jeśli symulacja jest aktywna, przeprowadzamy kroki propagacji i kolizji
        if simulation_running:
            LBM.step()


        draw_LBM_Panel(LBM.map, plane_size)
        clock.tick(fps)

    pygame.quit()


#automat=Automaton(200,0.5)
#simul(automat)