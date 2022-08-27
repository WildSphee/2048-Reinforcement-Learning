import numpy as np
import re as regex
import random


# board is the visual presentation of the board, fboard is the flattened version for the ML
class Game:
    def __init__(self, size):
        self.board = []
        self.board_size = size

    def createboard(self):
        self.board = [['' for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.board[random.randint(0, self.board_size - 1)][random.randint(0, self.board_size - 1)] = 2
        self.board[random.randint(0, self.board_size - 1)][random.randint(0, self.board_size - 1)] = 4

    def getboard(self) -> list:
        k = np.reshape(self.board, (1, -1))
        k[k == ''] = 0
        k = list(map(int, k[0]))
        return np.array(k)

    def printboard(self) -> None:
        for r in self.board:
            print(r, '\t')

    # push the array to the left
    def c_dir(self) -> None:
        for r, re in enumerate(self.board):
            # table test for unique values
            table = np.unique(re).tolist()
            table.remove('') if '' in table else ''
            # table = list(filter(('').__ne__, table))
            table = list(map(int, table))

            # turn the list into a text
            t = '_' + '__'.join(map(str, re)) + '_'

            # use regex replace method to combine unique values
            for v in table:
                t = regex.sub(f'_{v}_+{v}_', f'{int(v) * 2}._', t)

            # filter out the '' values
            l = regex.split('\_|\.', t)
            l = list(filter(('').__ne__, l))
            # set size to the board_size
            l += ['' for _ in range(self.board_size)]
            l = l[:self.board_size]

            self.board[r] = l

    # returns whether anything changed on the board
    def push_dir(self, dir=2) -> bool:
        # Apply action
        # 0 = up
        # 1 = down
        # 2 = left
        # 3 = right

        old_board = self.getboard()
        if dir == 2:
            self.c_dir()
        elif dir == 0:
            self.board = np.transpose(self.board).tolist()
            self.c_dir()
            self.board = np.transpose(self.board).tolist()
        elif dir == 3:
            self.board = np.fliplr(self.board).tolist()
            self.c_dir()
            self.board = np.fliplr(self.board).tolist()
        elif dir == 1:
            self.board = np.fliplr(np.transpose(self.board)).tolist()
            self.c_dir()
            self.board = np.transpose(np.fliplr(self.board)).tolist()

        comparison = old_board == self.getboard()
        if comparison.all():
            return False
        else:
            return True

    # place random
    def place_random(self):
        pool = []
        for r in range(self.board_size):
            for c in range(self.board_size):
                if self.board[r][c] == '':
                    pool.append((r, c))

        if len(pool) == 0:
            return

        r, c = random.choice(pool)
        self.board[r][c] = random.choice(['2', '2', '4'])

    # check if the AI lost - no more adjacent tiles with same value
    def check_game_ends(self) -> bool:
        for r in range(self.board_size):
            for c in range(self.board_size):
                if self.board[r][c] == '':
                    return False

                if r < self.board_size - 1:
                    if self.board[r][c] == self.board[r + 1][c]:
                        return False

                if c < self.board_size - 1:
                    if self.board[r][c] == self.board[r][c + 1]:
                        return False
                continue
        return True

    def current_v(self) -> int:
        counts = np.count_nonzero(self.board==0)
        return counts

def main():
    game = Game(size=4)
    game.createboard()
    game.printboard()

    while True:

        old_v = game.current_v()

        u = int(input('please input a direction: '))
        if not game.push_dir(u):
            continue

        print(f'rewards: {game.current_v() - old_v}')

        game.place_random()
        game.printboard()
        if game.check_game_ends():
            break

    print('game ends with the final score of', game.current_v())


if __name__ == '__main__':
    main()
