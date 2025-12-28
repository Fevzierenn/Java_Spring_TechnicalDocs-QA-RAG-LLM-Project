# Initializing Arrays in Java

## **1\. Overview**

An [array](/java-arrays-guide) is a data structure that allows us to store and manipulate a collection of elements of the same data type. **Arrays have a fixed size, determined during initialization, that cannot be altered during runtime**.

In this tutorial, we’ll see how to declare an array. Also, we’ll examine the different ways we can initialize an array and the subtle differences between them.

## 2\. Understanding Arrays

In Java, arrays are objects that can store multiple elements of the same data type. We can access all elements in an array through their indices, which are numerical positions starting from zero. Also, the length of an array represents the total number of elements it can hold:

[![Represenation of array element and indices](/wp-content/uploads/2017/10/array_reprsentation.png)](/wp-content/uploads/2017/10/array_reprsentation.png)

In the image above, we have a one-dimensional array of eight items.

Notably,**if we try to access an element outside the valid index range of the array, it throws[ _ArrayIndexOutOfBoundsException_](/java-arrayindexoutofboundsexception)**.

## 3\. Declaring and Initializing One-Dimensional Arrays

We can easily declare an array by **specifying its data type followed by square brackets and the array name** :
    
    
    int[] numbers;

In the code above, we declare an uninitialized array of _int_ type.

Alternatively, we can place the square brackets after the array name, but **this approach is less common** :
    
    
    int numbers[];

Furthermore, **we must initialize an array to use it**. Initialization involves allocating memory using the _new_ keyword and specifying the array length:
    
    
    var numbers = new int[7];

In the code above, we initialize a _numbers_ array to hold seven elements of _int_ type.

After initialization, we can assign values to individual elements using their indices:
    
    
    numbers[0] = 10;
    numbers[1] = 20;

Here, we add _10_ and _20_ to indices _0_ and _1_ , respectively.

Furthermore, we can retrieve an element value by using its index:
    
    
    assertEquals(20, numbers[1]);

In the code above, we assert that the element in index one is _20_.

**It’s possible to declare and initialize an array in a single step** :
    
    
    int[] numbers = new int[5];

Notably, the length of an array is always fixed and cannot be extended after initialization.

Alternatively, we can specify the length of an array using a variable:
    
    
    int length = 7;
    int[] numbers = new int[length];

Here, we declare a variable used as the length of the array. **Importantly,_length_ can only be of type **_**int**. _Any other type apart from _int_ throws an incompatible type error.

## 4\. Declare Array of Unknown Size

When we declare an array, knowing the size is unnecessary. We can either **assign an array to _null_ or an empty array**:
    
    
    int[] numbers = null;
    
    int[] numbers = new int[0];

But we **need to know the size when we initialize it** because the Java virtual machine must reserve the contiguous memory block for it. As we discussed earlier, we can initialize an array with the _new_ keyword:
    
    
    int[] numbers =  new int[5];

If we want to resize the array, we can do it by creating an array of larger size and copying the previous array elements to the new array:
    
    
    int newSize = 10; // New desired size
    int[] newArray = new int[newSize];
    
    // Copy elements from the old array to the new array
    System.arraycopy(numbers, 0, newArray, 0, numbers.length);
    
    numbers = newArray // reference to new array

If we’re allowed to use _ArrayList_ , then for dynamic resizing we should always use _ArrayList_ :
    
    
    // we can add elements dynamically without specifying the size
    List<Integer> numbers = new ArrayList<>();
    numbers.add(1);
    numbers.add(2);
    numbers.add(3);
    

_ArrayList_ internally uses an array and _System.arrayCopy()_ to support dynamic resizing.

## 5\. Default Values for Array Elements

Upon initialization, **the elements of an array are automatically assigned default values based on the data type of the array**. These values represent the array elements’ initial state before we explicitly assign any values.

Arrays of _int_ , _short_ , _long_ , _float_ , and _double_ data types set all elements to zero by default:
    
    
    int[] array = new int[5];
    assertArrayEquals(new int[] { 0, 0, 0, 0, 0 }, array);

Furthermore, for _boolean_ arrays, the default value for all elements is _false_ :
    
    
    boolean[] array = new boolean[5];
    assertArrayEquals(new boolean[] { false, false, false, false, false }, array);

Finally, for arrays of object types, such as _String_ , the default value for all elements is set to _null_ :
    
    
    String[] array = new String[5];
    assertArrayEquals(new String[] { null, null, null, null, null }, array);

Notably, when we use or access an element of an array without explicitly assigning a value, we are automatically using or accessing the default value.

