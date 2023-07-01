def solution(wallpaper):
    y_position = []
    x_position = []
    for y_idx, line in enumerate(wallpaper):
        for x_idx, paper in enumerate(line):
            if paper == "#":
                y_position.append(y_idx)
                x_position.append(x_idx)
    y_position.sort()
    x_position.sort()

    answer = [y_position[0], x_position[0], y_position[-1] + 1, x_position[-1] + 1]
    return answer


solution([".#...", "..#..", "...#."])
