# The Java Stream API Tutorial

## **1\. Overview**

In this comprehensive tutorial, we’ll go through the practical uses of Java Streams from their introduction in Java 8 to the latest enhancements in Java 9.

To understand this material, readers need to have a basic knowledge of Java 8 (lambda expressions, _Optional,_ method references) and of the Stream API. In order to be more familiar with these topics, please take a look at our previous articles: [New Features in Java 8](/java-8-new-features) and [Introduction to Java 8 Streams](/java-8-streams-introduction).

## **2\. Stream Creation**

There are many ways to create a stream instance of different sources. Once created, the instance **will not modify its source,** therefore allowing the creation of multiple instances from a single source.

### **2.1. Empty Stream**

We should use the **_empty()_** method in case of the creation of an empty stream:
    
    
    Stream<String> streamEmpty = Stream.empty();

We often use the _empty()_ method upon creation to avoid returning _null_ for streams with no element:
    
    
    public Stream<String> streamOf(List<String> list) {
        return list == null || list.isEmpty() ? Stream.empty() : list.stream();
    }

### **2.2. Stream of _Collection_**

We can also create a stream of any type of _Collection_(_Collection, List, Set_):
    
    
    Collection<String> collection = Arrays.asList("a", "b", "c");
    Stream<String> streamOfCollection = collection.stream();

### **2.3. Stream of Array**

An array can also be the source of a stream:
    
    
    Stream<String> streamOfArray = Stream.of("a", "b", "c");

We can also create a stream out of an existing array or of part of an array:
    
    
    String[] arr = new String[]{"a", "b", "c"};
    Stream<String> streamOfArrayFull = Arrays.stream(arr);
    Stream<String> streamOfArrayPart = Arrays.stream(arr, 1, 3);

### **2.4._Stream.builder()_**

**When builder is used,****the desired type should be additionally specified in the right part of the statement,** otherwise the _build()_ method will create an instance of the _Stream <Object>:_
    
    
    Stream<String> streamBuilder =
      Stream.<String>builder().add("a").add("b").add("c").build();

### **2.5._Stream.generate()_**

The **_generate()_** method accepts a _Supplier <T> _for element generation. As the resulting stream is infinite, the developer should specify the desired size, or the _generate()_ method will work until it reaches the memory limit:
    
    
    Stream<String> streamGenerated =
      Stream.generate(() -> "element").limit(10);

The code above creates a sequence of ten strings with the value _“element.”_

### **2.6._Stream.iterate()_**

Another way of creating an infinite stream is by using the **_iterate()_** method:
    
    
    Stream<Integer> streamIterated = Stream.iterate(40, n -> n + 2).limit(20);

The first element of the resulting stream is the first parameter of the _iterate()_ method. When creating every following element, the specified function is applied to the previous element. In the example above the second element will be 42.

### **2.7. Stream of Primitives**

Java 8 offers the possibility to create streams out of three primitive types: _int, long_ and _double._ As _Stream <T>_ is a generic interface, and there is no way to use primitives as a type parameter with generics, three new special interfaces were created: **_IntStream, LongStream, DoubleStream._**

Using the new interfaces alleviates unnecessary auto-boxing, which allows for increased productivity:
    
    
    IntStream intStream = IntStream.range(1, 3);
    LongStream longStream = LongStream.rangeClosed(1, 3);

The **_range(int startInclusive, int endExclusive)_** method creates an ordered stream from the first parameter to the second parameter. It increments the value of subsequent elements with the step equal to 1. The result doesn’t include the last parameter, it is just an upper bound of the sequence.

The  _**rangeClosed(int startInclusive, int endInclusive)** _method does the same thing with only one difference, the second element is included. We can use these two methods to generate any of the three types of streams of primitives.

Since Java 8, the [_Random_](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/Random.html) class provides a wide range of methods for generating streams of primitives. For example, the following code creates a _DoubleStream,_ which has three elements:
    
    
    Random random = new Random();
    DoubleStream doubleStream = random.doubles(3);

### **2.8. Stream of _String_**

We can also use _String_ as a source for creating a stream with the help of the _chars()_ method of the _String_ class. Since there is no interface for _CharStream_ in JDK, we use the _IntStream_ to represent a stream of chars instead.
    
    
    IntStream streamOfChars = "abc".chars();

