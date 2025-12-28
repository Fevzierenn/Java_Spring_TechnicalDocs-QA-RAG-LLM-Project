# Guide to Java Collectors

## **1\. Overview**

In this tutorial, we’ll be going through Java 8’s collectors, which are used in the final step of processing a _Stream_. To read more about the _Stream_ API itself, please refer to [this article](/java-8-streams).

If we want to see how to leverage the power of collectors for parallel processing, we can look at [this project.](https://github.com/pivovarit/parallel-collectors)

## **2._Stream.collect()_ Method**

The _collect()_ method is one of Java 8’s _Stream_ API terminal methods. It allows us to perform mutable fold operations (repackaging elements to some data structures and applying some additional logic, concatenating them, etc.) on data elements held in a _Stream_ instance.

The strategy for this operation is provided via the _Collector_ interface implementation.

## **3._Collectors_**

Typically, we can find all the predefined implementations in the _Collectors_ class. It’s common practice to use the following static import with them to leverage increased readability:
    
    
    import static java.util.stream.Collectors.*;

Furthermore, we can also use single import collectors of our choice:
    
    
    import static java.util.stream.Collectors.toList;
    import static java.util.stream.Collectors.toMap;
    import static java.util.stream.Collectors.toSet;

In the following examples, we’ll be reusing the following list:
    
    
    List<String> givenList = Arrays.asList("a", "bb", "ccc", "dd");

### **3.1._Collectors.toCollection()_**

As we’ve already noted, when using the _toSet()_ and _toList()_ collectors, we can’t make any assumptions about their implementations. If we want to use a custom implementation, we’ll need to use the _toCollection()_ collector with a provided collection of our choice.

Let’s create a _Stream_ instance representing a sequence of elements, and then collect them into a _LinkedList_ instance:
    
    
    List<String> result = givenList.stream()
      .collect(toCollection(LinkedList::new))

Notice that this will not work with any immutable collections. **In such a case, we would need to either write a custom collector implementation or use _collectingAndThen()_**.

### **3.2._Collectors.toList()_**

**As the name implies, the main purpose of the _toList()_ method is to collect all _Stream_ elements into a _List_ instance**. The important thing to remember is that we can’t assume any particular _List_ implementation with this method. If we want to have more control over this, we can use _toCollection()_ instead.

Let’s create a _Stream_ instance representing a sequence of elements, and then collect them into a _List_ instance:
    
    
    List<String> result = givenList.stream()
      .collect(toList());

### **3.3._Collectors.toUnmodifiableList()_**

Java 10 introduced a convenient way to accumulate the _Stream_ elements into an [unmodifiable _List_](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/List.html#unmodifiable):
    
    
    List<String> result = givenList.stream()
      .collect(toUnmodifiableList());

So, if we try to modify the _result_ _List_ , we’ll get an _UnsupportedOperationException_ :
    
    
    assertThatThrownBy(() -> result.add("foo"))
      .isInstanceOf(UnsupportedOperationException.class);

### **3.4._Collectors.toSet()_**

The _toSet()_ collector can be used to collect all  _Stream_ elements in a _Set_ instance. The important thing to remember is that we can’t assume any particular _Set_ implementation with this method. **If we want to have more control over this, we can use _toCollection()_ instead**.

Let’s create a _Stream_ instance representing a sequence of elements, and then collect them into a _Set_ instance:
    
    
    Set<String> result = givenList.stream()
      .collect(toSet());

A _Set_ doesn’t contain duplicate elements. If our collection contains elements equal to each other, they appear in the resulting _Set_ only once:
    
    
    List<String> listWithDuplicates = Arrays.asList("a", "bb", "c", "d", "bb");
    Set<String> result = listWithDuplicates.stream()
      .collect(toSet();
    assertThat(result)
      .hasSize(4);

### **3.5._Collectors.toUnmodifiableSet()_**

Since Java 10, we can easily create an [unmodifiable _Set_](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/Set.html#unmodifiable) using the _toUnmodifiableSet()_ collector:
    
    
    Set<String> result = givenList.stream()
      .collect(toUnmodifiableSet());

However, any attempt to modify the _Set_ will end up with an _UnsupportedOperationException_ :
    
    
    assertThatThrownBy(() -> result.add("foo"))
      .isInstanceOf(UnsupportedOperationException.class);

### **3.6._Collectors_._toMap()_**

The _toMap()_ collector can be used to collect _Stream_ elements into a _Map_ instance. To do so, we need to provide two functions: _keyMapper()_ and _valueMapper()._

**Firstly, we’ll use _keyMapper()_ to extract a _Map_ key from a _Stream_ element**.**Then, we can use _valueMapper()_ to extract a value associated with a given key**.

So, let’s collect those elements into a _Map_ that stores strings as keys and their lengths as values:
    
    
    Map<String, Integer> result = givenList.stream()
      .collect(toMap(Function.identity(), String::length))

In a nutshell, _Function.identity()_ is just a shortcut for defining a function that accepts and returns the same value.

So what happens if our collection contains duplicate elements? Contrary to _toSet()_ , the _toMap()_ method doesn’t silently filter duplicates, which is understandable because how would it figure out which value to pick for this key?
    
    
    List<String> listWithDuplicates = Arrays.asList("a", "bb", "c", "d", "bb");
    assertThatThrownBy(() -> {
        listWithDuplicates.stream().collect(toMap(Function.identity(), String::length));
    }).isInstanceOf(IllegalStateException.class);

**Note that _toMap()_ doesn’t even evaluate whether the values are also equal**. If it sees duplicate keys, it immediately throws an _IllegalStateException_.

In such cases with key collision, we should use _toMap()_ with another signature:
    
    
    Map<String, Integer> result = givenList.stream()
      .collect(toMap(Function.identity(), String::length, (item, identicalItem) -> item));

The third argument here is a _BinaryOperator()_ , where we can specify how we want to handle collisions. In this case, we’ll just pick any of these two colliding values because we know that the same strings will always have the same lengths too.

### **3.7._Collectors.toUnmodifiableMap()_**

Similar to with _List_ s and _Set_ s, Java 10 introduced an easy way to collect _Stream_ elements into an [unmodifiable _Map_](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/Map.html#unmodifiable):
    
    
    Map<String, Integer> result = givenList.stream()
      .collect(toUnmodifiableMap(Function.identity(), String::length))

As we can see, if we try to put a new entry into a _result Map_ , we’ll get an _UnsupportedOperationException_ :
    
    
    assertThatThrownBy(() -> result.put("foo", 3))
      .isInstanceOf(UnsupportedOperationException.class);

### **3.8._Collectors._ c _ollectingAndThen()_**

**_CollectingAndThen()_ is a special collector that allows us to perform another action on a result straight after collecting ends**.

Let’s collect _Stream_ elements to a _List_ instance, and then convert the result into an _ImmutableList_ instance:
    
    
    List<String> result = givenList.stream()
      .collect(collectingAndThen(toList(), ImmutableList::copyOf))

### **3.9._Collectors.joining()_**

The _Joining()_ collector can be used for joining _Stream <String>_ elements.

We can join them together by doing:
    
    
    String result = givenList.stream()
      .collect(joining());
    

This will result in:
    
    
    "abbcccdd"

We can also specify custom separators, prefixes, and postfixes:
    
    
    String result = givenList.stream()
      .collect(joining(" "));

This will result in:
    
    
    "a bb ccc dd"

We can also write:
    
    
    String result = givenList.stream()
      .collect(joining(" ", "PRE-", "-POST"));

This will result in:
    
    
    "PRE-a bb ccc dd-POST"

### **3.10._Collectors._ c _ounting()_**

_Counting()_ is a simple collector that allows for the counting of all _Stream_ elements.

Now we can write:
    
    
    Long result = givenList.stream()
      .collect(counting());

### **3.11._Collectors._ s _ummarizingDouble/Long/Int()_**

_SummarizingDouble/Long/Int_ is a collector that returns a special class containing statistical information about numerical data in a _Stream_ of extracted elements.

We can obtain information about string lengths by doing:
    
    
    DoubleSummaryStatistics result = givenList.stream()
      .collect(summarizingDouble(String::length));

In this case, the following will be true:
    
    
    assertThat(result.getAverage()).isEqualTo(2);
    assertThat(result.getCount()).isEqualTo(4);
    assertThat(result.getMax()).isEqualTo(3);
    assertThat(result.getMin()).isEqualTo(1);
    assertThat(result.getSum()).isEqualTo(8);

### **3.12._Collectors.averagingDouble/Long/Int()_**

_AveragingDouble/Long/Int_ is a collector that simply returns an average of extracted elements.

We can get the average string length by doing:
    
    
    Double result = givenList.stream()
      .collect(averagingDouble(String::length));

### **3.13._Collectors._ s _ummingDouble/Long/Int()_**

_SummingDouble/Long/Int_ is a collector that simply returns a sum of extracted elements.

We can get the sum of all string lengths by doing:
    
    
    Double result = givenList.stream()
      .collect(summingDouble(String::length));

### **3.14._Collectors.maxBy/minBy_**

_MaxBy()_ and _MinBy()_ collectors return the biggest/smallest element of a _Stream_ according to a provided _Comparator_ instance.

We can pick the biggest element by doing:
    
    
    Optional<String> result = givenList.stream()
      .collect(maxBy(Comparator.naturalOrder()));

We can see that the returned value is wrapped in an _Optional_ instance. This forces users to rethink the empty collection corner case.

### **3.15._Collectors_._groupingBy()_**

**Typically, we can use the _GroupingBy()_ collector to group objects by a given property and then store the results in a _Map_ instance**.

We can group them by string length, and store the grouping results in _Set_ instances:
    
    
    Map<Integer, Set<String>> result = givenList.stream()
      .collect(groupingBy(String::length, toSet()));

This will result in the following being true:
    
    
    assertThat(result)
      .containsEntry(1, newHashSet("a"))
      .containsEntry(2, newHashSet("bb", "dd"))
      .containsEntry(3, newHashSet("ccc"));
    

We can see that the second argument of the _groupingBy()_ method is a _Collector._ In addition, we’re free to use any collector of our choice.

### **3.16._Collectors.partitioningBy()_**

_partitioningBy()_ is a specialized case of _groupingBy()_ that accepts a _Predicate_ instance, and then collects _Stream_ elements into a _Map_ instance that stores _Boolean_ values as keys and collections as values. **Under the _“true”_ key, we can find a collection of elements matching the given _Predicate_ , and under the _“false”_ key, we can find a collection of elements not matching the given _Predicate_**.

We can write:
    
    
    Map<Boolean, List<String>> result = givenList.stream()
      .collect(partitioningBy(s -> s.length() > 2))

This results in a _Map_ containing:
    
    
    {false=["a", "bb", "dd"], true=["ccc"]}
    

### **3.17._Collectors.teeing()_**

Let’s find the maximum and minimum numbers from a given _Stream_ using the collectors we’ve learned so far:
    
    
    List<Integer> numbers = Arrays.asList(42, 4, 2, 24);
    Optional<Integer> min = numbers.stream().collect(minBy(Integer::compareTo));
    Optional<Integer> max = numbers.stream().collect(maxBy(Integer::compareTo));
    // do something useful with min and max

Here we’re using two different collectors, and then combining the results of those two to create something meaningful. Before Java 12, in order to cover such use cases, we had to operate on the given _Stream_ twice, store the intermediate results into temporary variables, and then combine those results afterward.

Fortunately, Java 12 offers a built-in collector that takes care of these steps on our behalf; all we have to do is provide the two collectors and the combiner function.

**Since this new collector[tees](https://en.wikipedia.org/wiki/Tee_\(command\)) the given stream towards two different directions, it’s called _teeing():_**
    
    
    numbers.stream().collect(teeing(
      minBy(Integer::compareTo), // The first collector
      maxBy(Integer::compareTo), // The second collector
      (min, max) -> // Receives the result from those collectors and combines them
    ));

## **4\. Custom Collectors**

**If we want to write our own Collector implementation, we need to implement the _Collector_ interface, and specify its three generic parameters**:
    
    
    public interface Collector<T, A, R> {...}

  1. **T** – the type of objects that will be available for collection
  2. **A** – the type of a mutable accumulator object
  3. **R** – the type of a final result



Let’s write an example _Collector_ for collecting elements into an _ImmutableSet_ instance. We start by specifying the right types:
    
    
    private class ImmutableSetCollector<T>
      implements Collector<T, ImmutableSet.Builder<T>, ImmutableSet<T>> {...}

Since we need a mutable collection for internal collection operation handling, we can’t use _ImmutableSet_. Instead, we need to use some other mutable collection or any other class that could temporarily accumulate objects for us. **In this case, we will go with an _ImmutableSet.Builder()_ and now we need to implement 5 methods**:

  * _Supplier <ImmutableSet.Builder<T>> **supplier**()_
  * _BiConsumer <ImmutableSet.Builder<T>, T> **accumulator**()_
  * _BinaryOperator <ImmutableSet.Builder<T>> **combiner**()_
  * _Function <ImmutableSet.Builder<T>, ImmutableSet<T>> **finisher**()_
  * _Set <Characteristics> **characteristics**()_



The _supplier()_ method returns a _Supplier_ instance that generates an empty accumulator instance. So in this case, we can simply write:
    
    
    @Override
    public Supplier<ImmutableSet.Builder<T>> supplier() {
        return ImmutableSet::builder;
    }
    

The _accumulator()_ method returns a function that is used for adding a new element to an existing _accumulator_ object. So let’s just use the _Builder_ ‘s _add_ method:
    
    
    @Override
    public BiConsumer<ImmutableSet.Builder<T>, T> accumulator() {
        return ImmutableSet.Builder::add;
    }

The _combiner()_ method returns a function that is used for merging two accumulators together:
    
    
    @Override
    public BinaryOperator<ImmutableSet.Builder<T>> combiner() {
        return (left, right) -> left.addAll(right.build());
    }

The _finisher()_ method returns a function that is used for converting an accumulator to the final result type. So in this case, we’ll just use _Builder_ ‘s _build_ method:
    
    
    @Override
    public Function<ImmutableSet.Builder<T>, ImmutableSet<T>> finisher() {
        return ImmutableSet.Builder::build;
    }

The _characteristics()_ method is used to provide Stream with some additional information that will be used for internal optimizations. In this case, we don’t pay attention to the elements order in a _Set_ because we’ll use _Characteristics.UNORDERED_. To obtain more information regarding this subject, check _Characteristics_ ‘ JavaDoc:
    
    
    @Override public Set<Characteristics> characteristics() {
        return Sets.immutableEnumSet(Characteristics.UNORDERED);
    }

Here is the complete implementation along with the usage:
    
    
    public class ImmutableSetCollector<T>
      implements Collector<T, ImmutableSet.Builder<T>, ImmutableSet<T>> {
    
    @Override
    public Supplier<ImmutableSet.Builder<T>> supplier() {
        return ImmutableSet::builder;
    }
    
    @Override
    public BiConsumer<ImmutableSet.Builder<T>, T> accumulator() {
        return ImmutableSet.Builder::add;
    }
    
    @Override
    public BinaryOperator<ImmutableSet.Builder<T>> combiner() {
        return (left, right) -> left.addAll(right.build());
    }
    
    @Override
    public Function<ImmutableSet.Builder<T>, ImmutableSet<T>> finisher() {
        return ImmutableSet.Builder::build;
    }
    
    @Override
    public Set<Characteristics> characteristics() {
        return Sets.immutableEnumSet(Characteristics.UNORDERED);
    }
    
    public static <T> ImmutableSetCollector<T> toImmutableSet() {
        return new ImmutableSetCollector<>();
    }

Finally, here in action:
    
    
    List<String> givenList = Arrays.asList("a", "bb", "ccc", "dddd");
    
    ImmutableSet<String> result = givenList.stream()
      .collect(toImmutableSet());

## 5\. Java 9 Improvements

Here, we’re going to explore two new collectors added in Java 9: _filtering()_ and _flatMapping()_ used in combination with _Collectors.groupingBy()_ providing intelligent collections of elements.

### **5.1._Collectors.filtering()_**

**The _Collectors.filtering()_ is similar to the _Stream.filter()._ It’s used for filtering input elements but used for different scenarios**. The _filter()_ method from the Stream API is used in the stream chain whereas this new _filtering()_ method is a collector that was designed to be used along with _groupingBy()_.

With _filter()_ , the values are filtered first and then it’s grouped. In this way, the values which are filtered out are gone and there is no trace of it. If we need a trace then we would need to group first and then apply filtering which actually the _Collectors.filtering()_ does.

_Collectors.filtering()_ takes a function for filtering the input elements and a collector to collect the filtered elements:
    
    
    @Test
    public void givenList_whenSatifyPredicate_thenMapValueWithOccurences() {
        List<Integer> numbers = List.of(1, 2, 3, 5, 5);
    
        Map<Integer, Long> result = numbers.stream()
          .filter(val -> val > 3)
          .collect(Collectors.groupingBy(i -> i, Collectors.counting()));
    
        assertEquals(1, result.size());
    
        result = numbers.stream()
          .collect(Collectors.groupingBy(i -> i,
            Collectors.filtering(val -> val > 3, Collectors.counting())));
    
        assertEquals(4, result.size());
    }

### **5.2._Collectors.flatMapping()_**

The _Collectors.flatMapping()_ is similar to _Collectors.mapping()_ but has a more fine-grained objective. Both the collectors take a function and a collector where the elements are collected but _flatMapping()_ function accepts a _Stream_ of elements which is then accumulated by the collector.

Let’s see the following model class:
    
    
    class Blog {
        private String authorName;
        private List<String> comments;
          
        // constructor and getters
    }
    

**_Collectors.flatMapping()_ lets us skip intermediate collection and write directly to a single container which is mapped to that group defined by the _Collectors.groupingBy()_** :
    
    
    @Test
    public void givenListOfBlogs_whenAuthorName_thenMapAuthorWithComments() {
        Blog blog1 = new Blog("1", "Nice", "Very Nice");
        Blog blog2 = new Blog("2", "Disappointing", "Ok", "Could be better");
        List<Blog> blogs = List.of(blog1, blog2);
            
        Map<String,  List<List<String>>> authorComments1 = blogs.stream()
         .collect(Collectors.groupingBy(Blog::getAuthorName, 
           Collectors.mapping(Blog::getComments, Collectors.toList())));
           
        assertEquals(2, authorComments1.size());
        assertEquals(2, authorComments1.get("1").get(0).size());
        assertEquals(3, authorComments1.get("2").get(0).size());
    
        Map<String, List<String>> authorComments2 = blogs.stream()
          .collect(Collectors.groupingBy(Blog::getAuthorName, 
            Collectors.flatMapping(blog -> blog.getComments().stream(), 
            Collectors.toList())));
    
        assertEquals(2, authorComments2.size());
        assertEquals(2, authorComments2.get("1").size());
        assertEquals(3, authorComments2.get("2").size());
    }

The _Collectors.mapping()_ maps all grouped author’s comments to the collector’s container i.e. _List_ whereas this intermediate collection is removed with _flatMapping()_ as it gives a direct stream of the comment list to be mapped to the collector’s container.

## **6\. Conclusion**

In this article, we explored in depth Java 8’s _Collectors_ and showed how to implement a custom one. Along the way, we elucidated the Java 9 improvements. Make sure to [check out one of my projects that enhances the capabilities of parallel processing in Java.](https://github.com/pivovarit/parallel-collectors) More interesting articles can be read [on my site](http://4comprehension.com).
