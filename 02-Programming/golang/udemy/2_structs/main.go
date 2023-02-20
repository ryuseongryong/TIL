package main

import "fmt"

type contactInfo struct {
	email   string
	zipCode int
}
type person struct {
	firstName string
	lastName  string
	contact   contactInfo
}

func main() {
	jim := person{
		firstName: "Jim",
		lastName:  "Party",
		contact: contactInfo{
			email:   "jim@gmail.com",
			zipCode: 94000,
		},
	}

	fmt.Printf("%+v", jim)
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
