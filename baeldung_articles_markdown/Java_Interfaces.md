# Java Interfaces

## 1\. Overview

In this tutorial, we’re going to talk about interfaces in Java. We’ll also see how Java uses them to implement polymorphism and multiple inheritances.

## 2\. What Are Interfaces in Java?

In Java, an interface is an abstract type that contains a collection of methods and constant variables. It is one of the core concepts in Java and is **used to achieve abstraction,[polymorphism](/java-polymorphism) and [multiple inheritances](/java-inheritance)**.

Let’s see a simple example of an interface in Java:
    
    
    public interface Electronic {
    
        // Constant variable
        String LED = "LED";
    
        // Abstract method
        int getElectricityUse();
    
        // Static method
        static boolean isEnergyEfficient(String electtronicType) {
            if (electtronicType.equals(LED)) {
                return true;
            }
            return false;
        }
    
        //Default method
        default void printDescription() {
            System.out.println("Electronic Description");
        }
    }
    

We can implement an interface in a Java class by using the _implements_ keyword.

Next, let’s also create a _Computer_ class that implements the _Electronic_ interface we just created:
    
    
    public class Computer implements Electronic {
    
        @Override
        public int getElectricityUse() {
            return 1000;
        }
    }
    

### 2.1. Rules for Creating Interfaces

In an interface, we’re allowed to use:

  * [constants variables](/java-final)
  * [abstract methods](/java-abstract-class)
  * [static methods](/java-static-default-methods)
  * [default methods](/java-static-default-methods)



We also should remember that:

  * we can’t instantiate interfaces directly
  * an interface can be empty, with no methods or variables in it
  * we can’t use the _final_ word in the interface definition, as it will result in a compiler error
  * all interface declarations should have the  _public_ or default access modifier; the _abstract_ modifier will be added automatically by the compiler
  * an interface method can’t be  _protected_ or _final_
  * up until Java 9, interface methods could not be _private_ ; however, Java 9 introduced the possibility to define [private methods in interfaces](/java-interface-private-methods)
  * interface variables are  _public_ , _static_ , and _final_ by definition; we’re not allowed to change their visibility



## 3\. What Can We Achieve by Using Them?

### 3.1. Behavioral Functionality

We use interfaces to add certain behavioral functionality that can be used by unrelated classes. For instance, _Comparable_ , _Comparator_ , and _Cloneable_ are Java interfaces that can be implemented by unrelated classes. Below is an example of the _Comparator_ interface __ that is used to compare two instances of the _Employee_ class:
    
    
    public class Employee {
    
        private double salary;
    
        public double getSalary() {
            return salary;
        }
    
        public void setSalary(double salary) {
            this.salary = salary;
        }
    }
    
    public class EmployeeSalaryComparator implements Comparator<Employee> {
    
        @Override
        public int compare(Employee employeeA, Employee employeeB) {
            if (employeeA.getSalary() < employeeB.getSalary()) {
                return -1;
            } else if (employeeA.getSalary() > employeeB.getSalary()) { 
                return 1;
            } else {
                return 0;
            }
        }
    }
    

For more information, please visit our tutorial on [ _Comparator_ and _Comparable_ in Java.](/java-comparator-comparable)

### 3.2. Multiple Inheritances

Java classes support singular inheritance. However, by using interfaces, we’re also able to implement multiple inheritances.

For instance, in the example below, we notice that the  _Car_ class __ implements the _Fly_ and  _Transform_ interfaces. By doing so, it inherits the methods _fly_ and _transform_ :
    
    
    public interface Transform {
        void transform();
    }
    
    public interface Fly {
        void fly();
    }
    
    public class Car implements Fly, Transform {
    
        @Override
        public void fly() {
            System.out.println("I can Fly!!");
        }
    
        @Override
        public void transform() {
            System.out.println("I can Transform!!");
        }
    }
    

### 3.3. Polymorphism

Let’s start with asking the question: what is [polymorphism](/java-polymorphism)? It’s the ability for an object to take different forms during runtime. To be more specific it’s the execution of the override method that is related to a specific object type at runtime.

**In Java, we can achieve polymorphism using interfaces.** For example, the  _Shape_ interface can take different forms — it can be a _Circle_ or a _Square._

Let’s start by defining the _Shape_ interface:
    
    
    public interface Shape {
        String name();
    }
    

Now let’s also create the  _Circle_ class:
    
    
    public class Circle implements Shape {
    
        @Override
        public String name() {
            return "Circle";
        }
    }
    

And also the  _Square_ class:
    
    
    public class Square implements Shape {
    
        @Override
        public String name() {
            return "Square";
        }
    }
    

Finally, it’s time to see polymorphism in action using our  _Shape_ interface and its implementations. Let’s instantiate some  _Shape_ objects, add them to a _List_ _,_ and, finally, print their names in a loop:
    
    
    List<Shape> shapes = new ArrayList<>();
    Shape circleShape = new Circle();
    Shape squareShape = new Square();
    
    shapes.add(circleShape);
    shapes.add(squareShape);
    
    for (Shape shape : shapes) {
        System.out.println(shape.name());
    }
    

## 4\. Default Methods in Interfaces

Traditional interfaces in Java 7 and below don’t offer backward compatibility.

What this means is that **if you have legacy code written in Java 7 or earlier, and you decide to add an abstract method to an existing interface, then all the classes that implement that interface must override the new abstract method**. Otherwise, the code will break.

**Java 8 solved this problem by introducing the default method** that is optional and can be implemented at the interface level.

## 5\. Interface Inheritance Rules

In order to achieve multiple inheritances thru interfaces, we have to remember a few rules. Let’s go over these in detail.

### 5.1. Interface Extending Another Interface

When an interface _extends_ another interface, it inherits all of that interface’s abstract methods. Let’s start by creating two interfaces,  _HasColor_ and  _Shape_ :
    
    
    public interface HasColor {
        String getColor();
    }
    
    public interface Box extends HasColor {
        int getHeight()
    }
    

In the example above,  _Box_ inherits from  _HasColor_ using the keyword _extends._ By doing so, the _Box_ interface inherits  _getColor_. As a result, the  _Box_ interface now has two methods:  _getColor_ and  _getHeight_.

### 5.2. Abstract Class Implementing an Interface

When an abstract class implements an interface, it inherits all of its abstract and default methods. Let’s consider the  _Transform_ interface and the _abstract_ class  _Vehicle_ that implements it:
    
    
    public interface Transform {
        
        void transform();
        default void printSpecs(){
            System.out.println("Transform Specification");
        }
    }
    
    public abstract class Vehicle implements Transform {}
    

In this example, the _Vehicle_ class inherits two methods: the abstract  _transform_ method and the default  _printSpecs_ method.

## 6\. Functional Interfaces

Java has had many functional interfaces since its early days, such as _Comparable_ (since Java 1.2) and _Runnable_ (since Java 1.0).

Java 8 introduced new functional interfaces such as _Predicate_ , _Consumer_ , and _Function_. To learn more about these, please visit our tutorial on [Functional Interfaces in Java 8](/java-8-functional-interfaces).

## 7\. Conclusion

In this tutorial, we gave an overview of Java interfaces, and we talked about how to use them to achieve polymorphism and multiple inheritances.