The following example breaks a _String_ into sub-strings according to specified _RegEx_ :
    
    
    Stream<String> streamOfString =
      Pattern.compile(", ").splitAsStream("a, b, c");

### **2.9. Stream of File**

Furthermore, Java NIO class _Files_ allows us to generate a _Stream <String>_ of a text file through the _lines()_ method. Every line of the text becomes an element of the stream:
    
    
    Path path = Paths.get("C:\\file.txt");
    Stream<String> streamOfStrings = Files.lines(path);
    Stream<String> streamWithCharset = 
      Files.lines(path, Charset.forName("UTF-8"));

The _Charset_ can be specified as an argument of the _lines()_ method.

## **3\. Referencing a Stream**

We can instantiate a stream, and have an accessible reference to it, as long as only intermediate operations are called. Executing a terminal operation makes a stream inaccessible _._

To demonstrate this, we will forget for a while that the best practice is to chain the sequence of operation. Besides its unnecessary verbosity, technically the following code is valid:
    
    
    Stream<String> stream = 
      Stream.of("a", "b", "c").filter(element -> element.contains("b"));
    Optional<String> anyElement = stream.findAny();

However, an attempt to reuse the same reference after calling the terminal operation will trigger the _IllegalStateException:_
    
    
    Optional<String> firstElement = stream.findFirst();

As the _IllegalStateException_ is a _RuntimeException_ , a compiler will not signalize about a problem. So it is very important to remember that **Java 8****streams can’t be reused.**

This kind of behavior is logical. We designed streams to apply a finite sequence of operations to the source of elements in a functional style, not to store elements.

So to make the previous code work properly, some changes should be made:
    
    
    List<String> elements =
      Stream.of("a", "b", "c").filter(element -> element.contains("b"))
        .collect(Collectors.toList());
    Optional<String> anyElement = elements.stream().findAny();
    Optional<String> firstElement = elements.stream().findFirst();

## **4\. Stream Pipeline**

To perform a sequence of operations over the elements of the data source and aggregate their results, we need three parts: the **source** , **intermediate operation(s)** and a **terminal operation.**

Intermediate operations return a new modified stream. For example, to create a new stream of the existing one without few elements, the _skip()_ method should be used:
    
    
    Stream<String> onceModifiedStream =
      Stream.of("abcd", "bbcd", "cbcd").skip(1);

If we need more than one modification, we can chain intermediate operations. Let’s assume that we also need to substitute every element of the current _Stream <String>_ with a sub-string of the first few chars. We can do this by chaining the _skip()_ and _map()_ methods:
    
    
    Stream<String> twiceModifiedStream =
      stream.skip(1).map(element -> element.substring(0, 3));

As we can see, the _map()_ method takes a lambda expression as a parameter. If we want to learn more about lambdas, we can take a look at our tutorial [Lambda Expressions and Functional Interfaces: Tips and Best Practices](/java-8-lambda-expressions-tips).

A stream by itself is worthless; the user is interested in the result of the terminal operation, which can be a value of some type or an action applied to every element of the stream. **We can only use one terminal operation per stream.**

The correct and most convenient way to use streams is by a **stream pipeline, which is a chain of the stream source, intermediate operations, and a terminal operation:**
    
    
    List<String> list = Arrays.asList("abc1", "abc2", "abc3");
    long size = list.stream().skip(1)
      .map(element -> element.substring(0, 3)).sorted().count();

## **5\. Lazy Invocation**

**Intermediate operations are lazy.** This means that **they will be invoked only if it is necessary for the terminal operation execution.**

For example, let’s call the method _wasCalled()__,_ which increments an inner counter every time it’s called:
    
    
    private long counter;
     
    private void wasCalled() {
        counter++;
    }

Now let’s call the method _wasCalled_ _()_ from operation _filter()_ :
    
    
    List<String> list = Arrays.asList(“abc1”, “abc2”, “abc3”);
    counter = 0;
    Stream<String> stream = list.stream().filter(element -> {
        wasCalled();
        return element.contains("2");
    });

As we have a source of three elements, we can assume that the _filter()_ method will be called three times, and the value of the _counter_ variable will be 3. However, running this code doesn’t change _counter_ at all, it is still zero, so the _filter()_ method wasn’t even called once. The reason why is missing of the terminal operation.

