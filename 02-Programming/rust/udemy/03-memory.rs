// 러스트로 빌드하기 위해서는 메모리가 어떻게 작동하는지 알아야 함.
// 수동 메모리 관리의 기본적인 것들에 대해서
// - 스택
// - 힙
// - 포인터
// - 스마트 포인터

// 1. 스택
// - 각각의 함수에 의해 생성된 변수들을 저장하는 프로세스 메모리 영역
// - 각 함수의 메모리 정보를 스택 프레임이라고 함.
// - 여기에 지역 변수들이 저장되고, 모든 함수 호출에 대한 새로운 스택 프레임이 현재 프레임 위에 할당된다.
// - 스택 프레임을 생성한 함수만 여기에 접근할 수 있고, 그것이 함수의 범위를 지정한다.
// - 스택에 있는 모든 변수들의 크기는 컴파일할 때 알려져 있어야 함.
// - 만약 스택에 배열을 저장하고 싶다면, 배열에 얼마나 많은 요소들이 있는지 정확히 명시해야 한다.
// - 함수가 종료되면 스택 프레임도 해제된다.
// - 이것은 메모리 할당에 대해 걱정할 필요가 없고 알아서 관리한다는 뜻이다.
// 메모리 레이아웃
FUNCTION main {
    INTEGER a = 2
    CALL stack_only(a)
}

FUNCTION stack_only(INTEGER b) {
    INTEGER c = 3
}
// main -> 'a=2' -> stack_only -> 'b=2','c=3'

FUNCTION infinite {
    CALL infinite
}
// infinite -> infinite -> infinite -> 
// stack overflow 발생

// 2. 힙
// - 자동으로 관리되지 않는 프로세스 메모리 영역
// - 수동으로 힙에 메모리를 할당해야 한다.
// - 중요한 것은 사용이 끝나면 그 메모리를 수동으로 해제해야 한다.
// - 할당된 힙 메모리 해제에 실패하면 메모리 누수로 이어질 수 있다.
// - 힙은 크기의 제한이 없다.
// - 스택은 크기의 제한이 있지만 힙에는 방대한 양의 데이터를 저장할 수 있다.
// - 시스템의 물리적인 크기에만 제한을 받는다.
// - 프로그램의 모든 위치에서, 모든 함수에 의해 힙에 접근할 수 있다.
// - 스택에 있는 변수는 그 변수를 할당한 함수에 의해서만 접근 가능하지만, 힙에 있는 모든 것들은 프로그램에 있는 모든 함수에서 접근할 수 있다.
// - 힙에 할당하는 것은 과도한 비용을 초래할 수 있기 때문에 가능하면 피하는 것이 좋다.
// - 만약 프로그램이 힙에 수많은 블록을 할당하고, 해제를 반복하면 결국 힙이 조각난다.
// - 그러면 새로운 위치에 필요한 공간을 효율적으로 찾는 것이 훨씬 더 어려워진다.

FUNCTION main {
    INTEGER a = 2
    CALL stack_only(a)
}

FUNCTION stack_only(INTEGER b) {
    INTEGER c = 3
    CALL stack_and_heap
}

FUNCTION stack_and_heap {
    INTEGER d = 5
    POINTER e = ALLOCATE INTEGER 7
    DEALLOCATE e // <-- 힙 메모리 할당을 해제하는 것이 필수이다.
}
// stack
// main -> 'a=2' -> stack_only -> 'b=2,c=3' -> stack_and_heap -> 'd=5,e=0xf578bb60'
// heap : point와 값을 저장
// '0xf578bb60=>7'
// 힙에 메모리를 저장하고 스택에 해당 값의 주소를 저장하고 함수에서 참조할 수 있게 함
// 하지만 힙에는 메모리를 수동으로 할당해야 함
// 또한 사용이 끝나면 수동으로 해제해야 함
// 위의 경우에는 할당을 해제하지 않음.
// 따라서 스택과 힙의 함수가 종료되면 스택 프레임이 사라지고 포인터도 사라져 다시 힙에 접근할 수 없음.
// 메모리 누수가 발생할 것.
// 그렇기 때문에 반드시 할당 해제를 해줘야한다.
// 이런 수동 메모리 관리는 C, C++의 오래된 버전에서 같은 방법으로 관리하고 있다.
// 방대한 코드의 경우에는 더 처리하기 어렵고 더 많은 오류가 발생할 수 있다.
// 자바스크립트나 자바, go 같이 과도한 런타임을 갖거나 사용되지 않는 메모리를 관리하는 GC가 있는 고수준 언어에서는 문제가 없다.
// 하지만 과도한 런타임은 시스템 언어에서는 선택할 수 없다.
// 그래서 모던 C++과 러스트에서는 스마트 포인터를 사용한다.

// 3. 스마트 포인터
// 스마트 포인터는 추가적인 기능을 제공하는 raw pointer를 감싸는 래퍼이다.
// 스마트 포인터에는 여러 타입이 있지만, 
// 가장 일반적인 것은 포인터가 범위를 벗어났을 때 그것이 가리키는 메모리를 해제하도록 하는 것이다.

FUNCTION main {
    INTEGER a = 2
    CALL stack_only(a)
}

FUNCTION stack_only(INTEGER b) {
    INTEGER c = 3
    CALL stack_and_heap
}

FUNCTION stack_and_heap {
    INTEGER d = 5
    POINTER e = SMART_POINTER(7)
}
// 힙에 메모리를 할당하는 대신 스마트 포인터를 생성한 것이다.

// stack
// main -> 'a=2' -> stack_only -> 'b=2,c=3' -> stack_and_heap -> 'd=5,e=SM(0xf578bb60)'
// heap : point와 값을 저장
// '0xf578bb60=>7'
// 스택 프레임이 종료되면 스마트 포인터도 함께 사라짐

// ------------------------------------------------------------------------------------------------

list main.rs:0
fn main() {
    // Integer 지역 변수 a를 생성해서
    let a = 2;
    // stack_only 함수에 전달
    let result = stack_only(a);
    dbg!(result);
}

// stack_only 함수는 정수형 값을 받는다.
// i32 타입은 Integer 32bit를 뜻한다.
fn stack_only(b: i32) -> i32 {
    // 지역변수 c를 생성한다.
    let c = 3;
    // stack_and_heap 함수를 호출한다.
    return b + c + stack_and_heap();
}

fn stack_and_heap() -> i32 {
    // 지역변수 d 생성
    let d = 5;
    // Box 생성 및 7 전달
    // Box는 러스트의 스마트 포인터 타입
    let e = Box::new(7);
    return d + *e;
}

// 이 프로그램이 실행되면 heap에 메모리 할당
// 영역을 벗어나게되면 할당된 메모리를 해제

// stack_only 함수가 실행될 때, 
// #0 stack_and_heap::stack_only (b=2) at stack-and-heap/src/main.rs:8
// #1 0x000055555555869b in stack_and_heap::main () at stack-and-heap/src/main.rs:3
// (More stack frames follow...)
//스택 프레임 위에 stack_only 함수가 있음
// 그것은 main 함수 위의 스택 프레임에 위치하는데 main 함수가 호출한 함수이다.
// 지역 변수는 없는 상태(함수가 있는 스택 프레임에만 접근할 수 있어서 이전 함수에 있는 지역 변수에는 접근할 수 없음)
// 인수 b는 2로 설정되어 있음(함수가 호출한 인자, main함수에서 전달됨)
// 지역변수를 설정하는 부분(let c = 3;)을 지나면 지역 변수 c가 설정됨

// stack_and_heap 함수가 실행될 때,


