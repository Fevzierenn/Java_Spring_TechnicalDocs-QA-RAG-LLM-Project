# Guide to the this Java Keyword

## **1\. Introduction**

In this tutorial, **we’ll take a look at the _this_ Java keyword.**

In Java, **_this_ keyword is a reference to the current object whose method is being called**.

Let’s explore how and when we can use the keyword.

## **2\. Disambiguating Field Shadowing**

**The keyword is useful for disambiguating instance variables from local parameters**. The most common reason is when we have constructor parameters with the same name as instance fields:
    
    
    public class KeywordTest {
    
        private String name;
        private int age;
        
        public KeywordTest(String name, int age) {
            this.name = name;
            this.age = age;
        }
    }

As we can see here, we’re using  _this_ with the _name_ and _age_ instance fields – to distinguish them from parameters.

Another usage is to use _this_ with the parameter hiding or shadowing in the local scope. An example of use can be found in the [Variable and Method Hiding](/java-variable-method-hiding) article.

## **3\. Referencing Constructors of the Same Class**

**From a constructor, we can use _this()_ to call a different constructor of the same class**. Here, we use  _this()_ for the constructor chaining to reduce the code usage.

The most common use case is to call a default constructor from the parameterized constructor:
    
    
    public KeywordTest(String name, int age) {
        this();
        
        // the rest of the code
    }

Or, we can call the parameterized constructor from the no argument constructor and pass some arguments:
    
    
    public KeywordTest() {
        this("John", 27);
    }

Note, that _this()_ should be the first statement in the constructor, otherwise the compilation error will occur.

## **4\. Passing _this_ as a Parameter**

Here we have _printInstance()_ method, where the _this Keyword_ argument is defined:
    
    
    public KeywordTest() {
        printInstance(this);
    }
    
    public void printInstance(KeywordTest thisKeyword) {
        System.out.println(thisKeyword);
    }

Inside the constructor, we invoke _printInstance()_ method. With _this_ , we pass a reference to the current instance.

## **5\. Returning _this_**

**We can also use _this_ keyword to return the current class instance** from the method.

To not duplicate the code, here’s a full practical example of how it’s implemented in the [builder design pattern](/creational-design-patterns).

## **6\. The _this_ Keyword Within the Inner Class**

We also use _this_ to access the outer class instance from within the inner class:
    
    
    public class KeywordTest {
    
        private String name;
    
        class ThisInnerClass {
    
            boolean isInnerClass = true;
    
            public ThisInnerClass() {
                KeywordTest thisKeyword = KeywordTest.this;
                String outerString = KeywordTest.this.name;
            }
        }
    }

Here, inside the constructor, we can get a reference to the _KeywordTest_ instance with the _KeywordTest.this_ call _._ We can go even deeper and access the instance variables like _KeywordTest.this.name_ field.

## **7\. Conclusion**

In this article, we explored the _this_ keyword in Java.
