def solution(num, str_list):
    for i in range(num):
        str = str_list[0]
        str = str.upper()
        if str == str[::-1]:
            print(f"#{(i+1)} YES")
        else:
            print(f"#{(i+1)} NO")


solution(5, ["level"])
