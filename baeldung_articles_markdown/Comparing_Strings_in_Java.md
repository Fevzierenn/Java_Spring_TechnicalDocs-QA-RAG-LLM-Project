# Comparing Strings in Java

## **1\. Overview**

In this article, we’ll talk about the different ways of comparing _Strings_ in Java.

As _String_ is one of the most used data types in Java, this is naturally a very commonly used operation.

## **2._String_ Comparison With _String_ Class**

### **2.1. Using _“==”_ Comparison Operator**

Using the “==” operator for comparing text values is one of the most common mistakes Java beginners make. This is incorrect because **_“==”_ only checks the referential equality of two _Strings_** _,_ meaning if they reference the same object or not.

Let’s see an example of this behavior:
    
    
    String string1 = "using comparison operator";
    String string2 = "using comparison operator";
    String string3 = new String("using comparison operator");
     
    assertThat(string1 == string2).isTrue();
    assertThat(string1 == string3).isFalse();

In the example above, the first assertion is true because the two variables point to the same _String_ literal.

On the other hand, the second assertion is false because _string1_ is created with a literal and _string3_ is created using the _new_ operator – therefore they reference different objects.

### **2.2. Using _equals()_**

The _String_ class overrides the _equals()_ inherited from _Object._**This method compares two _Strings_ character by character, ignoring their address.**

It considers them equal if they are of the same length and the characters are in same order:
    
    
    String string1 = "using equals method";
    String string2 = "using equals method";
            
    String string3 = "using EQUALS method";
    String string4 = new String("using equals method");
    
    assertThat(string1.equals(string2)).isTrue();
    assertThat(string1.equals(string4)).isTrue();
    
    assertThat(string1.equals(null)).isFalse();
    assertThat(string1.equals(string3)).isFalse();

In this example, _string1, string2,_ and _string4_ variables are equal because they have the same case and value irrespective of their address.

For _string3_ the method returns _false,_ as it’s case sensitive.

Also, if any of the two strings is _null_ , then the method returns _false._

### **2.3. Using _equalsIgnoreCase()_**

The _equalsIgnoreCase()_ method returns a boolean value. As the name suggests this method **ignores casing in characters while comparing _Strings_** _:_
    
    
    String string1 = "using equals ignore case";
    String string2 = "USING EQUALS IGNORE CASE";
    
    assertThat(string1.equalsIgnoreCase(string2)).isTrue();

### **2.4. Using _compareTo()_**

The _compareTo()_ method returns an _int_ type value and**compares two _Strings_ character by character lexicographically** based on a dictionary or natural ordering.

This method returns 0 if two _Strings_ are equal _,_ a negative number if the first _String_ comes before the argument, and a number greater than zero if the first _String_ comes after the argument _String._

Let’s see an example:
    
    
    String author = "author";
    String book = "book";
    String duplicateBook = "book";
    
    assertThat(author.compareTo(book))
      .isEqualTo(-1);
    assertThat(book.compareTo(author))
      .isEqualTo(1);
    assertThat(duplicateBook.compareTo(book))
      .isEqualTo(0);

### **2.5. Using _compareToIgnoreCase()_**

The _compareToIgnoreCase()_ is similar to the previous method, except it ignores case:
    
    
    String author = "Author";
    String book = "book";
    String duplicateBook = "BOOK";
    
    assertThat(author.compareToIgnoreCase(book))
      .isEqualTo(-1);
    assertThat(book.compareToIgnoreCase(author))
      .isEqualTo(1);
    assertThat(duplicateBook.compareToIgnoreCase(book))
      .isEqualTo(0);

## **3._String_ Comparison With _Objects_ Class**

_Objects_ is a utility class which contains a static _equals()_ method, useful in this scenario – to compare two _Strings._

The method returns _true_ if two _Strings_ are equal by **first****comparing them using their address** i.e “ _==”_. Consequently, if both arguments are _null_ , it returns _true_ and if exactly one argument is _null_ , it returns false.

Otherwise, it then simply calls the _equals()_ method of the passed argument’s type’s class – which in our case is _String’s_ class _equals()_ method. This method is case sensitive because it internally calls _String_ class’s _equals()_ method.

