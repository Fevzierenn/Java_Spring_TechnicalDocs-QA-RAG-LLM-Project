# Java Switch Statement

## **1\. Overview**

In this tutorial, we’ll learn what the  _switch_ statement is and how to use it.

**The _switch_ statement allows us to replace several nested _if-else_ constructs and thus improve the readability of our code.**

_Switch_ has evolved over time. New supported types have been added, particularly in Java 5 and 7. Also, it continues to evolve — _switch_ expressions will likely be introduced in Java 12.

Below we’ll give some code examples to demonstrate the use of the _switch_ statement, the role of the _break_ statement, the requirements for the _switch_ argument/_case_ values and the comparison of _String_ s in a _switch_ statement.

Let’s move on to the example.

## **2\. Example of Use**

Let’s say we have the following nested _if-else_ statements:
    
    
    public String exampleOfIF(String animal) {
        String result;
        if (animal.equals("DOG") || animal.equals("CAT")) {
            result = "domestic animal";
        } else if (animal.equals("TIGER")) {
            result = "wild animal";
        } else {
            result = "unknown animal";
        }
        return result;
    }

The above code doesn’t look good and would be hard to maintain and reason about.

To improve readability, we could make use of a _switch_ statement:
    
    
    public String exampleOfSwitch(String animal) {
        String result;
        switch (animal) {
            case "DOG":
                result = "domestic animal"; 
                break;
            case "CAT":
                result = "domestic animal";
                break;
            case "TIGER":
                result = "wild animal";
                break;
            default:
                result = "unknown animal";
                break;
        }
        return result;
    }

We compare the _switch_ argument _animal_ with the several _case_ values. If none of the _case_ values is equal to the argument, the block under the _default_ label is executed.

**Simply put, the _break_ statement is used to exit a _switch_ statement.**

## **3\. The _break_ Statement**

Although most of the  _switch_ statements in real life imply that only one of the _case_ blocks should be executed, the _break_ statement is necessary to exit a _switch_ after the block completes.

**If we forget to write a _break_ , the blocks underneath will be executed.**

To demonstrate this, let’s omit the _break_ statements and add the output to the console for each block:
    
    
    public String forgetBreakInSwitch(String animal) {
        switch (animal) {
        case "DOG":
            System.out.println("domestic animal");
        default:
            System.out.println("unknown animal");
        }
    }

Let’s execute this code _forgetBreakInSwitch_(_“DOG”)_ and check the output to prove that all the blocks get executed:
    
    
    domestic animal
    unknown animal

So, we should be careful and add _break_ statements at the end of each block unless there is a need to pass through to the code under the next label.

The only block where a  _break_ is not necessary is the last one, but adding a  _break_ to the last block makes the code less error-prone.

We can also take advantage of this behavior to **omit _break_ when we want the same code executed for several case statements. **

Let’s rewrite the example in the previous section by grouping together the first two cases:
    
    
    public String exampleOfSwitch(String animal) {
        String result;
        switch (animal) {
            case "DOG":
            case "CAT":
                result = "domestic animal";
                break;
            case "TIGER":
                result = "wild animal";
                break;
            default:
                result = "unknown animal";
                break;
        }
        return result;
    }

## **4._switch_ Argument and _case_ Values**

Now let’s discuss the allowed types of _switch_ argument and _case_ values, the requirements for them and how the  _switch_ statement works with Strings.

### **4.1. Data Types**

We can’t compare all the types of objects and primitives in the  _switch_ statement. **A _switch_ works only with four primitives and their wrappers as well as with the _enum type_ and the  _String_ class**:

  * _byte_ and _Byte_
  * _short_ and _Short_
  * _int_ and _Integer_
  * _char_ and _Character_
  * _enum_
  * _String_



_String_ type is available in the _switch_ statement starting with Java 7.

_enum_ type was introduced in Java 5 and has been available in the _switch_ statement since then.

Wrapper classes have also been available since Java 5.

Of course, _switch_ argument and _case_ values should be of the same type.

### 4.2. **No _null_ Values**

**We can’t pass the _null_ value as an argument to a _switch_ statement. **

If we do, the program will throw _NullPointerException_ , using our first _switch_ example:
    
    
    @Test(expected=NullPointerException.class)
    public void whenSwitchAgumentIsNull_thenNullPointerException() {
        String animal = null;
        Assert.assertEquals("domestic animal", s.exampleOfSwitch(animal));
    }

Of course, we can’t also pass _null_ as a value to the _case_ label of a _switch_ statement. If we do, the code will not compile.

### **4.3._Case_ Values as Compile-Time Constants**

