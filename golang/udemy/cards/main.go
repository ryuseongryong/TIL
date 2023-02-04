package main

import "fmt"

func main() {
	cards := newDeck()
	fmt.Println((cards.toString()))
}

// basic Go types
// bool true false
// string "Hi" "Hows it going?"
// int 0 -10000 9999
// float64 10.001 0.009
