# Java Classes and Objects

## **1\. Overview**

In this quick tutorial, we’ll look at two basic building blocks of the Java programming language – classes and objects. They’re basic concepts of Object Oriented Programming (OOP), which we use to model real-life entities.

In OOP, **classes are blueprints or templates for objects. We use them to describe types of entities.**

On the other hand, **objects are living entities, created from classes. They contain certain states within their fields and present certain behaviors with their methods.**

## **2\. Classes**

Simply put, a class represent a definition or a type of object. In Java, classes can contain fields, constructors, and methods.

Let’s see an example using a simple Java class representing a _Car_ :
    
    
    class Car {
    
        // fields
        String type;
        String model;
        String color;
        int speed;
    
        // constructor
        Car(String type, String model, String color) {
            this.type = type;
            this.model = model;
            this.color = color;
        }
        
        // methods
        int increaseSpeed(int increment) {
            this.speed = this.speed + increment;
            return this.speed;
        }
        
        // ...
    }
    

This Java class represents a car in general. We can create any type of car from this class. We use fields to hold the state and a constructor to create objects from this class.

Every Java class has an empty constructor by default. We use it if we don’t provide a specific implementation as we did above. Here’s how the default constructor would look for our _Car_ class:
    
    
    Car(){}
    

**This constructor simply initializes all fields of the object with their default values. Strings are initialized to _null_ and integers to zero.**

Now, our class has a specific constructor because we want our objects to have their fields defined when we create them:
    
    
    Car(String type, String model) {
        // ...
    }
    

To sum up, we wrote a class that defines a car. Its properties are described by fields, which contain the state of objects of the class, and its behavior is described using methods.

## **3\. Objects**

While classes are translated during compile time, **objects are created from classes at runtime**.

Objects of a class are called instances, and we create and initialize them with constructors:
    
    
    Car focus = new Car("Ford", "Focus", "red");
    Car auris = new Car("Toyota", "Auris", "blue");
    Car golf = new Car("Volkswagen", "Golf", "green");
    

Now, we’ve created different _Car_ objects, all from a single class. **This is the point of it all, to define the blueprint in one place, and then, to reuse it many times in many places.**

So far, we have three _Car_ objects, and they’re all parked since their speed is zero. We can change this by invoking our _increaseSpeed_ method:
    
    
    focus.increaseSpeed(10);
    auris.increaseSpeed(20);
    golf.increaseSpeed(30);
    

Now, we’ve changed the state of our cars – they’re all moving at different speeds.

Furthermore, we can and should define access control to our class, its constructors, fields, and methods. We can do so by using access modifiers, as we’ll see in the next section.

## **4\. Access Modifiers**

In the previous examples, we omitted access modifiers to simplify the code. By doing so, we actually used a default package-private modifier. That modifier allows access to the class from any other class in the same package.

Usually, we’d use a _public_ modifier for constructors to allow access from all other objects:
    
    
    public Car(String type, String model, String color) {
        // ...
    }
    

Every field and method in our class should’ve also defined access control by a specific modifier. **Classes usually have _public_ modifiers, but we tend to keep our fields _private_.**

Fields hold the state of our object, therefore we want to control access to that state. We can keep some of them _private_ , and others _public_. We achieve this with specific methods called getters and setters.

Let’s have a look at our class with fully-specified access control:
    
    
    public class Car {
        private String type;
        // ...
    
        public Car(String type, String model, String color) {
           // ...
        }
    
        public String getColor() {
            return color;
        }
    
        public void setColor(String color) {
            this.color = color;
        }
    
        public int getSpeed() {
            return speed;
        }
    
        // ...
    }
    

**Our class is marked _public_ , which means we can use it in any package.** Also, the constructor is _public_ , which means we can create an object from this class inside any other object.

**Our fields are marked _private_ , which means they’re not accessible from our object directly**, but we provide access to them through getters and setters.

The  _type_ and _model_ fields do not have getters and setters, because they hold internal data of our objects. We can define them only through the constructor during initialization.

Furthermore, the _color_ can be accessed and changed, whereas  _speed_ can only be accessed, but not changed. We enforced speed adjustments through specialized _public_ methods _increaseSpeed()_ and _decreaseSpeed()_.

In other words, **we use access control to encapsulate the state of the object.**

## **5\. Conclusion**

In this article, we went through two basic elements of the Java language, classes, and objects, and showed how and why they are used. We also introduced the basics of access control and demonstrated its usage.

To learn other concepts of Java language, we suggest reading about [inheritance](/java-inheritance), [the super keyword](/java-super), and [abstract classes](/java-abstract-class) as a next step.
