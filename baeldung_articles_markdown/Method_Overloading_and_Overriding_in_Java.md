# Method Overloading and Overriding in Java

## **1\. Overview**

Method overloading and overriding are key concepts of the Java programming language, and as such, they deserve an in-depth look.

In this article, we’ll learn the basics of these concepts and see in what situations they can be useful.

## **2\. Method Overloading**

**Method overloading is a powerful mechanism that allows us to define cohesive class APIs.** To better understand why method overloading is such a valuable feature, let’s see a simple example.

Suppose that we’ve written a naive utility class that implements different methods for multiplying two numbers, three numbers, and so on.

If we’ve given the methods misleading or ambiguous names, such as _multiply2()_ , _multiply3()_ , _multiply4(),_ then that would be a badly designed class API. Here’s where method overloading comes into play.

**Simply put, we can implement method overloading in two different ways:**

  * implementing two or more **methods that have the same name but take different numbers of arguments**
  * implementing two or more **methods that have the same name but take arguments of different types**



### **2.1. Different Numbers of Arguments**

The _Multiplier_ class shows, in a nutshell, how to overload the _multiply()_ method by simply defining two implementations that take different numbers of arguments:
    
    
    public class Multiplier {
        
        public int multiply(int a, int b) {
            return a * b;
        }
        
        public int multiply(int a, int b, int c) {
            return a * b * c;
        }
    }

### **2.2. Arguments of Different Types**

Similarly, we can overload the _multiply()_ method by making it accept arguments of different types:
    
    
    public class Multiplier {
        
        public int multiply(int a, int b) {
            return a * b;
        }
        
        public double multiply(double a, double b) {
            return a * b;
        }
    }
    

Furthermore, it’s legitimate to define the _Multiplier_ class with both types of method overloading:
    
    
    public class Multiplier {
        
        public int multiply(int a, int b) {
            return a * b;
        }
        
        public int multiply(int a, int b, int c) {
            return a * b * c;
        }
        
        public double multiply(double a, double b) {
            return a * b;
        }
    }
    

It’s worth noting, however, that **it’s not possible to have two method implementations that differ only in their return types**.

To understand why – let’s consider the following example:
    
    
    public int multiply(int a, int b) { 
        return a * b; 
    }
     
    public double multiply(int a, int b) { 
        return a * b; 
    }

In this case, **the code simply wouldn’t compile because of the method call ambiguity** – the compiler wouldn’t know which implementation of _multiply()_ to call.

### **2.3. Type Promotion**

One neat feature provided by method overloading is the so-called _type promotion, a.k.a. widening primitive conversion_.

In simple terms, one given type is implicitly promoted to another one when there’s no matching between the types of the arguments passed to the overloaded method and a specific method implementation.

To understand more clearly how type promotion works, consider the following implementations of the _multiply()_ method:
    
    
    public double multiply(int a, long b) {
        return a * b;
    }
    
    public int multiply(int a, int b, int c) {
        return a * b * c;
    }
    

Now, calling the method with two _int_ arguments will result in the second argument being promoted to _long_ , as in this case there’s not a matching implementation of the method with two _int_ arguments.

Let’s see a quick unit test to demonstrate type promotion:
    
    
    @Test
    public void whenCalledMultiplyAndNoMatching_thenTypePromotion() {
        assertThat(multiplier.multiply(10, 10)).isEqualTo(100.0);
    }

Conversely, if we call the method with a matching implementation, type promotion just doesn’t take place:
    
    
    @Test
    public void whenCalledMultiplyAndMatching_thenNoTypePromotion() {
        assertThat(multiplier.multiply(10, 10, 10)).isEqualTo(1000);
    }

Here’s a summary of the type promotion rules that apply for method overloading:

  * _byte_ can be promoted to _short, int, long, float,_ or _double_
  * _short_ can be promoted to _int, long, float,_ or _double_
  * _char_ can be promoted to _int, long, float,_ or _double_
  * _int_ can be promoted to _long, float,_ or _double_
  * _long_ can be promoted to _float_ or _double_
  * _float_ can be promoted to _double_



### **2.4. Static Binding**

The ability to associate a specific method call to the method’s body is known as binding.

In the case of method overloading, the binding is performed statically at compile time, hence it’s called static binding.

The compiler can effectively set the binding at compile time by simply checking the methods’ signatures.

## **3\. Method Overriding**

**Method overriding allows us to provide fine-grained implementations in subclasses for methods defined in a base class.**

