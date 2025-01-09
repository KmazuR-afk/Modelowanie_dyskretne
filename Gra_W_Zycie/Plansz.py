import pygame
import sys

from pygame import mouse

import automaty

WIDTH, HEIGHT = 800, 800
ROWS, COLS = 200, 200
PLANE_SIZE=WIDTH//COLS
LEGEND = 200
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LINE_COL = (200, 200, 200)
TEXT_COLOR = (0, 0, 0)
DEFAULT=(200, 200, 200)
ACTIVE=(100, 100, 100)
pygame.init()
screen = pygame.display.set_mode((WIDTH+LEGEND, HEIGHT))
pygame.display.set_caption('Gra W Zycie')
font = pygame.font.Font(None, 24)
con="Periodyczne"
def draw_board(board):
    screen.fill(WHITE)
    #pola
    for row in range(ROWS):
        for col in range(COLS):
            color = BLACK if board[row][col]==1 else WHITE
            pygame.draw.rect(screen, color,(col*PLANE_SIZE, row*PLANE_SIZE, PLANE_SIZE, PLANE_SIZE))
    #linie
    for row in range(ROWS+1):
        pygame.draw.line(screen, LINE_COL,(0,row*PLANE_SIZE),(WIDTH,row*PLANE_SIZE),1)
    for col in range(COLS+1):
        pygame.draw.line(screen, LINE_COL,(col*PLANE_SIZE,0),(col*PLANE_SIZE,HEIGHT),1)


def draw_legend():
    legend_x = WIDTH + 20  # Początek legendy z prawej strony planszy
    lines = [
        "Legenda klawiszy:",
        "0 - pojedyńcza komurka",
        "1 - Glider",
        "2 - Blinker",
        "3 - Toad",
        "4 - Beacon",
        "5 - Pulsar",
        "6 - Glider Gun",
        "7 - Puffer brudas",
        "Spacja - Start/Pauza",
        "Backspace - wyczyszczenie planszy"
    ]

    y = 20  # Początkowy odstęp od góry
    for line in lines:
        text_surface = font.render(line, True, TEXT_COLOR)
        screen.blit(text_surface, (legend_x, y))
        y += 30  # Odstęp między wierszami

    pygame.draw.rect(screen, ACTIVE if con=="Periodyczne" else DEFAULT,(legend_x,y,150,50))
    pygame.draw.rect(screen, ACTIVE if con=="Odbicie" else DEFAULT,(legend_x,y+60,150,50))
    p_text=font.render("Periodyczne",True,TEXT_COLOR)
    screen.blit(p_text, (legend_x+20,y+10))
    o_text=font.render("Odbicie",True,TEXT_COLOR)
    screen.blit(o_text, (legend_x + 20, y + 70))
def but_usage(mouse_x,mouse_y,l_x=WIDTH+20,l_y=350):
    global con
    if l_x <= mouse_x<=l_x+150 and l_y <= mouse_y<=l_y+50:
        con="Periodyczne"
    elif l_x <= mouse_x<=l_x+150 and l_y+60 <= mouse_y<=l_y+110:
        con="Odbicie"

def main():
    board=[[0 for _ in range(COLS)] for _ in range(ROWS)]
    running=False
    selected_pattern="glider"
    while True:
        draw_board(board)
        draw_legend()
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = mouse.get_pos()
                if mouse_x<WIDTH and mouse_y<HEIGHT:
                    row, col=mouse_y//PLANE_SIZE, mouse_x//PLANE_SIZE
                    board[row][col]=1
                    board = automaty.add_pattern(board, automaty.patterns[selected_pattern], row, col)
                else:
                    but_usage(mouse_x, mouse_y)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Spacja rozpoczyna/zatrzymuje grę
                    running = not running
                elif event.key == pygame.K_0:
                    selected_pattern = "kom"
                elif event.key == pygame.K_1:
                    selected_pattern = "glider"
                elif event.key == pygame.K_2:
                    selected_pattern = "blinker"
                elif event.key == pygame.K_3:
                    selected_pattern = "toad"
                elif event.key == pygame.K_4:
                    selected_pattern = "beacon"
                elif event.key == pygame.K_5:
                    selected_pattern = "pulsar"
                elif event.key == pygame.K_6:
                    selected_pattern = "Glider gun"
                elif event.key == pygame.K_7:
                    selected_pattern = "puffer"
                elif event.key == pygame.K_BACKSPACE:
                    board=[[0 for _ in range(COLS)] for _ in range(ROWS)]

        if running:
            board = automaty.update_board(board,con)


if __name__ == "__main__":
    main()