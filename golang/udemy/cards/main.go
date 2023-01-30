package main

func main() {
	cards := deck{"Ace of Diamonds", newCard()}
	cards = append(cards, "Six of Spades")

	cards.print()
}

func newCard() string {
	return "Five of Diamonds"
}

// basic Go types
// bool true false
// string "Hi" "Hows it going?"
// int 0 -10000 9999
// float64 10.001 0.009
