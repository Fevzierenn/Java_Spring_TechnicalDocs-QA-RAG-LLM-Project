# Comparing Objects in Java

## 1\. Introduction

Comparing objects is an essential feature of object-oriented programming languages.

In this tutorial, we’ll explore some of the features of the Java language that allow us to compare objects. We’ll also look at such features in external libraries.

## _2\. ==_ and _!=_ Operators

Let’s begin with the _==_ and _!=_ operators, which can tell if two Java objects are the same or not, respectively.

### 2.1. Primitives

**For primitive types, being the same means having equal values:**
    
    
    assertThat(1 == 1).isTrue();

Thanks to auto-unboxing, **this also works when comparing a primitive value with its wrapper type counterpart** :
    
    
    Integer a = new Integer(1);
    assertThat(1 == a).isTrue();

If two integers have different values, the _==_ operator will return _false_ , while the _!=_ operator will return _true_.

### 2.2. Objects

Let’s say we want to compare two _Integer_ wrapper types with the same value:
    
    
    Integer a = new Integer(1);
    Integer b = new Integer(1);
    
    assertThat(a == b).isFalse();

By comparing two objects,**the value of those objects isn’t 1. Rather, it’s their[memory addresses in the stack](/java-stack-heap)** that are different, since both objects are created using the _new_ operator. If we assigned _a_ to _b_ , then we would have a different result:
    
    
    Integer a = new Integer(1);
    Integer b = a;
    
    assertThat(a == b).isTrue();

Now let’s see what happens when we use the _Integer#valueOf_ factory method:
    
    
    Integer a = Integer.valueOf(1);
    Integer b = Integer.valueOf(1);
    
    assertThat(a == b).isTrue();

In this case, they’re considered the same. This is because the _valueOf()_ method stores the _Integer_ in a cache to avoid creating too many wrapper objects with the same value. Therefore, the method returns the same _Integer_ instance for both calls.

Java also does this for _String_ :
    
    
    assertThat("Hello!" == "Hello!").isTrue();

However, if they’re created using the _new_ operator, then they won’t be the same.

Finally, **two _null_ references are considered the same, while any non-_null_ object is considered different from _null_** :
    
    
    assertThat(null == null).isTrue();
    
    assertThat("Hello!" == null).isFalse();

Of course, the behavior of the equality operators can be limiting. What if we want to compare two objects mapped to different addresses and yet have them considered equal based on their internal states? We’ll see how to do this in the next sections.

## _3\. Object#equals_ Method

Now let’s talk about a broader concept of equality with the _equals()_ method.

This method is defined in the _Object_ class so that every Java object inherits it. By default, **its implementation compares object memory addresses, so it works the same as the _==_ operator**. However, we can override this method in order to define what equality means for our objects.

First, let’s see how it behaves for existing objects like _Integer_ :
    
    
    Integer a = new Integer(1);
    Integer b = new Integer(1);
    
    assertThat(a.equals(b)).isTrue();

The method still returns _true_ when both objects are the same.

We should note that we can pass a _null_ object as the argument of the method, but not as the object we call the method upon.

We can also use the _equals()_ method with an object of our own. Let’s say we have a _Person_ class:
    
    
    public class PersonWithEquals {
        private String firstName;
        private String lastName;
    
        public PersonWithEquals(String firstName, String lastName) {
            this.firstName = firstName;
            this.lastName = lastName;
        }
    }

We can override the _equals()_ method for this class so that we can compare two _Person_ s based on their internal details:
    
    
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        PersonWithEquals that = (PersonWithEquals) o;
        return firstName.equals(that.firstName) &&
          lastName.equals(that.lastName);
    }

**For more information, check out our[article about this topic](/java-equals-hashcode-contracts).**

## _4\. Objects#equals_ Static Method

