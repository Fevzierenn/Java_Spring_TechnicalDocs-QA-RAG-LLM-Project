# A Guide to HashSet in Java

## 1\. Overview

In this tutorial, we’ll explore _HashSet_ , one of the most popular _Set_ implementations and an integral part of the Java Collections Framework.

## 2\. Intro to _HashSet_

_HashSet_ is one of the fundamental data structures in the Java Collections API _._

Let’s recall the most important aspects of this implementation:

  * It stores unique elements and permits nulls
  * It’s backed by a _HashMap_
  * It doesn’t maintain insertion order
  * It’s not thread-safe



Note that this internal _HashMap_ gets initialized when an instance of the _HashSet_ is created:
    
    
    public HashSet() {
        map = new HashMap<>();
    }

If we want to go deeper into how the _HashMap_ works, we can read [the article focused on it here](/java-hashmap).

## 3\. The API

In this section, we’re going to review the most commonly used methods and have a look at some simple examples.

### 3.1. _add()_

The _add()_ method can be used for adding elements to a set. **The method contract states that an element will be added only when it isn’t already present in a set.** If an element was added, the method returns _true,_ otherwise – _false._

We can add an element to a _HashSet_ like:
    
    
    @Test
    public void whenAddingElement_shouldAddElement() {
        Set<String> hashset = new HashSet<>();
     
        assertTrue(hashset.add("String Added"));
    }

From an implementation perspective, the _add_ method is extremely important. Implementation details illustrate how the _HashSet_ works internally and leverages the _HashMap’s_ _put_ method:
    
    
    public boolean add(E e) {
        return map.put(e, PRESENT) == null;
    }

The _map_ variable is a reference to the internal, backing _HashMap:_
    
    
    private transient HashMap<E, Object> map;

It’d be a good idea to get familiar with the [_hashcode_](/java-hashcode) first to get a detailed understanding of how the elements are organized in hash-based data structures.

Summarizing:

  * A _HashMap_ is an array of _buckets_ with a default capacity of 16 elements – each bucket corresponds to a different hashcode value
  * If various objects have the same hashcode value, they get stored in a single bucket
  * If the _load factor_ is reached, a new array gets created twice the size of the previous one and all elements get rehashed and redistributed among new corresponding buckets
  * To retrieve a value, we hash a key, mod it, and then go to a corresponding bucket and search through the potential linked list in case of there’s more than a one object



### 3.2. _contains()_

**The purpose of the _contains_ method is to check if an element is present in a given _HashSet_. **It returns _true_ if the element is found, otherwise _false._

We can check for an element in the _HashSet_ :
    
    
    @Test
    public void whenCheckingForElement_shouldSearchForElement() {
        Set<String> hashsetContains = new HashSet<>();
        hashsetContains.add("String Added");
     
        assertTrue(hashsetContains.contains("String Added"));
    }

Whenever an object is passed to this method, the hash value gets calculated. Then, the corresponding bucket location gets resolved and traversed.

### 3.3._remove()_

The method removes the specified element from the set if it’s present. This method returns _true_ if a set contained the specified element.

Let’s see a working example:
    
    
    @Test
    public void whenRemovingElement_shouldRemoveElement() {
        Set<String> removeFromHashSet = new HashSet<>();
        removeFromHashSet.add("String Added");
     
        assertTrue(removeFromHashSet.remove("String Added"));
    }

### 3.4. _clear()_

We use this method when we intend to remove all the items from a set. The underlying implementation simply clears all elements from the underlying _HashMap._

Let’s see that in action:
    
    
    @Test
    public void whenClearingHashSet_shouldClearHashSet() {
        Set<String> clearHashSet = new HashSet<>();
        clearHashSet.add("String Added");
        clearHashSet.clear();
        
        assertTrue(clearHashSet.isEmpty());
    }

### 3.5. _size()_

This is one of the fundamental methods in the API. It’s used heavily as it helps in identifying the number of elements present in the _HashSet_. The underlying implementation simply delegates the calculation to the _HashMap’s size()_ method.