Let’s test this:
    
    
    String string1 = "using objects equals";
    String string2 = "using objects equals";
    String string3 = new String("using objects equals");
    
    assertThat(Objects.equals(string1, string2)).isTrue();
    assertThat(Objects.equals(string1, string3)).isTrue();
    
    assertThat(Objects.equals(null, null)).isTrue();
    assertThat(Objects.equals(null, string1)).isFalse();

## **4._String_ Comparison With _Apache Commons_**

**The Apache Commons library contains a utility class called _StringUtils_ for _String-_ related operations**; this also has some very beneficial methods for _String_ comparison.

### **4.1. Using _equals()_ and _equalsIgnoreCase()_**

The _equals()_ method of _StringUtils_ class is an enhanced version of the _String_ class method _equals(),_ which also handles null values:
    
    
    assertThat(StringUtils.equals(null, null))
      .isTrue();
    assertThat(StringUtils.equals(null, "equals method"))
      .isFalse();
    assertThat(StringUtils.equals("equals method", "equals method"))
      .isTrue();
    assertThat(StringUtils.equals("equals method", "EQUALS METHOD"))
      .isFalse();

The _equalsIgnoreCase()_ method of _StringUtils_ returns a _boolean_ value. This works similarly to _equals(),_ except it ignores casing of characters in _Strings:_
    
    
    assertThat(StringUtils.equalsIgnoreCase("equals method", "equals method"))
      .isTrue();
    assertThat(StringUtils.equalsIgnoreCase("equals method", "EQUALS METHOD"))
      .isTrue();

### **4.2. Using _equalsAny()_ and _equalsAnyIgnoreCase()_**

The _equalsAny()_ method’s first argument is a _String_ and the second is a multi-args type _CharSequence._ The method returns _true_ if any of the other given _Strings_ match against the first _String_ case sensitively.

Otherwise, false is returned:
    
    
    assertThat(StringUtils.equalsAny(null, null, null))
      .isTrue();
    assertThat(StringUtils.equalsAny("equals any", "equals any", "any"))
      .isTrue();
    assertThat(StringUtils.equalsAny("equals any", null, "equals any"))
      .isTrue();
    assertThat(StringUtils.equalsAny(null, "equals", "any"))
      .isFalse();
    assertThat(StringUtils.equalsAny("equals any", "EQUALS ANY", "ANY"))
      .isFalse();

The _equalsAnyIgnoreCase()_ method works similarly to the _equalsAny()_ method, but also ignores casing:
    
    
    assertThat(StringUtils.equalsAnyIgnoreCase("ignore case", "IGNORE CASE", "any")).isTrue();

### **4.3. Using _compare()_ and _compareIgnoreCase()_**

The _compare()_ method in _StringUtils_ class is a **null-safe version of the _compareTo()_** method of _String_ class and handles _null_ values by **considering a _null_ value less than a _non-null_ value. **Two _null_ values are considered equal.

Furthermore, this method can be used to sort a list of _Strings_ with _null_ entries:
    
    
    assertThat(StringUtils.compare(null, null))
      .isEqualTo(0);
    assertThat(StringUtils.compare(null, "abc"))
      .isEqualTo(-1);
    assertThat(StringUtils.compare("abc", "bbc"))
      .isEqualTo(-1);
    assertThat(StringUtils.compare("bbc", "abc"))
      .isEqualTo(1);

The _compareIgnoreCase()_ method behaves similarly, except it ignores casing:
    
    
    assertThat(StringUtils.compareIgnoreCase("Abc", "bbc"))
      .isEqualTo(-1);
    assertThat(StringUtils.compareIgnoreCase("bbc", "ABC"))
      .isEqualTo(1);
    assertThat(StringUtils.compareIgnoreCase("abc", "ABC"))
      .isEqualTo(0);

The two methods can also be used with a _nullIsLess_ option. This is **a third _boolean_ argument which decides if null values should be considered less or not**.

A _null_ value is lower than another _String_ if _nullIsLess_ is true and higher if _nullIsLess_ is false.

Let’s try it out:
    
    
    assertThat(StringUtils.compare(null, "abc", true))
      .isEqualTo(-1);
    assertThat(StringUtils.compare(null, "abc", false))
      .isEqualTo(1);

The _compareIgnoreCase()_ method with a third _boolean_ argument work similarly, except by ignoring case.

## **5\. Conclusion**

In this quick tutorial, we discussed different ways of comparing _Strings._
