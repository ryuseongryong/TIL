
#! 2. 튜플
# x = tuple() 빈 튜플 생성
x = (1,2,3)
y = ("a","b","c")
z = (4,"d",5,"e")

print(x, y, z)
# list의 함수들을 고대로 사용할 수 있다.
print(x + y)
print("a" in y)
print(z.index(4))
# list와 차이점은 assignment가 불가능하다는 것이다.
# 즉 list는 mutable, tuple은 immutable하다.
# x[0] = 4 -> 에러 발생