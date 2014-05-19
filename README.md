# Language Designer


## Instructions


### Data Dictionary for executor classes
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
