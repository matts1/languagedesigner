# Language Designer

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

### Data Dictionary for executor classes (first attributes, then methods)
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
Doesn't work with left-recursive EBNFs
