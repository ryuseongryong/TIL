// main 함수는 항상 러스트 파일이 실행될 때 제일 먼저 실행되는 코드
fn main() {
    println!("Hello, world!");
    calculate_weight_on_mars(100.0);
}

// 러스트 코드는 함수와 변수명을 작성할 때 스네이크 케이스를 사용함
// 함수의 마지막 표현식에서 끝에 세미콜론을 넣지 않는다. 반환 값 앞에 키워드 return을 사용하지 않아도 반환됨
// 함수에서 조기 반화을 윌해서 return 키워드를 사용할 수 있다.
// 대부분의 경우에는 return 키워드와 세미콜론이 제외된 반환값을 사용한다.

fn calculate_weight_on_mars(weight: f32) -> f32 {
    50.0
}