If we try to replace the  _DOG_ case value with the variable dog, the code won’t compile until we mark the _dog_ variable as  _final_ :
    
    
    final String dog="DOG";
    String cat="CAT";
    
    switch (animal) {
    case dog: //compiles
        result = "domestic animal";
    case cat: //does not compile
        result = "feline"
    }

### **4.4._String_ Comparison**

If a _switch_ statement used the equality operator to compare strings, we couldn’t compare a  _String_ argument created with the _new_ operator to a  _String_ case value correctly.

Luckily, the ** _switch_ operator uses the _equals()_ method under the hood.**

Let’s demonstrate this:
    
    
    @Test
    public void whenCompareStrings_thenByEqual() {
        String animal = new String("DOG");
        assertEquals("domestic animal", s.exampleOfSwitch(animal));
    }

## **5._switch_ Expressions**

[JDK 13](https://openjdk.java.net/jeps/354) is now available and brings an improved version of a new feature first introduced in [JDK 12](https://openjdk.java.net/jeps/325): the _switch_ expression.

**In order to enable it, we need to pass _–enable-preview_ to the compiler.**

### 5.1. The New _switch_ Expression

Let’s see what the new _switch_ expression looks like when switching over months:
    
    
    var result = switch(month) {
        case JANUARY, JUNE, JULY -> 3;
        case FEBRUARY, SEPTEMBER, OCTOBER, NOVEMBER, DECEMBER -> 1;
        case MARCH, MAY, APRIL, AUGUST -> 2;
        default -> 0; 
    };
    

Sending in a value such as _Month.JUNE_ would set _result_ to _3_.

Notice that the new syntax uses the _- > _operator instead of the colon we’re used to with _switch_ statements. Also, there’s no _break_ keyword: The _switch_ expression doesn’t fall through  _case_ s.

Another addition is the fact that we can now have comma-delimited criteria.

### 5.2. The _yield_ Keyword

Going a bit further, there’s a possibility to obtain fine-grain control over what’s happening on the right side of the expression by using code blocks.

In such a case, we need to use the keyword _yield_ :
    
    
    var result = switch (month) {
        case JANUARY, JUNE, JULY -> 3;
        case FEBRUARY, SEPTEMBER, OCTOBER, NOVEMBER, DECEMBER -> 1;
        case MARCH, MAY, APRIL, AUGUST -> {
            int monthLength = month.toString().length();
            yield monthLength * 4;
        }
        default -> 0;
    };

While our example is a bit arbitrary, the point is that we’ve got access to more of the Java language here.

### 5.3. Returning Inside _switch_ Expressions

As a consequence of the distinction between _switch_ statements and _switch_ expressions, **it is possible to _return_ from inside a _switch_ statement, but we’re not allowed to do so from within a _switch_ expression.**

The following example is perfectly valid and will compile:
    
    
    switch (month) {
        case JANUARY, JUNE, JULY -> { return 3; }
        default -> { return 0; }
    }

However, the following code will not compile, as we are trying to _return_ outside of an enclosing switch expression:
    
    
    var result = switch (month) {
        case JANUARY, JUNE, JULY -> { return 3; }
        default -> { return 0; }
    };

### 5.4. Exhaustiveness

When using _switch_ statements, **it doesn’t really matter if all cases are covered.**

The following code, for example, is perfectly valid and will compile:
    
    
    switch (month) { 
        case JANUARY, JUNE, JULY -> 3; 
        case FEBRUARY, SEPTEMBER -> 1;
    }

For _switch_ expressions though, the compiler insists that **all possible cases are covered.**

The following code snippet would not compile, as there’s no default case and not all possible cases are covered:
    
    
    var result = switch (month) {
        case JANUARY, JUNE, JULY -> 3;
        case FEBRUARY, SEPTEMBER -> 1;
    }

The _switch_ expression, however, will be valid when all possible cases are covered:
    
    
    var result = switch (month) {
        case JANUARY, JUNE, JULY -> 3;
        case FEBRUARY, SEPTEMBER, OCTOBER, NOVEMBER, DECEMBER -> 1;
        case MARCH, MAY, APRIL, AUGUST -> 2;
    }

Please note that the above code snippet does not have a _default_ case. As long as all cases are covered, the _switch_ expression will be valid.

**Note: since this writing,[pattern matching](/java-switch-pattern-matching) was included in Java 21.**

## **6\. Conclusion**

In this article, we discussed the subtleties of using the _switch_ statement in Java. We can decide whether to use _switch_ based on readability and the type of the compared values.

The switch statement is a good candidate for cases when we have a limited number of options in a predefined set (e.g., days of the week).

Otherwise, we’d have to modify the code each time a new value is added or removed, which may not be feasible. For these cases, we should consider other approaches such as [polymorphism](/java-polymorphism) or other design patterns such as [Command](/java-command-pattern).
