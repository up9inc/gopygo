import pytest

from gopygo import parse, unparse
from gopygo.exceptions import LexerError


class TestParser():

    def setup_method(self):
        self.program = None

    def parse_unparse(self):
        self.program = self.program.lstrip()

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
fmt.Sprintf("Hi, %v. Welcome!", name)
"""
        self.parse_unparse()

    def test_009_assign_stmt(self):
        self.program = """
message = fmt.Sprintf("Hi, %v. Welcome!", name)
message := fmt.Sprintf("Hi, %v. Welcome!", name)
a += 3
a -= 3
a *= 3
a /= 3
a %= 3
a &= 3
a |= 3
a ^= 3
a &^= 3
a <<= 3
a >>= 3
"""
        self.parse_unparse()

    def test_010_return_stmt(self):
        self.program = """
func Hello(name string) (string, string) {
    message := fmt.Sprintf("Hi, %v. Welcome!", name)
    message2 := fmt.Sprintf("%v, GO!", name)
    return message, message2
}
"""
        self.parse_unparse()

    def test_011_variable_declaration(self):
        self.program = """
var ret string
var ret2 string
var a = "initial"
var a uint8 = 2
var b, c string
var b, c int = 1, 2
var b, c int32 = 1, 2
var a, b, c int32 = 1, 2, 3
var d = true
var e int
f := "apple"
var X uint8 = 225
var Y int16 = 32767
a := 20.45
b := 34.89
c := b - a
var a complex128 = complex(6, 2)
var b complex64 = complex(9, 2)
str1 := "Test"
var ToBe bool = false
ToBe = true
var absoluteZero int = -459
sum := 116 - 68
var maxUint32 uint32 = 4294967295
var pi float64
var pi float64 = 3.14
var x complex128 = 1 + 2i
var y complex128 = 1 + 3.14i
var r rune = 'a'
var b byte = 'b'
"""
        self.parse_unparse()

    def test_012_lhs_list_assign_stmt(self):
        self.program = """
var ret string
var ret2 string
ret, ret2 = Hello("gopygo")
fmt.Println(ret)
fmt.Println(ret2)
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
fmt.Println()
"""
        self.parse_unparse()

    def test_015_operators(self):
        self.program = """
a := 3 + 5
b := 3 - 5
c := 3 * 5
d := 3 / 5
d := 10 % 9
e := -5
f := 3 * (5 + 7)
a := 3 + 5 + 3
b := "go" + "lang"
d := true && false
c := true || false
c := true == false
c := a << b
c := a >> b
c := a &^ b
c := a != b
c := a >= b
c := a <= b
c := a & b
c := a | b
c := a ^ b
c := a > b
c := a < b
e := d <- c
f := ++a
f := a++
f := --a
f := a--
a := ^0011
a := !false
"""
        self.parse_unparse()

    def test_016_only_import(self):
        self.program = """
import "fmt"
"""
        self.parse_unparse()

    def test_017_only_imports(self):
        self.program = """
import "fmt"
import "rsc.io/quote"
"""
        self.parse_unparse()

    def test_018_const(self):
        self.program = """
const s string = "constant"
const n = 500000000
const d = 3e20 / n
"""
        self.parse_unparse()

    def test_019_empty_line_after_block_stmt_start(self):
        self.program = """
package main

import "fmt"

func main() {

    fmt.Println("go" + "lang")
}
"""
        self.program = self.program[1:]

        tree = parse(self.program)
        text = unparse(tree)
        lines = self.program.split('\n')
        del lines[5]
        self.program = '\n'.join(lines)
        assert self.program == text

    def test_020_import_list(self):
        self.program = """
import (
    "fmt"
    "math"
)
"""
        self.parse_unparse()

    def test_021_type_support_in_field_list(self):
        self.program = """
package main

import "fmt"

func plus(a int, b int) int {
    return a + b
}

func plus(a float32, b float64) (rune, byte) {
    return a + b
}

func main() {
    res := plus(1, 2)
    fmt.Println("1+2 =", res)
    res = plusPlus(1, 2, 3)
    fmt.Println("1+2+3 =", res)
}
"""
        self.parse_unparse()

    def test_022_for(self):
        self.program = """
