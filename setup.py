from setuptools import setup


setup(
    name="gopygo",
    packages=["gopygo"],
    version="0.3.1",
    author="M. Mert Yildiran",
    author_email="mehmet@up9.com",
    url="http://github.com/up9inc/gopygo",
    description="Pure Python Go parser, AST and unparser library",
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries"
        ],
    long_description="""\
========
gopygo
========

gopygo is a Go programming language parser written in Python.
AST library based on original go/ast package https://golang.org/pkg/go/ast/

""",
    zip_safe=False,
    install_requires=['sly'],
    extras_require={
        'dev': [
            'flake8',
            'pytest',
            'coverage',
            'codecov'
        ]
    },
)
