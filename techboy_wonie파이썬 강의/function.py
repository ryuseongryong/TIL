def chat():
  print("철수: 안녕? 넌 몇 살이니?")
  print("영희: 나는 20")

chat()

def chat2(name1, name2, age):
  print("%s: 안녕? 넌 몇 살이니?" % name1)
  print("%s: 나는 %d" % (name2, age))
  
chat2("???", "성룡", 30)

def dsum(a, b):
  result = a + b
  return result

print(dsum(2, 4))

# 이름과 나이를 받아서 나이에 따른 인사말 구분 출력하기
def sayHello(name, age):
  if(age < 20):
    print("안녕, " + name)
  elif(age >= 20 and age <= 30):
    print("안녕하세요, " + name + "님")
  else:
    print("안녕하십니까! " + name + "님")
    
sayHello("고딩", 18)
sayHello("대딩", 22)
sayHello("초년생", 27)
sayHello("친구", 30)
sayHello("형", 35)