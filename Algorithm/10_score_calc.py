def solution(n, score_list):
    sum = 0
    count = 0
    for score in score_list:
        if score == 1:
            count += 1
            sum += count
        else:
            count = 0
    print(sum)


solution(10, [1, 0, 1, 1, 1, 0, 0, 1, 1, 0])
