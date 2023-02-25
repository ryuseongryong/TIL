# 포인터란?
- memory address
- 변수를 선언하면 메모리 영역에 공간이 할당되고, 그 메모리 영역의 주소를 가리키는 것이 포인터
- 포인터 변수는 메모리 주소를 값으로 가짐

# 인스턴스란?
- 메모리의 실체
- 변수를 선언하면 변수의 자료형 크기만큼 메모리가 할당됨
- 인스턴스는 그 할당된 메모리의 실체를 가리키는 말

# 포인터는 왜 사용하나
- 포인터를 사용하여 메모리 영역에 직접 접근하여 인스턴스를 조작할 수 있음
- 포인터 타입을 반환하는 함수를 사용할 때는 사용할 수 밖에 없음
- 인스턴스를 메모리에 통채로 복사해서 사용할 때, 인스턴스의 주소만 넘겨 메모리 낭비를 줄일 떄 사용할 수 있다.

# &(ampersand) operator
- `&variable` 형식으로 사용
- `variable`을 보고, `variable`이 가리키는 메모리 주소에 액세스 권한을 주게 됨
- 즉 `variable`이 메모리에 있는 해당 `variable` 자체를 가리키고 있고 그 `variable`은 특정 램 주소에 존재하고 있고, `ampersand`가 있는 경우 `variable`이 존재하는 메모리 주소로 접근을 가능하게 해줌
- `&variable`를 출력하면 메모리 주소를 볼 수 있음
- "Give me the memory address of the value this variable is pointing at"
```
# 생략하여 사용하는 방법
jimPointer := &jim
jimPointer.updateName("jimmy")
## jimPointer : Type of *person, or a pointer to a person

jim.updateName("jimmy')
## jim : Type of person

func(pointerToPerson *Person) updateName() 
## *person : Type of *person, or a pointer to a person
```

# *(asterisk) operator
- `*pointer` 형식으로 사용
- `asterisk`뒤에 메모리 주소나 포인터를 배치하여 사용함
- 해당 메모리 주소, 포인터에서 가리키는 값을 요청하는 것임
- "Give me the value this memory address is pointing at"
```
func (pointerToPerson *person) updateName() {
    *pointerToPerson
}

# *person : type description,'person'에 대한 포인터로 작업할 것을 의미함
# *pointerToPerson : an operator, 포인터가 참조하는 값을 조작할 것임을 뜻함
```
