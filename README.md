# gopygo

Pure Python Go parser, AST and unparser library

## Installation

```shell
$ pip3 install -e .
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
>>> program = program[1:]
>>> tree = gopygo.parse(program)
>>> tree
<gopygo.ast.Package object at 0x7efdc6a2e610>
>>> tree.__dict__
{'name': 'main', 'imports': [<gopygo.ast.ImportSpec object at 0x7efdc6a2e670>], 'decls': [<gopygo.ast.FuncDecl object at 0x7efdc6a2e760>]}
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
