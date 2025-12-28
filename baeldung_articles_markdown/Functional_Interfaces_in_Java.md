# Functional Interfaces in Java

## **1\. Introduction**

This tutorial is a guide to different functional interfaces present in Java 8, as well as their general use cases, and usage in the standard JDK library.

## **2\. Lambdas in Java 8**

Java 8 brought a powerful new syntactic improvement in the form of lambda expressions. A lambda is an anonymous function that we can handle as a first-class language citizen. For instance, we can pass it to or return it from a method.

Before Java 8, we would usually create a class for every case where we needed to encapsulate a single piece of functionality. This implied a lot of unnecessary boilerplate code to define something that served as a primitive function representation.

The article [“Lambda Expressions and Functional Interfaces: Tips and Best Practices”](/java-8-lambda-expressions-tips) describes in more detail the functional interfaces and best practices of working with lambdas. This guide focuses on some particular functional interfaces that are present in the _java.util.function_ package.

## **3\. Functional Interfaces**

It’s recommended that all functional interfaces have an informative _@FunctionalInterface_ annotation. This clearly communicates the purpose of the interface, and also allows a compiler to generate an error if the annotated interface does not satisfy the conditions.

**Any interface with a SAM(Single Abstract Method) is a functional interface** , and its implementation may be treated as lambda expressions.

Note that Java 8’s _default_ methods are not _abstract_ and do not count; a functional interface may still have multiple _default_ methods. We can observe this by looking at the _Function’s_ [documentation](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/function/Function.html).

## **4\. Functions**

The most simple and general case of a lambda is a functional interface with a method that receives one value and returns another. This function of a single argument is represented by the _Function_ interface, which is parameterized by the types of its argument and a return value:
    
    
    public interface Function<T, R> { … }

One of the usages of the _Function_ type in the standard library is the _Map.computeIfAbsent_ method. This method returns a value from a map by key, but calculates a value if a key is not already present in a map. To calculate a value, it uses the passed Function implementation:
    
    
    Map<String, Integer> nameMap = new HashMap<>();
    Integer value = nameMap.computeIfAbsent("John", s -> s.length());

In this case, we will calculate a value by applying a function to a key, put inside a map, and also returned from a method call. **W****e may replace the lambda with a method reference that matches passed and returned value types**.

Remember that an object we invoke the method on is, in fact, the implicit first argument of a method. This allows us to cast an instance method _length_ reference to a _Function_ interface:
    
    
    Integer value = nameMap.computeIfAbsent("John", String::length);

The _Function_ interface also has a default _compose_ method that allows us to combine several functions into one and execute them sequentially:
    
    
    Function<Integer, String> intToString = Object::toString;
    Function<String, String> quote = s -> "'" + s + "'";
    
    Function<Integer, String> quoteIntToString = quote.compose(intToString);
    
    assertEquals("'5'", quoteIntToString.apply(5));

The _quoteIntToString_ function is a combination of the _quote_ function applied to a result of the _intToString_ function.

## **5\. Primitive Function Specializations**

Since a primitive type can’t be a generic type argument, there are versions of the _Function_ interface for the most used primitive types _double_ ,_int_ , _long_ , and their combinations in argument and return types:

  * _IntFunction_ , _LongFunction_ , _DoubleFunction:_ arguments are of specified type, return type is parameterized
  * _ToIntFunction_ , _ToLongFunction_ , _ToDoubleFunction:_ return type is of specified type, arguments are parameterized
  * _DoubleToIntFunction_ , _DoubleToLongFunction_ , _IntToDoubleFunction_ , _IntToLongFunction_ , _LongToIntFunction_ , _LongToDoubleFunction:_ having both argument and return type defined as primitive types, as specified by their names



As an example, there is no out-of-the-box functional interface for a function that takes a _short_ and returns a _byte_ , but nothing stops us from writing our own:
    
    
    @FunctionalInterface
    public interface ShortToByteFunction {
    
        byte applyAsByte(short s);
    
    }