Now let’s look at the [_Objects#equals_ static method](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/Objects.html#equals\(java.lang.Object,java.lang.Object\)). We mentioned earlier that we can’t use _null_ as the value of the first object, otherwise a _NullPointerException_ will be thrown.

**The _equals()_ method of the _Objects_ helper class solves that problem. It takes two arguments and compares them, also handling _null_ values.**

Let’s compare _Person_ objects again:
    
    
    PersonWithEquals joe = new PersonWithEquals("Joe", "Portman");
    PersonWithEquals joeAgain = new PersonWithEquals("Joe", "Portman");
    PersonWithEquals natalie = new PersonWithEquals("Natalie", "Portman");
    
    assertThat(Objects.equals(joe, joeAgain)).isTrue();
    assertThat(Objects.equals(joe, natalie)).isFalse();

As we explained, this method handles _null_ values. Therefore, if both arguments are _null,_ it’ll return _true_ , and if only one of them is _null_ , it’ll return _false_.

This can be really handy. Let’s say we want to add an optional birth date to our _Person_ class:
    
    
    public PersonWithEquals(String firstName, String lastName, LocalDate birthDate) {
        this(firstName, lastName);
        this.birthDate = birthDate;
    }

Then we have to update our _equals()_ method, but with _null_ handling. We can do this by adding the condition to our _equals()_ method:
    
    
    birthDate == null ? that.birthDate == null : birthDate.equals(that.birthDate);

However, if we add too many nullable fields to our class, it can become really messy. Using the _Objects#equals_ method in our _equals()_ implementation is much cleaner, and improves readability:
    
    
    Objects.equals(birthDate, that.birthDate);

## _5\. Comparable_ Interface

Comparison logic can also be used to place objects in a specific order. **The[ _Comparable_ interface](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/Comparable.html) allows us to define an ordering between objects** by determining if an object is greater, equal, or lesser than another.

The _Comparable_ interface is generic and has only one method, _compareTo()_ , which takes an argument of the generic type and returns an _int_. The returned value is negative if _this_ is lower than the argument, 0 if they’re equal, and positive otherwise.

Let’s say, in our _Person_ class, we want to compare _Person_ objects by their last name:
    
    
    public class PersonWithEqualsAndComparable implements Comparable<PersonWithEqualsAndComparable> {
        //...
    
        @Override
        public int compareTo(PersonWithEqualsAndComparable o) {
            return this.lastName.compareTo(o.lastName);
        }
    }

The _compareTo()_ method will return a negative _int_ if called with a _Person_ having a greater last name than _this_ , zero if the same last name, and positive otherwise.

**For more information, take a look at our[article about this topic](/java-comparator-comparable).**

## _6\. Comparator_ Interface

The [_Comparator_ interface](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/Comparator.html) is generic and has a _compare_ method that takes two arguments of that generic type and returns an _integer_. We already saw this pattern earlier with the _Comparable_ interface.

_Comparator_ is similar; however, it’s separated from the definition of the class. Therefore, **we can define as many _Comparators_ as we want for a class, where we can only provide one _Comparable_ implementation.**

Let’s imagine we have a web page displaying people in a table view, and we want to offer the user the possibility to sort them by first names rather than last names. This isn’t possible with _Comparable_ if we also want to keep our current implementation, but we can implement our own _Comparators_.

Let’s create a _Person_ _Comparator_ that will compare them only by their first names:
    
    
    Comparator<Person> compareByFirstNames = Comparator.comparing(Person::getFirstName);

Now let’s sort a _List_ of people using that _Comparator_ :
    
    
    Person joe = new Person("Joe", "Portman");
    Person allan = new Person("Allan", "Dale");
    
    List<Person> people = new ArrayList<>();
    people.add(joe);
    people.add(allan);
    
    people.sort(compareByFirstNames);
    
    assertThat(people).containsExactly(allan, joe);

There are also other methods on the _Comparator_ interface we can use in our _compareTo()_ implementation:
    
    
    @Override
    public int compareTo(Person o) {
        return Comparator.comparing(Person::getLastName)
          .thenComparing(Person::getFirstName)
          .thenComparing(Person::getBirthDate, Comparator.nullsLast(Comparator.naturalOrder()))
          .compare(this, o);
    }

In this case, we’re first comparing last names, then first names. Next we compare birth dates, but as they’re nullable, we must say how to handle that. To do this, we give a second argument to say that they should be compared according to their natural order, with _null_ values going last.

## 7\. Apache Commons

Let’s take a look at the [Apache Commons library](/java-commons-lang-3). First of all, let’s import the [Maven dependency](https://mvnrepository.com/artifact/org.apache.commons/commons-lang3):
    
    
    <dependency>
        <groupId>org.apache.commons</groupId>
        <artifactId>commons-lang3</artifactId>
        <version>3.12.0</version>
    </dependency>

### _7.1.__ObjectUtils#notEqual_ Method

First, let’s talk about the _ObjectUtils#notEqual_ method. It takes two _Object_ arguments to determine if they’re not equal, according to their own _equals()_ method implementation. It also handles _null_ values.

Let’s reuse our _String_ examples:
    
    
    String a = new String("Hello!");
    String b = new String("Hello World!");
    
    assertThat(ObjectUtils.notEqual(a, b)).isTrue();
    

It should be noted that _ObjectUtils_ has an _equals()_ method. However, that’s deprecated since Java 7, when _Objects#equals_ appeared

### _7.2. ObjectUtils#compare_ Method

Now let’s compare object order with the _ObjectUtils#compare_ method. **It’s a generic method that takes two _Comparable_ arguments of that generic type and returns an _Integer_.**

Let’s see it using _Strings_ again:
    
    
    String first = new String("Hello!");
    String second = new String("How are you?");
    
    assertThat(ObjectUtils.compare(first, second)).isNegative();

By default, the method handles _null_ values by considering them greater. It also offers an overloaded version that offers to invert that behavior and consider them lesser, taking a _boolean_ argument.

## 8\. Guava

Let’s take a look at [Guava](https://guava.dev/). First of all, let’s import [the dependency](https://mvnrepository.com/artifact/com.google.guava/guava):
    
    
    <dependency>
        <groupId>com.google.guava</groupId>
        <artifactId>guava</artifactId>
        <version>31.0.1-jre</version>
    </dependency>

### _8.1. Objects#equal_ Method

**Similar to the Apache Commons library, Google provides us with a method to determine if two objects are equal,_Objects#equal_. Though they have different implementations, they return the same results:**
    
    
    String a = new String("Hello!");
    String b = new String("Hello!");
    
    assertThat(Objects.equal(a, b)).isTrue();

Though it’s not marked as deprecated, the JavaDoc for this method says that it should be considered as deprecated, since Java 7 provides the _Objects#equals_ method.

### 8.2. Comparison Methods

The Guava library doesn’t offer a method to compare two objects (we’ll see in the next section what we can do to achieve that though), but **it does provide us with methods to compare primitive values**. Let’s take the _Ints_ helper class and see how its _compare()_ method works:
    
    
    assertThat(Ints.compare(1, 2)).isNegative();

As usual, it returns an _integer_ that may be negative, zero, or positive if the first argument is lesser, equal, or greater than the second, respectively. Similar methods exist for all the primitive types, except for _bytes_.

### _8.3. ComparisonChain_ Class

Finally, the Guava library offers the _ComparisonChain_ class that allows us to compare two objects through a chain of comparisons. We can easily compare two _Person_ objects by the first and last names:
    
    
    Person natalie = new Person("Natalie", "Portman");
    Person joe = new Person("Joe", "Portman");
    
    int comparisonResult = ComparisonChain.start()
      .compare(natalie.getLastName(), joe.getLastName())
      .compare(natalie.getFirstName(), joe.getFirstName())
      .result();
    
    assertThat(comparisonResult).isPositive();

The underlying comparison is achieved using the _compareTo()_ method, so the arguments passed to the _compare()_ methods must either be primitives or _Comparable_ s.

## 9\. Conclusion

In this article, we learned different ways to compare objects in Java. We examined the difference between sameness, equality, and ordering. We also looked at the corresponding features in the Apache Commons and Guava libraries.
