package main

import "fmt"

func main() {
	nums := []int{0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10}

	for _, num := range nums {
		isEven := true
		if num%2 == 1 {
			isEven = false
		}

		if isEven {
			fmt.Println(num, " is even")
		} else if !isEven {
			fmt.Println(num, " is odd")
		}

	}
}
