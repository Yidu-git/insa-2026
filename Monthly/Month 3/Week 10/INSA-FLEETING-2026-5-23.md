---
cssclasses:
  - jbm-note
---
# REVERSE ENGINEERING
## What Is Reverse Engineering?

Reverse engineering is essentially being given a result and figuring out how it got there. That knowledge can be used to find vulnerabilities in the logic and methods used to achieve the result. It starts with finding what you want to attack, then figuring out how it works, then finally doing what you want with it. For security researchers, the goal of reverse engineering is to find where the developers made a mistake or got lazy. For example, developers often think encrypting network traffic is enough, but reverse engineers can get around that encryption. This is why developers shouldn't encrypt the data their software sends to their servers, and then be lazy about sanitizing the data when it hits the server.

## Instructions

The ability to read and comprehend assembly code is vital to reverse engineering. There are roughly 1,500 instructions, however, a majority of the instructions are not commonly used or they're just variations (such as MOV and MOVS). Just like in high-level programming, don't hesitate to look up something you don't know.

Before we get started there are three different terms you should know: **immediate**, **register**, and **memory**.

- An **immediate value** (or just immediate, sometimes IM) is something like the number 12. An immediate value is _not_ a memory address or register, instead, it's some sort of constant data.
    
- A **register** is referring to something like RAX, RBX, R12, AL, etc.
    
- **Memory** or a **memory address** refers to a location in memory (a memory address) such as 0x7FFF842B.
    

> You may see a semicolon at the end of, or in-between, a few Assembly instructions. This is because the semicolon (;) is used to write a comment in Assembly.

It's important to know the format of instructions which is as follows:

`**(Instruction/Opcode/Mnemonic) <Destination Operand>, <Source Operand>**`

> I will be referring to Instructions/Opcodes/Mnemonics as instructions, just note that some people call it different things.

Example:

```asm
mov RAX, 5
```

MOV is the instruction, RAX is the destination operand, and 5 is the source operand. The capitalization of instructions or operands does not matter. You will see me use a mixture of all letters capitalized and all letters lowercase. In the example given, 5 is an immediate value because it's not a valid memory address and it's certainly not a register.

## Common Instructions

### Data Movement

**MOV** is used to move/store the source operand into the destination. The source doesn't have to be an immediate value like it is in the following example. In the following example, the immediate value of 5 is being moved into RAX.

**This is equivalent to RAX = 5.**

```nasm
mov RAX, 5
```

**LEA** is short for Load Effective Address. This is essentially the same as MOV except for addresses. They key difference between MOV and LEA is that LEA doesn't dereference. It's also commonly used to compute addresses. In the following example, RAX will contain the memory address/location of num1.

```asm
lea RAX, num1
```

```asm
lea RAX, [struct+8]
```

```asm
mov RBX, 5
lea RAX, [RBX+1]
```

In the first example, RAX is set to the address of num1. In the second, RAX is set to the address of the member in a structure which is 8 bytes from the start of the structure. This would usually be the second member. The third example RBX is set to 5, then LEA is used to set RAX to RBX + 1. RAX will be 6.  

**PUSH** is used to push data onto the stack. Pushing refers to putting something on the top of the stack. In the following example, RAX is pushed onto the stack. Pushing will act as a copy so RAX will still contain the value it had before it was pushed. Pushing is often used to save the data inside a register by pushing it onto the stack, then later restoring it with `pop`.

```asm
push RAX
```

**POP** is used to take whatever is on the top of the stack and store it in the destination. In the following example whatever is on the top of the stack will be put into RAX.

```asm
pop RAX
```

#### Arithmetic:

**INC** will increment data by one. In the following example RAX is set to 8, then incremented. RAX will be 9 by the end.

```asm
mov RAX, 8
inc RAX
```

**DEC** decrements a value. In the following example, RAX ends with a value of 7.

```asm
mov RAX, 8
dec RAX
```

**ADD** adds a source to a destination and stores the result in the destination. In the following example, 2 is moved into RAX, 3 into RBX, then they are added together. The result (5) is then stored in RAX.

Same as RAX = RAX + RBX or RAX += RBX.

```asm
mov RAX, 2
mov RBX, 3
add RAX, RBX
```

**SUB** subtracts a source from a destination and stores the result in the destination. In the following example, RAX will end with a value of 2.

Same as RAX = RAX - RBX or RAX -= RBX.

```asm
mov RAX, 5
mov RBX, 3
sub RAX, RBX
```

##### **Multiplication and division are a bit different.**

