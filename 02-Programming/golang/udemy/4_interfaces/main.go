// mini chat bot program

// type englishBot struct
// func (englishBot) getGreeting() string
// func printGreeting(eb englishBot)

// type spanishBot struct
// func (spanishBot) getGreeting() string
// func printGreeting(sb spanishBot)

// func getGreeting() : very differnet logic in each funcs
// func printGreeting() : these will have identical logic

package main

import "fmt"

type englishBot struct{}
type spanishBot struct{}

func main() {
	eb := englishBot{}
	sb := spanishBot{}

	printGreeting(eb)
	printGreeting(sb)
}

func printGreeting(eb englishBot) {
	fmt.Println(eb.getGreeting())
}

func printGreeting(sb spanishBot) {
	fmt.Println(sb.getGreeting())
}

func (englishBot) getGreeting() string {
	// custom logic fo generating an english greeting
	return "Hi There!"
}

func (spanishBot) getGreeting() string {
	return "Hola!"
}
