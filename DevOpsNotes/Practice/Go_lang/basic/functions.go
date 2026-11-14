package main

import "fmt"

func add(x int, y int) int {
	return x + y
}

func add_with_omited_type(x, y int) int {
	return x + y
}

func main() {
	fmt.Println(add_with_omited_type(42, 13))
}
