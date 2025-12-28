# Immutable Objects in Java

## **1\. Overview**

In this tutorial, we’ll learn what makes an object immutable, how to achieve immutability in Java, and what advantages come with doing so.

## **2\. What’s an Immutable Object?**

An immutable object is an **object whose internal state remains constant after it has been entirely created**.

This means that the public API of an immutable object guarantees us that it will behave in the same way during its whole lifetime.

If we take a look at the class  _String_ , we can see that even when its API seems to provide us a mutable behavior with its  _replace_ method, the original  _String_ doesn’t change:
    
    
    String name = "baeldung";
    String newName = name.replace("dung", "----");
    
    assertEquals("baeldung", name);
    assertEquals("bael----", newName);

The API gives us read-only methods, it should never include methods that change the internal state of the object.

## **3\. The _final_ Keyword in Java**

Before trying to achieve immutability in Java, we should talk about the  _final_ keyword.

In Java, **variables are mutable by default, meaning we can change the value they hold**.

By using the _final_ keyword when declaring a variable, the Java compiler won’t let us change the value of that variable. Instead, it will report a compile-time error:
    
    
    final String name = "baeldung";
    name = "bael...";

Note that  _final_ only forbids us from changing the reference the variable holds, it doesn’t protect us from changing the internal state of the object it refers to by using its public API:
    
    
    final List<String> strings = new ArrayList<>();
    assertEquals(0, strings.size());
    strings.add("baeldung");
    assertEquals(0, strings.size());

The second  _assertEquals_ will fail because adding an element to the list changes its size, therefore, it isn’t an immutable object.

## **4\. Immutability in Java**

Now that we know how to avoid changes to the content of a variable, we can use it to build the API of immutable objects.

Building the API of an immutable object requires us to guarantee that its internal state won’t change no matter how we use its API.

A step forward in the right direction is to use  _final_ when declaring its attributes:
    
    
    class Money {
        private final double amount;
        private final Currency currency;
    
        // ...
    }

Note that Java guarantees us that the value of  _amount_ won’t change, that’s the case with all primitive type variables.

However, in our example we are only guaranteed that the  _currency_ won’t change, so **we must rely on the _Currency_****API to protect itself from changes**.

Most of the time, we need the attributes of an object to hold custom values, and the place to initialize the internal state of an immutable object is its constructor:
    
    
    class Money {
        // ...
        public Money(double amount, Currency currency) {
            this.amount = amount;
            this.currency = currency;
        }
    
        public Currency getCurrency() {
            return currency;
        }
    
        public double getAmount() {
            return amount;
        }
    }

As we’ve said before, to meet the requirements of an immutable API, our  _Money_ class only has read-only methods.

Using the reflection API, we can break immutability and [change immutable objects](https://stackoverflow.com/questions/20945049/is-a-java-string-really-immutable). However, reflection violates immutable object’s public API, and usually, we should avoid doing this.

## **5\. Benefits**

Since the internal state of an immutable object remains constant in time, **we can share it safely among multiple threads**.

We can also use it freely, and none of the objects referencing it will notice any difference, we can say that **immutable objects are side-effects free**.

## **6\. Conclusion**

Immutable objects don’t change their internal state in time, they are thread-safe and side-effects free. Because of those properties, immutable objects are also especially useful when dealing with multi-thread environments.
