# gopygo

Pure Python Go parser, AST and unparser library

## Installation

```shell
$ pip3 install gopygo
```

## Usage

Parse and unparse the Go *Hello, World!* example:

```python
>>> import gopygo
>>> program = """
... package main
... 
... import "fmt"
... 
... func main() {
...     fmt.Println("Hello, World!")
... }
... """
>>> program = program.lstrip()
>>> tree = gopygo.parse(program)
>>> tree
<gopygo.ast.File object at 0x7f0b5dddb6d0>
>>> tree.__dict__
{'name': <gopygo.ast.Package object at 0x7f0b5dddb0a0>, 'imports': [<gopygo.ast.ImportSpec object at 0x7f0b5dddb190>], 'decls': [<gopygo.ast.FuncDecl object at 0x7f0b5dddb520>]}
>>> text = gopygo.unparse(tree)
>>> print(text)
package main

import "fmt"

func main() {
    fmt.Println("Hello, World!")
}

>>> assert program == text
```

## Roadmap

Implement the AST nodes specified in [here](https://golang.org/pkg/go/ast/) and the parser, unparser libraries accordingly.

Tokens are defined in [here](https://golang.org/pkg/go/token/#Token).

## Development

Here is an example access Go AST using original `go/parser` and `go/ast` packages:

```go
package main

import "fmt"
import "go/token"
import "go/parser"
import "go/ast"

func main() {
	src := `
package main

import "fmt"

func main() {
    fmt.Println("Hello, World!")
}
	`
	x, err := parser.ParseFile(token.NewFileSet(), "", src, 0)
	fmt.Println(x.Decls[1].(*ast.FuncDecl).Body.List[0].(*ast.ExprStmt).X.(*ast.CallExpr).Args[0].(*ast.BasicLit).Value)
	fmt.Println(err)
	fmt.Printf("type: %T\n", x.Decls[1].(*ast.FuncDecl).Body.List[0].(*ast.ExprStmt).X.(*ast.CallExpr).Args[0].(*ast.BasicLit).Value)
}
```

Gives this output:

```text
"Hello, World!"
<nil>
type: string
```
