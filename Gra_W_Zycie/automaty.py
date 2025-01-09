patterns = {
    "kom":[[1]],
    "glider": [
        [0, 1, 0],
        [0, 0, 1],
        [1, 1, 1]
    ],
    "blinker": [
        [1, 1, 1]
    ],
    "toad": [
        [0, 1, 1, 1],
        [1, 1, 1, 0]
    ],
    "beacon": [
        [1, 1, 0, 0],
        [1, 1, 0, 0],
        [0, 0, 1, 1],
        [0, 0, 1, 1]
    ],
    "pulsar": [
        [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
        # pozostałe rzędy...
    ],
    "Glider gun":[
        [0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0,0,0,0,1,0,0,0,0,0, 0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0,0,1,0,1,0,0,0,0,0, 0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0, 0,0,1,1,0,0,0,0,0,0, 1,1,0,0,0,0,0,0,0,0, 0,0,0,0,1,1,0,0],
        [0,0,0,0,0,0,0,0,0,0,0, 0,1,0,0,0,1,0,0,0,0, 1,1,0,0,0,0,0,0,0,0, 0,0,0,0,1,1,0,0],
        [0,1,1,0,0,0,0,0,0,0,0, 1,0,0,0,0,0,1,0,0,0, 1,1,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0],
        [0,1,1,0,0,0,0,0,0,0,0, 1,0,0,0,1,0,1,1,0,0, 0,0,1,0,1,0,0,0,0,0, 0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0, 1,0,0,0,0,0,1,0,0,0, 0,0,0,0,1,0,0,0,0,0, 0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0, 0,1,0,0,0,1,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0, 0,0,1,1,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0],
    ],
    "puffer": [  # Czołg-puffer
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 0],
        [0, 0, 0, 1, 0, 1, 0],
        [0, 0, 0, 0, 1, 0, 0]
    ],
}

# Funkcja do dodania wzorca na planszę w wybranym miejscu
def add_pattern(board, pattern, start_row, start_col):
    rows, cols = len(pattern), len(pattern[0])
    for i in range(rows):
        for j in range(cols):
            if start_row + i < len(board) and start_col + j < len(board[0]):
                board[start_row + i][start_col + j] = pattern[i][j]
    return board

def count_neighbors_reflective(board, row, col):
    rows, cols = len(board), len(board[0])
    neighbors = 0

    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue

            neigh_row=row+i
            neigh_col=col+j
            if 0>neigh_row:
                neigh_row=-neigh_row
            elif neigh_row>=rows:
                neigh_row=2*rows -2 -neigh_row

            if 0>neigh_col:
                neigh_col=-neigh_col
            elif neigh_col>=cols:
                neigh_col=2*cols -2-neigh_col

            neighbors += board[neigh_row][neigh_col]
    return neighbors


def count_neighbors(board, row, col):
    rows, cols = len(board), len(board[0])
    neighbors = 0

    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            neighbor_row = (row + i + rows) % rows
            neighbor_col = (col + j + cols) % cols

            neighbors += board[neighbor_row][neighbor_col]

    return neighbors


def update_board(board,choice=1):
    rows, cols = len(board), len(board[0])
    new_board = [[0 for _ in range(cols)] for _ in range(rows)]

    for row in range(rows):
        for col in range(cols):
            alive = board[row][col]
            if choice == "Periodyczne":
                neighbors = count_neighbors(board, row, col)
            elif choice == "Odbicie":
                neighbors = count_neighbors_reflective(board, row, col)
            if alive:
                if neighbors < 2 or neighbors > 3:
                    new_board[row][col] = 0
                else:
                    new_board[row][col] = 1
            else:
                if neighbors == 3:
                    new_board[row][col] = 1
    return new_board
