# A Guide to the Java LinkedList

## 1\. Introduction

_[LinkedList](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/LinkedList.html)_ is a doubly-linked list implementation of the _[List](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/List.html)_ and _[Deque](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/Iterator.html)_ interfaces. It implements all optional list operations and permits all elements (including _null_).

## 2\. Features

Below you can find the most important properties of the _LinkedList_ :

  * Operations that index into the list will traverse the list from the beginning or the end, whichever is closer to the specified index
  * It is not [synchronized](http://stackoverflow.com/a/1085745/2486904)
  * Its _[Iterator](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/Iterator.html)_ and _[ListIterator](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/ListIterator.html)_ iterators are [fail-fast](http://stackoverflow.com/questions/17377407/what-is-fail-safe-fail-fast-iterators-in-java-how-they-are-implemented) (which means that after the iterator’s creation, if the list is modified, a _[ConcurrentModificationException](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/ConcurrentModificationException.html)_ will be thrown)
  * Every element is a node, which keeps a reference to the next and previous ones
  * It maintains insertion order



Although _LinkedList_ is not synchronized, we can retrieve a synchronized version of it by calling the _[Collections.synchronizedList](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/Collections.html#synchronizedList\(java.util.List\))_ method, like:
    
    
    List list = Collections.synchronizedList(new LinkedList(...));

## 3\. Comparison to _ArrayList_

Although both of them implement the _List_ interface, they have different semantics – which will definitely affect the decision of which one to use.

### **3.1. Structure**

An _ArrayList_ is an index-based data structure backed by an _Array_. It provides random access to its elements with a performance equal to O(1).

On the other hand, a _LinkedList_ stores its data as a list of elements, and every element is linked to its previous and next element. In this case, the search operation for an item has execution time equal to O(n).

### **3.2. Operations**

The insertion, addition and removal operations of an item are faster in a _LinkedList_ because there is no need to resize an array or update the index when an element is added to some arbitrary position inside the collection, only references in surrounding elements will change.

### **3.3. Memory Usage**

A _LinkedList_ consumes more memory than an _ArrayList_ because of every node in a _LinkedList_ stores two references, one for its previous element and one for its next element, whereas _ArrayList_ holds only data and its index.

## 4\. Different Methods to Initialize a _LinkedList_

We can initialize a _LinkedList_ using one of two constructors. Further, we use constructors to initialize new instances of a class.

### 4.1. Initializing an Empty _LinkedList_

We use the empty _LinkedList()_ constructor to initialize an empty _LinkedList._

Let’s demonstrate an example of a _LinkedList_ parameterized over _String_ using [generics](/java-generics).

Let’s use a JUnit 5 test to verify the empty _LinkedList_ :
    
    
    @Test
    public void whenInitializingLinkedList_ShouldReturnEmptyList() throws Exception {
        LinkedList<String> linkedList=new LinkedList<String>();     
        Assertions.assertTrue(linkedList.isEmpty());
    }

Accordingly, we can add _String_ elements to this list:
    
    
    linkedList.addFirst("one");
    linkedList.add("two");
    linkedList.add("three");

Likewise, we can initialize a _LinkedList_ of any class type.

### 4.2. Initializing a _LinkedList_ From a Collection

We can also use the _LinkedList(Collection <? extends E> c)_ constructor when we want to initialize a _LinkedList_ whose elements are the elements of a given _Collection_. It adds the elements in the order in which the  _Collection_ ‘s iterator returns them.

Let’s demonstrate an example of a _LinkedList_ parameterized over _Integer_ using generics. However, first, we create a _Collection_ to use as the argument when we invoke the constructor. Let’s create a _Collection_ of type _ArrayList_ parameterized over _Integer_ using generics:
    
    
    ArrayList<Integer> arrayList = new ArrayList<Integer>(3);
    
     arrayList.add(Integer.valueOf(1));
     arrayList.add(Integer.valueOf(2));
     arrayList.add(Integer.valueOf(3));

Afterward, let’s call the constructor to initialize a _LinkedList_ :
    
    
    LinkedList<Integer> linkedList=new LinkedList<Integer>(arrayList);

Again, let’s use a JUnit 5 test to verify the _LinkedList_ derives its elements from the _ArrayList_ it is constructed from:
    
    
    @Test
    public void whenInitializingListFromCollection_ShouldReturnCollectionsElements() throws Exception {
        ArrayList<Integer> arrayList=new ArrayList<Integer>(3);
            
        arrayList.add(Integer.valueOf(1));
        arrayList.add(Integer.valueOf(2));
        arrayList.add(Integer.valueOf(3));
     
        LinkedList<Integer> linkedList=new LinkedList<Integer>(arrayList);
    
        Object[] linkedListElements = linkedList.toArray();
        Object[] collectionElements = arrayList.toArray();
    
        Assertions.assertArrayEquals(linkedListElements,collectionElements);
    }

Similarly, we can initialize _LinkedList_ using any Java _Collection_. Accordingly, the elements of the _LinkedList_ initialized from a _Collection_ are the type of the _Collection_ ‘s elements.

## 5\. Usage

Here are some code samples that show how you can use _LinkedList_ :

### **5.1. Creation**
    
    
    LinkedList<Object> linkedList = new LinkedList<>();

### **5.2. Adding Element**

_LinkedList_ implements _List_ and _Deque_ interface, besides standard _add()_ and _addAll()_ methods you can find _addFirst()_ and _addLast()_ , which adds an element in the beginning or the end, respectively.

### **5.3. Removing Element**

Similar to element addition, this list implementation offers _removeFirst()_ and _removeLast().  
_

Also, there are convenient methods, such as _removeFirstOccurence()_ and _removeLastOccurence()_ , which return a _boolean_ (true if the collection contained the specified element).

### **5.4. Queue Operations**

_Deque_ interface provides queue-like behaviors (actually, _Deque_ extends _Queue_ interface):
    
    
    linkedList.poll();
    linkedList.pop();

Those methods retrieve the first element and remove it from the list.

The difference between _poll()_ and _pop()_ is that _pop_ will throw _NoSuchElementException()_ on empty list, whereas _poll_ returns null. The APIs _pollFirst()_ and _pollLast()_ are also available.

Here’s, for example, how the _push_ API works:
    
    
    linkedList.push(Object o);

Which inserts the element as the head of the collection.

_LinkedList_ has many other methods, most of which should be familiar to a user who already used _Lists_. Others that are provided by _Deque_ might be a convenient alternative to “standard” methods.

The full documentation can be found [here](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/LinkedList.html).

## 6\. Insert an Element at a Specific Position in a _LinkedList_

When we want to add an element at a specific position in a _LinkedList_ , we have several method options:

Method | Description  
---|---  
_addFirst(E e)_ | Adds an element at the beginning of a list  
_addLast(E e)_ | Adds an element at the end of a list  
_add(E e)_ | Adds an element at the end of a list  
_add(int index, E element)_ | Adds an element at index position _i_ of a list  
  
Let’s demonstrate using each of these methods. Further, let’s initialize an empty list:
    
    
    LinkedList<String> linkedList=new LinkedList<String>();

Afterward, let’s add the first element using the method _addFirst(E e)_ :
    
    
    linkedList.addFirst("one");

Although we can build the list by repeatedly calling the _add(E e)_ method, we want to demonstrate the different options for adding an element at a specific position. Therefore, let’s add the last element in the list using the method _addLast(E e)_ :
    
    
    linkedList.addLast("three");

Let’s call the _add(E e)_ method to add an element to the end of the list built so far:
    
    
    linkedList.add("four");

A _LinkedList_ uses a  _0-_ based index, which means that the first element is at index _0_ , the second element at index _1_ , the third element at index _2_ , and so on. To create a sequence, let’s add the element “two” at index position _1_ using _add(int index, E element)_ :
    
    
    linkedList.add(1,"two");

Let’s use a JUnit 5 test to verify we added the elements in the _LinkedList_ at specific, respective positions:
    
    
    @Test
    public void whenAddingElementsInLinkedListAtSpecificPosition_ShouldReturnElementsInProperSequence() throws Exception {
        LinkedList<String> linkedList=new LinkedList<String>();
            
        linkedList.addFirst("one");
        linkedList.addLast("three");
        linkedList.add("four");
        linkedList.add(1,"two");
    
        Object[] linkedListElements = linkedList.toArray();
        Object[] expectedListElements = {"one","two","three","four"};
    
        Assertions.assertArrayEquals(linkedListElements,expectedListElements);
    }

The JUnit test should pass, verifying that we added elements at specific positions in a _LinkedList_.

## 7\. Converting an Array into a _LinkedList_

In some cases, we may have data in the form of an array, and we need to work with it as a _LinkedList_ for efficient insertions or to take advantage of the _Deque_ operations that _LinkedList_ provides. Converting an array to a _LinkedList_ is straightforward in Java.

First, let’s start with a sample array of elements:
    
    
    String[] array = { "apple", "banana", "cherry", "date" };

We can convert this array into a _LinkedList_ by **passing it to the _Arrays.asList()_ method and then creating a new _LinkedList_ from the resulting _List_** :
    
    
    List<String> list = Arrays.asList(array);  // Convert array to List
    LinkedList<String> linkedList = new LinkedList<>(list);

Now _linkedList_ contains all the elements from the original array, and we can use any of the _LinkedList_ operations on it.

Another approach to convert an array into a _LinkedList_ is by **using the _Collections.addAll()_ method**. This method provides a simple way to add all elements from an array directly into a _LinkedList_.

First, we create an empty _LinkedList_. Then we use the _Collections.addAll()_ method to add each element from the array into the _LinkedList_ :
    
    
    LinkedList<String> linkedList = new LinkedList<>();
    Collections.addAll(linkedList, array);

After this operation, _linkedList_ contains all the elements from the array and it preserves the order.

## 8\. Conclusion

_ArrayList_ is usually the default _List_ implementation.

However, there are certain use cases where using _LinkedList_ will be a better fit, such as preferences for constant insertion/deletion time (e.g., frequent insertions/deletions/updates), over constant access time and effective memory usage.
