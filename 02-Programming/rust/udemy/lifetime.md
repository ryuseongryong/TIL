- https://rinthel.github.io/rust-lang-book-ko/ch10-03-lifetime-syntax.html
- 라이프타임은 어떤 참조에 대한 수명을 표시하고 제약을 걸어서 안전성을 확보할 수 있는 문법요소
- 라이프타임은 Rust 컴파일러가 메모리 안전을 보장할 수 있게 하는 강력한 도구이다.
- 우리가 명시적으로 지정하는 라이프타임 파라미터는 어떤 값의 수명이 얼마나 길지 우리가 선택하도록 허용하지 않는다. 단지 어떤 참조는 동일한 메모리에 관련되어 있고 동일한 수명을 공유할 것으로 예상된다는 것을 우리가 컴파일러에게 알려주도록 해준다.
- 구조체 안에 저장하는 모든 참조에 대해 수명을 명시적으로 지정해야 한다.
- 일부 참조가 "관련"있으면서 동일한 수명을 공유할 것으로 기대되는 컴파일러와 통신할 수 있도록 합니다. (수명을 지정해서 값이 얼마나 오래 지속될 지 선택할 수 없음)
