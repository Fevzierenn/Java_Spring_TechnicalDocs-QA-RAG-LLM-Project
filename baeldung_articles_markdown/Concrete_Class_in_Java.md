# Concrete Class in Java

## **1\. Introduction**

In this quick guide, **we’ll discuss the term “concrete class” in Java**.

First, we’ll define the term. Then, we’ll see how it’s different from interfaces and abstract classes.

## **2\. What Is a Concrete Class?**

**A concrete class is a class that we can create an instance of, using the _new_ keyword**.

In other words, it’s a **full implementation of its blueprint**. A concrete class is complete.

Imagine, for example, a _Car_ class:
    
    
    public class Car {
        public String honk() {
            return "beep!";
        }
    
        public String drive() {
            return "vroom";
        }
    }

Because all of its methods are implemented, we call it a concrete class, and we can instantiate it:
    
    
    Car car = new Car();

Some examples of concrete classes from the JDK are **_HashMap_ , _HashSet_ , _ArrayList_ , and _LinkedList_.**

## **3\. Java Abstraction vs. Concrete Classes**

**Not all Java types implement all their methods, though.** This flexibility, also called _abstraction_ , allows us to think in more general terms about the domain we’re trying to model.

**In Java, we can achieve abstraction using interfaces and abstract classes.**

Let’s get a better look at concrete classes by comparing them to these others.

### **3.1. Interfaces**

**An interface is a blueprint for a class**. Or, in other words, its a collection of unimplemented method signatures:
    
    
    interface Driveable {
        void honk();
        void drive();
    }

**Note that it uses the _interface_ keyword instead of  _class._**

Because  _Driveable_ has unimplemented methods, we can’t instantiate it with the  _new_ keyword.

But, **concrete classes like _Car_ can implement these methods.**

The JDK provides a number of interfaces like ** _Map_ , _List_ , and _Set_.**

### **3.2. Abstract Classes**

**An abstract class is a class that has unimplemented methods,** though it can actually have both:
    
    
    public abstract class Vehicle {
        public abstract String honk();
    
        public String drive() {
            return "zoom";
        }
    }

**Note that we mark abstract classes with the keyword _abstract_.**

Again, since _Vehicle_ has an unimplemented method,  _honk_ , we won’t be able to use the _new_ keyword.

Some examples of abstract classes from the JDK are **_AbstractMap_ and _AbstractList_.**

### **3.3. Concrete Classes**

In contrast, **concrete classes don’t have any unimplemented methods.** Whether the implementations are inherited or not, so long as each method has an implementation, the class is concrete.

Concrete classes can be as simple as our _Car_ example earlier. They can also implement interfaces and extend abstract classes:
    
    
    public class FancyCar extends Vehicle implements Driveable {
        public String honk() { 
            return "beep";
        }
    }

The _FancyCar_ class provides an implementation for  _honk_ and it inherits the implementation of  _drive_ from  _Vehicle._

**As such, it has no unimplemented methods**. Therefore, we can create a _FancyCar_ class instance with the _new_ keyword.
    
    
    FancyCar car = new FancyCar();

**Or, simply put, all classes which are not abstract, we can call concrete classes.**

## **4\. Summary**

In this short tutorial, we learned about concrete classes and their specifications.

Additionally, we showed the differences between interfaces and concrete and abstract classes.