Let’s see that in action:
    
    
    @Test
    public void whenCheckingTheSizeOfHashSet_shouldReturnThesize() {
        Set<String> hashSetSize = new HashSet<>();
        hashSetSize.add("String Added");
        
        assertEquals(1, hashSetSize.size());
    }

### 3.6. _isEmpty()_

We can use this method to figure if a given instance of a _HashSet_ is empty or not. This method returns _true_ if the set contains no elements:
    
    
    @Test
    public void whenCheckingForEmptyHashSet_shouldCheckForEmpty() {
        Set<String> emptyHashSet = new HashSet<>();
        
        assertTrue(emptyHashSet.isEmpty());
    }

### 3.7. _iterator()_

The method returns an iterator over the elements in the _Set_. **The elements are visited in no particular order and iterators are fail-fast**.

We can observe the random iteration order here:
    
    
    @Test
    public void whenIteratingHashSet_shouldIterateHashSet() {
        Set<String> hashset = new HashSet<>();
        hashset.add("First");
        hashset.add("Second");
        hashset.add("Third");
        Iterator<String> itr = hashset.iterator();
        while(itr.hasNext()){
            System.out.println(itr.next());
        }
    }

**If the set is modified at any time after the iterator is created in any way except through the iterator’s own remove method, the _Iterator_ throws a _ConcurrentModificationException_.**

Let’s see that in action:
    
    
    @Test(expected = ConcurrentModificationException.class)
    public void whenModifyingHashSetWhileIterating_shouldThrowException() {
     
        Set<String> hashset = new HashSet<>();
        hashset.add("First");
        hashset.add("Second");
        hashset.add("Third");
        Iterator<String> itr = hashset.iterator();
        while (itr.hasNext()) {
            itr.next();
            hashset.remove("Second");
        }
    }
    

Alternatively, had we used the iterator’s remove method, then we wouldn’t have encountered the exception:
    
    
    @Test
    public void whenRemovingElementUsingIterator_shouldRemoveElement() {
     
        Set<String> hashset = new HashSet<>();
        hashset.add("First");
        hashset.add("Second");
        hashset.add("Third");
        Iterator<String> itr = hashset.iterator();
        while (itr.hasNext()) {
            String element = itr.next();
            if (element.equals("Second"))
                itr.remove();
        }
     
        assertEquals(2, hashset.size());
    }

**The fail-fast behavior of an iterator can’t be guaranteed as it’s impossible to make any hard guarantees in the presence of unsynchronized concurrent modification.**

Fail-fast iterators throw _ConcurrentModificationException_ on a best-effort basis. Therefore, it’d be wrong to write a program that depended on this exception for its correctness.

## 4\. How to Convert _HashSet_ to _TreeSet_ With an Object Collection

We can convert a _HashSet_ to a _TreeSet_ using the class constructor _TreeSet(Collection <? extends E> c)_. This creates a new _TreeSet_ object containing the elements in the collection passed to it, sorted according to the elements’ natural ordering.

Let’s demonstrate with an example how to convert a _HashSet_ comprised of elements, each of which is an object (instance of a class), to a _TreeSet_. We use an example class, _Employee_. This class should implement the _Comparable_ interface to convert a _HashSet_ with its elements derived from the class to a _TreeSet_. Accordingly, we override the _compareTo(Object)_ method in _Comparable_ to compare two _Employee_ objects based on their IDs:
    
    
    public class Employee implements Comparable {
        private int employeeId;
        private String employeeName;
    
        Employee(int employeeId, String employeeName) {
            this.employeeId = employeeId;
            this.employeeName = employeeName;
        }
    
        int getEmployeeId() {
            return employeeId;
        }
    
        public String getEmployeeName() {
            return employeeName;
        }
    
        @Override
        public String toString() {
            return employeeId + " " + employeeName;
        }
    
        @Override
        public int compareTo(Employee o) {
            if (this.employeeId == o.employeeId) {
                return 0;
            } else if (this.employeeId < o.employeeId) {
                return 1;
            } else {
                return -1;
            }
        }
    }

