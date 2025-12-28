# Guide to the Java ArrayList

## 1\. Overview

In this tutorial, we’ll look at the _ArrayList_ class from the [Java Collections Framework](/java-collections). We’ll discuss its properties, common use cases, and advantages and disadvantages.

_ArrayList_ resides within Java Core Libraries; therefore, we don’t need additional libraries. To use it, we add its _import_ statement:
    
    
    import java.util.ArrayList;

The _List_ represents an ordered sequence of values where a value can occur more than once.

_ArrayList_ is a _List_ implementation built atop an array that can dynamically grow and shrink as we add/remove elements. We can easily access an element by its index starting from zero. This implementation has the following properties:

  * Random access takes _O(1)_ time
  * Adding an element takes amortized constant time _O(1)_
  * Inserting/Deleting takes _O(n)_ time
  * Searching takes _O(n)_ time for an unsorted array and _O(log n)_ for a sorted one



## 2\. Creating an _ArrayList_

Let’s introduce _ArrayList_ constructors.

At the outset, _ArrayList <E>_ is a generic class; therefore, we can parameterize it with any type we want. The compiler ensures that we can’t use a non-compatible type. For example, we can’t put _Integer_ values inside a collection of _Strings_. Furthermore, we don’t need to cast elements when retrieving them from a collection.

We should use the generic interface _List <E>_ as a variable type as a best practice because it decouples it from any specific implementation.

### **2.1. Default No-Arg Constructor**

We can create an empty _ArrayList_ instance using the no-arg constructor:
    
    
    List<String> list = new ArrayList<>();
    assertTrue(list.isEmpty());

### 2.2. Constructor Accepting Initial Capacity

We can specify the initial length of an underlying array to avoid unnecessary resizing while adding new items using the constructor that accepts initial capacity:
    
    
    List<String> list = new ArrayList<>(20);

### 2.3. Constructor Accepting _Collection_

We can create a new _ArrayList_ instance using elements of a _Collection_ instance for populating the underlying array:
    
    
    Collection<Integer> numbers 
      = IntStream.range(0, 10).boxed().collect(toSet());
    
    List<Integer> list = new ArrayList<>(numbers);
    assertEquals(10, list.size());
    assertTrue(numbers.containsAll(list));

## 3\. Adding Elements to the _ArrayList_

We can add an element either at the end or at a specific index position:
    
    
    List<Long> list = new ArrayList<>();
    
    list.add(1L);
    list.add(2L);
    list.add(1, 3L);
    
    assertThat(Arrays.asList(1L, 3L, 2L), equalTo(list));

We can also add a collection or a batch of elements:
    
    
    List<Long> list = new ArrayList<>(Arrays.asList(1L, 2L, 3L));
    LongStream.range(4, 10).boxed()
      .collect(collectingAndThen(toCollection(ArrayList::new), ys -> list.addAll(0, ys)));
    assertThat(Arrays.asList(4L, 5L, 6L, 7L, 8L, 9L, 1L, 2L, 3L), equalTo(list));

## 4\. Iterating Over the _ArrayList_

We have two types of iterators available: _Iterator_ and _ListIterator_.

We use _an Iterator_ to traverse the list in one direction only and a  _ListIterator_ to traverse it in both directions.

Let’s use the _ListIterator_ as an example:
    
    
    List<Integer> list = new ArrayList<>(
      IntStream.range(0, 10).boxed().collect(toCollection(ArrayList::new))
    );
    ListIterator<Integer> it = list.listIterator(list.size());
    List<Integer> result = new ArrayList<>(list.size());
    while (it.hasPrevious()) {
        result.add(it.previous());
    }
    
    Collections.reverse(list);
    assertThat(result, equalTo(list));

We can also search, add, or remove elements using iterators.

## 5\. Searching the _ArrayList_

Let’s demonstrate searching using a collection:
    
    
    List<String> list = LongStream.range(0, 16)
      .boxed()
      .map(Long::toHexString)
      .collect(toCollection(ArrayList::new));
    List<String> stringsToSearch = new ArrayList<>(list);
    stringsToSearch.addAll(list);

