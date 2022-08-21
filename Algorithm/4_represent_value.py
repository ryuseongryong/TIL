def solution(n, val_list):
    avg_val = round(sum(val_list) / n)
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