Now we can write a method that transforms an array of _short_ to an array of _byte_ using a rule defined by a _ShortToByteFunction_ :
    
    
    public byte[] transformArray(short[] array, ShortToByteFunction function) {
        byte[] transformedArray = new byte[array.length];
        for (int i = 0; i < array.length; i++) {
            transformedArray[i] = function.applyAsByte(array[i]);
        }
        return transformedArray;
    }

Here’s how we could use it to transform an array of shorts to an array of bytes multiplied by 2:
    
    
    short[] array = {(short) 1, (short) 2, (short) 3};
    byte[] transformedArray = transformArray(array, s -> (byte) (s * 2));
    
    byte[] expectedArray = {(byte) 2, (byte) 4, (byte) 6};
    assertArrayEquals(expectedArray, transformedArray);

## **6\. Two-Arity Function Specializations**

To define lambdas with two arguments, we have to use additional interfaces that contain “ _Bi”_ keyword in their names: _BiFunction_ , _ToDoubleBiFunction_ , _ToIntBiFunction_ , and _ToLongBiFunction_.

_BiFunction_ has both arguments and a return type generified, while _ToDoubleBiFunction_ and others allow us to return a primitive value.

One of the typical examples of using this interface in the standard API is in the _Map.replaceAll_ method, which allows replacing all values in a map with some computed value.

Let’s use a _BiFunction_ implementation that receives a key and an old value to calculate a new value for the salary and return it.
    
    
    Map<String, Integer> salaries = new HashMap<>();
    salaries.put("John", 40000);
    salaries.put("Freddy", 30000);
    salaries.put("Samuel", 50000);
    
    salaries.replaceAll((name, oldValue) -> 
      name.equals("Freddy") ? oldValue : oldValue + 10000);

## **7\. Suppliers**

The _Supplier_ functional interface is yet another _Function_ specialization that does not take any arguments. We typically use it for lazy generation of values. For instance, let’s define a function that squares a _double_ value. It will not receive a value itself, but a _Supplier_ of this value:
    
    
    public double squareLazy(Supplier<Double> lazyValue) {
        return Math.pow(lazyValue.get(), 2);
    }

This allows us to lazily generate the argument for invocation of this function using a _Supplier_ implementation. This can be useful if the generation of the argument takes a considerable amount of time. We’ll simulate that using Guava’s _sleepUninterruptibly_ method:
    
    
    Supplier<Double> lazyValue = () -> {
        Uninterruptibles.sleepUninterruptibly(1000, TimeUnit.MILLISECONDS);
        return 9d;
    };
    
    Double valueSquared = squareLazy(lazyValue);

Another use case for the _Supplier_ is defining logic for sequence generation. To demonstrate it, let’s use a static _Stream.generate_ method to create a _Stream_ of Fibonacci numbers:
    
    
    int[] fibs = {0, 1};
    Stream<Integer> fibonacci = Stream.generate(() -> {
        int result = fibs[1];
        int fib3 = fibs[0] + fibs[1];
        fibs[0] = fibs[1];
        fibs[1] = fib3;
        return result;
    });

The function that we pass to the _Stream.generate_ method implements the _Supplier_ functional interface. Notice that to be useful as a generator, the _Supplier_ usually needs some sort of external state. In this case, its state comprises the last two Fibonacci sequence numbers.

To implement this state, we use an array instead of a couple of variables because **all external variables used inside the lambda have to be effectively final**.

Other specializations of the _Supplier_ functional interface include _BooleanSupplier_ , _DoubleSupplier_ , _LongSupplier_ and _IntSupplier_ , whose return types are corresponding primitives.

## **8\. Consumers**

As opposed to the _Supplier_ , the _Consumer_ accepts a generified argument and returns nothing. It is a function that is representing side effects.

For instance, let’s greet everybody in a list of names by printing the greeting in the console. The lambda passed to the _List.forEach_ method implements the _Consumer_ functional interface:
    
    
    List<String> names = Arrays.asList("John", "Freddy", "Samuel");
    names.forEach(name -> System.out.println("Hello, " + name));

