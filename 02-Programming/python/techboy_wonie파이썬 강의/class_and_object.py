# class = function + variable, 빵틀
# object = class를 이용해 만들어낸 물체, 빵, object == instance

class Person:
  def __init__(self, name, age): # init은 Person obj를 만들 때 name 인자를 받아서 name 변수에 할당
      self.name = name
      self.age = age
  
  def say_hello(self, to_name): 
    print("안녕! "+ to_name + " 나는 " + self.name)
    
  def introduce(self):
    print("내 이름은 " + self.name + "이야, 나는 " + str(self.age) + "살이야!")
    

# 상속 inherit
class Police(Person): #Police class가 Person class를 상속받겠다. = Person의 내용을 모두 상속 받음
  def arrest(self, to_arrest):
    print("넌 체포됐다! " + to_arrest + "! 손 들어! 꼼짝마!")
    
class Programmer(Person):
  def program(self, to_program):
    print("이번 프로젝트는 " + to_program + "이군! 열심히 해보자!")
    
seongryong = Person("성룡", 30)
michael = Police("마이클", 40)
jenny = Programmer("제니", 25)

seongryong.say_hello("철수")
michael.say_hello("영희")
jenny.say_hello("미자")

seongryong.introduce()
michael.introduce()
jenny.introduce()

michael.arrest("성룡")
jenny.program("이메일 클라이언트")