package main

import "fmt"

func main() {
	// var card string = "Ace of Spades"
	cards := deck{"Ace of Diamonds", newCard()}
	cards = append(cards, "Six of Spades")

	for i, card := range cards {
		fmt.Println(i, card)
	}
}

func newCard() string {
	return "Five of Diamonds"
}
