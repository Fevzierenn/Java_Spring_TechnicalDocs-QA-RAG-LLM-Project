# Guide to the java.util.Arrays Class

## **1\. Introduction**

In this tutorial, we’ll take a look at _java.util.Arrays_ , a utility class that has been part of Java since Java 1.2.

Using  _Arrays,_ we can create, compare, sort, search, stream, and transform arrays.

## **2\. Creating**

Let’s take a look at some of the ways we can create arrays:  _copyOf_ , _copyOfRange_ , and _fill._

### **2.1.****_copyOf_ and  _copyOfRange_**

To use _copyOfRange_ , we need our original array and the beginning index (inclusive) and end index (exclusive) that we want to copy:
    
    
    String[] intro = new String[] { "once", "upon", "a", "time" };
    String[] abridgement = Arrays.copyOfRange(storyIntro, 0, 3); 
    
    assertArrayEquals(new String[] { "once", "upon", "a" }, abridgement); 
    assertFalse(Arrays.equals(intro, abridgement));

And to use  _copyOf_ , we’d take _intro_ and a target array size and we’d get back a new array of that length:
    
    
    String[] revised = Arrays.copyOf(intro, 3);
    String[] expanded = Arrays.copyOf(intro, 5);
    
    assertArrayEquals(Arrays.copyOfRange(intro, 0, 3), revised);
    assertNull(expanded[4]);

Note that **_copyOf_ pads the array with  _null_ s if our target size is bigger than the original size.**

### **2.2._fill_**

