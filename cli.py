#!/usr/bin/python

from ebnf import Parser

# needs to be a folder called language in languages folder, with a file called "ebnf"
# executor is by default 'executors.py'
#language = Parser('c_variant')
#language.load_program('average')
#language.load_program('abc')
#language.run_program('average')
#language.run_program('abc')

# executor here is pseudocode.py
language = Parser('c_variant', executor='pseudocode')
language.load_program('average')
language.load_program('abc')
language.run_program('average')
language.run_program('abc')
