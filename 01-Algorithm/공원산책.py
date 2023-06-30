def solution(park, routes):
    x = 0
    y = 0

    for i in range(len(park)):
        for j in range(len(park[i])):
            if park[i][j] == "S":
                x = j
                y = i
                break

    for route in routes:
        xx = x
        yy = y

        for move in range(int(route[2])):
            if route[0] == "E" and xx != len(park[0]) - 1 and park[yy][xx + 1] != "X":
                xx += 1
                if move == int(route[2]) - 1:
                    x = xx
            elif route[0] == "W" and xx != 0 and park[yy][xx - 1] != "X":
                xx -= 1
                if move == int(route[2]) - 1:
                    x = xx
            elif route[0] == "S" and yy != len(park) - 1 and park[yy + 1][xx] != "X":
                yy += 1
                if move == int(route[2]) - 1:
                    y = yy
            elif route[0] == "N" and yy != 0 and park[yy - 1][xx] != "X":
                yy -= 1
                if move == int(route[2]) - 1:
                    y = yy
    return [y, x]