While method overriding is a powerful feature – considering that is a logical consequence of using [inheritance](https://en.wikipedia.org/wiki/Inheritance_\(object-oriented_programming\)), one of the biggest pillars of [OOP](https://en.wikipedia.org/wiki/Object-oriented_programming) – **when and where to utilize it should be analyzed carefully, on a per-use-case basis**.

Let’s see now how to use method overriding by creating a simple, inheritance-based (“is-a”) relationship.

Here’s the base class:
    
    
    public class Vehicle {
        
        public String accelerate(long mph) {
            return "The vehicle accelerates at : " + mph + " MPH.";
        }
        
        public String stop() {
            return "The vehicle has stopped.";
        }
        
        public String run() {
            return "The vehicle is running.";
        }
    }

And here’s a contrived subclass:
    
    
    public class Car extends Vehicle {
    
        @Override
        public String accelerate(long mph) {
            return "The car accelerates at : " + mph + " MPH.";
        }
    }

In the hierarchy above, we’ve simply overridden the _accelerate()_ method in order to provide a more refined implementation for the subtype _Car._

Here, it’s clear to see that **if an application uses instances of the _Vehicle_ class, then it can work with instances of _Car_ as well**, as both implementations of the _accelerate()_ method have the same signature and the same return type.

Let’s write a few unit tests to check the _Vehicle_ and _Car_ classes:
    
    
    @Test
    public void whenCalledAccelerate_thenOneAssertion() {
        assertThat(vehicle.accelerate(100))
          .isEqualTo("The vehicle accelerates at : 100 MPH.");
    }
        
    @Test
    public void whenCalledRun_thenOneAssertion() {
        assertThat(vehicle.run())
          .isEqualTo("The vehicle is running.");
    }
        
    @Test
    public void whenCalledStop_thenOneAssertion() {
        assertThat(vehicle.stop())
          .isEqualTo("The vehicle has stopped.");
    }
    
    @Test
    public void whenCalledAccelerate_thenOneAssertion() {
        assertThat(car.accelerate(80))
          .isEqualTo("The car accelerates at : 80 MPH.");
    }
        
    @Test
    public void whenCalledRun_thenOneAssertion() {
        assertThat(car.run())
          .isEqualTo("The vehicle is running.");
    }
        
    @Test
    public void whenCalledStop_thenOneAssertion() {
        assertThat(car.stop())
          .isEqualTo("The vehicle has stopped.");
    }
    

Now, let’s see some unit tests that show how the _run()_ and _stop()_ methods, which aren’t overridden, return equal values for both _Car_ and _Vehicle_ :
    
    
    @Test
    public void givenVehicleCarInstances_whenCalledRun_thenEqual() {
        assertThat(vehicle.run()).isEqualTo(car.run());
    }
     
    @Test
    public void givenVehicleCarInstances_whenCalledStop_thenEqual() {
       assertThat(vehicle.stop()).isEqualTo(car.stop());
    }

In our case, we have access to the source code for both classes, so we can clearly see that calling the _accelerate()_ method on a base _Vehicle_ instance and calling _accelerate()_ on a _Car_ instance will return different values for the same argument.

Therefore, the following test demonstrates that the overridden method is invoked for an instance of _Car_ :
    
    
    @Test
    public void whenCalledAccelerateWithSameArgument_thenNotEqual() {
        assertThat(vehicle.accelerate(100))
          .isNotEqualTo(car.accelerate(100));
    }

### **3.1. Type Substitutability**

A core principle in OOP is that of type substitutability, which is closely associated with the [Liskov Substitution Principle (LSP)](https://en.wikipedia.org/wiki/Liskov_substitution_principle).

Simply put, the LSP states that **if an application works with a given base type, then it should also work with any of its subtypes**. That way, type substitutability is properly preserved.

**The biggest problem with method overriding is that some specific method implementations in the derived classes might not fully adhere to the LSP and therefore fail to preserve type substitutability.**

Of course, it’s valid to make an overridden method to return a different type as well, but with full adherence to these rules:

  * If a method in the base class returns _void_ , the overridden method should return _void_
  * If a method in the base class returns a primitive, the overridden method should return the same primitive
  * If a method in the base class returns a certain type, the overridden method should return the same type or a subtype (a.k.a. _covariant_ return type)
  * If a method in the base class throws an exception, the overridden method must throw the same exception or a subtype of the base class exception



### **3.2. Dynamic Binding**

Considering that method overriding can be only implemented with inheritance, where there is a hierarchy of a base type and subtype(s), the compiler can’t determine at compile time what method to call, as both the base class and the subclasses define the same methods.

As a consequence, the compiler needs to check the type of object to know what method should be invoked.

As this checking happens at runtime, method overriding is a typical example of dynamic binding.

## **4\. Conclusion**

In this tutorial, we learned how to implement method overloading and method overriding, and we explored some typical situations where they’re useful.
