# Input Handling
mysh handles input by splitting your input line into tokens, separated by whitespace, '|' characters, or quotation marks.

For example:
```
Hello World ! --> ["Hello", "World", "!"]

Hello | World! --> ["Hello", "|", "World!"]

Hello "World !" --> ["Hello", "World !"]
```


## Parsing a line of input
This is done through combined use of a parsing module I created, and the 'shlex' module. First the line is filtered for variables with the
'${<var-name>}'. Then the line is checked for pipes, and any syntax errors to do with pipes, e.g. two pipes following eachother, or a
trailing pipe. Next the line is turned into a list with shlex, and finally any escaping backslashes ('\\') are removed.

My program then takes this list of arguments and expands any user paths, e.g. '~' to get absolute paths. It first checks if the program
name, (first argument), is a builtin function, and if so returns the output of that function to be written to stdout after running it.
Else, the program is expanded into an absolute path by searching through the environment PATH and then run as an executable.


## Substituting variables
In order to find and substitute variables, I made a parsing function that would first find the starting and ending indexes of any variables, 
(excluding escaped ones), and then replace the variables with the value of the corresponding environment variable, after checking for proper
syntax such as valid characters in variable names.

The program handles escaped variables by keeping track of whether the last character was a backslash, and this is true when starting a
variable, the variable is skipped.


## Pipelines
My program knows to use the specific pipes function if there is an argument in the argument list that is just a pipe, rather than seeing if any 
arguments contain the pipe character, as this avoids interpreting quoted pipes as pipes rather than the literal character. My program first
splits the argument list into a list of lists, where each list is a command separated by a pipe. Next, the program loops through the commands,
running each program and appending the pid to a list so that all processes can be shut down when a interrupt signal is sent. 


### Stdin/ Stdout redirection
The program uses stdin/ stdout redirection to allow previously run commands to use the last commands output as input. I keep track of the last
commands read pipe, (variable is initially set to None), so that rather than the next command reading from stdin, it will read the last commands
output. The fact the variable is initially None also allows me to avoid this behaviour on the first program, as it has no previous command to
read from. Finally, each commands stdout is redirected to a pipe, and the read end of this pipe is stored as the previous read pipe.


## Testing
I have created end-to-end testcases for builtin commands and commands that run common executables that can be found on any linux machine. These
files are structured in the tests directory as follows:
```
tests
|   curr.out
|   run_tests.sh
|
+---builtin_tests
|   |   ...
|
+---executable_tests
|   |   ...
```