## **6\. Initializing Arrays With Values**

Also, we can assign values to an array during initialization. **This is often called array literals** :
    
    
    String[] brand = new String[] { "Toyota", "Mercedes", "BMW", "Volkswagen", "Skoda" };

In the code above, we initialize a string array with five brand names. The total number of elements within the curly braces determines the length/size of the array.

Furthermore, we can omit the array type for primitive data types:
    
    
    int[] array = { 1, 2, 3, 4, 5 };

Additionally, **when using the _var_ keyword for type inference, we cannot initialize an array literal without the _new_ keyword**:
    
    
    var array = {1, 2, 3, 4, 5};

The code above results in a compilation error.

To use the _var_ keyword with array literals, we must introduce the _new_ keyword, allowing the compiler to infer the type from the right-hand side of the assignment:
    
    
    var arr = new int[]{1,2,3,4,5};

Here, the compiler can infer it’s an array of integers.

## **7\. Adding Values to Arrays Using _Arrays.fill()_**

The _java.util.Arrays_ class has several methods named _fill()_ that accept different types of arguments and fill the whole array with the same value:
    
    
    long array[] = new long[5];
    Arrays.fill(array, 30);

This method can be useful when we need to update multiple elements of an array with the same value.

The method also has several alternatives that set a given range of an array to a particular value:
    
    
    int[] array = new int[5];
    Arrays.fill(array, 0, 3, -50);

Here, the _fill()_ method accepts the initialized array, the index to start the filling, the index to end the filling (exclusive), and the value itself respectively as arguments. The first three elements of the array are set to -50 and the remaining elements retain their default value which is zero.

Notably, if the range between the start and the end index is greater than the size of the array, it throws _ArrayIndexOutOfBoundsException_.

## **8\. Copying Arrays Using _Arrays.copyOf()_**

The method _Arrays.copyOf()_ creates a new array by copying elements from an existing array. The method has many overloads, which accept different types of arguments.

Let’s see a quick example:
    
    
    int[] array = { 1, 2, 3, 4, 5 };
    int[] copy = Arrays.copyOf(array, 5);

There are a few things to note in this example:

  * The method accepts two arguments – the source array and the desired length of the new array to be created.
  * If the length is greater than the length of the array to be copied, then the extra elements will be initialized using their type’s default value.
  * If the source array hasn’t been initialized, then a _NullPointerException_ is thrown.



## **9\. Adding Values to Arrays Using _Arrays.setAll()_**

The method _Arrays.setAll()_ **sets all elements of an array using a generator function**. This method can be useful when we need to add values that follow a specific pattern or logic to an array.

Let’s see an example using the _Arrays.setAll()_ method:
    
    
    int[] numbers = new int[5];
    Arrays.setAll(numbers, i -> i * 2);
    assertArrayEquals(new int[] {0, 2, 4, 6, 8}, numbers);

In the code above, we create an array of _int_ data types and use the _setAll()_ method to populate it with even numbers.

Here’s another example that demonstrates a more complex generator function:
    
    
    int[] array = new int[20];
    Arrays.setAll(array, p -> p > 9 ? 0 : p);
    
    // [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

Here, the generator function sets the first ten elements of the array to their respective indices and sets the remaining elements to zero.

