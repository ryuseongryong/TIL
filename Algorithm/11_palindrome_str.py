def solution(num, str_list):
    # for i in range(num):
    #     str = str_list[i]
    #     str = str.upper()
    #     if str == str[::-1]:
    #         print(f"#{(i+1)} YES")
    #     else:
    #         print(f"#{(i+1)} NO")

    for i in range(num):
        s = str_list[i]
        s = s.upper()
        size = len(s)
        for j in range(size // 2):
            if s[j] != s[-1 - j]:
                print(f"#{i+1} NO")
                break
        else:
            print(f"{i+1} YES")


solution(
    5,
    ["level", "moon", "abcba", "soon", "gooG"],
)
