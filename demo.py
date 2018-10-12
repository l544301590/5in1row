# -*-coding:utf-8-*-
import tkinter as tk
import tkinter.messagebox
import random
from ai1 import *

offset = 3
piece_r = 17
win_width = 800
win_height = 600
canvas_a = 600
summary_width = 200
summary_height = 600
block_a = canvas_a // 15


class GameWin(tk.Frame):
    def __init__(self, master=None):
        # ***********logically************
        self.status = -1  # 表示尚未开始
        # self.status = 0 表示轮到黑棋下
        # self.status = 1 表示轮到白棋下
        self.board = [[-1 for j in range(15)] for i in range(15)]

        # **********graphically***********
        # 窗口
        tk.Frame.__init__(self, master, width=win_width + offset, height=win_height + offset)
        self.pack()

        # 棋盘
        self.board_canvas = tk.Canvas(self, width=canvas_a + offset, height=canvas_a + offset, bg='#D3D3D3')
        self.board_canvas.pack(side='left')
        self.draw_board()

        # 计分板
        self.summary = tk.Frame(self, width=summary_width + offset, height=summary_height + offset)
        self.summary.pack(side='right')

        # # 每个格子的评分Label
        # self.labels = [[tk.Label(self.board_canvas, text="0000") for j in range(15)] for i in range(15)]
        # for i in range(15):
        #     for j in range(15):
        #         self.labels[i][j].place(relx=block_a * i + (block_a - piece_r * 2) // 2 + offset,
        #                                 rely=block_a * j + (block_a - piece_r * 2) // 2 + offset)

    def draw_board(self):
        for i in range(16):
            self.board_canvas.create_line(i * block_a + offset, 0 + offset, i * block_a + offset, canvas_a + offset)
        for i in range(16):
            self.board_canvas.create_line(0 + offset, i * block_a + offset, canvas_a + offset, i * block_a + offset)

    def draw_piece(self, x, y, side):
        color = 'black'
        if side == 1:
            color = 'white'

        self.board_canvas.create_oval(block_a * x + (block_a - piece_r * 2) // 2 + offset,
                                      block_a * y + (block_a - piece_r * 2) // 2 + offset,
                                      block_a * x + piece_r * 2 + offset,
                                      block_a * y + piece_r * 2 + offset,
                                      fill=color)

    def click_canvas(self, evt):
        x, y = evt.x // 40, evt.y // 40
        if self.board[x][y] == -1:
            self.draw_piece(x, y, 0)

            self.board[x][y] = 0  # 下黑子
            if win(self.board, x, y, 0):
                tk.messagebox.showinfo(title='提示', message='黑子赢')
                self.game_start()
                return

            x, y, table = play(self.board, 1)  # 下白子
            self.draw_piece(x, y, 1)
            self.draw_value_table(table)
            self.board[x][y] = 1  # 下白子
            # self.status = 0
            if win(self.board, x, y, 1):
                tk.messagebox.showinfo(title='提示', message='白子赢')
                self.game_start()
                return

    def draw_value_table(self, table):
        self.board_canvas.delete("text")
        for i in range(15):
            for j in range(15):
                self.board_canvas.create_text(block_a * i + 10 + offset,
                                              block_a * j + 10 + offset,
                                              text=str(table[i][j]),
                                              fill="red",
                                              tags="text")

    def game_start(self):
        self.board = [[-1 for j in range(15)] for i in range(15)]
        self.board_canvas.delete("all")
        self.draw_board()
        self.board_canvas.bind('<Button-1>', self.click_canvas)


def win(grid, x, y, side):
    """
    :param grid: (2D List) 棋盘
    :param x:
    :param y:
    :param side: 0 or 1
    :return: True or False
    """
    for i in range(5):
        o = 0
        try:
            for o in range(-4 + i, -4 + i + 5):
                if x + o < 0:
                    break
                if grid[x + o][y] != side:
                    break
            else:
                return True
        except IndexError:
            continue

    for i in range(5):
        o = 0
        try:
            for o in range(-4 + i, -4 + i + 5):
                if y + o < 0:
                    break
                if grid[x][y + o] != side:
                    break
            else:
                return True
        except IndexError:
            continue

    for i in range(5):
        o = 0
        try:
            for o in range(-4 + i, -4 + i + 5):
                if x + o < 0 or y + o < 0:
                    break
                if grid[x + o][y + o] != side:
                    break
            else:
                return True
        except IndexError:
            continue

    for i in range(5):
        o = 0
        try:
            for o in range(-4 + i, -4 + i + 5):
                if x + o < 0 or y - o < 0:
                    break
                if grid[x + o][y - o] != side:
                    break
            else:
                return True
        except IndexError:
            continue

    return False


if __name__ == '__main__':
    game = GameWin()
    game.game_start()
    tk.mainloop()
