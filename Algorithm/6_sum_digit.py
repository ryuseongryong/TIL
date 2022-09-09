def solution(n, var_list):
    def digit_sum(n):
        sum_num = 0
        for i in str(n):
            sum_num += int(i)
        return sum_num

    max_num = -((2**31) - 1)
    for x in var_list:
        total = digit_sum(x)
        if total > max_num:
            max_num = total
            res = x
    print(res)


solution(3, [125, 1532, 97])
