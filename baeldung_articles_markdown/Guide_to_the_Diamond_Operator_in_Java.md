# Guide to the Diamond Operator in Java

## **1\. Overview**

In this article, we’ll look at the **diamond operator in Java and how[generics](/java-generics) and the Collections API influenced its evolution**.

## **2\. Raw Types**

**Prior to Java 1.5, the Collections API supported only raw types** – there was no way for type arguments to be parameterized when constructing a collection:
    
    
    List cars = new ArrayList();
    cars.add(new Object());
    cars.add("car");
    cars.add(new Integer(1));

This allowed any type to be added and **led to potential casting exceptions at runtime**.

## **3\. Generics**

In Java 1.5, Generics were introduced – **which allowed us to parameterize the type arguments for classes** , including those in the Collections API – when declaring and constructing objects:
    
    
    List<String> cars = new ArrayList<String>();

At this point, we have to**specify the parameterized type in the constructor** , which can be somewhat unreadable:
    
    
    Map<String, List<Map<String, Map<String, Integer>>>> cars 
     = new HashMap<String, List<Map<String, Map<String, Integer>>>>();

The reason for this approach is that **raw types still exist for the sake of backward compatibility** , so the compiler needs to differentiate between these raw types and generics:
    
    
    List<String> generics = new ArrayList<String>();
    List<String> raws = new ArrayList();

Even though the compiler still allows us to use raw types in the constructor, it will prompt us with a warning message:
    
    
    ArrayList is a raw type. References to generic type ArrayList<E> should be parameterized

## **4\. Diamond Operator**

The diamond operator – introduced in Java 1.7 – **adds type inference and reduces the verbosity in the assignments – when using generics** :
    
    
    List<String> cars = new ArrayList<>();

The Java 1.7 compiler’s type inference feature **determines the most suitable constructor declaration that matches the invocation**.

Consider the following interface and class hierarchy for working with vehicles and engines:
    
    
    public interface Engine { }
    public class Diesel implements Engine { }
    public interface Vehicle<T extends Engine> { }
    public class Car<T extends Engine> implements Vehicle<T> { }

Let’s create a new instance of a _Car_ using the diamond operator:
    
    
    Car<Diesel> myCar = new Car<>();

Internally, the compiler knows that _Diesel_ implements the _Engine_ interface and then is able to determine a suitable constructor by inferring the type.

## **5\. Conclusion**

Simply put, the diamond operator adds the type inference feature to the compiler and reduces the verbosity in the assignments introduced with generics.
