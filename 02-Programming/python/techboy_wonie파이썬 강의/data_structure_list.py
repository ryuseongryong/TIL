# 자료구조

#! 1. 리스트
# elements를 grouping할 때 사용
# x = list() 빈 배열 생성
x = [1, 2, 3, 4]
y = ["a","b"]
z = ["c", "d", 5, 6]
a = [4, 2, 3, 1]

print(x, y)
print(x + y + z)
print(x[0])
# print(x[4]) list크기 보다 더 큰 것에 접근하면 에러 발생

# 길이를 가져오는 len함수
num_elements = len(x)
print(num_elements)

# 정렬 시켜주는 sorted함수
sorted_a = sorted(a)
print(a)
print(sorted_a)

# 요소들을 합해주는 sum함수
sum_x = sum(x)
print(sum_x)

# loop + list

# list의 elements를 돌아가면서 하나씩 보여줘
for n in a:
  print(n)
  
for s in y:
  print(s)

for some in z:
  print(some)

# list의 element index검색
print(x.index(3))
print(y.index("a"))
# print(a.index(10)) # 없으면 에러발생

# list의 element가 존재하는지 확인
print("a" in y)
print("a" in x)

if "a" in y:
  print("a가 있어요")