Let’s rewrite this code a little bit by adding a _map()_ operation and a terminal operation, _findFirst()._ We will also add the ability to track the order of method calls with the help of logging:
    
    
    Optional<String> stream = list.stream().filter(element -> {
        log.info("filter() was called");
        return element.contains("2");
    }).map(element -> {
        log.info("map() was called");
        return element.toUpperCase();
    }).findFirst();

The resulting log shows that we called the _filter()_ method twice and the _map()_ method once. This is because the pipeline executes vertically. In our example, the first element of the stream didn’t satisfy the filter’s predicate. Then we invoked the _filter()_ method for the second element, which passed the filter. Without calling the _filter()_ for the third element, we went down through the pipeline to the _map()_ method.

The _findFirst()_ operation satisfies by just one element. So, in this particular example, the lazy invocation allowed us to avoid one method call for _filter()._

## **6\. Order of Execution**

From the performance point of view, **the right order is one of the most important aspects of chaining operations in the stream pipeline:**
    
    
    long size = list.stream().map(element -> {
        wasCalled();
        return element.substring(0, 3);
    }).skip(2).count();

Execution of this code will increase the value of the counter by three. This means that we called the _map()_ method of the stream three times, but the value of the _size_ is one. So the resulting stream has just one element, and we executed the expensive _map()_ operations for no reason two out of the three times.

If we change the order of the _skip()_ and the _map()_ methods _,_ the _counter_ will increase by only one. So we will call the _map()_ method only once:
    
    
    long size = list.stream().skip(2).map(element -> {
        wasCalled();
        return element.substring(0, 3);
    }).count();

This brings us to the following rule: **intermediate operations which reduce the size of the stream should be placed before operations which are applying to each element.** So we need to keep methods such as s _kip(), filter(),_ and _distinct()_ at the top of our stream pipeline.

## **7\. Stream Reduction**

The API has many terminal operations which aggregate a stream to a type or to a primitive: _count(), max(), min(),_ and _sum()._ However, these operations work according to the predefined implementation. So what **if a developer needs to customize a Stream’s reduction mechanism?** There are two methods which allow us to do this, the _**reduce()** _and the **_collect()_** methods.

### **7.1. The _reduce()_ Method**

There are three variations of this method, which differ by their signatures and returning types. They can have the following parameters:

**identity –** the initial value for an accumulator, or a default value if a stream is empty and there is nothing to accumulate

**accumulator –** a function which specifies the logic of the aggregation of elements. As the accumulator creates a new value for every step of reducing, the quantity of new values equals the stream’s size and only the last value is useful. This is not very good for the performance.

**combiner –** a function which aggregates the results of the accumulator. We only call combiner in a parallel mode to reduce the results of accumulators from different threads.

Now let’s look at these three methods in action:
    
    
    OptionalInt reduced =
      IntStream.range(1, 4).reduce((a, b) -> a + b);

_reduced_ = 6 (1 + 2 + 3)
    
    
    int reducedTwoParams =
      IntStream.range(1, 4).reduce(10, (a, b) -> a + b);

_reducedTwoParams_ = 16 (10 + 1 + 2 + 3)
    
    
    int reducedParams = Stream.of(1, 2, 3)
      .reduce(10, (a, b) -> a + b, (a, b) -> {
         log.info("combiner was called");
         return a + b;
      });

The result will be the same as in the previous example (16), and there will be no login, which means that combiner wasn’t called. To make a combiner work, a stream should be parallel:
    
    
    int reducedParallel = Arrays.asList(1, 2, 3).parallelStream()
        .reduce(10, (a, b) -> a + b, (a, b) -> {
           log.info("combiner was called");
           return a + b;
        });

The result here is different (36), and the combiner was called twice. Here the reduction works by the following algorithm: the accumulator ran three times by adding every element of the stream to _identity_. These actions are being done in parallel. As a result, they have (10 + 1 = 11; 10 + 2 = 12; 10 + 3 = 13;). Now combiner can merge these three results. It needs two iterations for that (12 + 13 = 25; 25 + 11 = 36).

### **7.2. The _collect()_ Method**

The reduction of a stream can also be executed by another terminal operation, the _collect()_ method. It accepts an argument of the type _Collector,_ which specifies the mechanism of reduction. There are already created, predefined collectors for most common operations. They can be accessed with the help of the _Collectors_ type.

