import random
from idlelib.configdialog import is_int
import time


def create_gb(clicked, size=8, mines=10):
    gb = [[0 for _ in range(size)] for _ in range(size)]
    ml = []
    while len(ml) < mines:
        mine = (random.randint(0, size - 1), random.randint(0, size - 1))
        if mine not in ml and mine != clicked:
            ml.append(mine)
    dirs = [(-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1)]
    for mine in ml:
        gb[mine[0]][mine[1]] = '*'
        for adir in dirs:
            i = mine[0] + adir[0]
            j = mine[1] + adir[1]
            if 0 <= i < size and 0 <= j < size and gb[i][j] != '*':
                gb[i][j] += 1
    return gb


def revealchain(rvl, gb):
    dirs = [(-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1)]
    checked = []
    c = 0
    for coord in rvl:
        if coord not in checked:
            checked.append(coord)
            for adir in dirs:
                i = coord[0] + adir[0]
                j = coord[1] + adir[1]
                if c < 4:
                    if 0 <= i < len(gb) and 0 <= j < len(gb) and gb[i][j] != '*':
                        rvl.append((i, j))
                else:
                    if 0 <= i < len(gb) and 0 <= j < len(gb) and gb[i][j] == 0:
                        rvl.append((i, j))
        c += 1
    return rvl


def update_gb(dgb, gb, clicked, rvl, safe):
    start = True
    rvl.append(clicked)
    rvl = revealchain(rvl, gb)
    for coord in rvl:
        if coord not in safe:
            if gb[coord[0]][coord[1]] == '*':
                start = False
            dgb[coord[0]][coord[1]] = gb[coord[0]][coord[1]]
        else:
            print('this square is marked')
            rvl.remove(clicked)
    return dgb, gb, rvl, start


def print_gb(gb):
    for i in range(len(gb)):
        print(' '.join([str(gb[i][j]) for j in range(len(gb[i]))]))


def start_game(size=8, mines=10):
    start = True
    dgb = [['■' for _ in range(size)] for _ in range(size)]
    dgb[3][3] = '□'
    cursor = (3, 3)
    print_gb(dgb)
    move_dict = {'w': (-1, 0), 'a': (0, -1), 's': (1, 0), 'd': (0, 1)}
    first = True
    comp = False
    rvl = []
    safe = []
    init_time = time.time()
    while start:
        move = input()
        # wasd controls
        if (move in move_dict and 0 <= cursor[0] + move_dict[move][0] < size and 0 <= cursor[1] + move_dict[move][
            1] < size):
            if cursor not in rvl and cursor not in safe:
                dgb[cursor[0]][cursor[1]] = '■'
            elif cursor in safe:
                dgb[cursor[0]][cursor[1]] = '▲'
            else:
                dgb[cursor[0]][cursor[1]] = gb[cursor[0]][cursor[1]]
            cursor = (cursor[0] + move_dict[move][0], cursor[1] + move_dict[move][1])
            dgb[cursor[0]][cursor[1]] = '□'
        # quit game
        elif move == 'q':
            start = False
        if move == 'e':
            if not first:
                if cursor not in safe:
                    safe.append(cursor)
                    dgb[cursor[0]][cursor[1]] = '▲'
                else:
                    safe.remove(cursor)
            else:
                print('click a square to start first!')
        # coord controls
        elif len(tuple(move)) == 2 and is_int(move) and 0 <= int(move) <= 77:
            move = tuple(move)
            move = [int(move[i]) for i in range(len(move))]
            if 0 <= move[0] < size and 0 <= move[1] < size:
                move = tuple(move)
                dgb[cursor[0]][cursor[1]] = '■'
                cursor = (move[0], move[1])
                dgb[cursor[0]][cursor[1]] = '□'
        # cell clicked!
        elif move == '':
            clicked = cursor
            if first:
                gb = create_gb(clicked, size, mines)
                first = False
            dgb, gb, rvl, start = update_gb(dgb, gb, clicked, rvl, safe)
        # check game success
        if not first:
            for row in dgb:
                if '■' not in row:
                    comp = True
                else:
                    comp = False
                    break
            if comp:
                start = False
        print_gb(dgb)
    if not start and not comp:
        print('womp womp! time:', int(time.time() - init_time))
    elif not start:
        print('yay! time:', int(time.time() - init_time))


if __name__ == '__main__':
    start_game(size=int(input('size: ')), mines=int(input('mines: ')))
