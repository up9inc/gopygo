# goparser

Pure Python Go parser, AST and unparser library

## Installation

```shell
$ pip3 install -e .
```

## Usage

Parse and unparse the Go *Hello, World!* example:

```python
>>> import goparser
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
>>> tree = goparser.parse(program)
>>> tree
<goparser.ast.Package object at 0x7efdc6a2e610>
>>> tree.__dict__
{'name': 'main', 'imports': [<goparser.ast.ImportSpec object at 0x7efdc6a2e670>], 'decls': [<goparser.ast.FuncDecl object at 0x7efdc6a2e760>]}
>>> text = goparser.unparse(tree)
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
