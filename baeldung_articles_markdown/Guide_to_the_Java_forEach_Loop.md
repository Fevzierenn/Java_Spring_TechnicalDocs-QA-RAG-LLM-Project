# Guide to the Java forEach Loop

## **1\. Overview**

Introduced in Java 8, the _forEach()_ method provides programmers with **a concise way to iterate over a collection.**

In this tutorial, we’ll see how to use the _forEach()_ method with collections, what kind of argument it takes, and how this loop differs from the enhanced [_for-loop_](/java-for-each-loop).

If you need to brush up on some Java 8 concepts, check out our [collection of articles](/tag/jdk8-and-later).

## **2\. Basics of _forEach()_**

In Java, the  _Collection_ interface has  _Iterable_ as its super interface. This interface has a new API starting with Java 8:
    
    
    void forEach(Consumer<? super T> action)

Simply put, the [Javadoc](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/Iterable.html#forEach\(java.util.function.Consumer\)) of _forEach_ states that it “performs the given action for each element of the _Iterable_ until all elements have been processed or the action throws an exception.”

And so, with _forEach()_ , we can iterate over a collection and perform a given action on each element.

For instance, let’s consider an enhanced _for-loop_ version of iterating and printing a _Collection_ of _Strings_ :
    
    
    List names = List.of("Larry", "Steve", "James", "Conan", "Ellen");
    
    for (String name : names) {
        LOG.info(name);
    }

We can write this using _forEach()_ :
    
    
    names.forEach(name -> {
        LOG.info(name);
    });

Here, we invoke the _forEach()_ on the collection and log the names to the console.

## **3\. Using the _forEach()_ Method with Collections**

The _forEach()_ method aligns with the Java functional programming paradigm, making code more declarative.

### 3.1. Iterating Over a List

The _forEach()_ method can be used on lists:
    
    
    List names = List.of("Larry", "Steve", "James", "Conan", "Ellen");
    names.forEach(name -> logger.info(name));

The code above logs all elements of the collection to the console.

### 3.2. Iterating Over a _Map_ Using _forEach()_

Maps are not _Iterable_ , but they do **provide their own variant of _forEach()_ that accepts a **_**BiConsumer**_**.**

Java 8 introduces a _BiConsumer_ instead of _Consumer_ in _Map_ ‘s _forEach()_ so that an action can be performed on both the key and value of a _Map_ simultaneously.

Let’s create a _Map_ with these entries:
    
    
    Map<Integer, String> namesMap = new HashMap<>();
    namesMap.put(1, "Larry");
    namesMap.put(2, "Steve");
    namesMap.put(3, "James");

Next, let’s iterate over _namesMap_ using Map’s _forEach()_ :
    
    
    namesMap.forEach((key, value) -> LOG.info(key + " " + value));

As we can see here, we’ve used a _BiConsumer_ to iterate over the entries of the _Map._

### 3.3. Iterating Over a _Map_ by Iterating _entrySet()_

We can also iterate the _EntrySet_ of a _Map_ using Iterable’s _forEach()_.

Since **the entries of a _Map_ are stored in a _Set_ called  _EntrySet,_ we can iterate that using a _forEach()_** :
    
    
    namesMap.entrySet().forEach(entry -> LOG.info(entry.getKey() + " " + entry.getValue()));

### 3.4. Using _forEach()_ Method for Parallel Operation

For large collections, using _forEach()_ with a parallel stream can improve performance by utilizing multiple CPU cores:
    
    
    List names = List.of("Larry", "Steve", "James", "Conan", "Ellen");
    names.parallelStream().forEach(LOG::info);

The code above runs in parallel. However, parallel execution may increase resource consumption.

## 4\. How Not to Use _forEach()_

Although the _forEach()_ method is convenient, it has limitations.

### 4.1. Cannot Be Directly Invoked on Arrays

We can’t directly invoke the method on an array:
    
    
    String[] foodItems = {"rice", "beans", "egg"};
    foodItems.forEach(food -> logger.info(food));

The code above fails to compile because arrays don’t have the _forEach()_ method. However, we can make it compile by converting the array to a stream:
    
    
    Arrays.stream(foodItems).forEach(food -> logger.info(food));

Since stream has the _forEach()_ method, we can convert an array into a stream and iterate over its element.

### 4.2. Cannot Modify the Collection Itself

Moreover, we can’t modify the collection itself using the method:
    
    
    List<String> names = List.of("Larry", "Steve", "James", "Conan", "Ellen");
    names.forEach(name -> {
        if (name.equals("Larry")) {
            names.remove(name);
        }
    });

**The code above throws a _ConcurrentModificationException_ error because modifying collections while iterating over it with _forEach()_ is not allowed**. Unlike the traditional _for_ loop, which allows modification with careful indexing.

### 4.3. Cannot Break or Continue a Loop

Unlike traditional _for_ loop, _forEach()_ doesn’t support _break_ or _continue_ :
    
    
    List<String> names = List.of("Larry", "Steve", "James", "Conan", "Ellen");
    names.forEach(name -> {
        if (name.equals("Steve")) {
            break;
        }
        logger.info(name);
    });

The code above throws an exception.

### 4.4. Doesn’t Permit Counter

The _forEach()_ method doesn’t support modifying a counter variable during iteration:
    
    
    List<String> names = List.of("Larry", "Steve", "James", "Conan", "Ellen");
    int count = 0;
    names.forEach(name -> {
        count++;
    });

The code above results in a compilation error because lambda expression requires variables used inside them to be _final_ , meaning their value can’t be modified after initialization.

However, we can use an [atomic variable](/java-atomic-variables) instead, which allows modification inside a lambda expression.

### 4.5. Cannot Access Next or Previous Element

Furthermore, we can reference the previous or next element of a collection using the traditional _for_ loop:
    
    
    List<String> names = List.of("Larry", "Steve", "James", "Conan", "Ellen");
    for (int i = 0; i < names.size(); i++) {
        String current = names.get(i);
        String previous = (i > 0) ? names.get(i - 1) : "None";
        String next = (i < names.size() - 1) ? names.get(i + 1) : "None";
    
        LOG.info("Current: {}, Previous: {}, Next: {}", current, previous, next);
    }

In the code above, we use the index _i_ to determine the previous _(i – 1)_ and next _(i + 1)_ elements.

However, this isn’t possible with the _forEach()_ method because it processes elements individually without exposing their index.

## 5\. _forEach()_ vs. Traditional _for_ Loop

Both can iterate over collections and arrays. However, the _forEach()_ method isn’t as flexible as the traditional _for_ loop.

The _for_ loop allows us to explicitly define the loop control variables, conditions, and increments, while the _forEach()_ method abstracts these details:
    
    
    List names = List.of("Larry", "Steve", "James", "Conan", "Ellen");
    for (int i = 0; i < names.size(); i++) {
        LOG.info(names.get(i));
    }

Also, we can modify the loop conditions:
    
    
    for (int i = 0; i < names.size() - 1; i++) {
        LOG.info(names.get(i));
    }

In the code above, we skip the last element in the collection by modifying the loop condition – _names.size() – 1_. This level of flexibility isn’t possible with the _forEach()_ method.

The _forEach()_ method allows us to perform operations on the collection element and doesn’t permit modification to the collection itself.

The _for_ loop allows us to perform operations on individual elements of a collection and permits us to modify the collection itself.

## **6._forEach()_ vs. Enhanced _for_ Loop**

From a simple point of view, both loops provide the same functionality: loop through elements in a collection.

**The main difference between them is that they are different iterators. The enhanced _for-loop_ is an external iterator, whereas the new _forEach_ method is internal.**

### **6.1. Internal Iterator – _forEach()_**

This type of iterator manages the iteration in the background and leaves the programmer to just code what is meant to be done with the elements of the collection.

The iterator instead manages the iteration and makes sure to process the elements one by one.

Let’s see an example of an internal iterator:
    
    
    List<String> names = List.of("Larry", "Steve", "James", "Conan", "Ellen");
    names.forEach(name -> LOG.info(name));

In the _forEach_ method above, we can see that the argument provided is a lambda expression. This means that **the method only needs to know what is to be done** , and all the work of iterating will be taken care of internally.

### **6.2. External Iterator – _for-loop_**

**External iterators mix what and how the loop is to be done.**

_Enumerations_ , _Iterators,_ and enhanced _for-loop_ are all external iterators (remember the methods _iterator()_ , _next(),_ or _hasNext()_?). In all these iterators, it’s our job to specify how to perform iterations.

Consider this familiar loop:
    
    
    List<String> names = List.of("Larry", "Steve", "James", "Conan", "Ellen");
    for (String name : names) {
        LOG.info(name);
    }

Although we are not explicitly invoking _hasNext()_ or _next()_ methods while iterating over the list, the underlying code that makes this iteration work uses these methods. This implies that the complexity of these operations is hidden from the programmer, but it still exists.

Contrary to an internal iterator in which the collection does the iteration itself, here we require external code that takes every element out of the collection.

## **7.****Conclusion**

In this article, we showed that the _forEach_ loop is more convenient than the normal _for-loop_.

We also saw how the _forEach_ method works and what kind of implementation can be received as an argument to perform an action on each element in the collection.
