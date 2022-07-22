def solution(n, k, arr):
    non_conflict = set()
    for i in range(n):
        for j in range(i + 1, n):
            for l in range(j + 1, n):
                print(arr[i], arr[j], arr[l])
                non_conflict.add(arr[i] + arr[j] + arr[l])

    non_conflict = list(non_conflict)
    non_conflict.sort(reverse=True)
    print(non_conflict[k - 1])
