# type = 숫자, 문자열, Boolean

#! 숫자
x = 1
y = 2
z = 1.2

# 사칙연산
print(x + y)
print(x - y)
print(x * y)
print(x / y)
print(x % y) # 나머지
print(x ** y) # 제곱

#! 문자열
a = "hello"
b = 'bye'
c = """
안녕하세요
성룡입니다
""" # 여러줄 가능

print(a)
print(b)
print(c)

# 더하기를 문자열로 할 수 있음
print( "안녕" + " 잘지내니")

# 문자열과 숫자를 섞어서 쓸 수는 없음
# print( "너 혹시 몇 살이니?" + 4) -> error
print( "너 혹시 몇 살이니? " + str(4)) # -> casting 해서 출력해야함

number = 4
string = '4'
# print(number + string) -> error
print(str(number) + string)
print(number + int(string))

#! Boolean
t = True
f = False
print(t, f)