package main

import "fmt"

func main() {
    i := 1
    for i <= 3 {
        fmt.Println(i)
        i = i + 1
    }
    for j := 7; j <= 9; j++ {
        fmt.Println(j)
    }
    for {
        fmt.Println("loop")
        break
    }
    for n := 0; n <= 5; n++ {
        fmt.Println(n)
        continue
    }
}
"""
        self.parse_unparse()

    def test_023_goto(self):
        self.program = """
package main

import "fmt"

func main() {
    var a int = 10
    MAIN_START:
    a = 3
    goto MAIN_START
}
"""
        self.parse_unparse()

    def test_024_if_else(self):
        self.program = """
package main

import "fmt"

func main() {
    if 7 % 2 == 0 {
        fmt.Println("7 is even")
    } else {
        fmt.Println("7 is odd")
    }
    if 8 % 4 == 0 {
        fmt.Println("8 is divisible by 4")
    }
    if num := 9; num < 0 {
        fmt.Println(num, "is negative")
    } else if num < 10 {
        fmt.Println(num, "has 1 digit")
    } else {
        fmt.Println(num, "has multiple digits")
    }
}
"""
        self.parse_unparse()

    def test_025_switch_case(self):
        self.program = """
package main

import (
    "fmt"
    "time"
)

func main() {
    i := 2
    switch i {
    case 1:
        fmt.Println("one")
    case 2:
        fmt.Println("two")
    case 3:
        fmt.Println("three")
    }
    switch time.Now().Weekday() {
    case time.Saturday, time.Sunday:
        fmt.Println("It's the weekend")
    default:
        fmt.Println("It's a weekday")
    }
    t := time.Now()
    switch {
    case t.Hour() < 12:
        fmt.Println("It's before noon")
    default:
        fmt.Println("It's after noon")
    }
    switch t := 2; t + 1 {
    case 1:
        fmt.Println("one")
    case 2:
        fmt.Println("two")
    case 3:
        fmt.Println("three")
    }
    switch t := i.(type) {
    case bool:
        fmt.Println("I'm a bool")
    case int, float32:
        fmt.Println("I'm an int")
    default:
        fmt.Printf("Don't know type %T\n", t)
    }
}
"""
        self.parse_unparse()

    def test_024_arrays(self):
        self.program = """
package main

import "fmt"

func main() {
    var a [5]int
    fmt.Println("emp:", a)
    a[4] = 100
    fmt.Println("set:", a)
    fmt.Println("get:", a[4])
    fmt.Println("len:", len(a))
    b := [5]int{1, 2, 3, 4, 5}
    fmt.Println("dcl:", b)
    var twoD [2][3]int
    var twoD [2][3]int
    for i := 0; i < 2; i++ {
        for j := 0; j < 3; j++ {
            twoD[i][j] = i + j
        }
    }
    fmt.Println("2d: ", twoD)
}
"""
        self.parse_unparse()

    def test_025_slices(self):
        self.program = """
package main

import (
    "fmt"
    "time"
)

func main() {
    s := make([]string, 3)
    fmt.Println("emp:", s)
    s[0] = "a"
    s[1] = "b"
    s[2] = "c"
    fmt.Println("set:", s)
    fmt.Println("get:", s[2])
    fmt.Println("len:", len(s))
    s = append(s, "d")
    s = append(s, "e", "f")
    fmt.Println("apd:", s)
    c := make([]string, len(s))
    copy(c, s)
    fmt.Println("cpy:", c)
    l := s[2:5]
    fmt.Println("sl1:", l)
    l = s[:5]
    fmt.Println("sl2:", l)
    l = s[2:]
    fmt.Println("sl3:", l)
    t := []string{"g", "h", "i"}
    fmt.Println("dcl:", t)
    l := s[2:5:7]
    twoD := make([][]int, 3)
    for i := 0; i < 3; i++ {
        innerLen := i + 1
        twoD[i] = make([]int, innerLen)
        for j := 0; j < innerLen; j++ {
            twoD[i][j] = i + j
        }
    }
    fmt.Println("2d: ", twoD)
}
"""
        self.parse_unparse()

    def test_026_maps(self):
        self.program = """
