# package = modules의 합, ==library
# module = 코드를 모아서 기능 하나를 구현해 놓은 파일

# animal package
# dog, cat modules
# dog, cat modules can say "hi"

# from animal import dog
# from animal import cat

from animal import *

d = dog.Dog() # dog파일의 Dog class를 instance로 만든 것
d.hi()

c = cat.Cat()
c.hi()