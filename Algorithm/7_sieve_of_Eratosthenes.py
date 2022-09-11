def solution(n):
    num_list = [0] * (n + 1)
    count = 0
    for i in range(2, n + 1):
        if num_list[i] == 0:
            count += 1
            for j in range(i, n + 1, i):
                num_list[j] = 1
    print(count)


solution(200000)
