# -*-coding:utf-8-*-



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
        x, y = play(b, 1)
    else:
        b[8][8] = 1

    my_action = {"x": x, "y": y}
    print(json.dumps({
        "response": my_action
    }))
