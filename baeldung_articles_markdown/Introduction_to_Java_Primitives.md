# Introduction to Java Primitives

## 1\. Overview

The Java Programming Language features eight primitive data types.

In this tutorial, we’ll look at what these primitives are and go over each type.

## 2\. Primitive Data Types

The eight primitives defined in Java are _int_ , _byte_ , _short_ , _long_ , _float_ , _double_ , _boolean_ and _char_. These aren’t considered objects and represent raw values.

**They’re stored directly on the stack** (check out [this article](/java-initialization) for more information about memory management in Java).

We’ll take a look at storage size, default values and examples of how to use each type.

Let’s start with a quick reference:

Type | Size (bits) | Minimum | Maximum | Example  
---|---|---|---|---  
_byte_ | 8 | -27 | 27– 1 | _byte b = 100;_  
_short_ | 16 | -215 | 215– 1 | _short s = 30_000;_  
_int_ | 32 | -231 | 231– 1 | _int i = 100_000_000;_  
_long_ | 64 | -263 | 263– 1 | _long l = 100_000_000_000_000;_  
_float_ | 32 | -2-149 | (2-2-23)·2127 | _float f = 1.456f;_  
_double_ | 64 | -2-1074 | (2-2-52)·21023 | _double f = 1.456789012345678;_  
_char_ | 16 | 0 | 216– 1 | _char c = ‘c’;_  
_boolean_ | 1 | – | – | _boolean b = true;_  
  
### 2.1. _int_

The first primitive data type we’re going to cover is _int_. Also known as an integer, _int_ type holds a wide range of non-fractional number values.

Specifically, **Java stores it using 32 bits of memory.** In other words, it can represent values from -2,147,483,648 (-231) to 2,147,483,647 (231-1).

In Java 8, it’s possible to store an unsigned integer value up to 4,294,967,295 (232-1) by using new special helper functions.

We can simply declare an _int_ :
    
    
    int x = 424_242;
    
    int y;

**The default value of an _int_ declared without an assignment is 0.**

**If the variable is defined in a method, we must assign a value before we can use it.**

We can perform all standard arithmetic operations on _int_ s. Just be aware that **decimal values will be chopped off** when performing these on integers.

### 2.2. _byte_

_byte_ is a primitive data type similar to _int_ , except**it only takes up 8 bits of memory.** This is why we call it a byte. Because the memory size is so small, _byte_ can only hold the values from -128 (-27) to 127 (27 – 1).

Here’s how we can create _byte_ :
    
    
    byte b = 100;
    
    byte empty;

**The default value of _byte_ is also 0.**

### 2.3. _short_

The next stop on our list of primitive data types in Java is _short_.

If we want to save memory and _byte_ is too small, we can use the type halfway between _byte_ and _int_ : _short_.

At 16 bits of memory, it’s half the size of _int_ and twice the size of _byte_. Its range of possible values is -32,768(-215) to 32,767(215 – 1).

_short_ is declared like this:
    
    
    short s = 20_020;
    
    short s;

Also similar to the other types, the default value is 0. We can use all standard arithmetic on it as well.

### 2.4. _long_

Our last primitive data type related to integers is _long_.

_long_ is the big brother of _int_. **It’s stored in 64 bits of memory** , so it can hold a significantly larger set of possible values.

The possible values of a long are between -9,223,372,036,854,775,808 (-263) to 9,223,372,036,854,775,807 (263 – 1).

We can simply declare one:
    
    
    long l = 1_234_567_890;
    
    long l;

As with other integer types, the default is also 0. We can use all arithmetic on _long_ that works on _int_.

### 2.5. _float_

We represent basic fractional numbers in Java using the _float_ type. This is a single-precision decimal number. This means that if we get past six decimal points, the number becomes less precise and more of an estimate.

In most cases, we don’t care about the precision loss. But if our calculation requires absolute precision (e.g., financial operations, landing on the moon, etc.), we need to use specific types designed for this work. For more information, check out the Java class [Big Decimal](/java-bigdecimal-biginteger).

**This type is stored in 32 bits of memory just like _int_.** However, because of the floating decimal point, its range is much different. It can represent both positive and negative numbers. The smallest decimal is 1.40239846 x 10-45, and the largest value is 3.40282347 x 1038.

We declare _float_ s the same as any other type:
    
    
    float f = 3.145f;
    
    float f;

**And the default value is 0.0 instead of 0.** Also, notice we add the _f_ designation to the end of the literal number to define a float. Otherwise, Java will throw an error because the default type of a decimal value is _double_.

We can also perform all standard arithmetic operations on _float_ s. However, it’s important to note that we perform floating point arithmetic very differently than integer arithmetic.

### 2.6. _double_

Next, we look at _double_. Its name comes from the fact that it’s a double-precision decimal number.

**It’s stored in 64 bits of memory.** This means it represents a much larger range of possible numbers than _float_.

Although, it does suffer from the same precision limitation as _float_ does. The range is 4.9406564584124654 x 10-324 to 1.7976931348623157 x 10308. That range can also be positive or negative.

Declaring _double_ is the same as other numeric types:
    
    
    double d = 3.13457599923384753929348D;
    
    double d;

**The default value is also 0.0 as it is with** _**float**_**.** Similar to _float,_ we attach the letter _D_ to designate the literal as a double.

### 2.7. _boolean_

The simplest primitive data type is _boolean_. It can contain only two values: _true_ or _false_. **It stores its value in a single bit.**

**However, for convenience, Java pads the value and stores it in a single byte.**

Here’s how we declare _boolean_ :
    
    
    boolean b = true;
    
    boolean b;

Declaring it without a value defaults to _false_. _boolean_ is the cornerstone of controlling our programs flow. We can use boolean operators on them (e.g., _and_ ,_or_ , etc.).

### 2.8. _char_

The final primitive data type to look at is _char_.

Also called a character, _char_ is a 16-bit integer representing a Unicode-encoded character. Its range is from 0 to 65,535. In Unicode, this represents _‘\u0000’_ to _‘\uffff’_.

For a list of all possible Unicode values, check out sites such as [Unicode Table](https://unicode-table.com/en/).

Let’s now declare a _char_ :
    
    
    char c = 'a';
    
    char c = 65;
    
    char c;

When defining our variables, we can use any character literal, and they will get automatically transformed into their Unicode encoding for us. A character’s default value is _‘/u0000’_.

### 2.9. Overflow

The primitive data types have size limits. But what happens if we try to store a value that’s larger than the maximum value?

**We run into a situation called _overflow_. **

When an integer overflows, it rolls over to the minimum value and begins counting up from there.

Floating point numbers overflow by returning Infinity:
    
    
    int i = Integer.MAX_VALUE;
    int j = i + 1;
    // j will roll over to -2_147_483_648
    
    double d = Double.MAX_VALUE;
    double o = d + 1;
    // o will be Infinity

_Underflow_ is the same issue except it involves storing a value smaller than the minimum value. When the numbers underflow, they return 0.0.

### 2.10. Autoboxing

Each primitive data type also has a full Java class implementation that can wrap it. For instance, the _Integer_ class can wrap an _int_. There is sometimes a need to convert from the primitive type to its object wrapper (e.g., using them with [generics](/java-generics)).

Luckily, Java can perform this conversion for us automatically, a process called _Autoboxing_ :
    
    
    Character c = 'c';
    
    Integer i = 1;

## 3\. Conclusion

In this article, we’ve covered the eight primitive data types supported in Java.

These are the building blocks used by most, if not all, Java programs out there, so it’s well worth understanding how they work.