In this section, we will use the following _List_ as a source for all streams:
    
    
    List<Product> productList = Arrays.asList(new Product(23, "potatoes"),
      new Product(14, "orange"), new Product(13, "lemon"),
      new Product(23, "bread"), new Product(13, "sugar"));

**Converting a stream to the _Collection_ (_Collection, List_ or _Set_):**
    
    
    List<String> collectorCollection = 
      productList.stream().map(Product::getName).collect(Collectors.toList());

**Reducing to _String_ :**
    
    
    String listToString = productList.stream().map(Product::getName)
      .collect(Collectors.joining(", ", "[", "]"));

The _joining()_ method can have from one to three parameters (delimiter, prefix, suffix). The most convenient thing about using _joining()_ is that the developer doesn’t need to check if the stream reaches its end to apply the suffix and not to apply a delimiter. _Collector_ will take care of that.

**Processing the average value of all numeric elements of the stream:**
    
    
    double averagePrice = productList.stream()
      .collect(Collectors.averagingInt(Product::getPrice));

**Processing the sum of all numeric elements of the stream:**
    
    
    int summingPrice = productList.stream()
      .collect(Collectors.summingInt(Product::getPrice));

The methods _averagingXX(), summingXX()_ and _summarizingXX()_ can work with primitives (_int, long, double_) and with their wrapper classes (_Integer, Long, Double_). One more powerful feature of these methods is providing the mapping. As a result, the developer doesn’t need to use an additional _map()_ operation before the _collect()_ method.

**Collecting statistical information about stream’s elements:**
    
    
    IntSummaryStatistics statistics = productList.stream()
      .collect(Collectors.summarizingInt(Product::getPrice));

By using the resulting instance of type _IntSummaryStatistics_ , the developer can create a statistical report by applying the _toString()_ method. The result will be a _String_ common to this one _“IntSummaryStatistics{count=5, sum=86, min=13, average=17,200000, max=23}.”_

It is also easy to extract from this object separate values for _count, sum, min,_ _average_ , and  _max_ by applying the methods _getCount(), getSum(), getMin(), getAverage(),_ and _getMax()._ All of these values can be extracted from a single pipeline.

**Grouping of stream’s elements according to the specified function:**
    
    
    Map<Integer, List<Product>> collectorMapOfLists = productList.stream()
      .collect(Collectors.groupingBy(Product::getPrice));

In the example above, the stream was reduced to the _Map_ , which groups all products by their price.

**Dividing stream’s elements into groups according to some predicate:**
    
    
    Map<Boolean, List<Product>> mapPartioned = productList.stream()
      .collect(Collectors.partitioningBy(element -> element.getPrice() > 15));

**Pushing the collector to perform additional transformation:**
    
    
    Set<Product> unmodifiableSet = productList.stream()
      .collect(Collectors.collectingAndThen(Collectors.toSet(),
      Collections::unmodifiableSet));

In this particular case, the collector has converted a stream to a _Set_ , and then created the unchangeable _Set_ out of it.

**Custom collector:**

