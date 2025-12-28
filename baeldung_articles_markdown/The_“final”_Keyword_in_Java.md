# The “final” Keyword in Java

## **1\. Overview**

While inheritance enables us to reuse existing code, sometimes we do need to **set limitations on extensibility** for various reasons; the _final_ keyword allows us to do exactly that.

In this tutorial, we’ll take a look at what the _final_ keyword means for classes, methods, and variables.

## **2._Final_ Classes**

**Classes marked as _final_ can’t be extended.** If we look at the code of Java core libraries, we’ll find many _final_ classes there. One example is the _String_ class.

Consider the situation if we can extend the _String_ class, override any of its methods, and substitute all the _String_ instances with the instances of our specific _String_ subclass.

The result of the operations over _String_ objects will then become unpredictable. And given that the _String_ class is used everywhere, it’s unacceptable. That’s why the _String_ class is marked as _final_.

Any attempt to inherit from a _final_ class will cause a compiler error. To demonstrate this, let’s create the _final_ class _Cat_ :
    
    
    public final class Cat {
    
        private int weight;
    
        // standard getter and setter
    }

And let’s try to extend it:
    
    
    public class BlackCat extends Cat {
    }

We’ll see the compiler error:
    
    
    The type BlackCat cannot subclass the final class Cat

Note that **the _final_ keyword in a class declaration doesn’t mean that the objects of this class are immutable**. We can change the fields of _Cat_ object freely:
    
    
    Cat cat = new Cat();
    cat.setWeight(1);
    
    assertEquals(1, cat.getWeight());
    

We just can’t extend it.

If we follow the rules of good design strictly, we should create and document a class carefully or declare it _final_ for safety reasons. However, we should use caution when creating _final_ classes.

Notice that making a class _final_ means that no other programmer can improve it. Imagine that we’re using a class and don’t have the source code for it, and there’s a problem with one method.

If the class is _final,_ we can’t extend it to override the method and fix the problem. In other words, we lose extensibility, one of the benefits of object-oriented programming.

## **3._Final_ Methods**

**Methods marked as _final_ cannot be overridden.** When we design a class and feel that a method shouldn’t be overridden, we can make this method _final_. We can also find many _final_ methods in Java core libraries.

Sometimes we don’t need to prohibit a class extension entirely, but only prevent overriding of some methods. A good example of this is the _Thread_ class. It’s legal to extend it and thus create a custom thread class. But its _isAlive()_ methods is _final_.

This method checks if a thread is alive. It’s impossible to override the _isAlive()_ method correctly for many reasons. One of them is that this method is native. Native code is implemented in another programming language and is often specific to the operating system and hardware it’s running on.

Let’s create a _Dog_ class and make its _sound()_ method _final_ :
    
    
    public class Dog {
        public final void sound() {
            // ...
        }
    }

Now let’s extend the _Dog_ class and try to override its _sound()_ method:
    
    
    public class BlackDog extends Dog {
        public void sound() {
        }
    }

We’ll see the compiler error:
    
    
    - overrides
    com.baeldung.finalkeyword.Dog.sound
    - Cannot override the final method from Dog
    sound() method is final and can’t be overridden

If some methods of our class are called by other methods, we should consider making the called methods _final_. Otherwise, overriding them can affect the work of callers and cause surprising results.

If our constructor calls other methods, we should generally declare these methods _final_ for the above reason.

What’s the difference between making all methods of the class _final_ and marking the class itself _final_? In the first case, we can extend the class and add new methods to it.

In the second case, we can’t do this.

## **4._Final_ Variables**

**Variables marked as _final_ can’t be reassigned.** Once a _final_ variable is initialized, it can’t be altered.

### **4.1._Final_ Primitive Variables**

Let’s declare a primitive _final_ variable _i,_ then assign 1 to it.

And let’s try to assign a value of 2 to it:
    
    
    public void whenFinalVariableAssign_thenOnlyOnce() {
        final int i = 1;
        //...
        i=2;
    }

The compiler says:
    
    
    The final local variable i may already have been assigned

### **4.2._Final_ Reference Variables**

If we have a _final_ reference variable, we can’t reassign it either. But **this doesn’t mean that the object it refers to is immutable**. We can change the properties of this object freely.

To demonstrate this, let’s declare the _final_ reference variable _cat_ and initialize it:
    
    
    final Cat cat = new Cat();

If we try to reassign it we’ll see a compiler error:
    
    
    The final local variable cat cannot be assigned. It must be blank and not using a compound assignment

But we can change the properties of _Cat_ instance:
    
    
    cat.setWeight(5);
    
    assertEquals(5, cat.getWeight());

### **4.3._Final_ Fields**

**_Final_ fields can be either constants or write-once fields.** To distinguish them, we should ask a question — would we include this field if we were to serialize the object? If no, then it’s not part of the object, but a constant.

Note that according to naming conventions, class constants should be uppercase, with components separated by underscore (“_”) characters:
    
    
    static final int MAX_WIDTH = 999;

Note that **any _final_ field must be initialized before the constructor completes**.

For _static final_ fields, this means that we can initialize them:

  * upon declaration as shown in the above example
  * in the static initializer block



For instance _final_ fields, this means that we can initialize them:

  * upon declaration
  * in the instance initializer block
  * in the constructor



Otherwise, the compiler will give us an error.

### **4.4._Final_ Parameters**

The _final_ keyword is also legal to put before method parameters. **A _final_ parameter can’t be changed inside a method**:
    
    
    public void methodWithFinalArguments(final int x) {
        x=1;
    }

The above assignment causes the compiler error:
    
    
    The final local variable x cannot be assigned. It must be blank and not using a compound assignment

## **5\. Conclusion**

In this article, we learned what the _final_ keyword means for classes, methods, and variables. Although we may not use the _final_ keyword often in our internal code, it may be a good design solution.
