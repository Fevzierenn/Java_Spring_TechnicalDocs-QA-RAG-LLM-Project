# Java main() Method Explained

## **1\. Overview**

Every program needs a place to start its execution; talking about Java programs, that’s the _main_ method.

We’re so used to writing the _main_ method during our code sessions, that we don’t even pay attention to its details. In this quick article, we’ll analyze this method and show some other ways of writing it.

## **2\. Common Signature**

The most common main method template is:
    
    
    public static void main(String[] args) { }

That’s the way we’ve learned it, that’s the way the IDE autocompletes the code for us. But that’s not the only form this method can assume, **there are some valid variants we can use** and not every developer pays attention to this fact.

Before we dive into those method signatures, let’s review the meaning of each keyword of the common signature:

  * _public_ – access modifier, meaning global visibility
  * _static_ – the method can be accessed straight from the class, we don’t have to instantiate an object to have a reference and use it
  * _void_ – means that this method doesn’t return a value
  * _main_ – the name of the method, that’s the identifier JVM looks for when executing a Java program



As for the _args_ parameter, it represents the values received by the method. This is how we pass arguments to the program when we first start it.

The parameter _args_ is an array of _String_ s. In the following example:
    
    
    java CommonMainMethodSignature foo bar

we’re executing a Java program called _CommonMainMethodSignature_ and passing 2 arguments: _foo_ and _bar_. Those values can be accessed inside of the _main_ method as _args[0]_ (having _foo_ as value) and _args[1]_ (having _bar_ as value).

In the next example, we’re checking args to decide whether to load test or production parameters:
    
    
    public static void main(String[] args) {
        if (args.length > 0) {
            if (args[0].equals("test")) {
                // load test parameters
            } else if (args[0].equals("production")) {
                // load production parameters
            }
        }
    }

It’s always good to remember that IDEs can also pass arguments to the program.

## **3\. Different Ways to Write a _main()_ Method**

Let’s check some different ways to write the _main_ method. Although they’re not very common, they’re valid signatures.

Note that none of these are specific to the _main_ method, they can be used with any Java method but they are also a valid part of the _main_ method.

The square brackets can be placed near _String_ , as in the common template, or near _args_ on either side:
    
    
    public static void main(String []args) { }
    
    
    
    public static void main(String args[]) { }

Arguments can be represented as varargs:
    
    
    public static void main(String...args) { }

We can even add _strictfp_ for the _main()_ method, which is used for compatibility between processors when working with floating point values:
    
    
    public strictfp static void main(String[] args) { }

_synchronized_ and _final_ are also valid keywords for the _main_ method but they won’t have an effect here.

On the other hand, _final_ can be applied on _args_ to prevent the array from being modified:
    
    
    public static void main(final String[] args) { }

To end these examples, we can also write the _main_ method with all of the above keywords (which, of course, you probably won’t ever use in a practical application):
    
    
    final static synchronized strictfp void main(final String[] args) { }

## 4\. Having More Than One _main()_ Methods

We can also define **more than one _main_ method inside our application.**

In fact, some people use it as a primitive test technique to validate individual classes (although test frameworks like _JUnit_ are way more indicated for this activity).

To specify which _main_ method the JVM should execute as the entry point of our application, we use the _MANIFEST.MF_ file. Inside the manifest, we can indicate the main class:
    
    
    Main-Class: mypackage.ClassWithMainMethod

This is mostly used when creating an executable _.jar_ file. We indicate which class has the _main_ method to start the execution, through the manifest file located at _META-INF/MANIFEST.MF_ (encoded in UTF-8).

## **5\. Conclusion**

This tutorial described the details of the _main_ method and some other forms it can assume, even the ones that aren’t very common to most of the developers.

Keep in mind that, **although all the examples that we’ve shown are valid in terms of syntax, they just serve the educational purpose** and most of the time we’ll stick with the common signature to do our job.
