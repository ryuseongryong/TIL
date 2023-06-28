def solution(players, callings):
    for i, _x in enumerate(callings):
        a = players.index(callings[i])
        if i != len(callings) - 1:
            b = players.index(callings[i + 1])

        if a - 1 != b:
            players[a], players[a - 1] = players[a - 1], players[a]
    print(players)
    return players


def solution2(players, callings):
    players_dict = {player: rank for rank, player in enumerate(players)}
    ranks_dict = {rank: player for rank, player in enumerate(players)}
    print(players_dict)
    print(ranks_dict)

    for call in callings:
        rank = players_dict[call]

        players_dict[ranks_dict[rank - 1]], players_dict[ranks_dict[rank]] = (
            players_dict[ranks_dict[rank]],
            players_dict[ranks_dict[rank - 1]],
        )
        ranks_dict[rank - 1], ranks_dict[rank] = ranks_dict[rank], ranks_dict[rank - 1]

    print(list(ranks_dict.values()))
    return list(ranks_dict.values())


solution(["mumu", "soe", "poe", "kai", "mine"], ["kai", "kai", "mine", "mine"])
solution2(["mumu", "soe", "poe", "kai", "mine"], ["kai", "kai", "mine", "mine"])