If for some reason a [custom collector](/java-8-collectors#Custom) should be created, the easiest and least verbose way of doing so is to use the method _of()_ of the type _Collector._
    
    
    Collector<Product, ?, LinkedList<Product>> toLinkedList =
      Collector.of(LinkedList::new, LinkedList::add, 
        (first, second) -> { 
           first.addAll(second); 
           return first; 
        });
    
    LinkedList<Product> linkedListOfPersons =
      productList.stream().collect(toLinkedList);

In this example, an instance of the _Collector_ got reduced to the _LinkedList_ <Persone>.

## **8\. Parallel Streams**

Before Java 8, parallelization was complex. The emergence of the [_ExecutorService_](/java-executor-service-tutorial) and the _[ForkJoin](/java-fork-join) _simplified a developer’s life a little bit, but it was still worth remembering how to create a specific executor, how to run it, and so on. Java 8 introduced a way of accomplishing parallelism in a functional style.

The API allows us to create parallel streams, which perform operations in a parallel mode. When the source of a stream is a _Collection_ or an _array_ , it can be achieved with the help of the **_parallelStream()_** method:
    
    
    Stream<Product> streamOfCollection = productList.parallelStream();
    boolean isParallel = streamOfCollection.isParallel();
    boolean bigPrice = streamOfCollection
      .map(product -> product.getPrice() * 12)
      .anyMatch(price -> price > 200);

If the source of a stream is something other than a _Collection_ or an _array_ , the **_parallel()_** method should be used:
    
    
    IntStream intStreamParallel = IntStream.range(1, 150).parallel();
    boolean isParallel = intStreamParallel.isParallel();

Under the hood, Stream API automatically uses the _ForkJoin_ framework to execute operations in parallel. By default, the common thread pool will be used and there is no way (at least for now) to assign some custom thread pool to it. [This can be overcome by using a custom set of parallel collectors.](https://github.com/pivovarit/parallel-collectors)

When using streams in parallel mode, avoid blocking operations. It is also best to use parallel mode when tasks need a similar amount of time to execute. If one task lasts much longer than the other, it can slow down the complete app’s workflow.

The stream in parallel mode can be converted back to the sequential mode by using the _sequential()_ method:
    
    
    IntStream intStreamSequential = intStreamParallel.sequential();
    boolean isParallel = intStreamSequential.isParallel();

## 9\. Stream API Enhancements in Java 9

Java 9 introduces a few notable improvements to the Stream API that make working with streams even more expressive and efficient. In this section, we’ll cover the _takeWhile()_ , _dropWhile()_ , _iterate()_ , and _ofNullable()_ methods, exploring how they simplify various operations compared to Java 8.

### 9.1. _takeWhile()_ and _dropWhile()_

The new _takeWhile()_ and _dropWhile()_ methods use a _Predicate_ to specify a condition for including or excluding elements in the stream. These methods are particularly useful for ordered streams, as they allow us to process elements based on a condition applied sequentially.

**With _takeWhile()_ , we can collect elements from the start of a stream until a given condition is no longer met.** As soon as an element fails this condition, _takeWhile()_ stops collecting further elements:
    
    
    Stream<String> stream = Stream.iterate("", s -> s + "s")
      .takeWhile(s -> s.length() < 10);

Here, _takeWhile()_ applies the predicate _“ _s - > s.length() < 10__“, which means it will keep adding elements to the stream as long as the string length is less than 10. The collection stops collecting elements as soon as an element no longer meets the condition.

**In contrast,_dropWhile()_ discards elements from the start of the stream as long as they satisfy the given _Predicate_.** It stops dropping elements the moment an element fails the condition, at which point it includes the remaining elements in the stream:
    
    
    Stream<String> stream = Stream.of("a", "aa", "aaa", "aaaaa")
      .dropWhile(s -> s.length() < 5);

In this case, _dropWhile()_ will skip over elements until it encounters a string with a length of 5 or greater, at which point it stops dropping elements.

### 9.2. Enhanced _iterate()_ Method

**Java 9 adds a variant of the _iterate()_ method that allows us to specify a condition under which the stream will stop generating elements, effectively creating a finite stream.** This enhanced _iterate()_ function can specify a stopping condition when needed:
    
    
    Stream.iterate(0, i -> i < 10, i -> i + 1)
      .forEach(System.out::println);

This example generates numbers from 0 to 9, directly integrating the stopping condition within the _iterate()_ method itself, making it simpler and clearer than Java 8’s infinite streams.

### 9.3. _ofNullable()_ for _Optional_ Elements

Often, we may need to create a stream with a single element that might be _null_. Java 9’s _ofNullable()_ method addresses this by returning an empty stream if the provided element is _null_ , avoiding the need for complex conditional logic:
    
    
    collection.stream()
      .flatMap(s -> Stream.ofNullable(map.get(s)))
      .collect(Collectors.toList());

This _ofNullable()_ method removes the need for ternary expressions or null checks, streamlining the code where conditional element addition is necessary.

## **10\. Conclusion**

The Stream API is a powerful, but simple to understand set of tools for processing the sequence of elements. When used properly, it allows us to reduce a huge amount of boilerplate code, create more readable programs, and improve an app’s productivity.

In most of the code samples shown in this article, we left the streams unconsumed (we didn’t apply the _close()_ method or a terminal operation). In a real app, **don’t leave an instantiated stream unconsumed, as that will lead to memory leaks.**
