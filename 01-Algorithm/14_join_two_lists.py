def solution(s1, list1, s2, list2):
    p1 = p2 = 0
    c = []
    while p1 < s1 and p2 < s2:
        if list1[p1] <= list2[p2]:
            c.append(list1[p1])
            p1 += 1
        else:
            c.append(list2[p2])
            p2 += 1
    if p1 < s1:
        c = c + list1[p1:]
    if p2 < s2:
        c = c + list2[p2:]

    print(c)


solution(3, [1, 3, 5], 5, [2, 3, 6, 7, 9])
