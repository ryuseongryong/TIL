// https://play.rust-lang.org/?version=stable&mode=debug&edition=2021

// C, C++ 빠름 + 안전함, but 어려움

// comment
/// documentation
/* comments */

/* 
Rust types(https://dhghomon.github.io/easy_rust/Chapter_7.html)

Integers
- primitive types
- integers, char
- Signed integers : i8, i16, i32, i64, i128, isize
- Unsigned integers : u8, u16, u32, u64, u128, usize
- 숫자는 bits 수를 뜻함. 8bits = 1byte. u8 <= 255, u16 <= 65535, u128 <= 340282366920938463463374607431768211455
- isize, usize는 컴퓨터의 bits 수. e.g. 32bits computer의 isize, usize는 i32, u32.
- byte수가 적을수록 처리 속도가 빠름. 정수의 유형이 다른 것이 이 성능이 이유인 것도 있지만, 다른 용도로 사용할 수도 있음.

Characters
- char이라고 함.
- letter A는 숫자 65, 중국어 友는 21451 등 모든 문자에는 숫자가 있음.
- 이 숫자 목록을 unicode라고 함.
- Unicode는 A~Z까지 모두 0~9까지의 숫자나 공백과 같이 더 많이 사용되는 문자에 더 작은 숫자를 사용함.
- 가장 많이 사용되는 문자는 256보다 작은 숫자로 u8에 들어갈 수 있음. u8은 0~255까지의 모든 숫자를 더한 값으로 총 256개이다.
- 즉 Rust는 as를 사용하여 u8을 안전하게 char로 캐스팅할 수 있다.("Cast u8 as char")
- Rust는 매우 엄격하기 때문에 as로 캐스팅하는 것이 유용함. 항상 type을 알아야 하고, 두 가지 type이 모두 정수인 경우에도 두 가지 type을 함께 사용할 수 없다. 
- i32를 char로 캐스팅할 수 없지만, i32를 u8으로 캐스팅할 수 있다. 그런 다음 u8에서 char로 동일한 작업을 수행할 수 있다. 따라서 한 줄에서 as를 사용하여 u8으로 만들고 다시 char로 만들 수 있다.
- i32 -> char (X)
- i32 -> u8 -> char (O)
```
fn main() { // main() is where Rust programs start to run. Code goes inside {} (curly brackets)

    let my_number = 100; // We didn't write a type of integer,
                         // so Rust chooses i32. Rust always
                         // chooses i32 for integers if you don't
                         // tell it to use a different type

    println!("{}", my_number as char); // ⚠️
}

-->
    error[E0604]: only `u8` can be cast as `char`, not `i32`
    --> src\main.rs:3:20
    |
    3 |     println!("{}", my_number as char);
    |                    ^^^^^^^^^^^^^^^^^

-->
    fn main() {
        let my_number = 100;
        println!("{}", my_number as u8 as char);
    }
```

- 100번 자리에 있는 문자이기 때문에 d를 인쇄한다. 더 쉬운 방법은 Rust에 my_number가 u8이라고 알려주는 것이다.

fn main() {
    let my_number: u8 = 100; //  change my_number to my_number: u8
    println!("{}", my_number as char);
}

*/
