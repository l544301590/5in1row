# -*-coding:utf-8-*-
import json


# side: -1(无子), 0(对方), 1(己方)
board = [[0 for j in range(15)] for i in range(15)]
enemy_list = []
my_list = []
DEPTH = 3
MIN = -99999999
MAX = 99999999


def min_max(depth, side, alpha, beta):
    res = 0

    if depth == 0:
        return evaluation(side)

    candidates = gen_list()
    if side == 1:  # 己方，求最大
        for x, y in candidates:
            board[x][y] = side  # 在(x, y)处落子
            alpha = max(alpha, min_max(depth-1, 1-side, alpha, beta))
            board[x][y] = -1    # 撤回(x, y)处的落子
            if beta <= alpha:  # 剪枝，之后的兄弟结点就不用算了
                break
        res = alpha
    else:
        for x, y in candidates:
            board[x][y] = side
            beta = min(beta, min_max(depth-1, 1-side, alpha, beta))
            board[x][y] = -1
            if beta <= alpha:
                break
        res = beta

    return res


def decide(depth):
    res_x, res_y, _max = -1, -1, MIN
    candidates = gen_list()
    for x, y in candidates:
        board[x][y] = 1
        value = min_max(depth, 0, MIN, MAX)
        if value > _max:
            _max = value
            res_x, res_y = x, y
        board[x][y] = -1
    return res_x, res_y


def gen_list():
    res = []
    return res


def evaluation(side):
    pass


if __name__ == '__main__':
    # 解析读入的JSON
    full_input = json.loads(input())

    # 分析自己收到的输入和自己过往的输出，并恢复状态
    all_requests = full_input["requests"]
    all_responses = full_input["responses"]
    for i in range(len(all_responses)):
        myInput = all_requests[i]  # i回合我的输入
        myOutput = all_responses[i]  # i回合我的输出
        placeAt(myInput['x'], myInput['y'], -1)
        placeAt(myOutput['x'], myOutput['y'], 1)
        list1.append((myOutput['x'], myOutput['y']))
        list2.append((myInput['x'], myInput['y']))
        list3.append((myOutput['x'], myOutput['y']))
        list3.append((myInput['x'], myInput['y']))
    # 对面的最后一手输入， -1 表示序列最后一项
    curr_input = all_requests[-1]
    placeAt(curr_input['x'], curr_input['y'], -1)
    list2.append((curr_input['x'], curr_input['y']))
    list3.append((curr_input['x'], curr_input['y']))
    last_point = (curr_input['x'], curr_input['y'])
    i = len(all_responses)
    # 如果现在进行到第三手
    if i>=2:
        # 己方换手或者对方换手
        # 则改变前两手棋色
        if all_responses[1]['x'] == -1 or all_requests[2]['x'] == -1:
            for j in range(2):
                placeAt(all_requests[j]['x'], all_requests[j]['y'], 1)
                placeAt(all_responses[j]['x'], all_responses[j]['y'], -1)
                list1.remove((all_responses[j]['x'],all_responses[j]['y']))
                list2.remove((all_requests[j]['x'], all_requests[j]['y']))
                list1.append((all_requests[j]['x'],all_requests[j]['y']))
                list2.append((all_responses[j]['x'], all_responses[j]['y']))

    for i in range(15):
        for j in range(15):
            list_all.append((i,j))
    # 复原棋盘后获取棋盘所有空的位置，方便最后decide()

    # for i in range(15):
    #     print('第{0: >2}行'.format(i), end=' ')
    #     for j in range(15):
    #         print('{0: >3}'.format(Grid[j][i]), end='')
    #     print()

    #f1 = open('/test.txt', 'a')

    # 我方先手 默认下（7，7）
    x, y = 7, 7
    if not(all_requests[0]['x'] == -1 and len(all_responses) == 0):
        x, y = decide(DEPTH)
    board[x][y] = 1

    my_action = {"x": x, "y": y}
    print(json.dumps({
        "response": my_action,
    }))