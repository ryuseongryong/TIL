def solution(n, m):
    count = [0] * (n + m + 3)
    max_num = -((2**31) - 1)
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            count[i + j] += 1
    for i in range(n + m + 1):
        if count[i] > max_num:
            max_num = count[i]
    for i in range(n + m + 1):
        if count[i] == max_num:
            print(i)


solution(4, 6)
