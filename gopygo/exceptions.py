#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: __init__
    :synopsis: module that contains the exceptions.
"""


class LexerError(Exception):
    """Raised in case of a tokenizer error.
    """

    def __init__(self, message):
        super().__init__(message)
