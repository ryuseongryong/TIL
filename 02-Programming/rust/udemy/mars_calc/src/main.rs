// main 함수는 항상 러스트 파일이 실행될 때 제일 먼저 실행되는 코드
fn main() {
    let mut mars_weight = calculate_weight_on_mars(100.0);
    // 변수를 재지정하면 
    // cannot assign twice to immutable variable 에러가 발생함
    // 러스트 변수는 기본적으로 불변 변수라는 것을 알 수 있다.
    // 가변 변수로 만들려면 명시적으로 선언해줘야한다.
    mars_weight = mars_weight * 1000.0;
    // println! 는 매크로, !가 붙어있으면 매크로라는 의미
    // cargo expand로 확인 가능
    println!("Weight on Mars: {}g", mars_weight);
}

// 러스트 코드는 함수와 변수명을 작성할 때 스네이크 케이스를 사용함
// 함수의 마지막 표현식에서 끝에 세미콜론을 넣지 않는다. 반환 값 앞에 키워드 return을 사용하지 않아도 반환됨
// 함수에서 조기 반화을 윌해서 return 키워드를 사용할 수 있다.
// 대부분의 경우에는 return 키워드와 세미콜론이 제외된 반환값을 사용한다.

fn calculate_weight_on_mars(weight: f32) -> f32 {
    (weight / 9.81) * 3.711
}