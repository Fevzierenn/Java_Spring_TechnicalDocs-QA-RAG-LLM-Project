# Guide to Inheritance in Java

## **1\. Overview**

One of the core principles of Object-Oriented Programming – **inheritance – enables us to reuse existing code or extend an existing type.**

Simply put, in Java, a class can inherit another class and multiple interfaces, while an interface can inherit other interfaces.

In this article, we’ll start with the need for inheritance, moving to how inheritance works with classes and interfaces.

Then, we’ll cover how the variable/ method names and access modifiers affect the members that are inherited.

And at the end, we’ll see what it means to inherit a type.

## **2\. The Need for Inheritance**

Imagine, as a car manufacturer, you offer multiple car models to your customers. Even though different car models might offer different features like a sunroof or bulletproof windows, they would all include common components and features, like engine and wheels.

It makes sense to **create a basic design and extend it to create their specialized versions,** rather than designing each car model separately, from scratch.

In a similar manner, with inheritance, we can create a class with basic features and behavior and create its specialized versions, by creating classes, that inherit this base class. In the same way, interfaces can extend existing interfaces.

We’ll notice the use of multiple terms to refer to a type which is inherited by another type, specifically:

  * **a base type is also called a super or a parent type**
  * **a derived type is referred to as an extended, sub or a child type**



## **3\. Class Inheritance**

### **3.1. Extending a Class**

A class can inherit another class and define additional members.

Let’s start by defining a base class _Car_ :
    
    
    public class Car {
        int wheels;
        String model;
        void start() {
            // Check essential parts
        }
    }

The class _ArmoredCar_ can inherit the members of _Car_ class by **using the keyword _extends_ in its declaration**:
    
    
    public class ArmoredCar extends Car {
        int bulletProofWindows;
        void remoteStartCar() {
    	// this vehicle can be started by using a remote control
        }
    }

We can now say that the _ArmoredCar_ class is a subclass of _Car,_ and the latter is a superclass of _ArmoredCar._

**Classes in Java support single inheritance** ; the _ArmoredCar_ class can’t extend multiple classes.

Also, note that in the absence of an _extends_ keyword, a class implicitly inherits class _java.lang.Object_.

**A subclass class inherits the non-static _protected_ and _public_ members from the superclass class.** In addition, the members with _default_ (_package-private)_ access are inherited if the two classes are in the same package.

On the other hand, the _private_ and  _static_ members of a class are not inherited.

### **3.2. Accessing Parent Members from a Child Class**

To access inherited properties or methods, we can simply use them directly:
    
    
    public class ArmoredCar extends Car {
        public String registerModel() {
            return model;
        }
    }

Note that we don’t need a reference to the superclass to access its members.

## **4\. Interface Inheritance**

### **4.1. Implementing Multiple Interfaces**

**Although classes can inherit only one class, they can implement multiple interfaces.**

Imagine the _ArmoredCar_ that we defined in the preceding section is required for a super spy. So the _Car_ manufacturing company thought of adding flying and floating functionality:
    
    
    public interface Floatable {
        void floatOnWater();
    }
    
    
    public interface Flyable {
        void fly();
    }
    
    
    public class ArmoredCar extends Car implements Floatable, Flyable{
        public void floatOnWater() {
            System.out.println("I can float!");
        }
     
        public void fly() {
            System.out.println("I can fly!");
        }
    }

In the example above, we notice the use of the keyword _implements_ to inherit from an interface.

### **4.2. Issues With Multiple Inheritance**

**Java allows multiple inheritance using interfaces.**

Until Java 7, this wasn’t an issue. Interfaces could only define _abstract_ methods, that is, methods without any implementation. So if a class implemented multiple interfaces with the same method signature, it was not a problem. The implementing class eventually had just one method to implement.

Let’s see how this simple equation changed with the introduction of _default_ methods in interfaces, with Java 8.

**Starting with Java 8, interfaces could choose to define default implementations for its methods** (an interface can still define _abstract_ methods). This means that if a class implements multiple interfaces, which define methods with the same signature, the child class would inherit separate implementations. This sounds complex and is not allowed.

**Java disallows inheritance of multiple implementations of the same methods, defined in separate interfaces.**

Here’s an example:
    
    
    public interface Floatable {
        default void repair() {
        	System.out.println("Repairing Floatable object");	
        }
    }
    
    
    public interface Flyable {
        default void repair() {
        	System.out.println("Repairing Flyable object");	
        }
    }
    
    
    public class ArmoredCar extends Car implements Floatable, Flyable {
        // this won't compile
    }