Because the sizes of data can vary and change greatly when multiplying and dividing, they use a concatenation of two registers to store the result. The upper half of the result is stored in RDX, and the lower half is in RAX. The total result of the operation is RDX:RAX, however, referencing just RAX is usually good enough. Furthermore, only _one_ operand is given to the instruction. Whatever you want to multiply or divide is stored in RAX, and what you want to multiply or divide _by_ is passed as the operand. Examples are provided in the following descriptions.

**MUL** (unsigned) or **IMUL** (signed) multiplies RAX by the operand. The result is stored in RDX:RAX. In the following example, RDX:RAX will end with a value of 125.  

The following is the same as 25*5

```asm
mov RAX, 25
mov RBX, 5
mul RBX ; Multiplies RAX (25) with RBX (5)
```

After that code runs, the result is stored in RDX:RAX but in this case, and in most cases, RAX is enough.

**DIV** (unsigned) and **IDIV** (unsigned) work the same as MUL. What you want to divide (dividend) is stored in RAX, and what you want to divide it by (divisor) is passed as the operand. The result is stored in RDX:RAX, but once again RAX alone is usually enough.  

```asm
mov RAX, 18
mov RBX, 3
div RBX ; Divides RAX (18) by RBX (3)
```

After that code executes, RAX would be 6.
#### Flow Control:

RET is short for return. This will return execution to the function that called the currently executing function, aka the caller. As you will soon learn, one of the purposes of RAX is to hold return values. The following example sets RAX to 10 then returns. This is equivalent to `return 10;` in higher-level programming languages.

```asm
mov RAX, 10 ret
```

**CMP** compares two operands and sets the appropriate flags depending on the result. The following would set the Zero Flag (ZF) to 1 which means the comparison determined that RAX was equal to five. Flags are talked about in the next section. In short, flags are used to represent the result of a comparison, such as if the two numbers were equal or not.

```asm
mov RAX, 5
cmp RAX, 5
```

**JCC** instructions are conditional jumps that jump based on the flags that are currently set. JCC is not an instruction, rather a term used to mean the set of instructions that includes JNE, JLE, JNZ, and many more. JCC instructions are usually self-explanatory to read. JNE will jump if the comparison is not equal, and JLE jumps if less than or equal, JG jumps if greater, etc. This is the assembly version of if statements.

The following example will return if RAX isn't equal to 5. If it is equal to 5 then it will set RBX to 10, _then_ return.

```asm
mov RAX, 5
cmp RAX, 5
jne 5 ; Jump to line 5 (ret) if not equal.
mov RBX, 10
ret
```

**NOP** is short for No Operation. This instruction effectively does nothing. It's typically used for padding because some parts of code like to be on specific boundaries such as 16-bit or 32-bit boundaries.  

### Back To The Example

Remember the example from 3.1? Here it is:

```cpp
if(x == 4){
    func1();
}
else{
    return;
}
```

is the same as

```nasm
mov RAX, x
cmp RAX, 4
jne 5 ; Line 5 (ret)
call func1
ret
```

Hopefully, you can now work out the assembly version on its own. It moves the variable `x` into RAX, then it compares `x` to 4. If they _are not equal_ then it will return, if they _are equal_ then it calls "func1".

## Flipping Out

Remember how the compiler is all about efficiency? Let me show you how the compiler thinks, as you're going to see it constantly.

Instead of what a programmer would typically write:

```cpp
if(x == 4){
    func1();
}
else{
    return;
}
```

The compiler will generate something closer to:

```cpp
if(x != 4){
    goto __exit;
}
func1();
__exit:
return;
```

The compiler generates code this way because it's almost always more efficient and skips more code. The above examples may not see much of a performance improvement over one another, however, in larger programs the improvement can be quite significant.

## Pointers

Assembly has its ways of working with pointers and memory addresses as C/C++ does. In C/C++ you can use dereferencing to get the value inside of a memory address. For example:

```cpp
int main(){
    int num = 10;
    int* ptr = &num
    return (*ptr + 5);
}
```

- `ptr` is a pointer to `num`, which means `ptr` is holding the memory address of `num`.
    
- Then return the sum of what's at the address inside `ptr` (`num` which is 10) and 5.
    

Two of the most important things to know when working with pointers and addresses in Assembly are **LEA** and **square brackets**.

- **Square Brackets** - Square brackets dereference in assembly. For example, `[var]` is the address pointed to by var. In other words, when using `[var]` we want to access the memory address that `var` is holding.
    
- **LEA** - Ignore everything about square brackets when working with LEA. LEA is short for Load Effective Address and it's used for calculating and loading addresses.
    

