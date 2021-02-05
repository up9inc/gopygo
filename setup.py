from setuptools import setup


setup(
    name = "goparser",
    packages = ["goparser"],
    version = "0.1.0",
    author = "M. Mert Yildiran",
    author_email = "mehmet@up9.com",
    url = "http://github.com/up9inc/goparser",
    description = "Pure Python Go parser, AST and unparser library",
    classifiers = [
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries"
        ],
    long_description = """\
========
goparser
========

goparser is a Go programming language parser written in Python.
AST library based on original go/ast package https://golang.org/pkg/go/ast/

""",
    zip_safe = False,
    install_requires = ['sly']
)