If we do want to implement both interfaces, we’ll have to override the _repair()_ method.

If the interfaces in the preceding examples define variables with the same name, say _duration_ , we can’t access them without preceding the variable name with the interface name:
    
    
    public interface Floatable {
        int duration = 10;
    }
    
    
    public interface Flyable {
        int duration = 20;
    }
    
    
    public class ArmoredCar extends Car implements Floatable, Flyable {
     
        public void aMethod() {
        	System.out.println(duration); // won't compile
        	System.out.println(Floatable.duration); // outputs 10
        	System.out.println(Flyable.duration); // outputs 20
        }
    }

### **4.3. Interfaces Extending Other Interfaces**

An interface can extend multiple interfaces. Here’s an example:
    
    
    public interface Floatable {
        void floatOnWater();
    }
    
    
    interface interface Flyable {
        void fly();
    }
    
    
    public interface SpaceTraveller extends Floatable, Flyable {
        void remoteControl();
    }

An interface inherits other interfaces by using the keyword _extends_. Classes use the keyword _implements_ to inherit an interface.

## **5\. Inheriting Type**

When a class inherits another class or interfaces, apart from inheriting their members, it also inherits their type. This also applies to an interface that inherits other interfaces.

This is a very powerful concept, which allows developers to **program to an interface (base class or interface)** , rather than programming to their implementations.

For example, imagine a condition, where an organization maintains a list of the cars owned by its employees. Of course, all employees might own different car models. So how can we refer to different car instances? Here’s the solution:
    
    
    public class Employee {
        private String name;
        private Car car;
        
        // standard constructor
    }

Because all derived classes of _Car_ inherit the type _Car_ , the derived class instances can be referred by using a variable of class _Car_ :
    
    
    Employee e1 = new Employee("Shreya", new ArmoredCar());
    Employee e2 = new Employee("Paul", new SpaceCar());
    Employee e3 = new Employee("Pavni", new BMW());

## 6\. Hidden Class Members

### **6.1. Hidden Instance Members**

What happens if **both the superclass and subclass define a variable or method with the same name**? Don’t worry; we can still access both of them. However, we must make our intent clear to Java, by prefixing the variable or method with the keywords _this_ or _super_.

The _this_ keyword refers to the instance in which it’s used. The _super_ keyword (as it seems obvious) refers to the parent class instance:
    
    
    public class ArmoredCar extends Car {
        private String model;
        public String getAValue() {
        	return super.model;   // returns value of model defined in base class Car
        	// return this.model;   // will return value of model defined in ArmoredCar
        	// return model;   // will return value of model defined in ArmoredCar
        }
    }

A lot of developers use _this_ and _super_ keywords to explicitly state which variable or method they’re referring to. However, using them with all members can make our code look cluttered.

### **6.2. Hidden Static Members**

What happens **when our base class and subclasses define static variables and methods with the same name**? Can we access a _static_ member from the base class, in the derived class, the way we do for the instance variables?

Let’s find out using an example:
    
    
    public class Car {
        public static String msg() {
            return "Car";
        }
    }
    
    
    public class ArmoredCar extends Car {
        public static String msg() {
            return super.msg(); // this won't compile.
        }
    }

No, we can’t. The static members belong to a class and not to instances. So we can’t use the non-static _super_ keyword in _msg()_.

Since static members belong to a class, we can modify the preceding call as follows:
    
    
    return Car.msg();

Consider the following example, in which both the base class and derived class define a static method _msg()_ with the same signature:
    
    
    public class Car {
        public static String msg() {
            return "Car";
        }
    }
    
    
    public class ArmoredCar extends Car {
        public static String msg() {
            return "ArmoredCar";
        }
    }

Here’s how we can call them:
    
    
    Car first = new ArmoredCar();
    ArmoredCar second = new ArmoredCar();

For the preceding code, _first.msg()_ will output “Car _“_ and _second.msg()_ will output “ArmoredCar”. The static message that is called depends on the type of the variable used to refer to _ArmoredCar_ instance.

## **7\. Conclusion**

In this article, we covered a core aspect of the Java language – inheritance.

We saw how Java supports single inheritance with classes and multiple inheritance with interfaces and discussed the intricacies of how the mechanism works in the language.
