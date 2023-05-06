// https://play.rust-lang.org/?version=stable&mode=debug&edition=2021

// C, C++ 빠름 + 안전함, but 어려움

// comment
/// documentation
/* comments */

/* 
Rust types(https://dhghomon.github.io/easy_rust/Chapter_7.html)
- primitive types
- integers, char
- Signed integers : i8, i16, i32, i64, i128, isize
- Unsigned integers : u8, u16, u32, u64, u128, usize
- 숫자는 bits 수를 뜻함. 8bits = 1byte. u8 <= 255, u16 <= 65535, u128 <= 340282366920938463463374607431768211455
- isize, usize는 컴퓨터의 bits 수. e.g. 32bits computer의 isize, usize는 i32, u32.
- byte수가 적을수록 처리 속도가 빠름. 정수의 유형이 다른 것이 이 성능이 이유인 것도 있지만, 다른 용도로 사용할 수도 있음.
*/
