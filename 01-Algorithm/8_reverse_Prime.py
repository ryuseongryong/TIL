def reverse(n):
    res = 0
    while n > 0:
        m = n % 10
        res = res * 10 + m
        n = n // 10
    return res


def isPrime(n):
    if n == 1:
        return False
    for i in range(2, (n // 2) + 1):
        if n % i == 0:
            return False
    else:
        return True


def solution(n, num_list):
    for m in num_list:
        temp = reverse(m)
        if isPrime(temp):
            print(temp)


solution(5, [32, 55, 62, 3700, 250])