There are also specialized versions of the _Consumer_ — _DoubleConsumer_ , _IntConsumer_ and _LongConsumer_ — that receive primitive values as arguments. More interesting is the _BiConsumer_ interface. One of its use cases is iterating through the entries of a map:
    
    
    Map<String, Integer> ages = new HashMap<>();
    ages.put("John", 25);
    ages.put("Freddy", 24);
    ages.put("Samuel", 30);
    
    ages.forEach((name, age) -> System.out.println(name + " is " + age + " years old"));

Another set of specialized _BiConsumer_ versions is comprised of _ObjDoubleConsumer_ , _ObjIntConsumer_ , and _ObjLongConsumer,_ which receive two arguments; one of the arguments is generified, and the other is a primitive type.

## **9\. Predicates**

In mathematical logic, a predicate is a function that receives a value and returns a boolean value.

The _Predicate_ functional interface is a specialization of a _Function_ that receives a generified value and returns a boolean. A typical use case of the _Predicate_ lambda is to filter a collection of values:
    
    
    List<String> names = Arrays.asList("Angela", "Aaron", "Bob", "Claire", "David");
    
    List<String> namesWithA = names.stream()
      .filter(name -> name.startsWith("A"))
      .collect(Collectors.toList());

In the code above, we filter a list using the _Stream_ API and keep only the names that start with the letter “A”. The _Predicate_ implementation encapsulates the filtering logic.

As in all of the previous examples, there are _IntPredicate_ , _DoublePredicate_ and _LongPredicate_ versions of this function that receive primitive values.

## **10\. Operators**

_Operator_ interfaces are special cases of a function that receive and return the same value type. The _UnaryOperator_ interface receives a single argument. One of its use cases in the Collections API is to replace all values in a list with some computed values of the same type:
    
    
    List<String> names = Arrays.asList("bob", "josh", "megan");
    
    names.replaceAll(name -> name.toUpperCase());

The _List.replaceAll_ function returns _void_ as it replaces the values in place. To fit the purpose, the lambda used to transform the values of a list has to return the same result type as it receives. This is why the _UnaryOperator_ is useful here.

Of course, instead of _name - > name.toUpperCase()_, we can simply use a method reference:
    
    
    names.replaceAll(String::toUpperCase);

One of the most interesting use cases of a _BinaryOperator_ is a reduction operation. Suppose we want to aggregate a collection of integers in a sum of all values. With _Stream_ API, we could do this using a collector _,_ but a more generic way to do it would be to use the _reduce_ method:
    
    
    List<Integer> values = Arrays.asList(3, 5, 8, 9, 12);
    
    int sum = values.stream()
      .reduce(0, (i1, i2) -> i1 + i2);
    

The _reduce_ method receives an initial accumulator value and a _BinaryOperator_ function. The arguments of this function are a pair of values of the same type; the function itself also contains a logic for joining them in a single value of the same type. **The passed function must be associative** , which means that the order of value aggregation does not matter, i.e. the following condition should hold:
    
    
    op.apply(a, op.apply(b, c)) == op.apply(op.apply(a, b), c)

The associative property of a _BinaryOperator_ operator function allows us to easily parallelize the reduction process.

Of course, there are also specializations of _UnaryOperator_ and _BinaryOperator_ that can be used with primitive values, namely _DoubleUnaryOperator_ , _IntUnaryOperator_ , _LongUnaryOperator_ , _DoubleBinaryOperator_ , _IntBinaryOperator_ , and _LongBinaryOperator_.

## **11\. Legacy Functional Interfaces**

Not all functional interfaces appeared in Java 8. Many interfaces from previous versions of Java conform to the constraints of a _FunctionalInterface_ , and we can use them as lambdas. Prominent examples include the _Runnable_ and _Callable_ interfaces that are used in concurrency APIs. In Java 8, these interfaces are also marked with a _@FunctionalInterface_ annotation. This allows us to greatly simplify concurrency code:
    
    
    Thread thread = new Thread(() -> System.out.println("Hello From Another Thread"));
    thread.start();

## **12\. Conclusion**

In this article, we examined different functional interfaces present in the Java 8 API that we can use as lambda expressions.
