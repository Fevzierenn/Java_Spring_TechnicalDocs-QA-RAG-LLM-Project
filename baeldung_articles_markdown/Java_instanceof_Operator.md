# Java instanceof Operator

## 1\. Introduction

In this quick tutorial, we’ll learn about the  _instanceof_ operator in Java.

## 2\. What Is the _instanceof_ Operator?

**_instanceof is_ a binary operator we use to test if an object is of a given type.** The result of the operation is either _true_ or _false_. It’s also known as a type comparison operator because it compares the instance with the type.

Before [casting](/java-type-casting) an unknown object, the  _instanceof_ check should always be used. Doing this helps to avoid a _ClassCastException_ at runtime.

The _instanceof_ operator’s basic syntax is:
    
    
    (object) instanceof (type)

Now let’s see a basic example for the _instanceof_ operator. First, we’ll create a class _Round_ :
    
    
    public class Round {
        // implementation details
    }

Next, we’ll create a class _Ring_ that extends  _Round_ :
    
    
    public class Ring extends Round {
        // implementation details
    }

We can use _instanceof_ to check if an instance of _Ring_ is of _Round_ type:
    
    
    @Test
    void givenWhenInstanceIsCorrect_thenReturnTrue() {
        Ring ring = new Ring();
        assertTrue(ring instanceof Round);
    }

## 3\. How Does the  _instanceof_ Operator Work?

**The _instanceof_ operator works on the principle of the is-a relationship**. The concept of an is-a relationship is based on class [inheritance](/java-inheritance-composition) or interface implementation.

To demonstrate this, we’ll create a _Shape_ interface:
    
    
    public interface Shape {
        // implementation details
    }

We’ll also create a class _Circle,_ which implements the _Shape_ interface and also extends the  _Round_ class:
    
    
    public class Circle extends Round implements Shape {
        // implementation details
    }

**The _instanceof_ result will be _true_ if the object is an instance of the type:**
    
    
    @Test
    void givenWhenObjectIsInstanceOfType_thenReturnTrue() {
        Circle circle = new Circle();
        assertTrue(circle instanceof Circle);
    }

**It will also be _true_ if the object is an instance of a subclass of the type:**
    
    
    @Test
    void givenWhenInstanceIsOfSubtype_thenReturnTrue() {
        Circle circle = new Circle();
        assertTrue(circle instanceof Round);
    }

**If the type is an interface, it will return _true_ if the object implements the interface:**
    
    
    @Test
    void givenWhenTypeIsInterface_thenReturnTrue() {
        Circle circle = new Circle();
        assertTrue(circle instanceof Shape);
    }

**The _instanceof_ operator can’t be used if there’s no relationship between the object that’s being compared and the type it’s being compared with.**

We’ll create a new class, _Triangle,_ that implements _Shape,_ but has no relationship with _Circle_ :
    
    
    public class Triangle implements Shape {
        // implementation details
    }

Now if we use _instanceof_ to check if a _Circle_ is an instance of _Triangle_ :
    
    
    @Test
    void givenWhenComparingClassInDiffHierarchy_thenCompilationError() {
        Circle circle = new Circle();
        assertFalse(circle instanceof Triangle);
    }

We’ll get a compilation error because there’s no relationship between the _Circle_ and _Triangle_ classes:
    
    
    java.lang.Error: Unresolved compilation problem:
      Incompatible conditional operand types Circle and Triangle

## 4\. Using  _instanceof_ With the  _Object_ Type

In Java, every class implicitly inherits from the  _Object_ class. Therefore, using the  _instanceof_ operator with the _Object_ type will always evaluate to _true_ :
    
    
    @Test
    void givenWhenTypeIsOfObjectType_thenReturnTrue() {
        Thread thread = new Thread();
        assertTrue(thread instanceof Object);
    }

## 5\. Using the  _instanceof_ Operator When an Object Is _null_

If we use the _instanceof_ operator on any object that’s _null_ , it returns _false_. We also don’t need a null check when using an _instanceof_ operator.
    
    
    @Test
    void givenWhenInstanceValueIsNull_thenReturnFalse() {
        Circle circle = null;
        assertFalse(circle instanceof Round);
    }

## 6\.  _instanceof_ and Generics

**Instance tests and casts depend on inspecting the type information at runtime. Therefore, we can’t use _instanceof_ along with [erased generic types](/java-type-erasure)**.

For instance, if we try to compile the following snippet:
    
    
    public static <T> void sort(List<T> collection) {
        if (collection instanceof List<String>) {
            // sort strings differently
        }
            
        // omitted
    }

Then we get this compilation error:
    
    
    error: illegal generic type for instanceof
            if (collection instanceof List<String>) {
                                          ^

**Technically speaking, we’re only allowed to use _instanceof_ along with reified __ types in Java.** A type is reified if its type information is present at runtime.

The reified types in Java are as follows:

  * Primitive types, like _int_
  * Non-generic classes and interfaces, like _String_ or _Random_
  * Generic types in which all types are unbounded wildcards, like _Set <?> _or _Map <?, ?>_
  * Raw types, like _List or HashMap_
  * Arrays of other reifiable types, like _String[], List[],_ or _Map <?, ?>[]_



Because generic type parameters aren’t reified, we can’t use them either:
    
    
    public static <T> boolean isOfType(Object input) {
        return input instanceof T; // won't compile
    }

However, it’s possible to test against something like _List <?>_:
    
    
    if (collection instanceof List<?>) {
        // do something
    }

## 7\. Stream API – Filtering Types Using _instanceof_ Before Casting

One great feature that Java 8 has brought us is the [Stream API](/java-8-streams). We often convert a type _A_ collection to a type _B_ collection using _Stream_ ‘s _[map()](/java-difference-map-and-flatmap)_ method.

If the type conversion is done by typecasting, **we may want to check the types before performing the typecasting to avoid the[ _ClassCastException_](/java-classcastexception)**.

Next, let’s see an example. Let’s say we have a _Stream_ of _Round_ instances:
    
    
    Stream<Round> roundStream = Stream.of(new Ring(), new Ring(), new Circle());

As the code above shows, the _roundStream_ object contains two _Ring_ objects and one _Circle_ instance.

Now, if we convert _roundStream_ to a list of _Ring_ without checking the types, _ClassCastException_ will be raised as a _Circle_ is not a _Ring_ :
    
    
    @Test
    void givenWhenStream_whenCastWithoutInstanceOfChk_thenGetException() {
        Stream<Round> roundStream = Stream.of(new Ring(), new Ring(), new Circle());
        assertThrows(ClassCastException.class, () -> roundStream.map(it -> (Ring) it).collect(Collectors.toList()));
    }

However, if we filter _Ring_ objects before the  _map()_ call, we’ll get the expected list:
    
    
    @Test
    void givenWhenStream_whenCastAfterInstanceOfChk_thenGetExpectedResult() {
        Stream<Round> roundStream = Stream.of(new Ring(), new Ring(), new Circle());
        List<Ring> ringList = roundStream.filter(it -> it instanceof Ring).map(it -> (Ring) it).collect(Collectors.toList());
        assertEquals(2, ringList.size());
    }

## 8\. Conclusion

In this brief article, we learned about the _instanceof_ operator and how to use it.
