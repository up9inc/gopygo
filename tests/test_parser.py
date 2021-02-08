import pytest

from gopygo import parse, unparse
from gopygo.exceptions import LexerError


class TestParser():

    def setup_method(self):
        self.program = None

    def parse_unparse(self):
        self.program = self.program[1:]

        tree = parse(self.program)
        text = unparse(tree)
        assert self.program == text

    def test_001_hello_world(self):
        self.program = """
package main

import "fmt"

func main() {
    fmt.Println("Hello, World!")
}
"""
        self.parse_unparse()

    def test_002_only_package(self):
        self.program = """
package main
"""
        self.parse_unparse()

    def test_003_no_declarations(self):
        self.program = """
package main

import "fmt"
"""
        self.parse_unparse()

    def test_004_multiple_imports(self):
        self.program = """
package main

import "fmt"
import "rsc.io/quote"
"""
        self.parse_unparse()

    def test_005_single_line_comment(self):
        self.program = """
package main

import "fmt"

// Main function
func main() {
    fmt.Println("Hello, World!")
}
"""
        self.parse_unparse()

    def test_006_func_type(self):
        self.program = """
package main

import "fmt"

func Hello(name string) string {
    fmt.Println("Hello, World!")
}
"""
        self.parse_unparse()

    def test_007_comment_inside_function_body(self):
        self.program = """
package main

import "fmt"

// Main function
func main() {
    // Comment inside function body
    fmt.Println("Hello, World!")
}
"""
        self.parse_unparse()

    def test_008_multiple_function_call_args(self):
        self.program = """
package main

import "fmt"

// Hello returns a greeting for the named person.
func Hello(name string) string {
    // Return a greeting that embeds the name in a message.
    fmt.Sprintf("Hi, %v. Welcome!", name)
}
"""
        self.parse_unparse()

    def test_009_assign_stmt(self):
        self.program = """
package main

import "fmt"

// Hello returns a greeting for the named person.
func Hello(name string) string {
    // Return a greeting that embeds the name in a message.
    ret = Hello("gopygo")
    message := fmt.Sprintf("Hi, %v. Welcome!", name)
}
"""
        self.parse_unparse()

    def test_010_return_stmt(self):
        self.program = """
package main

import "fmt"

// Hello returns a greeting for the named person.
func Hello(name string) (string, string) {
    // Return a greeting that embeds the name in a message.
    message := fmt.Sprintf("Hi, %v. Welcome!", name)
    message2 := fmt.Sprintf("%v, GO!", name)
    return message, message2
}
"""
        self.parse_unparse()

    def test_011_variable_declaration(self):
        self.program = """
package main

import "fmt"

func main() {
    var ret string
    var ret2 string
}
"""
        self.parse_unparse()

    def test_012_lhs_list_assign_stmt(self):
        self.program = """
package main

import "fmt"

func main() {
    var ret string
    var ret2 string
    ret, ret2 = Hello("gopygo")
    fmt.Println(ret)
    fmt.Println(ret2)
}
"""
        self.parse_unparse()

    def test_013_milestone_1_multiple_func_decls(self):
        self.program = """
package main

import "fmt"

// Hello returns a greeting for the named person.
func Hello(name string) (string, string) {
    // Return a greeting that embeds the name in a message.
    message := fmt.Sprintf("Hi, %v. Welcome!", name)
    message2 := fmt.Sprintf("%v, GO!", name)
    return message, message2
}

func main() {
    var ret string
    var ret2 string
    ret, ret2 = Hello("gopygo")
    fmt.Println(ret)
    fmt.Println(ret2)
}
"""
        self.parse_unparse()

    def test_014_no_call_args(self):
        self.program = """
package main

import "fmt"

func Hello(name string) string {
    fmt.Println()
}
"""
        self.parse_unparse()

    def test_015_operators(self):
        self.program = """
package main

import "fmt"

func main() {
    a := 3 + 5
    b := 3 - 5
    c := 3 * 5
    d := 3 / 5
    e := - 5
    f := 3 * (5 + 7)
    fmt.Println(a)
    fmt.Println(b)
    fmt.Println(c)
    fmt.Println(d)
    fmt.Println(e)
    fmt.Println(f)
}
"""
        self.parse_unparse()


class TestExceptions():

    def test_001_lexer_error(self):
        program = """
package ~
"""
        program = program[1:]
        with pytest.raises(
            LexerError,
            match=r"Illegal character '~'"
        ):
            parse(program)
