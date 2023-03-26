package main

import "fmt"

type shape interface {
	getArea() float64
}

type triangle struct {
	base   float64
	height float64
}

type square struct {
	sideLength float64
}

func (t triangle) getArea() float64 {
	fmt.Println(0.5 * t.base * t.height)
	return 0.5 * t.base * t.height
}

func (s square) getArea() float64 {
	fmt.Println(s.sideLength * s.sideLength)
	return s.sideLength * s.sideLength
}

func main() {
	nt := triangle{
		base:   4.5,
		height: 5.5,
	}

	ns := square{
		sideLength: 6.6,
	}

	nt.getArea()
	ns.getArea()

}
