package main

import (
	"fmt"
	"time"
)

func main() {
	// var a int = 20
	a := 20
	fmt.Println("hello")
	fmt.Println(a)

	x := 19
	if x < 20 {
		fmt.Println("x is lower than 20")
	}

	array := [3]int{1, 2, 3}
	fmt.Println(array, "Array range is 3")

	// no fixed array range
	array2 := []int{1, 2, 3, 4}
	fmt.Println(array2)

	// map(Python;dictionary, JS;object)
	mapping := make(map[string]int)
	mapping["age"] = 123
	fmt.Println(mapping["age"])

	point := 10
	point1 := &point  // convert pointer address
	point2 := *point1 // convert pointer variable

	fmt.Println(point1)
	fmt.Println(point2)

	// concurrency
	go function1()
	function2()

}

func function1() {
	for i := 1; i < 100; i++ {
		fmt.Println("hello")
		time.Sleep(time.Second * 1)
	}
}

func function2() {
	for i := 1; i < 100; i++ {
		fmt.Println(("What's up"))
		time.Sleep(time.Second * 1)
	}
}

// run the code : go run "FILE PATH"
// build the code : go build "FILE PATH"
