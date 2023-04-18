package main

import "fmt"

type deck []string

func newDeck() deck {
	// cards := deck{"Ace of Spades", "Two of Spades"}
	cards := deck{}
	cardSuits := []string{"Spades", "Hearts", "Diamonds"}
	cardValues := []string{"Ace", "Two", "Three"}

	for _, suit := range cardSuits {
		for _, value := range cardValues {
			cards = append(cards, suit+" of "+value)
		}
	}
}

func (d deck) print() {
	for i, card := range d {
		fmt.Println(i, card)
	}
}
