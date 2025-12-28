# Guide to Java Packages

## 1\. Introduction

In this quick tutorial, we’ll cover the basics of packages in Java. We’ll see how to create packages and access the types we place inside them.

We’ll also discuss naming conventions and how that relates to the underlying directory structure.

Finally, we’ll compile and run our packaged Java classes.

## 2\. Overview of Java Packages

In Java, we **use packages to group related classes, interfaces, and sub-packages**.

The main benefits of doing this are:

  * Making related types easier to find – packages usually contain types that are logically related
  * Avoiding naming conflicts – a package will help us to uniquely identify a class; for example, we could have a _com.baeldung.Application,_ as well as _com.example.Application_ classes
  * Controlling access – we can control visibility and access to types by combining packages and [access modifiers](/java-access-modifiers)



Next, let’s see how we can create and use Java packages.

## 3\. Creating a Package

To create a package, **we have to use the _package_ statement by adding it as the very first line of code in a file**.

Let’s place a type in a package named _com.baeldung.packages_ :
    
    
    package com.baeldung.packages;

**It’s highly recommended to place each new type in a package.** If we define types and don’t place them in a package, they will go in the _default_ or unnamed package. Using default packages comes with a few disadvantages:

  * We lose the benefits of having a package structure and we can’t have sub-packages
  * We can’t import the types in the default package from other packages
  * The [ _protected_ and _package-private_](/java-access-modifiers) access scopes would be meaningless



As the [Java language specification states](https://docs.oracle.com/javase/specs/jls/se14/html/jls-7.html#jls-7.4.2), unnamed packages are provided by the Java SE Platform principally for convenience when developing small or temporary applications or when just beginning development.

Therefore, **we should avoid using unnamed or default packages in real-world applications**.

### 3.1. Naming Conventions

In order to avoid packages with the same name, we follow some naming conventions:

  * we define our package **names in all lower case**
  * package names are period-delimited
  * names are also determined by **the company or organization that creates them**



To determine the package name based on an organization, we’ll typically start by reversing the company URL. After that, the naming convention is defined by the company and may include division names and project names.

For example, to make a package out of _www.baeldung.com_ , let’s reverse it:
    
    
    com.baeldung

We can then further define sub-packages of this, like _com.baeldung.packages_ or _com.baeldung.packages.domain._

### 3.2. Directory Structure

Packages in Java correspond with a directory structure.

**Each package and subpackage has its own directory.** So, for the package _com.baeldung.packages_ , we should have a directory structure of _com - > baeldung -> packages_.

Most IDE’s will help with creating this directory structure based on our package names, so we don’t have to create these by hand.

## 4\. Using Package Members

Let’s start by defining a class _TodoItem_ in a subpackage named _domain_ :
    
    
    package com.baeldung.packages.domain;
    
    public class TodoItem {
        private Long id;
        private String description;
        
        // standard getters and setters
    }

### 4.1. Imports

In order to use our _TodoItem_ class from a class in another package, we need to import it. Once it’s imported, we can access it by name.

**We can import a single type from a package or use an asterisk to import all of the types in a package.**

Let’s import the entire _domain_ subpackage:
    
    
    import com.baeldung.packages.domain.*;

Now, let’s import only the _TodoItem_ class:
    
    
    import com.baeldung.packages.domain.TodoItem;

The JDK and other Java libraries also come with their own packages. **We can import pre-existing classes that we want to use in our project in the same manner.**

For example, let’s import the Java core _List_ interface and _ArrayList_ class:
    
    
    import java.util.ArrayList;import java.util.List;

**We can then use these types in our application by simply using their name:**
    
    
    public class TodoList {
        private List<TodoItem> todoItems;
    
        public void addTodoItem(TodoItem todoItem) {
            if (todoItems == null) {
                todoItems = new ArrayList<TodoItem>();
            }
            todoItems.add(todoItem);
        }
    }

Here, we’ve used our new classes along with Java core classes, to create a _List_ of _ToDoItems._

### 4.2. Fully Qualified Name

Sometimes, we may be using two classes with the same name from different packages. For example, we might be using both _java.sql.Date_ and _java.util.Date_. **When we run into naming conflicts, we need to use a fully qualified class name for at least one of the classes.**

Let’s use _TodoItem_ with a fully qualified name:
    
    
    public class TodoList {
        private List<com.baeldung.packages.domain.TodoItem> todoItems;
    
        public void addTodoItem(com.baeldung.packages.domain.TodoItem todoItem) {
            if (todoItems == null) {
                todoItems = new ArrayList<com.baeldung.packages.domain.TodoItem>();
            }todoItems.add(todoItem);
        }
    
        // standard getters and setters
    }

## 5\. Compiling with  _javac_

When it’s time to compile our packaged classes, we need to remember our directory structure. Starting in the source folder, we need to tell _javac_ where to find our files.

We need to compile our _TodoItem_ class first because our _TodoList_ class depends on it.

Let’s start by opening a command line or terminal and navigating to our source directory.

Now, let’s compile our _com.baeldung.packages.domain.TodoItem_ class:
    
    
    > javac com/baeldung/packages/domain/TodoItem.java

If our class compiles cleanly, we’ll see no error messages and a file _TodoItem.class_ should appear in our _com/baeldung/packages/domain_ directory.

For types that reference types in other packages, we should use the _-classpath_ flag to tell the _javac_ command where to find the other compiled classes.

Now that our _TodoItem_ class is compiled, we can compile our  _TodoList_ and _TodoApp_ classes:
    
    
    >javac -classpath . com/baeldung/packages/*.java

Again, we should see no error messages and we should find two class files in our _com/baeldung/packages_ directory.

Let’s run our application using the fully qualified name of our _TodoApp_ class:
    
    
    >java com.baeldung.packages.TodoApp

Our output should look like this:

![packages](/wp-content/uploads/2018/12/packages.jpg)

## 6\. Conclusion

In this short article, we learned what a package is and why we should use them.

We discussed naming conventions and how packages relate to the directory structure. We also saw how to create and use packages.

Finally, we went over how to compile and run an application with packages using the _javac_ and _java_ commands.
