#!/usr/bin/env python3


# by:
# Mohammadreza Shayganfar,
# Mohammad Madannezhad,
# Sam Riahi

# 2024-01-28


BOARD_WIDTH  = 4
BOARD_HEIGHT = 4

NEW_CELLS_PER_ROUND = 1
NEW_CELLS_START     = 2

NEW_CELL_WEIGHTS = {        # 2 is 9 times as likely to spawn as 4
    2: 9,
    4: 1
}


from random import choice
from copy import deepcopy


board = []
score = 0

for row in range(BOARD_HEIGHT):
    board += [[0] * BOARD_WIDTH]

random_numbers = []
for entry in NEW_CELL_WEIGHTS:
    random_numbers += [entry] * NEW_CELL_WEIGHTS[entry]


def move(cells):

    new_cells = cells.copy()

    keep_iterating = True

    while keep_iterating:

        keep_iterating = False

        for i in range(0, len(new_cells)-1):

            if new_cells[i+1] and not new_cells[i]:

                new_cells[i] = new_cells[i+1]
                new_cells[i+1] = 0

                keep_iterating = True

    return new_cells


def merge(cells):

    global score

    new_cells = cells.copy()

    for i in range(0, len(new_cells)-1):

        if new_cells[i] == new_cells[i+1]:

            new_cells[i] += new_cells[i+1]
            new_cells[i+1] = 0

            score += new_cells[i]

    return new_cells


def swipe(direction):

    global board

    cells = []

    if direction == 0 or direction == 1: # UP/DOWN

        for col in range(BOARD_WIDTH):

            cells = [board[row][col] for row in range(BOARD_HEIGHT)]

            if direction == 1: # DOWN (should invert the list)
                cells.reverse()

            cells = move(merge(move(cells)))

            if direction == 1: # DOWN (should invert the list)
                cells.reverse()

            for row in range(BOARD_HEIGHT):
                board[row][col] = cells[row]

    elif direction == 2 or direction == 3: # LEFT/RIGHT

        for row in range(BOARD_HEIGHT):

            cells = board[row].copy()

            if direction == 3: # RIGHT (should invert the list)
                cells.reverse()

            cells = move(merge(move(cells)))

            if direction == 3: # RIGHT (should invert the list)
                cells.reverse()

            board[row] = cells.copy()


def add_random_cell():

    global board, random_numbers

    empty_cells = []

    for row in range(BOARD_HEIGHT):
        for col in range(BOARD_WIDTH):

            if not board[row][col]:
                empty_cells += [(row, col)]

    if empty_cells:

        cell = choice(empty_cells)
        board[cell[0]][cell[1]] = choice(random_numbers)


def get_state():

    global board

    # check if the player has won (1)

    for row in board:
        for cell in row:

            if cell == 2048:
                return 1

    # otherwise, check if the player can keep playing (0)

    #   check if there are empty cells

    for row in board:
        for cell in row:

            if not cell:
                return 0

    #   if there are no empty cells, check if any cells can be merged

    #       check horizontally

    for row in range(BOARD_HEIGHT):
        for col in range(BOARD_WIDTH-1):

            if board[row][col] == board[row][col+1]:
                return 0

    #       check vertically

    for row in range(BOARD_HEIGHT-1):
        for col in range(BOARD_WIDTH):

            if board[row][col] == board[row+1][col]:
                return 0

    # otherwise, the player has lost (2)

    return 2


def handle_state(state):

    if state == 0:
        return
    elif state == 1:
        print("YOU WON")
    elif state == 2:
        print("YOU LOST")

    exit()


def print_board():

    global board

    for row in board:

        # top border of each row
        print("+------" * BOARD_WIDTH + "+")
        print("|      " * BOARD_WIDTH + "|")

        for cell in row:
            if cell:
                print("| % 4d " % cell, end="")
            else:
                print("|      ", end="")

        # right border of the right cell
        print("|")

        # bottom of each row
        print("|      " * BOARD_WIDTH + "|")

    # bottom border of the board
    print("+------" * BOARD_WIDTH + "+")


def main():

    try:

        for i in range(NEW_CELLS_START):
            add_random_cell()

        while True:

            print("")
            print_board()
            print("SCORE: " + str(score))
            print("")

            handle_state(get_state())

            print("enter a command:")
            print("L (LEFT) / R (RIGHT) / U (UP) / D (DOWN) / Q (QUIT)")
            print("")

            previous_board = deepcopy(board)

            cmd = (input(":").upper() + " ")[0]

            if cmd == "Q":
                exit()

            elif cmd == "U":
                swipe(0)

            elif cmd == "D":
                swipe(1)

            elif cmd == "L":
                swipe(2)

            elif cmd == "R":
                swipe(3)

            # make sure the move resulted in a change before adding new cells

            if board != previous_board:
                for i in range(NEW_CELLS_PER_ROUND):
                    add_random_cell()

    except (KeyboardInterrupt, EOFError):

        exit()


if __name__ == "__main__":

    main()
