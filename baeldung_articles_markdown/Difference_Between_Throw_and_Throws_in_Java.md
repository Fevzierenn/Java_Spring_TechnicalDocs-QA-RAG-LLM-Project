# Difference Between Throw and Throws in Java

## 1\. Introduction

In this tutorial, we’ll take a look at the _throw_ and _throws_ in Java. We’ll explain when we should use each of them.

Next, we’ll show some examples of their basic usage.

## 2\. _Throw_ and _Throws_

Let’s start with a quick introduction. These keywords are related to exception-handling. **Exceptions are raised when the normal of flow of our application is disrupted.**

There may be a lot of reasons. A user could send the wrong input data. We can lose a connection or other unexpected situation may occur. Good exceptions handling is a key to keep our application working after an appearance of those unpleasant moments.

**We use _throw_ keyword to explicitly throw an exception** from the code. It may be any method or static block. This exception must be a subclass of _Throwable._ Also, it can be a  _Throwable_ itself. We can’t throw multiple exceptions with a single _throw_.

_Throws_ keyword can be placed in the method declaration. **It denotes which exceptions can be thrown from this method.** We must handle these exceptions with try-catch.

**These two keywords aren’t interchangeable!**

## 3\. _Throw_ in Java

Let’s take a look at a basic example with throwing an exception from the method.

First of all, imagine that we’re writing a simple calculator. One of the basic arithmetic operations is division. Due to that, we were asked to implement this feature:
    
    
    public double divide(double a, double b) {
        return a / b;
    }

Because we can’t divide by zero, we need to add some modifications to our existing code. Seems like it’s a good moment for raising an exception.

Let’s do this:
    
    
    public double divide(double a, double b) {
        if (b == 0) {
            throw new ArithmeticException("Divider cannot be equal to zero!");
        }
        return a / b;
    }

As you can see, we have used _ArithmeticException_ with perfectly fits our needs. We can pass a single _String_ constructor parameter which is exception message.

### 3.1. Good Practices

**We should always prefer the most specific exception.** We need to find a class that fits the best for our exceptional event. For example, throw _NumberFormatException_ instead of _IllegalArgumentException._ We should avoid throwing an unspecific _Exception_.

For example, there is an _Integer_ class in _java.lang_ package. Let’s take a look at the one of the factory method declaration:
    
    
    public static Integer valueOf(String s) throws NumberFormatException
    

It’s a static factory method which creates _Integer_ instance from _String._ In case of wrong input _String_ , the method will throw _NumberFormatException._

**A good idea is to define our own, more descriptive exception.** In our _Calculator_ class that could be for example _DivideByZeroException._

Let’s take a look at sample implementation:
    
    
    public class DivideByZeroException extends RuntimeException {
    
        public DivideByZeroException(String message) {
            super(message);
        }
    }

### 3.2. Wrapping an Existing Exception

Sometimes we want to wrap an existing exception into the exception defined by us.

Let’s start with defining our own exception:
    
    
    public class DataAcessException extends RuntimeException {
        
        public DataAcessException(String message, Throwable cause) {
            super(message, cause);
        }
    }

The constructor takes two parameters: exception message, and a cause, which may be any subclass of _Throwable._

Let’s write a fake implementation for _findAll()_ function:
    
    
    public List<String> findAll() throws SQLException {
        throw new SQLException();
    }

Now, in _SimpleService_ let’s call a repository function, which can result in _SQLException:_
    
    
    public void wrappingException() {
        try {
            personRepository.findAll();
        } catch (SQLException e) {
            throw new DataAccessException("SQL Exception", e);
        }
    }

We are re-throwing _SQLException_ wrapped into our own exception called _DataAccessException._ Everything is verified by the following test:
    
    
    @Test
    void whenSQLExceptionIsThrown_thenShouldBeRethrownWithWrappedException() {
        assertThrows(DataAccessException.class,
          () -> simpleService.wrappingException());
    }

There are two reasons to do this. First of all, we use exception wrapping, because the rest of the code does not need to to know about every possible exception in the system.

Also higher level components do not need to know about bottom level components, nor the exceptions they throw.

### 3.3. Multi-Catch with Java

Sometimes, the methods that we use can throw many of different exceptions.

Let’s take a look at more extensive try-catch block:
    
    
    try {
        tryCatch.execute();
    } catch (ConnectionException | SocketException ex) {
        System.out.println("IOException");
    } catch (Exception ex) {
        System.out.println("General exception");
    }

The _execute_ method can throw three exceptions:  _SocketException, ConnectionException, Exception._ The first catch block will catch _ConnectionException_ or _SocketException_. The second catch block would catch  _Exception_ or any other subclass of _Exception._ Remember, that **we should always catch a more detailed exception first.**

We can swap the order of our catch blocks. Then, we’d never catch  _SocketException_ and _ConnectionException_ because everything will go to the catch with _Exception_.

## 4\. _Throws_ in Java

We add _throws_ to the method declaration.

Let’s take a look at one of our previous method declaration:
    
    
    public static void execute() throws SocketException, ConnectionException, Exception

**The method may throw multiple exceptions.** They are comma-separated at the end of a method declaration. We can put both, checked and unchecked exceptions in the  _throws._ We have described the difference between them below.

### 4.1. Checked and Unchecked Exceptions

**A checked exception means that it’s checked at the compile time.** Note, that we must handle this exception. Otherwise, a method must specify an exception by using _throws_ keyword.

The most common checked exceptions are  _IOException, FileNotFoundException, ParseException. FileNotFoundException_ may be thrown when we create _FileInputStream_ from _File._

There’s a short example:
    
    
    File file = new File("not_existing_file.txt");
    try {
        FileInputStream stream = new FileInputStream(file);
    } catch (FileNotFoundException e) {
        e.printStackTrace();
    }

We can avoid using try-catch block by adding _throws_ to the method declaration:
    
    
    private static void uncheckedException() throws FileNotFoundException {
        File file = new File("not_existing_file.txt");
        FileInputStream stream = new FileInputStream(file);
    }

Unfortunately, a higher level function still has to handle this exception. Otherwise, we have to put this exception in method declaration with _throws keyword._

As the opposite, **unchecked exceptions aren’t checked at the compile time.**

The most common unchecked exceptions are:  _ArrayIndexOutOfBoundsException, IllegalArgumentException, NullPointerException._

**Unchecked exceptions are thrown during runtime.** The following code will throw a _NullPointerException._ Probably it’s one of the most common exceptions in Java.

Calling a method on a null reference will result in this exception:
    
    
    public void runtimeNullPointerException() {
        String a = null;
        a.length();
    }

Let’s verify this behavior in the test:
    
    
    @Test
    void whenCalled_thenNullPointerExceptionIsThrown() {
        assertThrows(NullPointerException.class,
          () -> simpleService.runtimeNullPointerException());
    }

Please remember that this code and test does not many any sense. It’s only for learning purposes to explain runtime exceptions.

In Java, every subclass of _Error_ and _RuntimeException_ is an unchecked exception. A checked exception is everything else under the _Throwable_ class.

## 5\. Conclusion

In this article, we’ve discussed the difference between two Java keywords: _throw_ and _throws._ We’ve gone through the basic usage and talked a little about good practices _._ Then we’ve talked about checked and unchecked exceptions.

If you want to go deeper into Exception handling in Java, please take a look at our article [about Java exceptions](/java-exceptions).