### 5.1. Searching an Unsorted List

We may use the _indexOf()_ or the _lastIndexOf()_ method to find an element. They both accept an object and return an _int_ value:
    
    
    assertEquals(10, stringsToSearch.indexOf("a"));
    assertEquals(26, stringsToSearch.lastIndexOf("a"));

If we want to find all elements satisfying a predicate, we may filter collection using [Java 8 _Stream API_](/java-streams) using a _Predicate_ :
    
    
    Set<String> matchingStrings = new HashSet<>(Arrays.asList("a", "c", "9"));
    
    List<String> result = stringsToSearch
      .stream()
      .filter(matchingStrings::contains)
      .collect(toCollection(ArrayList::new));
    
    assertEquals(6, result.size());

It is also possible to use a _for_ loop or an iterator:
    
    
    Iterator<String> it = stringsToSearch.iterator();
    Set<String> matchingStrings = new HashSet<>(Arrays.asList("a", "c", "9"));
    
    List<String> result = new ArrayList<>();
    while (it.hasNext()) {
        String s = it.next();
        if (matchingStrings.contains(s)) {
            result.add(s);
        }
    }

### 5.2. Searching a Sorted List

To search a sorted array we may use a binary search algorithm, which works faster than linear search:
    
    
    List<String> copy = new ArrayList<>(stringsToSearch);
    Collections.sort(copy);
    int index = Collections.binarySearch(copy, "f");
    assertThat(index, not(equalTo(-1)));

Notice that if an element isn’t found then _-1_ is returned.

## 6\. Removing Elements from the _ArrayList_

To remove an element, we find its index and then remove it using the _remove()_ method. We can also use an overloaded version of this method, which accepts an object, searches for it, and removes its first occurrence:
    
    
    List<Integer> list = new ArrayList<>(
      IntStream.range(0, 10).boxed().collect(toCollection(ArrayList::new))
    );
    Collections.reverse(list);
    
    list.remove(0);
    assertThat(list.get(0), equalTo(8));
    
    list.remove(Integer.valueOf(0));
    assertFalse(list.contains(0));

Let’s remember that when working with boxed types such as _Integer_ , to remove a particular element, we should first box _int_ value or otherwise, an element is removed by its index.

We can use an iterator to remove several items:
    
    
    Set<String> matchingStrings
      = HashSet<>(Arrays.asList("a", "b", "c", "d", "e", "f"));
    
    Iterator<String> it = stringsToSearch.iterator();
    while (it.hasNext()) {
        if (matchingStrings.contains(it.next())) {
            it.remove();
        }
    }

We may use the _Stream API_ for removing several items, but we won’t show it here.

## 7\. Using a Sequenced Collection – _ArrayList_

We can add, get, and remove the first or the last element in an _ArrayList_ using a sequenced collection. Sequenced collections are introduced in Java 21 with the new _java.util.SequencedCollection <E>_ interface. A sequenced collection has a well-defined encounter order for its elements. Accordingly, the elements have a linear arrangement: first element, second element, …, and last element. With _java.util.Collection <E>_ as the root interface in the collection hierarchy, the _java.util.SequencedCollection <E>_ extends it to provide a sequential arrangement for a collection’s elements.

The _java.util.SequencedCollection <E>_ interface provides several methods for adding/getting/removing an element that’s either first or last in the sequence:

Method | Description  
---|---  
_addFirst(E e)_ | Adds an element as the first element  
_addLast(E e)_ | Adds an element as the last element  
_getFirst()_ | Gets the first element  
_getLast()_ | Gets the last element  
_removeFirst()_ | Removes and returns the first element  
_removeLast()_ | Removes and returns the last element  
  
Let’s discuss with examples how to perform the add/get/remove operations on an _ArrayList_ that’s a sequenced collection.

### 7.1. Getting First or Last Element

