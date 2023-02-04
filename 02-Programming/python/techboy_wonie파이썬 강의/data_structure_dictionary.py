
#! 3. 딕셔너리
# x = dict(), 빈 딕셔너리 생성
# dict는 key와 value로 이루어져 있음 *js의 Obj
x = {
  "name" : "성룡",
  "age" : 20,
  0 : "한국",
  1 : "파이썬"
  
}

print(x)
print(x["name"])
print(x["age"])
# print(x.age) dot은 안 됨

# key가 dict에 있는지 확인할 수 있음
print("age" in x)

# dict에 포함된 모든 keys/values를 보여주는 함수
print(x.keys())
print(x.values())

# dict에 포함된 key를 돌아가면서 보여주는 반복문
for key in x:
  print("key: ", key)
  print("value: ", x[key])

# dict에 assign가능
x[0] = "Korea" # 기존 키의 값 변경
x["job"] = "Programmer" # 새로운 키/값 입력 가능
print(x)