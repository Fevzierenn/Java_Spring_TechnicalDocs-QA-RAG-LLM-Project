# Guide To Java Optional

## **1\. Overview**

In this tutorial, we’re going to show the  _Optional_ class that was introduced in Java 8.

The purpose of the class is to provide a type-level solution for representing optional values instead of  _null_ references.

To get a deeper understanding of why we should care about the _Optional_ class, take a look at [the official Oracle article](http://www.oracle.com/technetwork/articles/java/java8-optional-2175753.html).

## **2\. Creating _Optional_ Objects**

There are several ways of creating _Optional_ objects.

To create an empty _Optional_ object, we simply need to use its _empty()_ static method:
    
    
    @Test
    public void whenCreatesEmptyOptional_thenCorrect() {
        Optional<String> empty = Optional.empty();
        assertFalse(empty.isPresent());
    }

Note that we used the _isPresent()_ method to check if there is a value inside the _Optional_ object. A value is present only if we have created _Optional_ with a non-_null_ value. We’ll look at the _isPresent()_ method in the next section.

We can also create an _Optional_ object with the static method  _of()_ :
    
    
    @Test
    public void givenNonNull_whenCreatesNonNullable_thenCorrect() {
        String name = "baeldung";
        Optional<String> opt = Optional.of(name);
        assertTrue(opt.isPresent());
    }

However, the argument passed to the _of()_ method can’t be _null._ Otherwise, we’ll get a _NullPointerException_ :
    
    
    @Test(expected = NullPointerException.class)
    public void givenNull_whenThrowsErrorOnCreate_thenCorrect() {
        String name = null;
        Optional.of(name);
    }

But in case we expect some _null_ values, we can use the _ofNullable()_ method:
    
    
    @Test
    public void givenNonNull_whenCreatesNullable_thenCorrect() {
        String name = "baeldung";
        Optional<String> opt = Optional.ofNullable(name);
        assertTrue(opt.isPresent());
    }

By doing this, if we pass in a _null_ reference, it doesn’t throw an exception but rather returns an empty _Optional_ object:
    
    
    @Test
    public void givenNull_whenCreatesNullable_thenCorrect() {
        String name = null;
        Optional<String> opt = Optional.ofNullable(name);
        assertFalse(opt.isPresent());
    }

## **3\. Checking Value Presence:_isPresent()_ and _isEmpty()_**

When we have an _Optional_ object returned from a method or created by us, we can check if there is a value in it or not with the _isPresent()_ method:
    
    
    @Test
    public void givenOptional_whenIsPresentWorks_thenCorrect() {
        Optional<String> opt = Optional.of("Baeldung");
        assertTrue(opt.isPresent());
    
        opt = Optional.ofNullable(null);
        assertFalse(opt.isPresent());
    }

This method returns _true_ if the wrapped value is not _null._

Also, as of Java 11, we can do the opposite with the  _isEmpty_ method:
    
    
    @Test
    public void givenAnEmptyOptional_thenIsEmptyBehavesAsExpected() {
        Optional<String> opt = Optional.of("Baeldung");
        assertFalse(opt.isEmpty());
    
        opt = Optional.ofNullable(null);
        assertTrue(opt.isEmpty());
    }

## **4\. Conditional Action With _ifPresent()_**

The _ifPresent()_ method enables us to run some code on the wrapped value if it’s found to be non-_null_. Before _Optional_ , we’d do:
    
    
    if(name != null) {
        System.out.println(name.length());
    }

This code checks if the name variable is _null_ or not before going ahead to execute some code on it. This approach is lengthy, and that’s not the only problem — it’s also prone to error.

Indeed, what guarantees that after printing that variable, we won’t use it again and then **forget to perform the null check?**

**This can result in a _NullPointerException_ at runtime if a null value finds its way into that code.** When a program fails due to input issues, it’s often a result of poor programming practices.

_Optional_ makes us deal with nullable values explicitly as a way of enforcing good programming practices.

Let’s now look at how the above code could be refactored in Java 8.

In typical functional programming style, we can execute perform an action on an object that is actually present:
    
    
    @Test
    public void givenOptional_whenIfPresentWorks_thenCorrect() {
        Optional<String> opt = Optional.of("baeldung");
        opt.ifPresent(name -> System.out.println(name.length()));
    }

In the above example, we use only two lines of code to replace the five that worked in the first example: one line to wrap the object into an _Optional_ object and the next to perform implicit validation as well as execute the code.

## **5\. Default Value With _orElse()_**

The _orElse()_ method is used to retrieve the value wrapped inside an _Optional_ instance. It takes one parameter, which acts as a default value. The _orElse()_ method returns the wrapped value if it’s present, and its argument otherwise:
    
    
    @Test
    public void whenOrElseWorks_thenCorrect() {
        String nullName = null;
        String name = Optional.ofNullable(nullName).orElse("john");
        assertEquals("john", name);
    }

## **6\. Default Value With _orElseGet()_**

The _orElseGet()_ method is similar to _orElse()_. However, instead of taking a value to return if the _Optional_ value is not present, it takes a supplier functional interface, which is invoked and returns the value of the invocation:
    
    
    @Test
    public void whenOrElseGetWorks_thenCorrect() {
        String nullName = null;
        String name = Optional.ofNullable(nullName).orElseGet(() -> "john");
        assertEquals("john", name);
    }

## **7\. Difference Between _orElse_ and _orElseGet()_**

To a lot of programmers who are new to _Optional_ or Java 8, the difference between _orElse()_ and _orElseGet()_ is not clear. As a matter of fact, these two methods give the impression that they overlap each other in functionality.

However, there’s a subtle but very important difference between the two that can affect the performance of our code drastically if not well understood.

Let’s create a method called _getMyDefault()_ in the test class, which takes no arguments and returns a default value:
    
    
    public String getMyDefault() {
        System.out.println("Getting Default Value");
        return "Default Value";
    }

Let’s see two tests and observe their side effects to establish both where _orElse()_ and _orElseGet()_ overlap and where they differ:
    
    
    @Test
    public void whenOrElseGetAndOrElseOverlap_thenCorrect() {
        String text = null;
    
        String defaultText = Optional.ofNullable(text).orElseGet(this::getMyDefault);
        assertEquals("Default Value", defaultText);
    
        defaultText = Optional.ofNullable(text).orElse(getMyDefault());
        assertEquals("Default Value", defaultText);
    }

In the above example, we wrap a null text inside an _Optional_ object and attempt to get the wrapped value using each of the two approaches.

The side effect is:
    
    
    Getting default value...
    Getting default value...

The _getMyDefault()_ method is called in each case. It so happens that **when the wrapped value is not present, then both _orElse()_ and _orElseGet()_ work exactly the same way.**

Now let’s run another test where the value is present, and ideally, the default value should not even be created:
    
    
    @Test
    public void whenOrElseGetAndOrElseDiffer_thenCorrect() {
        String text = "Text present";
    
        System.out.println("Using orElseGet:");
        String defaultText 
          = Optional.ofNullable(text).orElseGet(this::getMyDefault);
        assertEquals("Text present", defaultText);
    
        System.out.println("Using orElse:");
        defaultText = Optional.ofNullable(text).orElse(getMyDefault());
        assertEquals("Text present", defaultText);
    }

In the above example, we are no longer wrapping a _null_ value, and the rest of the code remains the same.

Now let’s take a look at the side effects of running this code:
    
    
    Using orElseGet:
    Using orElse:
    Getting default value...

Notice that when using _orElseGet()_ to retrieve the wrapped value, the _getMyDefault()_ method is not even invoked since the contained value is present.

However, when using _orElse()_ , whether the wrapped value is present or not, the default object is created. So in this case, we have just created one redundant object that is never used.

In this simple example, there is no significant cost to creating a default object, as the JVM knows how to deal with such. **However, when a method such as _getMyDefault()_ has to make a web service call or even query a database, the cost becomes very obvious.**

## **8\. Exceptions With _orElseThrow()_**

The _orElseThrow()_ method follows from _orElse()_ and _orElseGet()_ and adds a new approach for handling an absent value.

Instead of returning a default value when the wrapped value is not present, it throws an exception:
    
    
    @Test(expected = IllegalArgumentException.class)
    public void whenOrElseThrowWorks_thenCorrect() {
        String nullName = null;
        String name = Optional.ofNullable(nullName).orElseThrow(
          IllegalArgumentException::new);
    }

Method references in Java 8 come in handy here, to pass in the exception constructor.

**Java 10 introduced a simplified no-arg version of _orElseThrow()_ method**. In case of an empty _Optional_ it throws a _NoSuchElementException_ :
    
    
    @Test(expected = NoSuchElementException.class)
    public void whenNoArgOrElseThrowWorks_thenCorrect() {
        String nullName = null;
        String name = Optional.ofNullable(nullName).orElseThrow();
    }

## **9\. Returning Value With _get()_**

The final approach for retrieving the wrapped value is the _get()_ method:
    
    
    @Test
    public void givenOptional_whenGetsValue_thenCorrect() {
        Optional<String> opt = Optional.of("baeldung");
        String name = opt.get();
        assertEquals("baeldung", name);
    }

However, unlike the previous three approaches, _get()_ can only return a value if the wrapped object is not _null_ ; otherwise, it throws a no such element exception:
    
    
    @Test(expected = NoSuchElementException.class)
    public void givenOptionalWithNull_whenGetThrowsException_thenCorrect() {
        Optional<String> opt = Optional.ofNullable(null);
        String name = opt.get();
    }

This is the major flaw of the _get()_ method. Ideally, _Optional_ should help us avoid such unforeseen exceptions. Therefore, this approach works against the objectives of _Optional_ and will probably be deprecated in a future release.

So, it’s advisable to use the other variants that enable us to prepare for and explicitly handle the _null_ case.

## **10\. Conditional Return With _filter()_**

We can run an inline test on our wrapped value with the _filter_ method. It takes a predicate as an argument and returns an _Optional_ object. If the wrapped value passes testing by the predicate, then the _Optional_ is returned as-is.

However, if the predicate returns _false_ , then it will return an empty _Optional_ :
    
    
    @Test
    public void whenOptionalFilterWorks_thenCorrect() {
        Integer year = 2016;
        Optional<Integer> yearOptional = Optional.of(year);
        boolean is2016 = yearOptional.filter(y -> y == 2016).isPresent();
        assertTrue(is2016);
        boolean is2017 = yearOptional.filter(y -> y == 2017).isPresent();
        assertFalse(is2017);
    }

The _filter_ method is normally used this way to reject wrapped values based on a predefined rule. We could use it to reject a wrong email format or a password that is not strong enough.

Let’s look at another meaningful example. Say we want to buy a modem, and we only care about its price.

We receive push notifications on modem prices from a certain site and store these in objects:
    
    
    public class Modem {
        private Double price;
    
        public Modem(Double price) {
            this.price = price;
        }
        // standard getters and setters
    }

We then feed these objects to some code whose sole purpose is to check if the modem price is within our budget range.

Let’s now take a look at the code without _Optional_ :
    
    
    public boolean priceIsInRange1(Modem modem) {
        boolean isInRange = false;
    
        if (modem != null && modem.getPrice() != null 
          && (modem.getPrice() >= 10 
            && modem.getPrice() <= 15)) {
    
            isInRange = true;
        }
        return isInRange;
    }

Pay attention to how much code we have to write to achieve this, especially in the _if_ condition. The only part of the _if_ condition that is critical to the application is the last price-range check; the rest of the checks are defensive:
    
    
    @Test
    public void whenFiltersWithoutOptional_thenCorrect() {
        assertTrue(priceIsInRange1(new Modem(10.0)));
        assertFalse(priceIsInRange1(new Modem(9.9)));
        assertFalse(priceIsInRange1(new Modem(null)));
        assertFalse(priceIsInRange1(new Modem(15.5)));
        assertFalse(priceIsInRange1(null));
    }

Apart from that, it’s possible to forget about the null checks over a long day without getting any compile-time errors.

Now let’s look at a variant with _Optional#filter_ :
    
    
    public boolean priceIsInRange2(Modem modem2) {
         return Optional.ofNullable(modem2)
           .map(Modem::getPrice)
           .filter(p -> p >= 10)
           .filter(p -> p <= 15)
           .isPresent();
     }

**The _map_ call is simply used to transform a value to some other value.** Keep in mind that this operation does not modify the original value.

In our case, we are obtaining a price object from the _Model_ class. We will look at the _map()_ method in detail in the next section.

First of all, if a _null_ object is passed to this method, we don’t expect any problem.

Secondly, the only logic we write inside its body is exactly what the method name describes — price-range check. _Optional_ takes care of the rest:
    
    
    @Test
    public void whenFiltersWithOptional_thenCorrect() {
        assertTrue(priceIsInRange2(new Modem(10.0)));
        assertFalse(priceIsInRange2(new Modem(9.9)));
        assertFalse(priceIsInRange2(new Modem(null)));
        assertFalse(priceIsInRange2(new Modem(15.5)));
        assertFalse(priceIsInRange2(null));
    }

The previous approach promises to check the price range but has to do more than that to defend against its inherent fragility. Therefore, we can use the _filter_ method to replace unnecessary _if_ statements and reject unwanted values.

## **11\. Transforming Value With _map()_**

In the previous section, we looked at how to reject or accept a value based on a filter.

We can use a similar syntax to transform the _Optional_ value with the _map()_ method:
    
    
    @Test
    public void givenOptional_whenMapWorks_thenCorrect() {
        List<String> companyNames = Arrays.asList(
          "paypal", "oracle", "", "microsoft", "", "apple");
        Optional<List<String>> listOptional = Optional.of(companyNames);
    
        int size = listOptional
          .map(List::size)
          .orElse(0);
        assertEquals(6, size);
    }

In this example, we wrap a list of strings inside an _Optional_ object and use its _map_ method to perform an action on the contained list. The action we perform is to retrieve the size of the list.

The _map_ method returns the result of the computation wrapped inside _Optional_. We then have to call an appropriate method on the returned _Optional_ to retrieve its value.

Notice that the _filter_ method simply performs a check on the value and returns an _Optional_ describing this value only if it matches the given predicate. Otherwise returns an empty  _Optional._ The _map_ method however takes the existing value, performs a computation using this value, and returns the result of the computation wrapped in an _Optional_ object:
    
    
    @Test
    public void givenOptional_whenMapWorks_thenCorrect2() {
        String name = "baeldung";
        Optional<String> nameOptional = Optional.of(name);
    
        int len = nameOptional
         .map(String::length)
         .orElse(0);
        assertEquals(8, len);
    }

We can chain _map_ and _filter_ together to do something more powerful.

Let’s assume we want to check the correctness of a password input by a user. We can clean the password using a _map_ transformation and check its correctness using a _filter_ :
    
    
    @Test
    public void givenOptional_whenMapWorksWithFilter_thenCorrect() {
        String password = " password ";
        Optional<String> passOpt = Optional.of(password);
        boolean correctPassword = passOpt.filter(
          pass -> pass.equals("password")).isPresent();
        assertFalse(correctPassword);
    
        correctPassword = passOpt
          .map(String::trim)
          .filter(pass -> pass.equals("password"))
          .isPresent();
        assertTrue(correctPassword);
    }

As we can see, without first cleaning the input, it will be filtered out — yet users may take for granted that leading and trailing spaces all constitute input. So, we transform a dirty password into a clean one with a _map_ before filtering out incorrect ones.

## **12\. Transforming Value With _flatMap()_**

Just like the _map()_ method, we also have the _flatMap()_ method as an alternative for transforming values. The difference is that _map_ transforms values only when they are unwrapped whereas _flatMap_ takes a wrapped value and unwraps it before transforming it.

Previously, we created simple _String_ and _Integer_ objects for wrapping in an _Optional_ instance. However, frequently, we will receive these objects from an accessor of a complex object.

To get a clearer picture of the difference, let’s have a look at a _Person_ object that takes a person’s details such as name, age and password:
    
    
    public class Person {
        private String name;
        private int age;
        private String password;
    
        public Optional<String> getName() {
            return Optional.ofNullable(name);
        }
    
        public Optional<Integer> getAge() {
            return Optional.ofNullable(age);
        }
    
        public Optional<String> getPassword() {
            return Optional.ofNullable(password);
        }
    
        // normal constructors and setters
    }

We would normally create such an object and wrap it in an _Optional_ object just like we did with String.

Alternatively, it can be returned to us by another method call:
    
    
    Person person = new Person("john", 26);
    Optional<Person> personOptional = Optional.of(person);

Notice now that when we wrap a _Person_ object, it will contain nested _Optional_ instances:
    
    
    @Test
    public void givenOptional_whenFlatMapWorks_thenCorrect2() {
        Person person = new Person("john", 26);
        Optional<Person> personOptional = Optional.of(person);
    
        Optional<Optional<String>> nameOptionalWrapper  
          = personOptional.map(Person::getName);
        Optional<String> nameOptional  
          = nameOptionalWrapper.orElseThrow(IllegalArgumentException::new);
        String name1 = nameOptional.orElse("");
        assertEquals("john", name1);
    
        String name = personOptional
          .flatMap(Person::getName)
          .orElse("");
        assertEquals("john", name);
    }

Here, we’re trying to retrieve the name attribute of the _Person_ object to perform an assertion.

Note how we achieve this with _map()_ method in the third statement, and then notice how we do the same with _flatMap()_ method afterwards.

The _Person::getName_ method reference is similar to the _String::trim_ call we had in the previous section for cleaning up a password.

The only difference is that _getName()_ returns an _Optional_ rather than a String as did the _trim()_ operation. This, coupled with the fact that a _map_ transformation wraps the result in an _Optional_ object, leads to a nested _Optional_.

While using _map()_ method, therefore, we need to add an extra call to retrieve the value before using the transformed value. This way, the _Optional_ wrapper will be removed. This operation is performed implicitly when using _flatMap_.

## 13\. Chaining _Optional_ s in Java 8

Sometimes, we may need to get the first non-empty _Optional_ object from a number of _Optional o_ bjects. In such cases, it would be very convenient to use a method like _orElseOptional()_. Unfortunately, such operation is not directly supported in Java 8.

Let’s first introduce a few methods that we’ll be using throughout this section:
    
    
    private Optional<String> getEmpty() {
        return Optional.empty();
    }
    
    private Optional<String> getHello() {
        return Optional.of("hello");
    }
    
    private Optional<String> getBye() {
        return Optional.of("bye");
    }
    
    private Optional<String> createOptional(String input) {
        if (input == null || "".equals(input) || "empty".equals(input)) {
            return Optional.empty();
        }
        return Optional.of(input);
    }

In order to chain several _Optional_ objects and get the first non-empty one in Java 8, we can use the _Stream_ API:
    
    
    @Test
    public void givenThreeOptionals_whenChaining_thenFirstNonEmptyIsReturned() {
        Optional<String> found = Stream.of(getEmpty(), getHello(), getBye())
          .filter(Optional::isPresent)
          .map(Optional::get)
          .findFirst();
        
        assertEquals(getHello(), found);
    }

The downside of this approach is that all of our _get_ methods are always executed, regardless of where a non-empty _Optional_ appears in the _Stream_.

If we want to lazily evaluate the methods passed to _Stream.of()_ , we need to use the method reference and the _Supplier_ interface:
    
    
    @Test
    public void givenThreeOptionals_whenChaining_thenFirstNonEmptyIsReturnedAndRestNotEvaluated() {
        Optional<String> found =
          Stream.<Supplier<Optional<String>>>of(this::getEmpty, this::getHello, this::getBye)
            .map(Supplier::get)
            .filter(Optional::isPresent)
            .map(Optional::get)
            .findFirst();
    
        assertEquals(getHello(), found);
    }

In case we need to use methods that take arguments, we have to resort to lambda expressions:
    
    
    @Test
    public void givenTwoOptionalsReturnedByOneArgMethod_whenChaining_thenFirstNonEmptyIsReturned() {
        Optional<String> found = Stream.<Supplier<Optional<String>>>of(
          () -> createOptional("empty"),
          () -> createOptional("hello")
        )
          .map(Supplier::get)
          .filter(Optional::isPresent)
          .map(Optional::get)
          .findFirst();
    
        assertEquals(createOptional("hello"), found);
    }

Often, we’ll want to return a default value in case all of the chained _Optional_ s are empty. We can do so just by adding a call to _orElse()_ or _orElseGet()_ :
    
    
    @Test
    public void givenTwoEmptyOptionals_whenChaining_thenDefaultIsReturned() {
        String found = Stream.<Supplier<Optional<String>>>of(
          () -> createOptional("empty"),
          () -> createOptional("empty")
        )
          .map(Supplier::get)
          .filter(Optional::isPresent)
          .map(Optional::get)
          .findFirst()
          .orElseGet(() -> "default");
    
        assertEquals("default", found);
    }

## 14\. JDK 9 _Optional_ API New Methods

The release of Java 9 added even more new methods to the _Optional_ API:

  * _or()_ method for providing a supplier that creates an alternative _Optional_
  * _ifPresentOrElse()_ method that allows executing an action if the _Optional_ is present or another action if not
  * _stream()_ method for converting an _Optional_ to a _Stream_



Let’s consider them in detail in the following paragraphs.

### 14.1. The _or()_ Method

Sometimes, when our _Optional_ is empty, we want to execute some other action that also returns an O _ptional._

Before the JDK 9, the _Optional_ class had only the _orElse()_ and _orElseGet()_ methods but both need to return unwrapped values.

Java 9 introduces the _or()_ method that returns another _Optional_ lazily if our _Optional_ is empty. If our first _Optional_ has a defined value, the lambda passed to the _or()_ method will not be invoked, and the value will not be calculated and returned:
    
    
    @Test
    public void givenOptional_whenPresent_thenShouldTakeAValueFromIt() {
        //given
        String expected = "properValue";
        Optional<String> value = Optional.of(expected);
        Optional<String> defaultValue = Optional.of("default");
    
        //when
        Optional<String> result = value.or(() -> defaultValue);
    
        //then
        assertThat(result.get()).isEqualTo(expected);
    }

In the case of _Optional_ bei _ng_ empty, the returned _result_ will be the same as the _defaultValue:_
    
    
    @Test
    public void givenOptional_whenEmpty_thenShouldTakeAValueFromOr() {
        // given
        String defaultString = "default";
        Optional<String> value = Optional.empty();
        Optional<String> defaultValue = Optional.of(defaultString);
    
        // when
        Optional<String> result = value.or(() -> defaultValue);
    
        // then
        assertThat(result.get()).isEqualTo(defaultString);
    }

### **14.2. The _ifPresentOrElse()_ Method**

When we have an _Optional_ instance, often we want to execute a specific action on the underlying value of it. On the other hand, if the _Optional_ is _empty_ we want to log it or track that fact by incrementing some metric.

The _ifPresentOrElse()_ method is created exactly for such scenarios. We can pass a _Consumer_ that will be invoked if the _Optional_ is defined, and a _Runnable_ that will be executed if the _Optional_ is empty.

Let’s say that we have a defined _Optional_ and we want to increment a specific counter if the value is present:
    
    
    @Test
    public void givenOptional_whenPresent_thenShouldExecuteProperCallback() {
        // given
        Optional<String> value = Optional.of("properValue");
        AtomicInteger successCounter = new AtomicInteger(0);
        AtomicInteger onEmptyOptionalCounter = new AtomicInteger(0);
    
        // when
        value.ifPresentOrElse(
          v -> successCounter.incrementAndGet(), 
          onEmptyOptionalCounter::incrementAndGet);
    
        // then
        assertThat(successCounter.get()).isEqualTo(1);
        assertThat(onEmptyOptionalCounter.get()).isEqualTo(0);
    }

Note, that the callback passed as the second argument was not executed.

In the case of an empty _Optional,_ the second callback gets executed:
    
    
    @Test
    public void givenOptional_whenNotPresent_thenShouldExecuteProperCallback() {
        // given
        Optional<String> value = Optional.empty();
        AtomicInteger successCounter = new AtomicInteger(0);
        AtomicInteger onEmptyOptionalCounter = new AtomicInteger(0);
    
        // when
        value.ifPresentOrElse(
          v -> successCounter.incrementAndGet(), 
          onEmptyOptionalCounter::incrementAndGet);
    
        // then
        assertThat(successCounter.get()).isEqualTo(0);
        assertThat(onEmptyOptionalCounter.get()).isEqualTo(1);
    }

### **14.3. The _stream()_ Method**

The last method, which is added to the _Optional_ class in Java 9, is the _stream()_ method.

Java has a very fluent and elegant _Stream_ API that can operate on the collections and utilizes many functional programming concepts. The newest Java version introduces the _stream()_ method on the _Optional_ class that **allows us to treat the _Optional_ instance as a _Stream._**

Let’s say that we have a defined _Optional_ and we are calling the _stream()_ method on it. This will create a _Stream_ of one element on which we can use all the methods that are available in the _Stream_ API _:_
    
    
    @Test
    public void givenOptionalOfSome_whenToStream_thenShouldTreatItAsOneElementStream() {
        // given
        Optional<String> value = Optional.of("a");
    
        // when
        List<String> collect = value.stream().map(String::toUpperCase).collect(Collectors.toList());
    
        // then
        assertThat(collect).hasSameElementsAs(List.of("A"));
    }

On the other hand, if _Optional_ is not present, calling the _stream()_ method on it will create an empty _Stream:_
    
    
    @Test
    public void givenOptionalOfNone_whenToStream_thenShouldTreatItAsZeroElementStream() {
        // given
        Optional<String> value = Optional.empty();
    
        // when
        List<String> collect = value.stream()
          .map(String::toUpperCase)
          .collect(Collectors.toList());
    
        // then
        assertThat(collect).isEmpty();
    }

We can now quickly filter [_Streams_ of _Optionals._](/java-filter-stream-of-optional)

Operating on the empty _Stream_ will not have any effect, but thanks to the _stream()_ method we can now chain the _Optional_ API with the _Stream_ API. This allows us to create more elegant and fluent code.

## 15\. Misuse of _Optional_ s

Finally, let’s see a tempting, however dangerous, way to use _Optional_ s: passing an  _Optional_ parameter to a method.

Imagine we have a list of  _Person_ objects and we want a method to search through that list for people with a given name. Also, we would like that method to match entries with at least a certain age, if it’s specified.

With this parameter being optional, we might come with this method:
    
    
    public static List<Person> search(List<Person> people, String name, Optional<Integer> age) {
        // Null checks for people and name
        return people.stream()
                .filter(p -> p.getName().equals(name))
                .filter(p -> p.getAge().get() >= age.orElse(0))
                .collect(Collectors.toList());
    }

Then we release our method, and another developer tries to use it:
    
    
    someObject.search(people, "Peter", null);

Now the developer executes its code and gets a _NullPointerException._ **There we are, having to null check our optional parameter, which defeats our initial purpose: avoiding this kind of situation.**

Here are some possibilities we could have done to handle it better:
    
    
    public static List<Person> search(List<Person> people, String name, Integer age) {
        // Null checks for people and name
        final Integer ageFilter = age != null ? age : 0;
    
        return people.stream()
                .filter(p -> p.getName().equals(name))
                .filter(p -> p.getAge().get() >= ageFilter)
                .collect(Collectors.toList());
    }

There, the parameter’s still optional, but we handle it in only one check.

Another possibility would have been to **create two overloaded methods** :
    
    
    public static List<Person> search(List<Person> people, String name) {
        return doSearch(people, name, 0);
    }
    
    public static List<Person> search(List<Person> people, String name, int age) {
        return doSearch(people, name, age);
    }
    
    private static List<Person> doSearch(List<Person> people, String name, int age) {
        // Null checks for people and name
        return people.stream()
                .filter(p -> p.getName().equals(name))
                .filter(p -> p.getAge().get().intValue() >= age)
                .collect(Collectors.toList());
    }

That way we offer a clear API with two methods doing different things (though they share the implementation).

So, there are solutions to avoid using  _Optional_ s as method parameters.**The intent of Java when releasing _Optional_ was to use it as a return type**, thus indicating that a method could return an empty value. As a matter of fact, the practice of using _Optional_ as a method parameter is even [discouraged by some code inspectors](https://rules.sonarsource.com/java/RSPEC-3553).

## 16\.  _Optional_ and Serialization

As discussed above, _Optional_ is meant to be used as a return type. Trying to use it as a field type is not recommended.

Additionally, **using _Optional_ in a serializable class will result in a _NotSerializableException_.** Our article [Java _Optional_ as Return Type](/java-optional-return) further addresses the issues with serialization.

And, in [Using _Optional_ With Jackson](/jackson-optional), we explain what happens when _Optional_ fields are serialized, along with a few workarounds to achieve the desired results.

## **17\. Conclusion**

In this article, we covered most of the important features of Java 8 _Optional_ class.

We briefly explored some reasons why we would choose to use _Optional_ instead of explicit null checking and input validation.

We also learned how to get the value of an _Optional_ , or a default one if empty, with the _get()_ , _orElse()_ and _orElseGet()_ methods (and saw [the important difference between the last two](/java-filter-stream-of-optional)).

Then we saw how to transform or filter our _Optional_ s with  _map(), flatMap()_ and  _filter()_. We discussed what a fluent _API_  _Optional_ offers, as it allows us to chain the different methods easily.

Finally, we saw why using _Optional_ s as method parameters is a bad idea and how to avoid it.