Another way, we can create a fixed-length array, is _fill,_ which is useful when we want an array where all elements are the same:
    
    
    String[] stutter = new String[3];
    Arrays.fill(stutter, "once");
    
    assertTrue(Stream.of(stutter)
      .allMatch(el -> "once".equals(el));

**Check out _setAll_ to create an array where the elements are different.**

Note that we need to instantiate the array ourselves beforehand–as opposed to something like  _String[] filled = Arrays.fill(“once”_ , 3)_;_ –since this feature was introduced before generics were available in the language.

## **3\. Comparing**

Now let’s switch to methods for comparing arrays.

### **3.1._equals_ and  _deepEquals_**

We can use  _equals_ for simple array comparison by size and contents. If we add a null as one of the elements, the content check fails:
    
    
    assertTrue(
      Arrays.equals(new String[] { "once", "upon", "a", "time" }, intro));
    assertFalse(
      Arrays.equals(new String[] { "once", "upon", "a", null }, intro));

When we have nested or multi-dimensional arrays, we can use _deepEquals_ to not only check the top-level elements but also perform the check recursively:
    
    
    Object[] story = new Object[] 
      { intro, new String[] { "chapter one", "chapter two" }, end };
    Object[] copy = new Object[] 
      { intro, new String[] { "chapter one", "chapter two" }, end };
    
    assertTrue(Arrays.deepEquals(story, copy));
    assertFalse(Arrays.equals(story, copy));

Note how _deepE_ _quals_ passes but  _equals_ fails _._

**This is because _deepEquals_ ultimately calls itself each time it encounters an array**, while  _equals_ will simply compare sub-arrays’ references.

**Also, this makes it dangerous to call on an array with a self-reference!**

### **3.2._hashCode_ and  _deepHashCode_**

The implementation of  _hashCode_ will give us the other part of the  _equals_ /_hashCode_ contract that is recommended for Java objects. We use _hashCode_ to compute an integer based on the contents of the array:
    
    
    Object[] looping = new Object[]{ intro, intro }; 
    int hashBefore = Arrays.hashCode(looping);
    int deepHashBefore = Arrays.deepHashCode(looping);

Now, we set an element of the original array to null and recompute the hash values:
    
    
    intro[3] = null;
    int hashAfter = Arrays.hashCode(looping);
    

Alternatively,  _deepHashCode_ checks the nested arrays for matching numbers of elements and contents. If we recalculate with  _deepHashCode_ :
    
    
    int deepHashAfter = Arrays.deepHashCode(looping);

Now, we can see the difference in the two methods:
    
    
    assertEquals(hashAfter, hashBefore);
    assertNotEquals(deepHashAfter, deepHashBefore);
    

**_deepHashCode_ is the underlying calculation used when we are working with data structures like  _HashMap_ and  _HashSet_ on arrays**.

## **4\. Sorting and Searching**

Next, let’s take a look at sorting and searching arrays.

### **4.1._sort_**

If our elements are either primitives or they implement _Comparable_ , we can use  _sort_ to perform an in-line sort:
    
    
    String[] sorted = Arrays.copyOf(intro, 4);
    Arrays.sort(sorted);
    
    assertArrayEquals(
      new String[]{ "a", "once", "time", "upon" }, 
      sorted);

**Take care that _sort_ mutates the original reference**, which is why we perform a copy here.

_sort_ will use a different algorithm for different array element types. [Primitive types use a dual-pivot quicksort](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/Arrays.html#sort\(byte%5B%5D\)) and [Object types use Timsort](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/Arrays.html#sort\(java.lang.Object%5B%5D\)). Both have the average case of  _O(n log(n))_ for a randomly-sorted array.

As of Java 8,  _parallelSort_ is available for a parallel sort-merge. It offers a concurrent sorting method using several  _Arrays.sort_ tasks.

### **4.2._binarySearch_**

Searching in an unsorted array is linear, but if we have a sorted array, then we can do it in _O(log n)_ , which is what we can do with  _binarySearch:_
    
    
    int exact = Arrays.binarySearch(sorted, "time");
    int caseInsensitive = Arrays.binarySearch(sorted, "TiMe", String::compareToIgnoreCase);
    
    assertEquals("time", sorted[exact]);
    assertEquals(2, exact);
    assertEquals(exact, caseInsensitive);

If we don’t provide a  _Comparator_ as a third parameter, then  _binarySearch_ counts on our element type being of type  _Comparable_.

And again, note that **if our array isn’t first sorted, then _binarySearch_ won’t work as we expect!**

## **5\. Streaming**

As we saw earlier,  _Arrays_ was updated in Java 8 to include methods using the Stream API such as _parallelSort_ (mentioned above),  _stream_ and  _setAll._

### **5.1._stream_**

_stream_ gives us full access to the Stream API for our array:
    
    
    Assert.assertEquals(Arrays.stream(intro).count(), 4);
    
    exception.expect(ArrayIndexOutOfBoundsException.class);
    Arrays.stream(intro, 2, 1).count();

We can provide inclusive and exclusive indices for the stream however we should expect an  _ArrayIndexOutOfBoundsException_ if the indices are out of order, negative, or out of range.

## **6\. Transforming**

Finally,  _toString,_  _asList,_ and  _setAll_ give us a couple different ways to transform arrays.

### **6.1.****_toString_ and  _deepToString_**

A great way we can get a readable version of our original array is with  _toString:_
    
    
    assertEquals("[once, upon, a, time]", Arrays.toString(storyIntro));
    

Again **we must use the deep version to print the contents of nested arrays** :
    
    
    assertEquals(
      "[[once, upon, a, time], [chapter one, chapter two], [the, end]]",
      Arrays.deepToString(story));

### **6.2._asList_**

Most convenient of all the _Arrays_ methods for us to use is the _asList._ We have an easy way to turn an array into a list:
    
    
    List<String> rets = Arrays.asList(storyIntro);
    
    assertTrue(rets.contains("upon"));
    assertTrue(rets.contains("time"));
    assertEquals(rets.size(), 4);

However, **the returned _List_ will be a fixed length so we won’t be able to add or remove elements**.

Note also that, curiously, ** _java.util.Arrays_ has its own  _ArrayList_ subclass, which  _asList_ returns**. This can be very deceptive when debugging!

### **6.3._setAll_**

With _setAll_ , we can set all of the elements of an array with a functional interface. The generator implementation takes the positional index as a parameter:
    
    
    String[] longAgo = new String[4];
    Arrays.setAll(longAgo, i -> this.getWord(i)); 
    assertArrayEquals(longAgo, new String[]{"a","long","time","ago"});

And, of course, exception handling is one of the more dicey parts of using lambdas. So remember that here, **if the lambda throws an exception, then Java doesn’t define the final state of the array.**

## 7\. Parallel Prefix

Another new method in  _Arrays_ introduced since Java 8 is _parallelPrefix_. With _parallelPrefix_ , we can operate on each element of the input array in a cumulative fashion.

### **7.1._parallelPrefix_**

If the operator performs addition like in the following sample, _[1, 2, 3, 4]_ will result in _[1, 3, 6, 10]:_
    
    
    int[] arr = new int[] { 1, 2, 3, 4};
    Arrays.parallelPrefix(arr, (left, right) -> left + right);
    assertThat(arr, is(new int[] { 1, 3, 6, 10}));

Also, we can specify a subrange for the operation:
    
    
    int[] arri = new int[] { 1, 2, 3, 4, 5 };
    Arrays.parallelPrefix(arri, 1, 4, (left, right) -> left + right);
    assertThat(arri, is(new int[] { 1, 2, 5, 9, 5 }));

Notice that the method is performed in parallel, so **the cumulative operation should be side-effect-free and[associative](https://en.wikipedia.org/wiki/Associative_property)**.

For a non-associative function:
    
    
    int nonassociativeFunc(int left, int right) {
        return left + right*left;
    }

using _parallelPrefix_ would yield inconsistent results:
    
    
    @Test
    public void whenPrefixNonAssociative_thenError() {
        boolean consistent = true;
        Random r = new Random();
        for (int k = 0; k < 100_000; k++) {
            int[] arrA = r.ints(100, 1, 5).toArray();
            int[] arrB = Arrays.copyOf(arrA, arrA.length);
    
            Arrays.parallelPrefix(arrA, this::nonassociativeFunc);
    
            for (int i = 1; i < arrB.length; i++) {
                arrB[i] = nonassociativeFunc(arrB[i - 1], arrB[i]);
            }
    
            consistent = Arrays.equals(arrA, arrB);
            if(!consistent) break;
        }
        assertFalse(consistent);
    }

### **7.2. Performance**

Parallel prefix computation is usually more efficient than sequential loops, especially for large arrays. When running micro-benchmark on an Intel Xeon machine(6 cores) with [JMH](/java-microbenchmark-harness), we can see a great performance improvement:
    
    
    Benchmark                      Mode        Cnt       Score   Error        Units
    largeArrayLoopSum             thrpt         5        9.428 ± 0.075        ops/s
    largeArrayParallelPrefixSum   thrpt         5       15.235 ± 0.075        ops/s
    
    Benchmark                     Mode         Cnt       Score   Error        Units
    largeArrayLoopSum             avgt          5      105.825 ± 0.846        ops/s
    largeArrayParallelPrefixSum   avgt          5       65.676 ± 0.828        ops/s

Here is the benchmark code:
    
    
    @Benchmark
    public void largeArrayLoopSum(BigArray bigArray, Blackhole blackhole) {
      for (int i = 0; i < ARRAY_SIZE - 1; i++) {
        bigArray.data[i + 1] += bigArray.data[i];
      }
      blackhole.consume(bigArray.data);
    }
    
    @Benchmark
    public void largeArrayParallelPrefixSum(BigArray bigArray, Blackhole blackhole) {
      Arrays.parallelPrefix(bigArray.data, (left, right) -> left + right);
      blackhole.consume(bigArray.data);
    }

## **7\. Conclusion**

In this article, we learned how some methods for creating, searching, sorting and transforming arrays using the _java.util.Arrays_ class.

This class has been expanded in more recent Java releases with the inclusion of stream producing and consuming methods in [Java 8](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/Arrays.html) and mismatch methods in [Java 9](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/Arrays.html).
