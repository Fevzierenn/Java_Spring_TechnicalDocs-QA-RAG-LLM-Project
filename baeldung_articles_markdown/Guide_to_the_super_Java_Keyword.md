# Guide to the super Java Keyword

## **1\. Introduction**

In this quick tutorial, **we’ll take a look at the _super_ Java keyword.**

**Simply put, we can use the _super_ keyword to access the parent class. **

Let’s explore the applications of the core keyword in the language.

## **2\. The _super_ Keyword With Constructors**

**We can use _super()_ to call the parent default constructor**. It should be the first statement in a constructor.

In our example, we use _super(message)_ with the _String_ argument:
    
    
    public class SuperSub extends SuperBase {
    
        public SuperSub(String message) {
            super(message);
        }
    }

Let’s create a child class instance and see what’s happening behind:
    
    
    SuperSub child = new SuperSub("message from the child class");

The _new_ keyword invokes the constructor of the _SuperSub_ , which itself calls the parent constructor first and passes the _String_ argument to it.

## **3\. Accessing Parent Class Variables**

Let’s create a parent class with the _message_ instance variable:
    
    
    public class SuperBase {
        String message = "super class";
    
        // default constructor
    
        public SuperBase(String message) {
            this.message = message;
        }
    }

Now, we create a child class with the variable of the same name:
    
    
    public class SuperSub extends SuperBase {
    
        String message = "child class";
    
        public void getParentMessage() {
            System.out.println(super.message);
        }
    }

We can access the parent variable from the child class by using the  _super_ keyword.

## **4\. The _super_ Keyword With Method Overriding**

Before going further, we advise reviewing our [method overriding](/java-method-overload-override) guide.

Let’s add an instance method to our parent class:
    
    
    public class SuperBase {
    
        String message = "super class";
    
        public void printMessage() {
            System.out.println(message);
        }
    }

And override the _printMessage()_ method in our child class:
    
    
    public class SuperSub extends SuperBase {
    
        String message = "child class";
    
        public SuperSub() {
            super.printMessage();
            printMessage();
        }
    
        public void printMessage() {
            System.out.println(message);
        }
    }

**We can use the _super_ to access the overridden method from the child class**. The _super.printMessage()_ in constructor calls the parent method from _SuperBase_.

## **5\. Conclusion**

In this article, we explored the  _super_ keyword.
