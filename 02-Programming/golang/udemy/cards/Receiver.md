### Golang Receiver
- Go에는 클래스가 없음
- 대신 receiver가 있는 함수로 그 기능을 대체할 수 있음

```
func (d deck) print() {
    fmt.Println(d)
}
```
- 리시버 함수 예시
```
type Vertex struct {
	X, Y float64
}

func (v Vertex) Abs() float64 {
	return math.Sqrt(v.X*v.X + v.Y*v.Y)
}

func main() {
	v := Vertex{3, 4}
	fmt.Println(v.Abs())
}

```

- 리시버가 없는 동일한 기능의 함수
```
type Vertex struct {
	X, Y float64
}

func Abs(v Vertex) float64 {
	return math.Sqrt(v.X*v.X + v.Y*v.Y)
}

func main() {
	v := Vertex{3, 4}
	fmt.Println(Abs(v))
}

```