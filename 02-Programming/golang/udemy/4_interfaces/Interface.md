- go에서 선언된 모든 값에 대해 할당된 type이 필요함
- receiver에서도 동일한데, receiver 함수가 필요할 때, receiver로 받는 인자의 type이 다르면, 동일한 로직의 receiver 함수를 type만 다르게 하여 반복해서 선언해야 하는 문제가 있음

```
func (d deck) shuffle()
func (s []float64) shuffle()
func (s []string) shuffle()
func (s []int) shuffle()
```

### interface type description as diagram
```
type englishBot struct
func (englishBot) getGreeting() string

type spanishBot struct
func (spanishBot) getGreeting() string
```

```
type bot interface{ // >> honorary type
    getGreeting() string // when getGreeting function return string, that type is automatically promote type bot
}
func printGreeting(b bot)
```

### complex interface type
```
// bot is interface name
type bot interface {
    // getGreeting is function name
    // (string, int) are List of argument types
    // (string, error) are List of return types
    getGreeting(string, int) (string, error)
}
```

### Concrete Type vs Interface Type
- Concrete Type : map, struct, int, string, englishBot
- Interface Type : bot