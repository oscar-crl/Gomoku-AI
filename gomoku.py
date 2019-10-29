#!/usr/bin/python3
import sys


class Game:
    board = []
    size = 0
    score = [0, 10, 100, 1000, 100000]


def begin():
    if Game.size == 0:
        print("ERROR message - Game isn't started")
        return
    ai_turn()


def board():
    if Game.size == 0:
        print("ERROR message - Game isn't started")
        return
    while 1:
        pos = input().upper()
        if pos == 'DONE':
            break
        try:
            if pos.split(',')[2] == '1':
                Game.board[int(pos.split(',')[1])][int(pos.split(',')[0])] = '1'
            elif pos.split(',')[2] == '2':
                Game.board[int(pos.split(',')[1])][int(pos.split(',')[0])] = '-1'
            else:
                print('ERROR message - Not a valid stone')
        except IndexError:
            print('ERROR message - Syntax error')
        except ValueError:
            print('ERROR message - Value error')
    ai_turn()


def score_row(y, x, stone, final_row, obstructed):
    if final_row > 4:
        final_row = 4
    if Game.board[y][x] == '.':
        if final_row == 4 and stone == '1':
            Game.board[y][x] = Game.score[final_row] * 100
        if obstructed == 2:
            Game.board[y][x] = Game.score[final_row] * 10
        elif obstructed == 0 and final_row <= 3:
            Game.board[y][x] = Game.score[final_row] / 10
        else:
            Game.board[y][x] = Game.score[final_row]
    else:
        if final_row == 4 and stone == '1':
            Game.board[y][x] += Game.score[final_row] * 100
        if obstructed == 2:
            Game.board[y][x] += Game.score[final_row] * 10
        elif obstructed == 0 and final_row <= 3:
            Game.board[y][x] += Game.score[final_row] / 10
        else:
            Game.board[y][x] += Game.score[final_row]


def out_of_board(y, x):
    if y >= Game.size or x >= Game.size or y < 0 or x < 0:
        return 1


def x_axis(y, x, stone):
    row = [0, 0, 0, 0]
    for i in range(4):
        if out_of_board(y, x - i - 1) == 1:
            break
        if Game.board[y][x - i - 1] == stone:
            row[0] += 1
        elif Game.board[y][x - i - 1] != '1' and Game.board[y][x - i - 1] != '-1':
            row[1] = 1
            break
        else:
            break
    for i in range(4):
        if out_of_board(y, x + i + 1):
            break
        if Game.board[y][x + i + 1] == stone:
            row[2] += 1
        elif Game.board[y][x + i + 1] != '1' and Game.board[y][x + i + 1] != '-1':
            row[3] = 1
            break
        else:
            break
    score_row(y, x, stone, row[0] + row[2], row[1] + row[3])


def y_axis(y, x, stone):
    row = [0, 0, 0, 0]
    for i in range(4):
        if out_of_board(y - i - 1, x):
            break
        if Game.board[y - i - 1][x] == stone:
            row[0] += 1
        elif Game.board[y - i - 1][x] != '1' and Game.board[y - i - 1][x] != '-1':
            row[1] = 1
            break
        else:
            break
    for i in range(4):
        if out_of_board(y + i + 1, x):
            break
        if Game.board[y + i + 1][x] == stone:
            row[2] += 1
        elif Game.board[y + i + 1][x] != '1' and Game.board[y + i + 1][x] != '-1':
            row[3] = 1
            break
        else:
            break
    score_row(y, x, stone, row[0] + row[2], row[1] + row[3])


def diagonal_top_axis(y, x, stone):
    row = [0, 0, 0, 0]
    for i in range(4):
        if out_of_board(y + i + 1, x + i + 1):
            break
        if Game.board[y + i + 1][x + i + 1] == stone:
            row[0] += 1
        elif Game.board[y + i + 1][x + i + 1] != '1' and Game.board[y + i + 1][x + i + 1] != '-1':
            row[1] = 1
            break
        else:
            break
    for i in range(4):
        if out_of_board(y - i - 1, x - i - 1):
            break
        if Game.board[y - i - 1][x - i - 1] == stone:
            row[2] += 1
        elif Game.board[y - i - 1][x - i - 1] != '1' and Game.board[y - i - 1][x - i - 1] != '-1':
            row[3] = 1
            break
        else:
            break
    score_row(y, x, stone, row[0] + row[2], row[1] + row[3])


def diagonal_bottom_axis(y, x, stone):
    row = [0, 0, 0, 0]
    for i in range(4):
        if out_of_board(y - i - 1, x + i + 1):
            break
        if Game.board[y - i - 1][x + i + 1] == stone:
            row[0] += 1
        elif Game.board[y - i - 1][x + i + 1] != '1' and Game.board[y - i - 1][x + i + 1] != '-1':
            row[1] = 1
            break
        else:
            break
    for i in range(4):
        if out_of_board(y + i + 1, x - i - 1):
            break
        if Game.board[y + i + 1][x - i - 1] == stone:
            row[2] += 1
        elif Game.board[y + i + 1][x - i - 1] != '1' and Game.board[y + i + 1][x - i - 1] != '-1':
            row[3] = 1
            break
        else:
            break
    score_row(y, x, stone, row[0] + row[2], row[1] + row[3])


