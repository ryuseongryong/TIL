def solution(n, dice_list):
    res = 0
    for i in range(n):
        temp = dice_list[i]
        temp.sort()
        a, b, c = map(int, temp)
        if a == b and b == c:
            money = 10000 + (a * 1000)
        elif a == b or a == c:
            money = 1000 + (a * 100)
        elif b == c:
            money = 1000 + (b * 100)
        else:
            money = c * 100
        if money > res:
            res = money
    print(res)


solution(3, [[3, 3, 6], [2, 2, 2], [6, 2, 5]])