To get the first element, we call the instance method _getFirst()_. To demonstrate, let’s create an _ArrayList_ :
    
    
    ArrayList<Integer> arrayList = new ArrayList<Integer>(Arrays.asList(3,1,2));

We can use a JUnit 5 test with an _assertEquals_ assertion to verify the first element returned:
    
    
    @Test
    public void givenSequencedArrayList_whenGetFirst_thenFirstElementReturnedCorrectly() {
    
        ArrayList arrayList = new ArrayList(Arrays.asList(3,1,2));
    
        Integer expectedElement=3;
        assertEquals(expectedElement, arrayList.getFirst());
    }

The JUnit assertion test should pass. Similarly, to get the last element, we call the instance method _getLast()_. To demonstrate, let’s create an _ArrayList_ as before. Again, we can use a JUnit 5 test to verify the last element returned:
    
    
    @Test
    public void givenSequencedArrayList_whenGetLast_thenLastElementReturnedCorrectly() {
           
        ArrayList arrayList = new ArrayList(Arrays.asList(3,1,2));
    
        Integer expectedElement=2;
        assertEquals(expectedElement, arrayList.getLast());
    }

The JUnit assertion test should pass because the _getLast()_ returns the last element.

### 7.2. Adding First or Last Element

To add a new first element in an existing collection, we call the instance method _addFirst(E e)_. To demonstrate, let’s create an _ArrayList_ , and add a new first element:
    
    
    ArrayList<Integer> arrayList = new ArrayList<Integer>(Arrays.asList(3,1,2));
    arrayList.addFirst(4);

We can use a JUnit 5 test with an _assertEquals_ assertion to verify the first element added:
    
    
    @Test
    public void givenSequencedArrayList_whenAddFirst_thenFirstElementAddedCorrectly() {
    
        ArrayList arrayList = new ArrayList(Arrays.asList(3,1,2));
        arrayList.addFirst(4);
         
        Integer expectedElement=4;
        assertEquals(expectedElement, arrayList.getFirst());
    }

Similarly, to add the last element to an existing collection, we call the instance method _addLast(E e)_. Again, let’s create an _ArrayList_ and use a JUnit 5 test to verify the last element added:
    
    
    @Test
    public void givenSequencedArrayList_whenAddLast_thenLastElementAddedCorrectly() {
           
        ArrayList arrayList = new ArrayList(Arrays.asList(3,1,2));
        arrayList.addLast(5);
        
        Integer expectedElement=5;
        assertEquals(expectedElement, arrayList.getLast());
    }

The JUnit assertion test should pass because the _getLast()_ returns the last element added with _addLast(E e)_.

### 7.3. Removing First or Last Element

To remove the first element in an existing collection, we call the instance method _removeFirst()_. To demonstrate, let’s create an _ArrayList_ and remove the first element. We can use a JUnit 5 test with an _assertEquals_ assertion to verify the first element is removed:
    
    
    @Test
    public void givenSequencedArrayList_whenRemoveFirst_thenFirstElementRemovedCorrectly() {
    
        ArrayList arrayList = new ArrayList(Arrays.asList(3,1,2));
           
        Integer expectedElement=3;
        assertEquals(expectedElement, arrayList.removeFirst());
    }

Similarly, to remove the last element in an existing collection, we call the instance method _removeLast()_. Let’s create an _ArrayList_ and use a JUnit 5 test to verify the last element is removed:
    
    
    @Test
    public void givenSequencedArrayList_whenRemoveLast_thenLastElementRemovedCorrectly() {
           
        ArrayList arrayList = new ArrayList(Arrays.asList(3,1,2));
         
        Integer expectedElement=2;
        assertEquals(expectedElement, arrayList.removeLast());
    } 

The JUnit assertion test should pass because the _removeLast()_ returns the removed last element.

## **8\. Summary**

In this quick article, we had a look at the _ArrayList_ in Java.

We showed how to create an _ArrayList_ instance, and how to add, find, or remove elements using different approaches. Furthermore, we showed how to add, get, and remove the first, or the last element using sequenced collections introduced in Java 21.
