def solution(cards):
    a = list(range(21))
    for _ in range(10):
        for card in cards:
            s, e = card[0], card[1]
            for i in range((e - s + 1) // 2):
                a[s + i], a[e - i] = a[e - i], a[s + i]
    a.pop(0)
    for x in a:
        print(x)


solution(
    [[5, 10], [9, 13], [1, 2], [3, 4], [5, 6], [1, 2], [3, 4], [5, 6], [1, 20], [1, 20]]
)
