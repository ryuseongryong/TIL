- go에서 선언된 모든 값에 대해 할당된 type이 필요함
- receiver에서도 동일한데, receiver 함수가 필요할 때, receiver로 받는 인자의 type이 다르면, 동일한 로직의 receiver 함수를 type만 다르게 하여 반복해서 선언해야 하는 문제가 있음

```
func (d deck) shuffle()
func (s []float64) shuffle()
func (s []string) shuffle()
func (s []int) shuffle()
```