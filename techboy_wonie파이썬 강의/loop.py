# for, while


for i in range(1):
  print(i)
  print("철수: 안녕 영희야 뭐해?")
  print("영희: 안녕 철수야 그냥 있어")

while i < 3:
  print(i)
  print("철수: 안녕 영희야 뭐해?")
  print("영희: 안녕 철수야 그냥 있어")
  i = i + 1

i = 0
while True:
  print(i)
  print("철수: 안녕 영희야 뭐해?")
  print("영희: 안녕 철수야 그냥 있어")
  i = i + 1
  
  if i > 2:
    break

for i in range(100):
  print(i)
  print("철수: 안녕 영희야 뭐해?")
  print("영희: 안녕 철수야 그냥 있어")
  
  if i > 2:
    break
  
for i in range(3):
  print(i)
  print("철수: 안녕 영희야 뭐해?")
  print("영희: 안녕 철수야 그냥 있어")
  
  if i == 1:
    continue
  
  print("안녕 디지몬")