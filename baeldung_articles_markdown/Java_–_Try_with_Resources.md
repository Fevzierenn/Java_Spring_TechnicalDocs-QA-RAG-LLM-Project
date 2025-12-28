# Java – Try with Resources

## **1\. Overview**

Support for _try-with-resources_ — introduced in Java 7 — allows us to declare resources to be used in a _try_ block with the assurance that the resources will be closed after the execution of that block.

The resources declared need to implement the _AutoCloseable_ interface.

## **2\. Using _try-with-resources_**

Simply put, to be auto-closed, a resource has to be declared inside the _try_ :
    
    
    try (PrintWriter writer = new PrintWriter(new File("test.txt"))) {
        writer.println("Hello World");
    }
    

## **3\. Replacing _try_ – _catch-finally_ With _try-with-resources_**

The simple and obvious way to use the new _try-with-resources_ functionality is to replace the traditional and verbose _try-catch-finally_ block.

Let’s compare the following code samples.

The first is a typical _try-catch-finally_ block:
    
    
    Scanner scanner = null;
    try {
        scanner = new Scanner(new File("test.txt"));
        while (scanner.hasNext()) {
            System.out.println(scanner.nextLine());
        }
    } catch (FileNotFoundException e) {
        e.printStackTrace();
    } finally {
        if (scanner != null) {
            scanner.close();
        }
    }

And here’s the new super succinct solution using _try-with-resources_ :
    
    
    try (Scanner scanner = new Scanner(new File("test.txt"))) {
        while (scanner.hasNext()) {
            System.out.println(scanner.nextLine());
        }
    } catch (FileNotFoundException fnfe) {
        fnfe.printStackTrace();
    }

Here’s where to further explore [the  _Scanner_ class](/java-scanner).

## **4._try-with-resources_ With Multiple Resources**

We can declare multiple resources just fine in a _try-with-resources_ block by separating them with a semicolon:
    
    
    try (Scanner scanner = new Scanner(new File("testRead.txt"));
        PrintWriter writer = new PrintWriter(new File("testWrite.txt"))) {
        while (scanner.hasNext()) {
    	writer.print(scanner.nextLine());
        }
    }

## **5\. A Custom Resource With** _**AutoCloseable** _

To construct a custom resource that will be correctly handled by a _try-with-resources_ block, the class should implement the _Closeable_ or _AutoCloseable_ interfaces and override the _close_ method:
    
    
    public class MyResource implements AutoCloseable {
        @Override
        public void close() throws Exception {
            System.out.println("Closed MyResource");
        }
    }

## **6\. Resource Closing Order**

Resources that were defined/acquired first will be closed last. Let’s look at an example of this behavior:

**Resource 1:**
    
    
    public class AutoCloseableResourcesFirst implements AutoCloseable {
    
        public AutoCloseableResourcesFirst() {
            System.out.println("Constructor -&gt; AutoCloseableResources_First");
        }
    
        public void doSomething() {
            System.out.println("Something -&gt; AutoCloseableResources_First");
        }
    
        @Override
        public void close() throws Exception {
            System.out.println("Closed AutoCloseableResources_First");
        }
    }
    

**Resource 2:**
    
    
    public class AutoCloseableResourcesSecond implements AutoCloseable {
    
        public AutoCloseableResourcesSecond() {
            System.out.println("Constructor -&gt; AutoCloseableResources_Second");
        }
    
        public void doSomething() {
            System.out.println("Something -&gt; AutoCloseableResources_Second");
        }
    
        @Override
        public void close() throws Exception {
            System.out.println("Closed AutoCloseableResources_Second");
        }
    }

**Code:**
    
    
    private void orderOfClosingResources() throws Exception {
        try (AutoCloseableResourcesFirst af = new AutoCloseableResourcesFirst();
            AutoCloseableResourcesSecond as = new AutoCloseableResourcesSecond()) {
    
            af.doSomething();
            as.doSomething();
        }
    }
    

**Output:**

_Constructor - > AutoCloseableResources_First_  
_Constructor - > AutoCloseableResources_Second_  
_Something - > AutoCloseableResources_First_  
_Something - > AutoCloseableResources_Second_  
_Closed AutoCloseableResources_Second_  
_Closed AutoCloseableResources_First_

## **7._catch_ and _finally_**

A _try-with-resources_ block **can still have the _catch_ and _finally_ blocks**, which will work in the same way as with a traditional _try_ block.

## 8\. Java 9 – Effectively Final __ Variables

Before Java 9, we could only use fresh variables inside a _try-with-resources_ block:
    
    
    try (Scanner scanner = new Scanner(new File("testRead.txt")); 
        PrintWriter writer = new PrintWriter(new File("testWrite.txt"))) { 
        // omitted
    }

As shown above, this was especially verbose when declaring multiple resources. As of Java 9 and as part of [JEP 213](https://openjdk.java.net/jeps/213), **we can now use[ _final_ or even effectively final](/java-effectively-final) variables inside a  _try-with-resources_ block**:
    
    
    final Scanner scanner = new Scanner(new File("testRead.txt"));
    PrintWriter writer = new PrintWriter(new File("testWrite.txt"))
    try (scanner;writer) { 
        // omitted
    }

Put simply, a variable is effectively final if it doesn’t change after the first assignment, even though it’s not explicitly marked as  _final_.

As shown above, the  _scanner_ variable is declared  _final_ explicitly, so we can use it with the  _try-with-resources_ block. Although the  _writer_ variable is not explicitly  _final,_ it doesn’t change after the first assignment. So, we can to use the _writer_ variable too.

## **9\. Conclusion**

In this article, we discussed how to use try-with-resources and how to replace _try_ , _catch_ , and _finally_ with try-with-resources.

We also looked at building custom resources with _AutoCloseable_ and the order in which resources are closed.
