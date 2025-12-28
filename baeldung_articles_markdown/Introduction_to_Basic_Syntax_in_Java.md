# Introduction to Basic Syntax in Java

## **1\. Overview**

Java is a statically-typed, object-oriented programming language. It’s also platform-independent — Java programs can be written and compiled on one type of machine, such as a Windows system, and executed on another, such as MacOS, without any modification to the source code.

In this tutorial, we’re going to look at and understand the basics of Java syntax.

## **2\. Data Types**

There are two broad categories of data types in Java: [primitive types and objects/reference types](/java-primitives-vs-objects).

[**Primitive types**](/java-primitives)**are the basic data types that store simple data** and form the foundation of data manipulation. For example, Java has primitive types for integer values (_int, long,_  _byte, short_)_,_ floating-point values (_float_ and _double_)_,_ character values (_char_), and logical values (_boolean_).

On the other hand, **reference types are objects that contain references to values and/or other objects** , or to the special value _null_ to denote the absence of value.

The _String_ class is a good example of a reference type. An instance of the class, called an object, represents a sequence of characters, such as “Hello World”.

## **3\. Declaring Variables in Java**

To declare a variable in Java, we must **specify its name (also called an identifier) and type**. Let’s see a simple example:
    
    
    int a;
    int b;
    double c;

In the above example, the variables will receive default initial values based on their declared types. Since we declared our variables to be  _int_ and _double_ , they’ll have a default of 0 and 0.0, respectively.

Alternatively, **we can use the assignment operator (=) to initialize variables during declaration:**
    
    
    int a = 10;

In the above example, we declare a variable with an **identifier** _**a** _to be of **type _int_** and **assign a value of 10** to it **using the assignment operator (=) and terminate the statement with a semi-colon (;)**.**** It’s compulsory, in Java, that all statements end with a semi-colon.

**An identifier is a name of any length, consisting of letters, digits, underscore, and dollar sign,** that conforms to the following rules:

  * starts with a letter, an underscore (_), or a dollar sign ($)
  * can’t be a reserved keyword
  * can’t be _true_ , _false,_ or _null_



Let’s expand our code snippet above to include a simple arithmetic operation:
    
    
    int a = 10;
    int b = 5;
    double c = a + b;
    System.out.println( a + " + " + b + " = " + c);

We can read the first three lines of the code snippet above as **“assign the value of 10 to _a,_ assign the value of 5 to  _b,_ sum the values of  _a_ and  _b_ and assign the result to ****c”**. In the last line, we output the result of the operation to the console:
    
    
    10 + 5 = 15.0

Declaration and initialization of variables of other types follow the same syntax that we’ve shown above. For example, let’s declare  _String_ , _char_ , and  _boolean_ variables:
    
    
    String name = "Baeldung Blog";
    char toggler = 'Y';
    boolean isVerified = true;

For emphasis sake**, the main difference in representing literal values of _char_ and  _String_ is the number of quotes that surrounds the values**. Therefore,  _‘a’_ is a  _char_ while _“a”_ is a  _String._

## **4\. Arrays**

An array is a reference type that can store a collection of values of a specific type. The general syntax for declaring an array in Java is:

_**type[] identifier = new type[length];**_

The type can any primitive or reference type.

For example, let’s see how to declare an array that can hold a maximum of 100 integers:
    
    
    int[] numbers = new int[100];

To refer to a specific element of an array, or to assign a value to an element, we use the variable name and its index:
    
    
    numbers[0] = 1;
    numbers[1] = 2;
    numbers[2] = 3;
    int thirdElement = numbers[2];

In Java, **array indexes start at zero.** The first element of an array is at index 0, the second element is at index 1, and so on.

Additionally, we can get the length of the array by calling _numbers.length_ :
    
    
    int lengthOfNumbersArray = numbers.length;

## **5\. Java Keywords**

**Keywords are reserved words that have special meaning in Java.**