package main

import (
    "fmt"
    "time"
)

func main() {
    m := make(map[string]int)
    m["k1"] = 7
    m["k2"] = 13
    fmt.Println("map:", m)
    v1 := m["k1"]
    fmt.Println("v1: ", v1)
    fmt.Println("len:", len(m))
    delete(m, "k2")
    fmt.Println("map:", m)
    _, prs := m["k2"]
    fmt.Println("prs:", prs)
    n := map[string]int{"foo": 1, "bar": 2}
    fmt.Println("map:", n)
}
"""
        self.parse_unparse()

    def test_027_range(self):
        self.program = """
package main

import "fmt"

func main() {
    nums := []int{2, 3, 4}
    sum := 0
    for _, num := range nums {
        sum += num
    }
    fmt.Println("sum:", sum)
    for i, num := range nums {
        if num == 3 {
            fmt.Println("index:", i)
        }
    }
    kvs := map[string]string{"a": "apple", "b": "banana"}
    for k, v := range kvs {
        fmt.Printf("%s -> %s\n", k, v)
    }
    for k := range kvs {
        fmt.Println("key:", k)
    }
    for i, c := range "go" {
        fmt.Println(i, c)
    }
    nums := []int{1, 2, 3, 4}
    var num int
    for _, num = range nums {
        fmt.Println("num:", num)
    }
    for range nums {
        num++
        fmt.Println("num:", num)
    }
}
"""
        self.parse_unparse()

    def test_028_ellipsis(self):
        self.program = """
package main

import "fmt"

func sum(nums ...int) {
    fmt.Print(nums, " ")
    total := 0
    for _, num := range nums {
        total += num
    }
    fmt.Println(total)
}

func main() {
    sum(1, 2)
    sum(1, 2, 3)
    nums := []int{1, 2, 3, 4}
    sum(nums...)
}
"""
        self.parse_unparse()

    def test_029_closures(self):
        self.program = """
package main

import "fmt"

func closure() func() int {
    i := 0
    return func() int {
        i++
        return i
    }
}

func main() {
    nextInt := closure()
    fmt.Println(nextInt())
    fmt.Println(nextInt())
    fmt.Println(nextInt())
    newInts := closure()
    fmt.Println(newInts())
}
"""
        self.parse_unparse()

    def test_030_multiple_closures(self):
        self.program = """
package main

import "fmt"

func closure() (func() int, func() int) {
    i := 0
    j := 0
    return func() int {
        i++
        return i
    }, func() int {
        j--
        return j
    }
}

func main() {
    nextInt, nextInt2 := closure()
    fmt.Println(nextInt())
    fmt.Println(nextInt())
    fmt.Println(nextInt())
    fmt.Println(nextInt2())
    fmt.Println(nextInt2())
    fmt.Println(nextInt2())
    newInts, nextInts2 := closure()
    fmt.Println(newInts())
    fmt.Println(nextInts2())
}
"""
        self.parse_unparse()

    def test_031_recursion(self):
        self.program = """
package main

import "fmt"

func fact(n int) int {
    if n == 0 {
        return 1
    }
    return n * fact(n - 1)
}

func main() {
    fmt.Println(fact(7))
}
"""
        self.parse_unparse()

    def test_032_pointers(self):
        self.program = """
package main

import "fmt"

func zeroval(ival int) {
    ival = 0
}

func zeroptr(iptr *int) {
    *iptr = 0
}

func main() {
    i := 1
    fmt.Println("initial:", i)
    zeroval(i)
    fmt.Println("zeroval:", i)
    zeroptr(&i)
    fmt.Println("zeroptr:", i)
    fmt.Println("pointer:", &i)
}
"""
        self.parse_unparse()

    def test_033_structs(self):
        self.program = """
type person struct {
    name string
    age int
}
type Vertex struct {
    X int
    Y int
}
type Employee struct {
    firstName string
    lastName string
    age int
    salary int
}
func newPerson(name string) *person {
    fmt.Println("Hello, World!")
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
