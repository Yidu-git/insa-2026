**Lua** was created in 1993 by a team of Brazilian computer scientists in Rio. It was never meant to be a language on its own, rather, to compliement bigger applications (think of games such as Roblox, World of Warcraft, Angry Birds). Lua was meant to allow devs to to modify game behavior without touching the original code written in C or C++.

(Lua means moon in Portuguese)

# Print
Similar to python, printing messages uses `print` function:
```Lua
print("Hello world")
```
You can add a "," between multiple values in the same print function to print multiple values on the same line.
# Comments
Comments in Lua start with double dashes (*`--`*):
```Lua
-- Lua comment
print("Hello World")
-- print("This line is commented")
```

Multi line comments are in closed in double brackets:
```Lua
--[[
This is a multi line comment.
]]
```

# Variables
Since Lua is a dynamic language like Python, variables are declared with a valid variable name followed by an equal sign (*"="*):
```Lua
variable1 = "String"
variable2 = 42
```

However, Lua has 8 distinct data types, we can check this with the *`type`* function:
```Lua
type(nil)         -- nil, the absence of a value
type(true)        -- boolean
type(10.4 * 12)   -- number
type("welcome")   -- string
type(print)       -- function
type({})          -- table
type(io.stdin)    -- userdata
```

# Operations
```Lua
score = 0           -- score is 0
score = 4 + 3       -- score is now 7
score = 4 - 3       -- score is now 1
score = 4 * 3       -- score is now 12
score = 4 / 3       -- score is now 1.3333
score = 4 % 3       -- score is now 1
score = 4 ^ 3       -- score is now 64

print(score)        -- Output: 64
```

**Note :** Notice that when printing a variable with "*/*" operation outputs a value with a "*.*" even when its a whole number. This is because it outputs a floating point integer.

# concatenating strings
We use two periods to concatenate strings
# Multi line strings (`[[` `]]`)
```Lua
MultiLineString = [[
This is a ...
Multi line string
]]
```