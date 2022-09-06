def solution(n, val_list):
    avg_val = sum(val_list) / n
    avg_val = int(avg_val + 0.5)
    min_val = (2**31) - 1
    for idx, val in enumerate(val_list):
        temp = abs(val - avg_val)
        if temp < min_val:
            min_val = temp
            score = val
            index = idx + 1
        elif temp == min_val:
            if val > score:
                score = val
                index = idx + 1
    print(avg_val, index)


"""
round는 round_half_even 방식
round(4.5) == 4
round(5.5) == 6

따라서 round대신 int() +0.5를 사용하는 것이 더 정확하다.
"""
print(round(5.5))
