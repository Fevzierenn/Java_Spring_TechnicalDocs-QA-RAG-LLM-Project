# Unnamed Classes and Instance Main Methods in Java

## **1\. Introduction**

Java 21 is here, and among the new features, we can see how Java is becoming increasingly accessible for beginners with [the unnamed classes and instance main methods](https://openjdk.org/jeps/445). The introductions of these are crucial steps forward in making Java a more beginner-friendly programming language.

In this tutorial, we’ll explore these new features and understand how they make the learning curve smoother for students.

## **2\. Writing a Basic Java Program**

Traditionally, for beginners, writing their first Java program was a little more complicated than in other programming languages. A basic Java program required the declaration of a _public_ class. This class encloses a _public static void main(String[] args)_ method, serving as the entry point of the program.

All of this is just to write a _“Hello world”_ in the console:
    
    
    public class HelloWorld {
        public static void main(String[] args) {
            System.out.println("Hello, World!");
        }
    }

Java 21 greatly simplifies the way we can write a simple program:
    
    
    void main() {
        System.out.println("Hello, World!");
    }

We’ll go into more detail about how we achieved this syntax simplification using the new features.

## **3\. Instance Main Methods**

The introduction of instance _main()_ methods allows developers to utilize a more dynamic approach to initializing their applications.

### 3.1. Understanding Instance Main Methods

This has changed the way Java programs declare their entry points. In fact, Java earlier required the presence of a [_static_ _main()_ method](/java-main-method) with a _String[]_ parameter in the _public_ class, as we saw in the previous section.

This new protocol is more lenient. It enables the use of _main()_ methods with varied [access levels](/java-access-modifiers): _public_ , _protected_ , or default (package).

**Also, it doesn’t require the methods to be _static_ or to have a _String[]_ parameter:**
    
    
    class HelloWorld {
        void main() {
            System.out.println("Hello, World!");
        }
    }

### 3.2. Choosing a Launch Protocol

The refined launch protocol chooses automatically a starting point for our program, taking into account both availability and access level.

**Instance _main()_ methods should always have a non-_private_ access level**. Moreover, the launch protocol follows a specific order to decide which method to use:

  1. a _static void main(String[] args)_ method declared in the launched class
  2. a _static void main()_ method declared in the launched class
  3. a _void main(String[] args)_ instance method declared in the launched class or inherited from a superclass
  4. a _void main()_ instance method



**When a class declares an instance _main()_ method and inherits a [standard _static_ _main()_ method](/java-hello-world), the system invokes the instance _main()_ method**. In such cases, the [JVM](/jvm-vs-jre-vs-jdk#jvm) issues a warning at runtime.

For example, let’s suppose we have a superclass _HelloWorldSuper,_ that implements a long-established _main()_ method:
    
    
    public class HelloWorldSuper {
        public static void main(String[] args) {
            System.out.println("Hello from the superclass");
        }
    }

This superclass is extended by a _HelloWorldChild_ class:
    
    
    public class HelloWorldChild extends HelloWorldSuper {
        void main() {
            System.out.println("Hello, World!");
        }
    }
    

Let’s compile the superclass and run the child using the _— source 21_ and _–enable-preview_ flags:
    
    
    javac --source 21 --enable-preview HelloWorldSuper.java
    java --source 21 --enable-preview HelloWorldChild

We’ll get the following output in the console:
    
    
    WARNING: "void HelloWorldChild.main()" chosen over "public static void HelloWorldSuper.main(java.lang.String[])"
    Hello, World!

We can see how the JVM warns us that we have two possible entry points in our program.

## **4\. Unnamed Classes**

Unnamed classes are a significant feature designed to simplify the learning curve for beginners. **It allows methods, fields, and classes to exist without explicit class declarations.**

Typically, in Java, every class exists within a package and every package within a module. Unnamed classes, however, exist in the unnamed package and unnamed module. They are _final_ and can only extend the _Object_ class without implementing any interface.

Given all this, we can declare the _main()_ method without declaring the class explicitly in the code:
    
    
    void main() { 
        System.out.println("Hello, World!");
    }

Using these two new features, we managed to turn the program into a very simple one that can be much easier to understand by any person who starts programming in Java.

An unnamed class is almost exactly like an explicitly declared class. Other methods or variables are interpreted as members of the unnamed class, so we can add them to our class:
    
    
    private String getMessage() {
        return "Hello, World!";
    }
    void main() {
        System.out.println(getMessage());
    }
    

Despite their simplicity and flexibility, unnamed classes have inherent limitations.

**Direct constructions or references by name are impossible, and they don’t define any API accessible from other classes**. This inaccessibility also causes the [Javadoc](/javadoc) tool to falter when generating API documentation for such classes. However, future Java releases may adjust and enhance these behaviors.

## **5\. Conclusion**

In this article, we learned that Java 21, with the introduction of unnamed classes and instance main() methods, has made significant progress in enhancing user experience, especially for those at the beginning of their programming journey.

By simplifying the structural aspects of programming, these features allow novices to focus on logical thinking and problem-solving more quickly.
