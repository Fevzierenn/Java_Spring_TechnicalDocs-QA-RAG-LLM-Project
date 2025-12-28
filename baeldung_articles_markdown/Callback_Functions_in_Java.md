# Callback Functions in Java

## 1\. Overview

A callback function is a function passed as an argument to another function and executed when that function completes or some event happens. In most programming languages, callback functions are especially useful when we’re working with asynchronous code.

In this article, we’ll learn the practical use cases of callback functions in Java and how we can implement them.

## 2\. Implementing Callback Functions

Generally, we can create a callback function in Java by exposing an interface and accepting its implementation as a parameter. Such a callback can be called synchronously or asynchronously.

### 2.1. Synchronous Callbacks

**Synchronous operations are those where one task needs to complete before another one starts**.

For example, imagine such an interface:
    
    
    public interface EventListener {
    
        String onTrigger();
    }

The above snippet declares an _EventListener_ interface with an _onTrigger()_ method with a _String_ return type. This will be our callback.

Next, let’s declare a concrete class that implements this interface:
    
    
    public class SynchronousEventListenerImpl implements EventListener {
    
        @Override
        public String onTrigger(){
            return "Synchronously running callback function";
        }
    }

The _SynchronousEventListenerImpl_ class implements the _EventListener_ interface, as shown above.

Next, let’s create a _SynchronousEventConsumer_ class that composes an instance of the _EventListener_ interface and invokes its _onTrigger()_ method:
    
    
    public class SynchronousEventConsumer {
    
        private final EventListener eventListener;
    
        // constructor
    
        public String doSynchronousOperation(){
            System.out.println("Performing callback before synchronous Task");
            // any other custom operations
               return eventListener.onTrigger();
        }
    }

The _SyncronousEventConsumer_ class has an _EventListener_ property that it initializes through its constructor. When the _doSynchronousOperation()_ method is invoked, it returns the value obtained from the _onTrigger()_ method belonging to the _EventListener_.

Let’s write a test to demonstrate that the _doSynchronousOperation()_ method invokes the _onTrigger()_ method of the listener variable and obtains its returned value:
    
    
    EventListener listener = new SynchronousEventListenerImpl();
    SynchronousEventConsumer synchronousEventConsumer = new SynchronousEventConsumer(listener);
    String result = synchronousEventConsumer.doSynchronousOperation();
    
    assertNotNull(result);
    assertEquals("Synchronously running callback function", result);

### 2.2. Asynchronous Callback Function

[Asynchronous operations](/java-asynchronous-programming) are operations that run in parallel to one another. Unlike synchronous operations illustrated in the previous section, **asynchronous tasks are non-blocking**. They don’t wait for one another before performing their operations. Let’s update the _EventListener_ interface to illustrate an asynchronous callback function in Java:
    
    
    public interface EventListener {
    
        String onTrigger();
    
        void respondToTrigger();
    }

Next, let’s create an implementation for the revised _EventListener_ :
    
    
    public class AsynchronousEventListenerImpl implements EventListener {
    
        @Override
        public String onTrigger(){
            respondToTrigger();
            return "Asynchronously running callback function";
        }
        @Override
        public void respondToTrigger(){
            System.out.println("This is a side effect of the asynchronous trigger.");
        }
    }

The above class implements the _EventListener_ interface we declared in the previous section and returns a _String_ literal in its overridden _onTrigger()_ method.

Next, we declare the class that asynchronously runs the _onTrigger()_ method as a callback function:
    
    
    public class AsynchronousEventConsumer{
    
        private EventListener listener;
    
        public AsynchronousEventConsumer(EventListener listener) {
            this.listener = listener;
        }
    
        public void doAsynchronousOperation(){
            System.out.println("Performing operation in Asynchronous Task");
    
            new Thread(() -> listener.onTrigger()).start();
        }
    }

The _AsynchronousEventConsumer_ class above declares a _doAsynchronousOperation()_ method that implicitly invokes the _onTrigger()_ method of the _EventListener_ in a new thread.

**Note that this approach of creating a new _Thread_ for each method call is an anti-pattern and is used here for demonstration purposes. Production-ready code should rely on properly sized and tuned thread pools.** Check out some of our other articles to learn more about [concurrency in Java](/java-concurrency).

Let’s verify that the program indeed invokes the _onTrigger()_ method from within the _doAsynchronousOperation()_ method:
    
    
    EventListener listener = Mockito.mock(AsynchronousEventListenerImpl.class);
    AsynchronousEventConsumer synchronousEventListenerConsumer = new AsynchronousEventConsumer(listener);
    synchronousEventListenerConsumer.doAsynchronousOperation();
    
    verify(listener, timeout(1000).times(1)).onTrigger();

### 2.3. Using Consumers

[_Consumers_](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/function/Consumer.html) are functional interfaces that are commonly used in [functional programming](/java-functional-programming) in Java. Implementations of the interface accept an argument and perform an operation with the provided argument but don’t return a result.

**Using _Consumers_ , we can pass a method as an argument to another method. This allows us to invoke and run the operations of the inner method from within the parent method**.

Let’s consider a method that increases the value of a given number represented as age. We can pass the initial age as the first argument and a _Consumer_ that will serve as the second method to increment the age.

Here’s an illustration of how we can implement this as a callback function using _Consumers_ :
    
    
    public class ConsumerCallback {
        public void getAge(int initialAge, Consumer<Integer> callback) {
            callback.accept(initialAge);
        }
    
        public void increaseAge(int initialAge, int ageDifference, Consumer<Integer> callback) {
            System.out.println("===== Increase age ====");
    
            int newAge = initialAge + ageDifference;
            callback.accept(newAge);
        }
    }

In the _getAge()_ method above, we pass the _initialAge_ variable as an argument to the _callback.accept()_ method. The _accept()_ method takes an argument (in this case, an integer), and then performs any operation on the input through the method or function passed to the _getAge()_ method as an argument at runtime.

The _increaseAge()_ method will perform the increment on the _initialAge_ variable. It adds the value of the _initialAge_ to the _ageDifference_ and then passes the result to the _accept()_ method of the third argument, the _Consumer_.

Here’s a demonstration of the above implementations:
    
    
    ConsumerCallback consumerCallback = new ConsumerCallback();
    int ageDifference = 10;
    AtomicInteger newAge1 = new AtomicInteger();
    int initialAge = 20;
    consumerCallback.getAge(initialAge, (initialAge1) -> {
        consumerCallback.increaseAge(initialAge, ageDifference, (newAge) -> {
            System.out.printf("New age ==> %s", newAge);
            newAge1.set(newAge);
         });
    });
    assertEquals(initialAge + ageDifference, newAge1.get());

In the above snippet, we pass a function to the _getAge()_ method. This function invokes the _increaseAge()_ method and asserts that the value of the _newAge_ variable equals the sum of the _initialAge_ and _ageDifference_.

The callback functions in this context are the functions passed to the _getAge()_ and _increaseAge()_ methods. These functions are triggered to perform any custom operation after each of the _getAge()_ and _increaseAge()_ methods have completed their tasks.

## 3\. Conclusion

In this article, we learned about the concept of callback functions in Java. We demonstrated how we could synchronously and asynchronously implement callback functions through interfaces. We also learned how to use the Java _Consumer_ functional interface to perform callback operations in Java.
