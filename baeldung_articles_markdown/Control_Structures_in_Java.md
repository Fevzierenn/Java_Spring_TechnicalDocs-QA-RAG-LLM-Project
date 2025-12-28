# Control Structures in Java

## **1\. Overview**

In the most basic sense, a program is a list of instructions. **Control structures are programming blocks that can change the path we take through those instructions.**

In this tutorial, we’ll explore control structures in Java.

**There are three kinds of control structures:**

  * Conditional Branches, which we use **for choosing between two or more paths.** There are three types in Java: _if/else/else if_ , _ternary operator_ and _switch_.
  * Loops that are used to **iterate through multiple values/objects and repeatedly run specific code blocks.** The basic loop types in Java are _for_ , _while_ and _do while_.
  * Branching Statements, which are used to **alter the flow of control in loops.** There are two types in Java:  _break_ and _continue_.



## 2\. If/Else/Else If

The _if/else_ statement is [the most basic of control structures](/java-if-else), but can also be considered the very basis of decision making in programming.

While _if_ can be used by itself, the most common use-scenario is choosing between two paths with _if/else_ :
    
    
    if (count > 2) {
        System.out.println("Count is higher than 2");
    } else {
        System.out.println("Count is lower or equal than 2");
    }

**Theoretically, we can infinitely chain or nest _if/else_ blocks but this will hurt code readability, and that’s why it’s not advised.**

We’ll explore alternative statements in the rest of this article.

## 3\. Ternary Operator

**We can[use a ternary operator](/java-ternary-operator) as a shorthand expression that works like an _if/else_ statement.**

Let’s see our _if/else_ example again:
    
    
    if (count > 2) {
        System.out.println("Count is higher than 2");
    } else {
        System.out.println("Count is lower or equal than 2");
    }

We can refactor this with a ternary as follows:
    
    
    System.out.println(count > 2 ? "Count is higher than 2" : "Count is lower or equal than 2");

While ternary can be a great way to make our code more readable, it isn’t always a good substitute for _if/else._

## 4\. Switch

**If we have multiple cases to choose from, we can use a _switch_ statement.**

Let’s again see a simple example:
    
    
    int count = 3;
    switch (count) {
    case 0:
        System.out.println("Count is equal to 0");
        break;
    case 1:
        System.out.println("Count is equal to 1");
        break;
    default:
        System.out.println("Count is either negative, or higher than 1");
        break;
    }

Three or more _if/else_ statements can be hard to read. As one of the possible workarounds, we can use  _switch,_ as seen above.

And also keep in mind that [_switch_ has scope and input limitations](/java-switch) that we need to remember before using it.

## 5\. Loops

**We use[loops](/java-loops) when we need to repeat the same code multiple times in succession.**

Let’s see a quick example of comparable _for_ and _while_ type of loops:
    
    
    for (int i = 1; i <= 50; i++) {
        methodToRepeat();
    }
    
    int whileCounter = 1;
    while (whileCounter <= 50) {
        methodToRepeat();
        whileCounter++;
    }
    

Both code blocks above will call  _methodToRepeat_ 50 times.

## 6\. Break

**We need to use[ _break_](/java-continue-and-break) to exit early from a loop.**

Let’s see a quick example:
    
    
    List<String> names = getNameList();
    String name = "John Doe";
    int index = 0;
    for ( ; index < names.length; index++) {
        if (names[index].equals(name)) {
            break;
        }
    }

Here, we are looking for a name in a list of names, and we want to stop looking once we’ve found it.

A loop would normally go to completion, but we’ve used  _break_ here to short-circuit that and exit early.

## 7\. Continue

Simply put, [ _continue_](/java-continue-and-break) **means to skip the rest of the loop we’re in:**
    
    
    List<String> names = getNameList();
    String name = "John Doe";
    String list = "";
    for (int i = 0; i < names.length; i++) { 
        if (names[i].equals(name)) {
            continue;
        }
        list += names[i];
    }

Here, we skip appending the duplicate  _names_ into the list.

**As we’ve seen here,_break_ and  _continue_ can be handy when iterating, though they can often be rewritten with  _return_ statements or other logic.**

## 8\. Conclusion

In this quick article, we learned what control structures are and how to use them to manage flow control in our Java programs.
