# -*-coding:utf-8-*-
# EMPTY = 7
# W = 35
# WW = 800
# WWW = 15000
# WWWW = 800000
crt1 = [7, 35, 800, 15000, 800000]  # 自己落子
# B = 15
# BB = 400
# BBB = 1800
# BBBB = 100000
crt2 = [7, 15, 400, 1800, 100000]  # 对手落子
# INVALID = 0
# BW = 0


def play(board, side):
    """
    对当前棋局的每一个格子试探性落子进行评分

    总分数 = 试探性下黑子前黑方得分 + 试探性下白子前白方得分

    对于包含试探性落子处的某一个五元组：
    以下B表示黑子看，W表示白子
    EMPTY, W, WW, WWW, WWWW, BW, B, BB, BBB, BBBB, INVALID
    WWW - 表示落子前，在五个空格内将有三个白子
    BW - 表示落子前，在五个空格内将有黑白混合
    EMPTY - 表示落子前，五元组为空
    INVALID - 表示五元组超出棋盘范围

    :param board:
    :return:
    """
    x, y = 0, 0
    table = value_table(board, side)  # 评分表
    # 找到评分表中最大值的坐标
    max_v = 0
    for i in range(15):
        for j in range(15):
            if table[i][j] > max_v:
                max_v = table[i][j]
                x, y = i, j

    return x, y, table


def value_table(board, side):
    """

    :param board: 当前棋局
    :param side: 当前哪一方下子
    :return:
    """
    table = [[0 for j in range(15)] for i in range(15)]

    for i in range(15):
        for j in range(15):
            if board[i][j] == -1:
                value = value_(board, i, j, crt1, side) + value_(board, i, j, crt2, 1 - side)
                table[i][j] = value

    return table


def value_(board, x, y, crt, side):
    # 所有得分累加在这个变量res中
    res = 0

    # 复杂的遍历开始了 @.@
    for i in range(5):
        o, n = 0, 0
        try:
            for o in range(-4 + i, -4 + i + 5):
                if x + o < 0:  # 下标越界（下标为负数在python中是合法的，需要另行判断）
                    raise IndexError  # 此处IndexError是为了另行判断下标为负的情况
                if board[x + o][y] == 1 - side:  # 若出现对方棋子，则不得分，即不执行res += ...
                    raise IndexError  # 此处IndexError是为了break，并跳过res += crt[n]这句话
                if board[x + o][y] == side:  # 若是自己的棋子，则计数
                    n += 1
            res += crt[n]
        except IndexError:
            continue

    for i in range(5):
        o, n = 0, 0
        try:
            for o in range(-4 + i, -4 + i + 5):
                if y + o < 0:
                    raise IndexError
                if board[x][y + o] == 1 - side:
                    raise IndexError
                if board[x][y + o] == side:
                    n += 1
            res += crt[n]
        except IndexError:
            continue

    for i in range(5):
        o, n = 0, 0
        try:
            for o in range(-4 + i, -4 + i + 5):
                if x + o < 0 or y + o < 0:
                    raise IndexError
                if board[x + o][y + o] == 1 - side:
                    raise IndexError
                if board[x + o][y + o] == side:
                    n += 1
            res += crt[n]
        except IndexError:
            continue

    for i in range(5):
        o, n = 0, 0
        try:
            for o in range(-4 + i, -4 + i + 5):
                if x + o < 0 or y - o < 0:
                    raise IndexError
                if board[x + o][y - o] == 1 - side:  # 若出现对方棋子，则不执行res += ...
                    raise IndexError
                if board[x + o][y - o] == side:
                    n += 1
            res += crt[n]
        except IndexError:
            continue

    return res


if __name__ == '__main__':
    import json

    b = [[-1 for j in range(15)] for i in range(15)]

    # 解析读入的JSON
    full_input = json.loads(input())

    # 分析自己收到的输入和自己过往的输出，并恢复状态
    all_requests = full_input["requests"]
    all_responses = full_input["responses"]

    for i in range(len(all_responses)):
        myInput = all_requests[i]  # i回合我的输入
        myOutput = all_responses[i]  # i回合我的输出
        b[myInput["x"]][myInput["y"]] = 0
        b[myOutput["x"]][myOutput["y"]] = 1

    x, y = 8, 8
    curr_input = all_requests[-1]
    if curr_input["x"] >= 0 and curr_input["y"] >= 0:
        b[curr_input["x"]][curr_input["y"]] = 0
        x, y, table = play(b, 1)
    else:
        b[8][8] = 1

    my_action = {"x": x, "y": y}
    print(json.dumps({
        "response": my_action
    }))