def get_mv(y, x, stone):
    x_axis(y, x, stone)
    y_axis(y, x, stone)
    diagonal_top_axis(y, x, stone)
    diagonal_bottom_axis(y, x, stone)


def get_stone(stone):
    for y in range(Game.size):
        for x in range(Game.size):
            if Game.board[y][x] == stone:
                if out_of_board(y, x + 1) != 1 and Game.board[y][x + 1] != '1' and Game.board[y][x + 1] != '-1':
                    get_mv(y, x + 1, stone)
                if out_of_board(y, x - 1) != 1 and Game.board[y][x - 1] != '1' and Game.board[y][x - 1] != '-1':
                    get_mv(y, x - 1, stone)
                if out_of_board(y + 1, x) != 1 and Game.board[y + 1][x] != '1' and Game.board[y + 1][x] != '-1':
                    get_mv(y + 1, x, stone)
                if out_of_board(y - 1, x) != 1 and Game.board[y - 1][x] != '1' and Game.board[y - 1][x] != '-1':
                    get_mv(y - 1, x, stone)
                if out_of_board(y + 1, x + 1) != 1 and Game.board[y + 1][x + 1] != '1' and Game.board[y + 1][x + 1] != '-1':
                    get_mv(y + 1, x + 1, stone)
                if out_of_board(y - 1, x - 1) != 1 and Game.board[y - 1][x - 1] != '1' and Game.board[y - 1][x - 1] != '-1':
                    get_mv(y - 1, x - 1, stone)
                if out_of_board(y + 1, x - 1) != 1 and Game.board[y + 1][x - 1] != '1' and Game.board[y + 1][x - 1] != '-1':
                    get_mv(y + 1, x - 1, stone)
                if out_of_board(y - 1, x + 1) != 1 and Game.board[y - 1][x + 1] != '1' and Game.board[y - 1][x + 1] != '-1':
                    get_mv(y - 1, x + 1, stone)


def play_turn(y, x):
    print('%d,%d' % (x, y))
    Game.board[y][x] = '1'


def best_move(best):
    for y in range(Game.size):
        for x in range(Game.size):
            if Game.board[y][x] != '.' and Game.board[y][x] != '1' and Game.board[y][x] != '-1':
                if int(Game.board[y][x]) > best[0]:
                    best[0] = int(Game.board[y][x])
                    best[1] = y
                    best[2] = x


def reset_score():
    for y in range(Game.size):
        for x in range(Game.size):
            if Game.board[y][x] != '.' and Game.board[y][x] != '1' and Game.board[y][x] != '-1':
                Game.board[y][x] = '.'


def ai_turn():
    best = [0, 10, 10]
    reset_score()
    get_stone('1')
    get_stone('-1')
    best_move(best)
    play_turn(best[1], best[2])


def get_turn(protocol):
    if Game.size == 0:
        print("ERROR message - Game isn't started")
        return
    protocol = protocol.split(' ')[1]
    try:
        Game.board[int(protocol.split(',')[1])][int(protocol.split(',')[0])] = '-1'
    except IndexError:
        print('ERROR message - Syntax error')
        return
    except ValueError:
        print('ERROR message - Value error')
        return
    ai_turn()


def start(protocol):
    if Game.size != 0:
        print('ERROR message - Already started')
        return 84
    try:
        Game.size = int(protocol.split(' ')[1])
    except ValueError:
        print('ERROR message - Syntax error')
        return 84
    if Game.size > 20 or Game.size < 5:
        print('ERROR message - Wrong board size')
        return 84
    Game.board = [['.' for x in range(Game.size)] for y in range(Game.size)]
    print('OK')


def print_board():
    for y in range(Game.size):
        print('MESSAGE -', end='')
        for x in range(Game.size):
            if Game.board[y][x] == '.':
                print('|__.__', end='')
            elif Game.board[y][x] == '1':
                print('|__o__', end='')
            elif Game.board[y][x] == '-1':
                print('|__x__', end='')
            elif int(Game.board[y][x]) < 0:
                print('|%05d' % int(Game.board[y][x]), end='')
            else:
                print('|%05d' % int(Game.board[y][x]), end='')
        print('|')


def main():
    while 1:
        try:
            protocol = input().upper()
            if protocol == 'BEGIN':
                begin()
                continue
            if protocol.find('START ') == 0:
                start(protocol)
                continue
            if protocol.find('TURN ') == 0:
                get_turn(protocol)
                continue
            if protocol == 'BOARD':
                board()
                continue
            if protocol.find('INFO') == 0:
                continue
            if protocol == 'ABOUT':
                print('name="btzrBrain", version="420.0", author="BTZR_GANG", country="FR"')
                continue
            if protocol == 'END':
                return 0
            print('ERROR message - %s' % protocol)
        except EOFError:
            return 0


if __name__ == "__main__":
    main()
