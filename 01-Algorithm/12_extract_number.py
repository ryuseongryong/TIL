def solution(word):
    result = 0
    for str in word:
        if str.isdecimal():
            result = result * 10 + int(str)
    print(result)

    count = 0
    for i in range(1, result + 1):
        if result % i == 0:
            count += 1

    print(count)


solution("t0e0a1c2h0er")