For example, _public, static, class, main, new, instanceof_ , are [keywords in Java](/tag/java-keyword/), and as such, **we can’t use them as identifiers (variable names)**.

## **6\. Operators in Java**

Now that we’ve seen the assignment operator (=) above, let’s explore some other types of [operators in the Java language](https://docs.oracle.com/javase/tutorial/java/nutsandbolts/opsummary.html):

### **6.1. Arithmetic Operators**

Java supports the following [arithmetic operators](https://docs.oracle.com/javase/tutorial/java/nutsandbolts/op1.html) that can be used for writing mathematical, computational logic:

  * \+ (plus or addition; also used for string concatenation)
  * – (minus or subtraction)
  * * (multiplication)
  * / (division)
  * % (modulus or remainder)



We’ve used the plus (+) operator in our previous code example to perform addition of two variables. The other arithmetic operators are used similarly.

Another use of plus (+) is for concatenation (joining) of strings to form a whole new string:
    
    
    String output =  a + " + " + b + " = " + c;

### **6.2. Logical Operators**

In addition to arithmetic operators, Java supports the following [logical operators](https://docs.oracle.com/javase/tutorial/java/nutsandbolts/op2.html) for evaluating boolean expressions:

  * && (AND)
  * || (OR)
  * ! (NOT)



Let’s consider the following code snippets that demonstrate the logical AND and OR operators. The first example shows a print statement that executes when the _number_ variable is divisible both by 2 AND by 3:
    
    
    int number = 6;
            
    if (number % 2 == 0 && number % 3 == 0) {
        System.out.println(number + " is divisible by 2 AND 3");
    }

While the second is executed when _number_ is divisible by 2 OR by 5:
    
    
    if (number % 2 == 0 || number % 5 == 0) {
        System.out.println(number + " is divisible by 2 OR 5");
    }

### **6.3. Comparison Operators**

When we need to compare the value of one variable to that of another, we can use Java’s [comparison operators](https://docs.oracle.com/javase/tutorial/java/nutsandbolts/op2.html):

  * _<_ (less than)
  * <= (less than or equal to)
  * > (greater than)
  * >= (greater than or equal to)
  * == (equal to)
  * != (NOT equal to)



For example, we can use a comparison operator to determine the eligibility of a voter:
    
    
    public boolean canVote(int age) {
        if(age < 18) {
            return false;
        }
        return true;
    }

## **7\. Java Program Structure**

Now that we’ve learned about data types, variables, and a few basic operators, let’s see how to put these elements together in a simple, executable program.

**The basic unit of a Java program is a _Class_.** A _Class_ can have one or more fields (sometimes called properties)_,_ methods, and even other class members called inner classes.

**For a _Class_ to be executable, it must have a  _main_ method.** The  _main_ method signifies the entry point of the program.

Let’s write a simple, executable _Class_ to exercise one of the code snippets we considered earlier:
    
    
    public class SimpleAddition {
    
        public static void main(String[] args) {
            int a = 10;
            int b = 5;
            double c = a + b;
            System.out.println( a + " + " + b + " = " + c);
        }
    }

The name of the class is  _SimpleAddition_ , and inside of it, we have a _main_ method that houses our logic. **The segment of code between an opening and closing curly braces is called a code block.**

The source code for a Java program is stored in a file with an extension of  _.java_.

## **8\. Compiling and Executing a Program**

To execute our source code, we first need to compile it. This process will generate a binary file with  _the .class_ file extension. We can execute the binary file on any machine that has a Java Runtime Environment (JRE) installed.

Let’s save our source code from the above example into a file named  _SimpleAddition.java_ and run this command from the directory where we’ve saved the file:
    
    
    javac SimpleAddition.java

To execute the program, we simply run:
    
    
    java SimpleAddition

This will produce the same output to the console as shown above:
    
    
    10 + 5 = 15.0

## **9\. Conclusion**

In this tutorial, we’ve looked at some of the basic syntax of Java. Just like any other programming language, it gets simpler with constant practice.
