# Sealed Classes and Interfaces in Java

## 1\. Overview

The release of Java SE 17 introduced sealed classes ([JEP 409](https://openjdk.org/jeps/409)). **This feature enables more fine-grained inheritance control in Java.**

**Sealing allows classes and interfaces to define their permitted subtypes.** In other words, a class or interface can define which classes can implement or extend it. It’s a useful feature for domain modeling, and increasing the security of libraries.

## 2\. Motivation

A class hierarchy enables us to reuse code via inheritance. However, the class hierarchy can also serve other purposes. Code reuse is great, but isn’t always our primary goal.

### 2.1. Modeling Possibilities

An alternate purpose of a class hierarchy can be to model various possibilities that exist in a domain.

As an example, imagine a business domain that only works with cars and trucks, not motorcycles. When creating the _Vehicle_ abstract class in Java, we should be able to allow only _Car_ and _Truck_ classes to extend it. As such, we want to ensure that there will be no misuse of the _Vehicle_ abstract class within our domain.

**In this example, we’re more interested in the clarity of code handling known subclasses, than defending against all unknown subclasses**.

Before version 15 (in which sealed classes were introduced as a preview), Java assumed that code reuse is always the goal. Every class was extendable by any number of subclasses.

### 2.2. The Package-Private Approach

In earlier versions, Java provided limited options in the area of inheritance control.

A [final class](/java-final) can have no subclasses. A [package-private class](/java-access-modifiers) can only have subclasses in the same package.

Using the package-private approach, users can’t access the abstract class without also allowing them to extend it:
    
    
    public class Vehicles {
    
        abstract static class Vehicle {
    
            private final String registrationNumber;
    
            public Vehicle(String registrationNumber) {
                this.registrationNumber = registrationNumber;
            }
    
            public String getRegistrationNumber() {
                return registrationNumber;
            }
    
        }
    
        public static final class Car extends Vehicle {
    
            private final int numberOfSeats;
    
            public Car(int numberOfSeats, String registrationNumber) {
                super(registrationNumber);
                this.numberOfSeats = numberOfSeats;
            }
    
            public int getNumberOfSeats() {
                return numberOfSeats;
            }
    
        }
    
        public static final class Truck extends Vehicle {
    
            private final int loadCapacity;
    
            public Truck(int loadCapacity, String registrationNumber) {
                super(registrationNumber);
                this.loadCapacity = loadCapacity;
            }
    
            public int getLoadCapacity() {
                return loadCapacity;
            }
    
        }
    
    }

### 2.3. Superclass Accessible, Not Extensible

A superclass that’s developed with a set of its subclasses should be able to document its intended usage, not constrain its subclasses. Also, having restricted subclasses shouldn’t limit the accessibility of its superclass.

**Thus, the main motivation behind sealed classes is to have the possibility for a superclass to be widely accessible, but not widely extensible.**

## 3\. Creation

The sealed feature introduces a couple of new modifiers and clauses in Java: _sealed, non-sealed,_ and _permits_.

### 3.1. Sealed Interfaces

To seal an interface, we can apply the _sealed_ modifier to its declaration. The _permits_ clause then specifies the classes that are permitted to implement the sealed interface:
    
    
    public sealed interface Service permits Car, Truck {
    
        int getMaxServiceIntervalInMonths();
    
        default int getMaxDistanceBetweenServicesInKilometers() {
            return 100000;
        }
    
    }

### 3.2. Sealed Classes

Similar to interfaces, we can seal classes by applying the same _sealed_ modifier. The _permits_ clause should be defined after any _extends_ or _implements_ clauses:
    
    
    public abstract sealed class Vehicle permits Car, Truck {
    
        protected final String registrationNumber;
    
        public Vehicle(String registrationNumber) {
            this.registrationNumber = registrationNumber;
        }
    
        public String getRegistrationNumber() {
            return registrationNumber;
        }
    
    }

A permitted subclass must define a modifier. It may be [declared _final_ ](/java-final)to prevent any further extensions:
    
    
    public final class Truck extends Vehicle implements Service {
    
        private final int loadCapacity;
    
        public Truck(int loadCapacity, String registrationNumber) {
            super(registrationNumber);
            this.loadCapacity = loadCapacity;
        }
    
        public int getLoadCapacity() {
            return loadCapacity;
        }
    
        @Override
        public int getMaxServiceIntervalInMonths() {
            return 18;
        }
    
    }

A permitted subclass may also be declared _sealed_. However, if we declare it _non-sealed,_ then it’s open for extension:
    
    
    public non-sealed class Car extends Vehicle implements Service {
    
        private final int numberOfSeats;
    
        public Car(int numberOfSeats, String registrationNumber) {
            super(registrationNumber);
            this.numberOfSeats = numberOfSeats;
        }
    
        public int getNumberOfSeats() {
            return numberOfSeats;
        }
    
        @Override
        public int getMaxServiceIntervalInMonths() {
            return 12;
        }
    
    }

### 3.4. Constraints

A sealed class imposes three important constraints on its permitted subclasses:

  1. All permitted subclasses must belong to the same module as the sealed class.
  2. Every permitted subclass must explicitly extend the sealed class.
  3. Every permitted subclass must define a modifier: _final_ , _sealed_ , or _non-sealed._



## 4\. Usage

### 4.1. The Traditional Way

**When sealing a class, we enable the client code to reason clearly about all permitted subclasses.**

The traditional way to reason about a subclass is using a set of _if-else_ statements and _instanceof_ checks:
    
    
    if (vehicle instanceof Car) {
        return ((Car) vehicle).getNumberOfSeats();
    } else if (vehicle instanceof Truck) {
        return ((Truck) vehicle).getLoadCapacity();
    } else {
        throw new RuntimeException("Unknown instance of Vehicle");
    }

### 4.2. Pattern Matching

By applying [pattern matching](/java-pattern-matching-instanceof), we can avoid the additional class cast, but we still need a set of i _f-else_ statements:
    
    
    if (vehicle instanceof Car car) {
        return car.getNumberOfSeats();
    } else if (vehicle instanceof Truck truck) {
        return truck.getLoadCapacity();
    } else {
        throw new RuntimeException("Unknown instance of Vehicle");
    }

Using i _f-else_ makes it difficult for the compiler to determine if we’ve covered all permitted subclasses. For this reason, we’re throwing a _RuntimeException_.

In future versions of Java, the client code will be able to use a _switch_ statement instead of i _f-else_ ([JEP 375](https://openjdk.java.net/jeps/375)).

By using [type test patterns](https://openjdk.java.net/jeps/8213076), the compiler will be able to check that every permitted subclass is covered. Thus, there will be no more need for a _default_ clause/case.

## 4\. Compatibility

Now let’s take a look at the compatibility of sealed classes with other Java language features, like records and the reflection API.

### 4.1. Records

Sealed classes work very well with [records](/java-record-keyword). Since records are implicitly final, the sealed hierarchy is even more concise. Let’s try to rewrite our class example using records:
    
    
    public sealed interface Vehicle permits Car, Truck {
    
        String getRegistrationNumber();
    
    }
    
    public record Car(int numberOfSeats, String registrationNumber) implements Vehicle {
    
        @Override
        public String getRegistrationNumber() {
            return registrationNumber;
        }
    
        public int getNumberOfSeats() {
            return numberOfSeats;
        }
    
    }
    
    public record Truck(int loadCapacity, String registrationNumber) implements Vehicle {
    
        @Override
        public String getRegistrationNumber() {
            return registrationNumber;
        }
    
        public int getLoadCapacity() {
            return loadCapacity;
        }
    
    }

### 4.2. Reflection

Sealed classes are also supported by the [reflection API](/java-reflection), where two public methods have been added to the _java.lang.Class:_

  * The _isSealed_ method returns _true_ if the given class or interface is sealed.
  * Method _getPermittedSubclasses_ returns an array of objects representing all the permitted subclasses.



We can make use of these methods to create assertions that are based on our example:
    
    
    Assertions.assertThat(truck.getClass().isSealed()).isEqualTo(false);
    Assertions.assertThat(truck.getClass().getSuperclass().isSealed()).isEqualTo(true);
    Assertions.assertThat(truck.getClass().getSuperclass().getPermittedSubclasses())
      .contains(Class.forName(truck.getClass().getCanonicalName()));

## 5\. Conclusion

**In this article, we explored sealed classes and interfaces, a new feature in Java SE 17. We covered the creation and usage of sealed classes and interfaces, as well as their constraints and compatibility with other language features.**

In the examples, we covered the creation of a sealed interface and a sealed class, the usage of the sealed class (with and without pattern matching), and the compatibility of sealed classes with records and the reflection API.