**It's important to note that when working with the LEA instruction, square brackets do _not_ dereference.**

LEA is used to load and calculate addresses, NOT data. It doesn't matter if there are square brackets or not, it's dealing with addresses ONLY. LEA is the instruction that will mess with your head when you're sleep-deprived.

Here is a simple example of dereferencing and a pointer in Assembly:

```cpp
lea RAX, [var]
mov [RAX], 12
```

In the example above the _address_ of `var` is loaded into RAX. This is LEA we are working with, there is _no_ dereferencing. RAX is now acting as a pointer since it holds the address to the variable. Then 12 is moved into the address pointed to by RAX). The address pointed to by RAX is the `var` variable. If that Assembly was executed, `var` would be 12. This is all the same as doing `mov var, 12`.

Going back to the code example from when we started talking about pointers, here it is in _pseudo_-assembly:

```cpp
mov num, 10
lea ptr, [num]
mov rax, [ptr]
add rax, 5
ret
```

1. Move 10 into `num`
    
2. Load the address of `num` into `ptr`
    
3. Move the data that is at the address inside `ptr` (`num` which is 10) into `rax`.
    
4. Add rax (10) and 5.
    
5. RET - This will return the data inside RAX. This is explained later in calling conventions.
    

Earlier I said that LEA can be used to calculate addresses, and it often is, here's an example.

```cpp
lea RAX, [RCX+8] ;This will add 8 to the address inside RCX, and set RAX to the resulting address.
```

```cpp
mov RAX, [RCX+8] ;This will add 8 to the address already held by RCX, then dereference the new address and put whatever is at that address into RAX.
```

One more time:

**It's important to note that when working with LEA square brackets do _not_ dereference.**

You'll see LEA and MOV used all the time so be sure you understand this and pay attention to details.

## Zero Extension

Zero extension is setting the rest of the remaining bits in a register to zero when modifying the other bits. For example, if you moved a value into EAX should the upper 32 bits of RAX change?

In general, a move to the lower 32 bits of RAX via EAX _will_ zero out/zero extend the upper 32 bits. A move to anything less will _not_ zero extend. So moving something into AX will not zero out the rest of RAX. If you _do_ want to zero extend no matter what, use `movzx` which performs zero extension no matter what.

## The JMP's Mason, what do they mean?!

Let's talk about the difference between instructions such as `jg` (jump if greater) and `ja` (jump if above). Knowing the difference can help you snipe those hard-to-understand data types. There are other instructions like this so be sure to look up what they do when you come across them. For example, there are several variants of `mov`.

Here's the rundown for the jump instructions when it comes to signed or unsigned. Ignore the "CF" and "ZF" if you don't know what they mean, I've included them for reference after you understand flags (covered next).

For **_unsigned_** comparisons:

- JB/JNAE (CF = 1) ; Jump if below/not above or equal
    
- JAE/JNB (CF = 0) ; Jump if above or equal/not below
    
- JBE/JNA (CF = 1 or ZF = 1) ; Jump if below or equal/not above
    
- JA/JNBE (CF = 0 and ZF = 0); Jump if above/not below or equal
    

For **_signed_** comparisons:

JL/JNGE (SF <> OF) ; Jump if less/not greater or equal

JGE/JNL (SF = OF) ; Jump if greater or equal/not less

JLE/JNG (ZF = 1 or SF <> OF); Jump if less or equal/not greater

JG/JNLE (ZF = 0 and SF = OF); Jump if greater/not less or equal

Easy way to remember this, and how I remember it:

Humans normally work with signed numbers, and we usually say greater than or less than. That's how I remember signed goes with the greater than and less than jumps.

## Final Note

There are many more Assembly instructions that I haven't covered. As we continue I will introduce more instructions as they come. Don't be afraid to look up instructions, because like I said, there are quite a few (hundreds or thousands).

call - calls a funciton
mov - moves


### Register Size Breakdown
In x86-64 architecture, RBX is a 64-bit general-purpose register. It can be broken down into smaller sub-registers:
- **RBX**: The complete 64-bit (**8 bytes**) register.
- **EBX**: The lower 32 bits (**4 bytes**) of RBX.
- **BX**: The lower 16 bits (**2 bytes**) of EBX.
- **BH**: The higher 8 bits (**1 byte**) of BX.
- **BL**: The lower 8 bits (**1 byte**) of BX.
If you are writing or analyzing assembly functions, would you like to know how RBX acts as a **callee-saved register**, or would you like to see how it is used for **base addressing** in memory?