Moreover, having defined an object class, let’s create a _HashSet_ from it. Let’s use a JUnit 5 integration test that includes an _assertDoesNotThrow()_ assertion to verify the conversion doesn’t throw an exception:
    
    
    @Test
    public void givenComparableObject_whenConvertingToTreeSet_thenNoExceptionThrown() {
    
        HashSet hashSet = new HashSet();
            
        hashSet.add(new Employee(3, "John"));
        hashSet.add(new Employee(5, "Mike"));
        hashSet.add(new Employee(2, "Bob"));
        hashSet.add(new Employee(1, "Tom"));
        hashSet.add(new Employee(4, "Johnny"));  
            
        assertDoesNotThrow(()->{
            TreeSet treeSet=new TreeSet(hashSet);
        });
    }

The JUnit integration test should pass when we use the _Employee_ class that implements the _Comparable_ interface.

However, when we use an _Employee_ class definition that doesn’t implement the _Comparable_ interface to create a _HashSet_ instance, converting it to _TreeSet_ throws an exception. Again, we can use a JUnit 5 test to verify it:
    
    
    @Test
    public void givenNonComparableObject_whenConvertingToTreeSet_thenExceptionThrown() {
    
        HashSet hashSet = new HashSet();
            
        hashSet.add(new Employee(3, "John"));
        hashSet.add(new Employee(5, "Mike"));
        hashSet.add(new Employee(2, "Bob"));
        hashSet.add(new Employee(1, "Tom"));
        hashSet.add(new Employee(4, "Johnny"));  
            
        assertThrows(ClassCastException.class,() -> { 
            TreeSet treeSet = new TreeSet(hashSet); 
        });
    }

This time, the conversion throws the _ClassCastException.class_ exception type, and the _assertThrows()_ test passes.

## 5\. How Does _HashSet_ Maintain Uniqueness?

When we put an object into a _HashSet_ , it uses the object’s _hashcode_ value to determine if an element is not already in the set.

Each hash code value corresponds to a certain bucket location which can contain various elements, for which the calculated hash value is the same. **But two objects with the same _hashCode_ might not be equal**.

So, objects within the same bucket will be compared using the _equals()_ method.

## 6\. Performance of _HashSet_

The performance of a _HashSet_ is affected mainly by two parameters – its _Initial Capacity_ and the _Load Factor_.

The expected time complexity of adding an element to a set is _O(1)_ which can drop to _O(n)_ in the worst case scenario (only one bucket present) – therefore, **it’s essential to maintain the right _HashSet’s_ capacity.**

An important note: since JDK 8, [the worst case time complexity is _O(log*n)_.](http://openjdk.java.net/jeps/180)

The load factor describes what is the maximum fill level, above which, a set will need to be resized.

We can also create a _HashSet_ with custom values for _initial capacity_ and _load factor_ :
    
    
    Set<String> hashset = new HashSet<>();
    Set<String> hashset = new HashSet<>(20);
    Set<String> hashset = new HashSet<>(20, 0.5f);
    

In the first case, the default values are used – the initial capacity of 16 and the load factor of 0.75. In the second, we override the default capacity and in the third one, we override both.

**A low initial capacity reduces space complexity but increases the frequency of rehashing which is an expensive process.**

On the other hand, **a high initial capacity increases the cost of iteration and the initial memory consumption.  
**

As a rule of thumb:

  * A high initial capacity is good for a large number of entries coupled with little to no iteration
  * A low initial capacity is good for a few entries with a lot of iteration



It’s, therefore, very important to strike the correct balance between the two. Usually, the default implementation is optimized and works just fine, should we feel the need to tune these parameters to suit the requirements, we need to do judiciously.

## 7\. Conclusion

In this article, we outlined the utility of a _HashSet_ , its purpose as well as its underlying working. We saw how efficient it is in terms of usability given its constant time performance and ability to avoid duplicates.

We studied some of the important methods from the API and how they can help us as a developer to use a HashSet to its potential.
