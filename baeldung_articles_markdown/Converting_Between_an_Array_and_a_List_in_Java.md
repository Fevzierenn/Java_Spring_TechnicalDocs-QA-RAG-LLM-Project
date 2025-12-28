# Converting Between an Array and a List in Java

## **1\. Overview**

In this quick tutorial, we’re going to learn how to **convert between an Array and a List** using core Java libraries, Guava and Apache Commons Collections.

This article is part of the [“Java – Back to Basic” series](/java-tutorial "The Java Guide on IO and Collections") here on Baeldung.

## **2\. Convert _List_ to Array**

### **2.1. Using Plain Java**

Let’s start with the conversion from _List_ to Array **using plain Java** :
    
    
    @Test
    public void givenUsingCoreJava_whenListConvertedToArray_thenCorrect() {
        List<Integer> sourceList = Arrays.asList(0, 1, 2, 3, 4, 5);
        Integer[] targetArray = sourceList.toArray(new Integer[0]);
    }

Note that the preferred way for us to use the method is _toArray(new T[0])_ versus _toArray(new T[size])_. As Aleksey Shipilëv proves in his [blog post](https://shipilev.net/blog/2016/arrays-wisdom-ancients/#_conclusion), it seems faster, safer, and cleaner.

### **2.2. Using Guava**

Now let’s use **the Guava API** for the same conversion:
    
    
    @Test
    public void givenUsingGuava_whenListConvertedToArray_thenCorrect() {
        List<Integer> sourceList = Lists.newArrayList(0, 1, 2, 3, 4, 5);
        int[] targetArray = Ints.toArray(sourceList);
    }

## **3\. Convert Array to _List_**

### **3.1. Using Plain Java**

Let’s start with the plain Java solution for converting the array to a _List_ :
    
    
    @Test
    public void givenUsingCoreJava_whenArrayConvertedToList_thenCorrect() {
        Integer[] sourceArray = { 0, 1, 2, 3, 4, 5 };
        List<Integer> targetList = Arrays.asList(sourceArray);
    }

Note that this is a fixed-sized list that will still be backed by the array. If we want a standard _ArrayList,_ we can simply instantiate one:
    
    
    List<Integer> targetList = new ArrayList<Integer>(Arrays.asList(sourceArray));

### **3.2. Using Guava**

Now let’s use **the Guava API** for the same conversion:
    
    
    @Test
    public void givenUsingGuava_whenArrayConvertedToList_thenCorrect() {
        Integer[] sourceArray = { 0, 1, 2, 3, 4, 5 };
        List<Integer> targetList = Lists.newArrayList(sourceArray);
    }
    

### **3.3. Using Commons Collections**

Finally, let’s use the [Apache Commons Collections](http://commons.apache.org/proper/commons-collections/javadocs/) _CollectionUtils.addAll_ API to fill in the elements of the array in an empty List:
    
    
    @Test 
    public void givenUsingCommonsCollections_whenArrayConvertedToList_thenCorrect() { 
        Integer[] sourceArray = { 0, 1, 2, 3, 4, 5 }; 
        List<Integer> targetList = new ArrayList<>(6); 
        CollectionUtils.addAll(targetList, sourceArray); 
    }

## **4\. Conclusion**
