# Inheritance and Composition (Is-a vs Has-a relationship) in Java

## **1\. Overview**

[Inheritance](/java-inheritance) and composition — along with abstraction, encapsulation, and polymorphism — are cornerstones of [object-oriented programming](https://en.wikipedia.org/wiki/Object-oriented_programming) (OOP).

In this tutorial, we’ll cover the basics of inheritance and composition, and we’ll focus strongly on spotting the differences between the two types of relationships.

## **2\. Inheritance’s Basics**

**Inheritance is a powerful yet overused and misused mechanism.**

Simply put, with inheritance, a base class (a.k.a. base type) defines the state and behavior common for a given type and lets the subclasses (a.k.a. subtypes) provide specialized versions of that state and behavior.

To have a clear idea on how to work with inheritance, let’s create a naive example: a base class _Person_ that defines the common fields and methods for a person, while the subclasses _Waitress_ and _Actress_ provide additional, fine-grained method implementations.

Here’s the _Person_ class:
    
    
    public class Person {
        private final String name;
    
        // other fields, standard constructors, getters
    }

And these are the subclasses:
    
    
    public class Waitress extends Person {
    
        public String serveStarter(String starter) {
            return "Serving a " + starter;
        }
        
        // additional methods/constructors
    }
    
    
    
    public class Actress extends Person {
        
        public String readScript(String movie) {
            return "Reading the script of " + movie;
        } 
        
        // additional methods/constructors
    }

In addition, let’s create a unit test to verify that instances of the _Waitress_ and _Actress_ classes are also instances of _Person_ , thus showing that the “is-a” condition is met at the type level:
    
    
    @Test
    public void givenWaitressInstance_whenCheckedType_thenIsInstanceOfPerson() {
        assertThat(new Waitress("Mary", "mary@domain.com", 22))
          .isInstanceOf(Person.class);
    }
        
    @Test
    public void givenActressInstance_whenCheckedType_thenIsInstanceOfPerson() {
        assertThat(new Actress("Susan", "susan@domain.com", 30))
          .isInstanceOf(Person.class);
    }

**It’s important to stress here the semantic facet of inheritance**. Aside from reusing the implementation of the _Person class_ , **we’ve created a well-defined “is-a” relationship** between the base type _Person_ and the subtypes _Waitress_ and _Actress_. Waitresses and actresses are, effectively, persons.

This may cause us to ask: **in which use cases is inheritance the right approach to take?**

**If subtypes fulfill the “is-a” condition and mainly provide additive functionality further down the classes hierarchy,** **then inheritance is the way to go.**

Of course, method overriding is allowed as long as the overridden methods preserve the base type/subtype substitutability promoted by the [Liskov Substitution Principle](https://en.wikipedia.org/wiki/Liskov_substitution_principle).

Additionally, we should keep in mind that**the subtypes inherit the base type’s API** , which is some cases may be overkill or merely undesirable.

Otherwise, we should use composition instead.

## **3\. Inheritance in Design Patterns**

While the consensus is that we should favor composition over inheritance whenever possible, there are a few typical use cases where inheritance has its place.

### **3.1. The Layer Supertype Pattern**

In this case, we **use inheritance to move common code to a base class (the supertype), on a per-layer basis**.

Here’s a basic implementation of this pattern in the domain layer:
    
    
    public class Entity {
        
        protected long id;
        
        // setters
    }
    
    
    
    public class User extends Entity {
        
        // additional fields and methods   
    }
    

We can apply the same approach to the other layers in the system, such as the service and persistence layers.

### **3.2. The Template Method Pattern**

In the template method pattern, we can **use a base class to define the invariant parts of an algorithm, and then implement the variant parts in the subclasses** :
    
    
    public abstract class ComputerBuilder {
        
        public final Computer buildComputer() {
            addProcessor();
            addMemory();
        }
        
        public abstract void addProcessor();
        
        public abstract void addMemory();
    }
    
    
    
    public class StandardComputerBuilder extends ComputerBuilder {
    
        @Override
        public void addProcessor() {
            // method implementation
        }
        
        @Override
        public void addMemory() {
            // method implementation
        }
    }

## **4\. Composition’s Basics**

The composition is another mechanism provided by OOP for reusing implementation.

In a nutshell, **composition allows us to model objects that are made up of other objects** , thus defining a “has-a” relationship between them.

Furthermore, **the composition is the strongest form of[association](https://en.wikipedia.org/wiki/Association_\(object-oriented_programming\))**, which means that **the object(s) that compose or are contained by one object are destroyed too when that object is destroyed**.

To better understand how composition works, let’s suppose that we need to work with objects that represent computers _._

A computer is composed of different parts, including the microprocessor, the memory, a sound card and so forth, so we can model both the computer and each of its parts as individual classes.

Here’s how a simple implementation of the _Computer_ class might look:
    
    
    public class Computer {
    
        private Processor processor;
        private Memory memory;
        private SoundCard soundCard;
    
        // standard getters/setters/constructors
        
        public Optional<SoundCard> getSoundCard() {
            return Optional.ofNullable(soundCard);
        }
    }

The following classes model a microprocessor, the memory, and a sound card (interfaces are omitted for brevity’s sake):
    
    
    public class StandardProcessor implements Processor {
    
        private String model;
        
        // standard getters/setters
    }
    
    
    public class StandardMemory implements Memory {
        
        private String brand;
        private String size;
        
        // standard constructors, getters, toString
    }
    
    
    
    public class StandardSoundCard implements SoundCard {
        
        private String brand;
    
        // standard constructors, getters, toString
    }
    

It’s easy to understand the motivations behind pushing composition over inheritance. **In every scenario where it’s possible to establish a semantically correct “has-a” relationship between a given class and others, the composition is the right choice to make.**

In the above example, _Computer_ meets the “has-a” condition with the classes that model its parts.

It’s also worth noting that in this case, **the containing _Computer_ object has ownership of the contained objects _if and only if_ the objects can’t be reused within another _Computer_ object.** If they can, we’d be using aggregation, rather than composition, where ownership isn’t implied.

## **5\. Composition Without Abstraction**

Alternatively, we could’ve defined the composition relationship by hard-coding the dependencies of the _Computer_ class, instead of declaring them in the constructor:
    
    
    public class Computer {
    
        private StandardProcessor processor
          = new StandardProcessor("Intel I3");
        private StandardMemory memory
          = new StandardMemory("Kingston", "1TB");
        
        // additional fields / methods
    }

**Of course, this would be a rigid, tightly-coupled design, as we’d be making _Computer_ strongly dependent on specific implementations of _Processor_ and _Memory_.**

We wouldn’t be taking advantage of the level of abstraction provided by interfaces and [dependency injection](https://en.wikipedia.org/wiki/Dependency_injection).

With the initial design based on interfaces, we get a loosely-coupled design, which is also easier to test.

## **6\. Conclusion**

In this article, we learned the fundamentals of inheritance and composition in Java, and we explored in depth the differences between the two types of relationships (“is-a” vs. “has-a”).
