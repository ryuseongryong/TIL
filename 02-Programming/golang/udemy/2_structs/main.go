package main

import "fmt"

type contactInfo struct {
	email   string
	zipCode int
}
type person struct {
	firstName string
	lastName  string
	contactInfo
}

func main() {
	jim := person{
		firstName: "Jim",
		lastName:  "Party",
		contactInfo: contactInfo{
			email:   "jim@gmail.com",
			zipCode: 94000,
		},
	}

	jim.updateName("jimmy")
	jim.print()
}

func (pointerToPerson *person) updateName(newFirstName string) {
	(*pointerToPerson).firstName = newFirstName
}

func (p person) print() {
	fmt.Printf("%+v", p)
}

// type     | default value
// string   | 0
// float    | 0
// bool     | false

// structs variable assignment 3ways
// 1. 	by struct order
//      e.g. alex := person{"Alex", "Anderson"}
// 2. 	assign as key
//      e.g. alex := person{firstName: "Alex", lastName: "Anderson"}
// 3.   create variable and update values
// 		e.g. var alex person
//      	 alex.firstName = "Alex"
//      	 alex.lastName = "Anderson"
//      	 fmt.Println(alex)
//      	 fmt.Printf("%+v", alex)

// struct type can be use value as own struct key