If the generator function is null, then a [_NullPointerException_](/java-avoid-null-check#NullPointer%20exception) is thrown.

## **10\. Cloning an Array Using _ArrayUtils.clone()_**

Let’s utilize the _ArrayUtils.clone()_ API **from Apache Commons Lang 3** , which initializes an array by creating a direct copy of another array:
    
    
    char[] array = new char[] {'a', 'b', 'c'};
    char[] copy = ArrayUtils.clone(array);

Note that **this method is overloaded for all primitive types**.

## 11\. Declaring and Initializing Two-Dimensional Arrays

Moreover, let’s see how to declare a two-dimensional array:
    
    
    int[][] matrix;

In the code above, we declare a two-dimensional array of _int_ data type by specifying two sets of square brackets. Let’s initialize the array and specify the number of rows and columns:
    
    
    matrix = new int[2][5];

We can think of this as an array with two rows and five columns.

Let’s assign value to the individual elements using nested indices, where **the first index represents the row and the second index represents the column** :
    
    
    matrix[0][0] = 10;
    matrix[0][1] = 20;
    matrix[0][2] = 30;
    matrix[0][3] = 40;
    matrix[0][4] = 50;
    matrix[1][0] = 60;
    matrix[1][1] = 70;
    matrix[1][2] = 80;
    matrix[1][3] = 90;
    matrix[1][4] = 100;

We can retrieve the value in a two-dimensional array by specifying its row and column indices:
    
    
    assertEquals(20, matrix[0][1]);

In the code above, we retrieve the value of an array at row _0_ and column _1_.

Alternatively, we can initialize a two-dimensional array using a less frequently used syntax:
    
    
    int[] array[] = new int[5][5];

Also, we can initialize a two-dimensional array with literals using nested curly brackets:
    
    
     int [][] twoDArray = { { 1, 2, 3 }, { 4, 5, 6 } };

In the code above, we initialized a two-dimensional array of _int_ type containing two one-dimensional arrays, which represent the two rows of our array.

## **12\. Adding Values to an Array Using a _for_ Loop**

We can assign values to each element of an array individually using a loop. This approach can be useful when we need to populate an array based on specific conditions or calculations.

Let’s look at an example that uses a loop-based approach:
    
    
    int[] array = new int [3];
    for (int i = 0; i < array.length; i++) {
        array[i] = i + 2;
    }

In the example above, we use a loop to assign values to each element. In this case, we assign the value _i + 2_ to the element at index _i_.

For [multi-dimensional](/java-jagged-arrays) arrays, we can use nested loops to iterate over each dimension and assign values to the elements:
    
    
    int[][] matrix = new int[3][4];
    for (int i = 0; i < matrix.length; i++) {
        for (int j = 0; j < matrix[i].length; j++) {
            matrix[i][j] = i * 4 + j;
        }
    }

Here, we use nested _for_ loops to iterate over the rows and columns, respectively. We assign each element the value _i * 4 + j_ , which is calculated based on the row and column indices.

## 13\. Initializing an Array Using the Stream API

The [Stream API](/java-8-streams) provides convenient methods for creating arrays from streams of elements, including methods such as _Arrays.stream()_ , _IntStream.of()_ , _DoubleStream.of()_ , and many others. These methods allow us to initialize arrays with specified values.

Let’s see an example that uses the _Instream.of()_ method to initialize and populate an array:
    
    
     int[] values = IntStream.of(1, 2, 3, 4, 5).toArray();

Here, we create an _IntStream_ with five values and use the _toArray()_ method to convert it to an array of integers.

Moreover, we can initialize a higher-dimensional array using the Stream API. Let’s use this approach to **initialize a two-dimensional array** :
    
    
    int[][] matrix = IntStream.range(0, 3)
      .mapToObj(i -> IntStream.range(0, 4).map(j -> i * 4 + j).toArray())
      .toArray(int[][]::new);

First, we generate a stream of integers using _IntStream.range(0, 3),_ corresponding to the indices of the rows in the _matrix_. Next, we use the _mapToObj()_ method to convert each integer in the original stream into an array of integers. Then, we generate another stream of integers corresponding to the indices of the columns in each row of our _matrix_.

Finally, we convert the stream of integer arrays into a two-dimensional array using the _toArray(int[][]::new)_ method, which is a method reference that creates a new two-dimensional array.

## 14\. Higher-Dimensional Arrays

Furthermore, we can have arrays of more than two dimensions. Depending on the specific use case, we can have a three-dimensional array, a four-dimensional array, and so on. The number of square brackets determines the dimensions.

Let’s see how to declare and initialize a three-dimensional array:
    
    
    int[][][] threeDArray = new int[3][4][5];

In the code above, we have three square brackets to indicate this is a three-dimensional array. **The first square bracket _[3]_ represents the depth of the array**. It indicates the number of two-dimensional arrays that the three-dimensional array contains. In this case, we have three two-dimensional arrays in the three-dimensional array.

Let’s add an element to the first 2D array:
    
    
    threeDArray[0][0][1] = 4;

Here, the first index _[0]_ indicates the first 2D array within the 3D array, the second index _[0]_ represents the first row of the first 2D array, and the third index _[1]_ represents the second column in the first column of the first 2D array.

Additionally, let’s add an element to the second 2D array:
    
    
    threeDArray[1][0][0] = 6;

First, we indicate the second 2D array via its index _[1]_. Then, we add an element to the first column of the first row of that 2D array.

**Simply put, a three-dimensional array is an array of two-dimensional arrays**.

Finally, a four-dimensional array is essentially an array of three-dimensional arrays.

## **15\. Conclusion**

In this article, we explored different ways of initializing arrays in Java. Also, we learned how to declare and allocate memory to arrays of any type, including one-dimensional and multi-dimensional arrays.

Additionally, we saw different ways to populate arrays with values, including assigning values individually using indices, and initializing arrays with values at the time of declaration.
