from goparser import parse, unparse


class TestParser():

    def test_001_hello_world(self):
        program = """
package main

import "fmt"

func main() {
    fmt.Println("Hello, World!")
}
"""
        program = program[1:]

        tree = parse(program)
        text = unparse(tree)
        assert program == text
