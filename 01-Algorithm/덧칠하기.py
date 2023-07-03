def solution(n, m, section):
    rolling = m

    count = {target: 0 for target in section}
    answer = 0

    for i in count:
        # print(i, count[i])
        if count[i] == 0:
            for j in range(i, i + rolling):
                # print(j)
                if j in count:
                    count.update({j: 1})
            answer += 1
        #         print(count)
        # print("after", section)
        print("after", count)

    print(answer)
    return answer


def solution2(n, m, section):
    answer = 1
    prev = section[0]
    for sec in section:
        print(sec, prev, sec - prev)
        if sec - prev >= m:
            prev = sec
            answer += 1
            print(sec, prev)

    return answer


# solution(8, 4, [2, 3, 6])
solution2(8, 4, [2, 3, 6])
