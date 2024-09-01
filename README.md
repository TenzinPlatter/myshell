# Input Handling
mysh handles input by splitting your input line into tokens, separated by whitespace, '|' characters, or quotation marks.

For example:
```
Hello World ! --> ["Hello", "World", "!"]
```
```
Hello |World! --> ["Hello", "|", "World!"]
```
```
Hello "World !" --> ["Hello", "World !"]
```
