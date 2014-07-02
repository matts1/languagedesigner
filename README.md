# Language Designer

## System Requirements
For now, it requires the 'gi' module for python 2. We have only been able to get this working under Ubuntu, for which it is preinstalled, but if you can get it working under mac / windows it should (theoretically) work.

## Installation
Hit the download zip button on the right hand side of this webpage and extract. You run gui.py with the working directory as the root languagedesigner folder to run the program.

## Differences to standard E-BNF and BNF
Firstly, note that BNF is the more common form in the HSC, but is often wrongly referred to as E-BNF. We tried to make it as similar to E-BNF as possible (as it is an improvement on BNF), but added things which would give us more power.
* E-BNF (like ours) uses no angle brackets around metaidentifiers, BNF does
* E-BNF (like ours) uses '=', and BNF uses '::=' to denote that a meta identifier maps to a production rule
* E-BNF (like ours) uses quotation marks around terminal strings. BNF doesn't put anything around them
* E-BNF uses {} to indicate any number of, [] to indicate optional, and () to indicate grouping. We used () to indicate grouping, and used regex syntax to specify a number ('*'=0-inf, '?'=0-1, '+'=1-inf, '{a,b}'=a-b, '{a,}'=a-inf, '{,a}'=0-a) of repetitions). This gives more power, as you can specify a certain number of repetitions.

## Instructions
### CLI instructions
Simply modify cli.py to get a feel for it. You can then change the files in languages/<language-name>/ebnf to change the E-BNF, or languages/<language-name>/executors.py to modify the execution of the language (as an E-BNF does not define the way a language is executed).

### Creating a language and program
Firstly, you create an E-BNF in the program, and save it. Then you create a program, and check that it is structured correctly. After that, you can create the executor nodes yourself. You must have a file called executor.py in the same directory as E-BNF. The file works like this (where myidentifier is a meta identifier defined in the E-BNF).

```python
from ebnf import TextNode, ExecuteNode
class MyNode(ExecuteNode):
    identifier = 'myidentifier'
    # override functions here eg
    def execute(self):
        pass
```

You can then run your program in the gui.

### Data Dictionary for executor classes (first attributes, then methods)
Data dictionary by Sam

Name | Type | Contents
--- | --- | ---
child | CompiledNode | The first item in the children list
children | list | A list of children in the tree (each child is a subclass of CompiledNode)
ebnf | MetaIdentifier | The EBNF item that compiled into this metaidentifier
identifier | string | The name of the Node
is_root | boolean | Whether or not this node is the root node
meta_child | CompiledMetaIdentifier | The first item in meta_children
meta_children | list | A list of meta_children in the tree (each child is a subclass of CompiledMetaIdentifier)
parent | CompiledNode | The node that is above this node in the tree
root | CompiledMetaIdentifier | The root node of the tree, which is a subclass of CompiledMetaIdentifier

Function Definition | Can override | Description
--- | --- | ---
```str get_text()``` | No | Returns the text contained by the metaidentifier
```void input(str prompt="Input: ")``` | No | Asks for input graphically
```void output(str args)``` | No | Shows the provided arguments graphically as it would in python normally
```list children_out()``` | Yes | Returns all children by default, can be overwritten to change what children are returned, used for drawing (but not executing) items in the parse trees
```void execute(args, kwargs)``` | Yes | The function which is automatically called at the root to start execution, is usually propagated down to the other nodes (but does not automatically execute its children)
```void teardown()``` | Yes | The function that is called automatically after execution - not used the vast majority of the time
```str out()``` | Yes | Override this to change the representation of the node in the compiled parse tree
```void setup()``` | Yes | The function that is called automatically before execution


### Bug Listing
What are you talking about, we don't have any bugs for our software. Our software is 100% bug free...  

I wish... On a more realistic note, as long as you try and use the program sensibly, it should be fine, but it is possible to get at least these errors (most of which result in an error being chucked, but the program still stays alive, so it is as if nothing happened):
* If you hit new program before you hit save, it tries to save the new program as an empty file, but doesn't know what folder to save it to
* If you open a language and it is a file rather than a folder, it chucks an assertionerror, because we didn't have the time to fix it
* If you open a language and the folder doesn't contain the EBNF file, it will chuck an error
* It will attempt to compile the text saying that you need to actually create / open a program

## Copyright
Language Designer Application  
Copyright Matt Stark, Emma Harding and Sam Ritchie 2014


## Contact Information
Matt Stark (mattstark75@gmail.com)  
Emma Harding (eharding365@gmail.com)  
Sam Ritchie (S1M1528P@gmail.com)

## Circumstances Of Project Creation
We had to create a program which would teach some aspect of SDD to students, and EBNFs were both extremely challenging and interesting, making it the perfect thing to do, especially given that Matt already had plenty of experience with recursive descent parsers.

## Group Member's Names
Matt Stark, Emma Harding, Sam Ritchie
