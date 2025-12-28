# Introduction to Java Streams

## **1\. Overview**

In this article, we’ll have a quick look at one of the major pieces of new functionality that Java 8 had added – Streams.

We’ll explain what streams are about and showcase the creation and basic stream operations with simple examples.

## **2\. Stream API**

One of the major new features in Java 8 is the introduction of the stream functionality – [_java.util.stream_](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/stream/package-summary.html) – which contains classes for processing sequences of elements.

The central API class is the _[Stream<T>](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/stream/Stream.html). _The following section will demonstrate how streams can be created using the existing data-provider sources.

### **2.1. Stream Creation**

Streams can be created from different element sources e.g. collections or arrays with the help of _stream()_ and _of()_ methods:
    
    
    String[] arr = new String[]{"a", "b", "c"};
    Stream<String> stream = Arrays.stream(arr);
    stream = Stream.of("a", "b", "c");

A _stream()_ default method is added to the _Collection_ interface and allows creating a _Stream <T> _using any collection as an element source _:_
    
    
    Stream<String> stream = list.stream();
    

### **2.2. Multi-threading With Streams**

Stream API also simplifies multithreading by providing the _parallelStream()_ method that runs operations over the stream’s elements in parallel mode.

The code below allows us to run method _doWork()_ in parallel for every element of the stream:
    
    
    list.parallelStream().forEach(element -> doWork(element));

In the following section, we will introduce some of the basic Stream API operations.

## **3\. Stream Operations**

There are many useful operations that can be performed on a stream.

They are divided into**intermediate operations** (return _Stream <T>_) and **terminal operations** (return a result of definite type). Intermediate operations allow chaining.

It’s also worth noting that operations on streams don’t change the source.

Here’s a quick example:
    
    
    long count = list.stream().distinct().count();

So, the _distinct()_ method represents an intermediate operation, which creates a new stream of unique elements of the previous stream. And the _count()_ method is a terminal operation _,_ which returns stream’s size.

### **3.1. Iterating**

Stream API helps to substitute _for_ , _for-each_ , and _while_ loops. It allows concentrating on operation’s logic, but not on the iteration over the sequence of elements. For example:
    
    
    for (String string : list) {
        if (string.contains("a")) {
            return true;
        }
    }

This code can be changed just with one line of Java 8 code:
    
    
    boolean isExist = list.stream().anyMatch(element -> element.contains("a"));

### **3.2. Filtering**

The _filter()_ method allows us to pick a stream of elements that satisfy a predicate.

For example, consider the following list:
    
    
    ArrayList<String> list = new ArrayList<>();
    list.add("One");
    list.add("OneAndOnly");
    list.add("Derek");
    list.add("Change");
    list.add("factory");
    list.add("justBefore");
    list.add("Italy");
    list.add("Italy");
    list.add("Thursday");
    list.add("");
    list.add("");

The following code creates a _Stream <String>_ of the _List <String>_, finds all elements of this stream which contain _char “d”_ , and creates a new stream containing only the filtered elements:
    
    
    Stream<String> stream = list.stream().filter(element -> element.contains("d"));

### **3.3. Mapping**

To convert elements of a _Stream_ by applying a special function to them and to collect these new elements into a _Stream_ , we can use the _map()_ method:
    
    
    List<String> uris = new ArrayList<>();
    uris.add("C:\\My.txt");
    Stream<Path> stream = uris.stream().map(uri -> Paths.get(uri));

So, the code above converts _Stream <String>_ to the _Stream <Path>_ by applying a specific lambda expression to every element of the initial _Stream_.

If you have a stream where every element contains its own sequence of elements and you want to create a stream of these inner elements, you should use the _flatMap()_ method:
    
    
    List<Detail> details = new ArrayList<>();
    details.add(new Detail());
    Stream<String> stream
      = details.stream().flatMap(detail -> detail.getParts().stream());

In this example, we have a list of elements of type _Detail_. The _Detail_ class contains a field _PARTS_ , which is a _List <String>_. With the help of the _flatMap()_ method, every element from field _PARTS_ will be extracted and added to the new resulting stream. After that, the initial _Stream <Detail>_ will be lost _._

### **3.4. Matching**

Stream API gives a handy set of instruments to validate elements of a sequence according to some predicate. To do this, one of the following methods can be used: _anyMatch(), allMatch(), noneMatch()._ Their names are self-explanatory. Those are terminal operations that return a _boolean_ :
    
    
    boolean isValid = list.stream().anyMatch(element -> element.contains("h")); // true
    boolean isValidOne = list.stream().allMatch(element -> element.contains("h")); // false
    boolean isValidTwo = list.stream().noneMatch(element -> element.contains("h")); // false

For empty streams, the  _allMatch()_ method with any given predicate will return  _true_ :
    
    
    Stream.empty().allMatch(Objects::nonNull); // true

This is a sensible default, as we can’t find any element that doesn’t satisfy the predicate.

Similarly, the  _anyMatch()_ method always returns  _false_ for empty streams:
    
    
    Stream.empty().anyMatch(Objects::nonNull); // false

Again, this is reasonable, as we can’t find an element satisfying this condition.

### **3.5. Reduction**

Stream API allows reducing a sequence of elements to some value according to a specified function with the help of the _reduce()_ method of the type _Stream_. This method takes two parameters: first – start value, second – an accumulator function.

Imagine that you have a _List <Integer>_ and you want to have a sum of all these elements and some initial _Integer_(in this example 23). So, you can run the following code and result will be 26 (23 + 1 + 1 + 1).
    
    
    List<Integer> integers = Arrays.asList(1, 1, 1);
    Integer reduced = integers.stream().reduce(23, (a, b) -> a + b);

### **3.6. Collecting**

The reduction can also be provided by the _collect()_ method of type _Stream._ This operation is very handy in case of converting a stream to a _Collection_ or a _Map_ and representing a stream in the form of a single string _._ There is a utility class _Collectors_ which provide a solution for almost all typical collecting operations. For some, not trivial tasks, a custom _Collector_ can be created.
    
    
    List<String> resultList 
      = list.stream().map(element -> element.toUpperCase()).collect(Collectors.toList());

This code uses the terminal _collect()_ operation to reduce a _Stream <String> _to the _List <String>._

## **4\. Conclusions**

In this article, we briefly touched upon Java streams — definitely one of the most interesting Java 8 features.

There are many more advanced examples of using Streams; the goal of this write-up was only to provide a quick and practical introduction to what you can start doing with the functionality and as a starting point for exploring and further learning.
