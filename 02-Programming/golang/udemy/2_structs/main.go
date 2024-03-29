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

// different between struct type and array for pointers

//          Arrays          |        Slices
// Primitive data structure | Can grow and shrink
// Can't be resized         | Used 99% of the time for lists of elements
// Rarely used directly

// Value Types | Reference Types
//     int     |    slices
//    float    |      maps
//    string   |    channels
//     bool    |    pointers
//    structs  |    functions
// Value Types : Use pointers to change these things in a function
// Reference Types : Don't worry about pointers with these

// --------codes--------
// package main

// import "fmt"

// func main() {
// 	mySlice := []string{"Hi", "There", "How", "Are", "you"}
// 	updateSlice(mySlice)
// 	fmt.Println(mySlice)

// }

// func updateSlice(s []string) {
// 	s[0] = "Bye"
// }
// --------codes done--------

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

// 항상 값을 복사하기 떄문에 주소에 대한 변수 또한 새로운 주소에 할당됨
// --------codes--------
// package main

// import "fmt"

// func main() {
//  name := "bill"

//  namePointer := &name

//  fmt.Println(&namePointer)
//  printPointer(namePointer)
// }

// func printPointer(namePointer *string) {
//  fmt.Println(&namePointer)
// }
// --------codes done--------
