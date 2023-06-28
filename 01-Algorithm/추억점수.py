def solution(name, yearning, photo):
    answer = []
    dictionary = dict(zip(name, yearning))
    for chapters in photo:
        _sum = 0
        for person in chapters:
            if person in dictionary:
                _sum += dictionary[person]
        answer.append(_sum)
    return answer


solution(
    ["may", "kein", "kain", "radi"],
    [5, 10, 1, 3],
    [
        ["may", "kein", "kain", "radi"],
        ["may", "kein", "brin", "deny"],
        ["kon", "kain", "may", "coni"],
    ],
)
solution(
    ["kali", "mari", "don"],
    [11, 1, 55],
    [["kali", "mari", "don"], ["pony", "tom", "teddy"], ["con", "mona", "don"]],
)
solution(
    ["may", "kein", "kain", "radi"],
    [5, 10, 1, 3],
    [["may"], ["kein", "deny", "may"], ["kon", "coni"]],
)
