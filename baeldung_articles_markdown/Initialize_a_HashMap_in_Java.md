# Initialize a HashMap in Java

## 1\. Overview

In this tutorial, we’ll learn about various ways of initializing a  _HashMap_ in Java.

We’ll use Java 8 as well as Java 9.

## 2\. The Static Initializer for a Static _HashMap_

We can initialize a  _HashMap_ using a _static_ block of code:
    
    
    public static Map<String, String> articleMapOne;
    static {
        articleMapOne = new HashMap<>();
        articleMapOne.put("ar01", "Intro to Map");
        articleMapOne.put("ar02", "Some article");
    }

**The advantage of this kind of initialization is that the map is mutable, but it will only work for static. Consequently, entries can be added and removed as and when required.**

Let’s go ahead and test it:
    
    
    @Test
    public void givenStaticMap_whenUpdated_thenCorrect() {
        
        MapInitializer.articleMapOne.put(
          "NewArticle1", "Convert array to List");
        
        assertEquals(
          MapInitializer.articleMapOne.get("NewArticle1"), 
          "Convert array to List");  
    }

We can also initialize the map using the double-brace syntax:
    
    
    Map<String, String> doubleBraceMap  = new HashMap<String, String>() {{
        put("key1", "value1");
        put("key2", "value2");
    }};

Note that **we must try to avoid this initialization technique because it creates an anonymous extra class at every usage, holds hidden references to the enclosing object,** and might cause memory leak issues.

## 3\. Using Java Collections

If we need to create a singleton immutable map with a single entry, _Collections.singletonMap()_ becomes very useful:
    
    
    public static Map<String, String> createSingletonMap() {
        return Collections.singletonMap("username1", "password1");
    }

Note that the map here is immutable, and if we try to add more entries, it’ll throw _java.lang.UnsupportedOperationException._

We can also create an immutable empty map by using  _Collections.emptyMap():_
    
    
    Map<String, String> emptyMap = Collections.emptyMap();

## 4\. The Java 8 Way

In this section, let’s look into the ways to initialize a map using Java 8 _Stream API._

### **4.1. Using _Collectors.toMap()_**

Let’s use a _Stream_ of a two-dimensional _String_ array and collect them into a map:
    
    
    Map<String, String> map = Stream.of(new String[][] {
      { "Hello", "World" }, 
      { "John", "Doe" }, 
    }).collect(Collectors.toMap(data -> data[0], data -> data[1]));

Notice here the data type of key and value of the _Map_ is the same.

In order to make it more generic, let’s take the array of _Objects_ and perform the same operation:
    
    
     Map<String, Integer> map = Stream.of(new Object[][] { 
         { "data1", 1 }, 
         { "data2", 2 }, 
     }).collect(Collectors.toMap(data -> (String) data[0], data -> (Integer) data[1]));

As a result, we create a map of the key as a _String_ and value as an _Integer_.

### 4.2. Using a Stream of  _Map.Entry_

Here we’ll use the instances of  _Map.Entry._ This is another approach where we have different key and value types.

First, let’s use  _SimpleEntry_ implementation of the  _Entry_ interface:
    
    
    Map<String, Integer> map = Stream.of(
      new AbstractMap.SimpleEntry<>("idea", 1), 
      new AbstractMap.SimpleEntry<>("mobile", 2))
      .collect(Collectors.toMap(Map.Entry::getKey, Map.Entry::getValue));

Now let’s create the map using _SimpleImmutableEntry_ implementation:
    
    
    Map<String, Integer> map = Stream.of(
      new AbstractMap.SimpleImmutableEntry<>("idea", 1),    
      new AbstractMap.SimpleImmutableEntry<>("mobile", 2))
      .collect(Collectors.toMap(Map.Entry::getKey, Map.Entry::getValue));

### 4.3. Initializing an Immutable Map

In certain use cases, we need to initialize an immutable map. This could be done by wrapping the _Collectors.toMap()_ inside _Collectors.collectingAndThen()_ :
    
    
    Map<String, String> map = Stream.of(new String[][] { 
        { "Hello", "World" }, 
        { "John", "Doe" },
    }).collect(Collectors.collectingAndThen(
        Collectors.toMap(data -> data[0], data -> data[1]), 
        Collections::<String, String> unmodifiableMap));

**Note that we should avoid using such initialization using _Streams,_ as it could cause a huge performance overhead and lots of garbage objects are created just to initialize the map.**

## 5\. The Java 9 Way

Java 9 comes with various factory methods in the  _Map_ interface that simplify the creation and initialization of immutable maps.

Let’s go ahead and look into these factory methods.

### **5.1._Map.of()_**

This factory method takes no argument, a single argument, and variable arguments:
    
    
    Map<String, String> emptyMap = Map.of();
    Map<String, String> singletonMap = Map.of("key1", "value");
    Map<String, String> map = Map.of("key1","value1", "key2", "value2");

Note that this method supports only a maximum of 10 key-value pairs.

### _**5.2. Map.ofEntries()**_

It’s similar to the  _Map.of()_ but has no limitations on the number of key-value pairs:
    
    
    Map<String, String> map = Map.ofEntries(
      new AbstractMap.SimpleEntry<String, String>("name", "John"),
      new AbstractMap.SimpleEntry<String, String>("city", "budapest"),
      new AbstractMap.SimpleEntry<String, String>("zip", "000000"),
      new AbstractMap.SimpleEntry<String, String>("home", "1231231231")
    );

Note that the factory methods produce immutable maps, hence any mutation will result in a  _UnsupportedOperationException._

Also, they do not allow null keys or duplicate keys.

Now if we need a mutable or growing map after initialization, we can create any of the implementations of the  _Map_ interface and pass these immutable maps in the constructor:
    
    
    Map<String, String> map = new HashMap<String, String> (
      Map.of("key1","value1", "key2", "value2"));
    Map<String, String> map2 = new HashMap<String, String> (
      Map.ofEntries(
        new AbstractMap.SimpleEntry<String, String>("name", "John"),    
        new AbstractMap.SimpleEntry<String, String>("city", "budapest")));

## 6\. Using Guava

As we’ve looked into the ways of using core Java, let’s move ahead and initialize a map using the Guava library:
    
    
    Map<String, String> articles 
      = ImmutableMap.of("Title", "My New Article", "Title2", "Second Article");

This would create an immutable map, and to create a mutable one:
    
    
    Map<String, String> articles 
      = Maps.newHashMap(ImmutableMap.of("Title", "My New Article", "Title2", "Second Article"));

The method  _[ImmutableMap.of()](https://guava.dev/releases/23.0/api/docs/com/google/common/collect/ImmutableMap.html#of--) _also has overloaded versions that can take up to 5 pairs of key-value parameters. Here’s what an example with 2 pairs of parameters would look like:
    
    
    ImmutableMap.of("key1", "value1", "key2", "value2");

## 7\. Conclusion

In this article we explored the various ways of initializing a _Map_ , particularly to create empty, singleton, immutable and mutable maps. **As we can see, there’s a huge improvement in this field since Java 9.**
