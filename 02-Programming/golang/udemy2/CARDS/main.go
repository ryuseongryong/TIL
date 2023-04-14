package main

import "fmt"

func main() {
	// var card string = "Ace of Spades"
	cards := []string{"Ace of Diamonds", newCard()}
	cards = append(cards, "Six of Spades")
	fmt.Println(cards)
}

func newCard() string {
	return "Five of Diamonds"
}
