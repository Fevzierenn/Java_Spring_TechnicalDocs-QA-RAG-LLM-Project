# A Guide to Java Modularity

## **1\. Overview**

Java 9 introduces a new level of abstraction above packages, formally known as the Java Platform Module System (JPMS), or “Modules” for short.

In this tutorial, we’ll go through the new system and discuss its various aspects.

We’ll also build a simple project to demonstrate all concepts we’ll be learning in this guide.

## **2\. What’s a Module?**

First of all, we need to understand what a module is before we can understand how to use them.

**A Module is a group of closely related packages and resources along with a new module descriptor file.**

In other words, it’s a “package of Java Packages” abstraction that allows us to make our code even more reusable.

### **2.1. Packages**

The packages inside a module are identical to the Java packages we’ve been using since the inception of Java.

When we create a module, **we organize the code internally in packages just like we previously did with any other project.**

Aside from organizing our code, packages are used to determine what code is publicly accessible outside of the module. We’ll spend more time talking about this later in the article.

### **2.2. Resources**

**Each module is responsible for its resources, like media or configuration files.**

Previously we’d put all resources into the root level of our project and manually manage which resources belonged to different parts of the application.

With modules, we can ship required images and XML files with the module that needs it, making our projects much easier to manage.

### **2.3. Module Descriptor**

When we create a module, we include a descriptor file that defines several aspects of our new module:

  * **Name** – the name of our module
  * **Dependencies** – a list of other modules that this module depends on
  * **Public Packages** – a list of all packages we want accessible from outside the module
  * **Services Offered** – we can provide service implementations that can be consumed by other modules
  * **Services Consumed** – allows the current module to be a consumer of a service
  * **Reflection Permissions** – explicitly allows other classes to use reflection to access the private members of a package



The module naming rules are similar to how we name packages (dots are allowed, dashes are not). It’s very common to do either project-style (my.module) or Reverse-DNS (_com.baeldung.mymodule_) style names. We’ll use project-style in this guide.

**We need to list all packages we want to be public because by default all packages are module private.**

The same is true for reflection. By default, we cannot use reflection on classes we import from another module.

Later in the article, we’ll look at examples of how to use the module descriptor file.

### **2.4. Module Types**

There are four types of modules in the new module system:

  * **System Modules __** – These are the modules listed when we run the _list-modules_ command, which we’ll detail in the next chapter. They include the Java SE and JDK modules.
  * **Application Modules** – These modules are what we usually want to build when we decide to use Modules. They are named and defined in the compiled  _module-info.class_ file included in the assembled JAR.
  * **Automatic Modules** – We can include unofficial modules by adding existing JAR files to the module path. The name of the module will be derived from the name of the JAR. Automatic modules will have full read access to every other module loaded by the path.
  * **Unnamed Module** – When a class or JAR is loaded onto the classpath, but not the module path, it’s automatically added to the unnamed module. It’s a catch-all module to maintain backward compatibility with previously-written Java code.



### **2.5. Distribution**

Modules can be distributed one of two ways: as a JAR file or as an “exploded” compiled project. This, of course, is the same as any other Java project so it should come as no surprise.

We can create multi-module projects comprised of a “main application” and several library modules.

**We have to be careful though because we can only have one module per JAR file.**

When we set up our build file, we need to make sure to bundle each module in our project as a separate jar.

## **3\. Default Modules**

When we install Java 9, we can see that the JDK now has a new structure.

They have taken all the original packages and moved them into the new module system.

We can see what these modules are by typing into the command line:
    
    
    java --list-modules

These modules are split into four major groups:  _java, javafx, jdk,_ and  _Oracle_.

_java_ modules are the implementation classes for the core SE Language Specification.

_javafx_ modules are the FX UI libraries.

**Anything needed by the JDK itself is kept in the _jdk_ modules.**

And finally, **anything that is Oracle-specific is in the _oracle_ modules.**

## **4\. Module Declarations**

**To set up a module, we need to put a special file at the root of our packages named _module-info.java_.**

This file is known as the module descriptor and contains all of the data needed to build and use our new module.

We construct the module with a declaration whose body is either empty or made up of module directives:
    
    
    module myModuleName {
        // all directives are optional
    }

We start the module declaration with the _module_ keyword, and we follow that with the name of the module.

The module will work with this declaration, but we’ll commonly need more information.

That is where the module directives come in.

### **4.1. Requires**

Our first directive is  _requires_. This module directive allows us to declare module dependencies:
    
    
    module my.module {
        requires module.name;
    }

Now,  _my.module_ has **both a runtime and a compile-time dependency** on _module.name_.

And all public types exported from a dependency are accessible by our module when we use this directive.

### **4.2. Requires Static**

Sometimes we write code that references another module, but that users of our library will never want to use.

For instance, we might write a utility function that pretty-prints our internal state when another logging module is present. But, not every consumer of our library will want this functionality, and they don’t want to include an extra logging library.

In these cases, we want to use an optional dependency. By using the  _requires static_ directive, we create a compile-time-only dependency:
    
    
    module my.module {
        requires static module.name;
    }

### **4.3. Requires Transitive**

We commonly work with libraries to make our lives easier.

But, we need to make sure that any module that brings in our code will also bring in these extra ‘transitive’ dependencies or they won’t work.

Luckily, we can use the  _requires transitive_ directive to force any downstream consumers also to read our required dependencies:
    
    
    module my.module {
        requires transitive module.name;
    }

Now, when a developer _requires my.module_ , they won’t also have also to say  _requires module.name_ for our module to still work.

### **4.4. Exports**

**By default, a module doesn’t expose any of its API to other modules.** This  _strong encapsulation_ was one of the key motivators for creating the module system in the first place.

Our code is significantly more secure, but now we need to explicitly open our API up to the world if we want it to be usable.

**We use the _exports_ directive to expose all public members of the named package:**
    
    
    module my.module {
        exports com.my.package.name;
    }

Now, when someone does  _requires my.module_ , they will have access to the public types in our  _com.my.package.name_ package, but not any other package.

### **4.5. Exports … To**

**We can use _exports…to_ to open up our public classes to the world.**

But, what if we don’t want the entire world to access our API?

**We can restrict which modules have access to our APIs using the _exports…to_ directive.**

Similar to the  _exports_ directive, we declare a package as exported. But, we also list which modules we are allowing to import this package as a _requires_. Let’s see what this looks like:
    
    
    module my.module {
        export com.my.package.name to com.specific.package;
    }

### **4.6. Uses**

A  _service_ is an implementation of a specific interface or abstract class that can be  _consumed_ by other classes.

**We designate the services our module consumes with the _uses_ directive.**

Note that **the class name we _use_ is either the interface or abstract class of the service, not the implementation class**:
    
    
    module my.module {
        uses class.name;
    }

We should note here that there’s a difference between a  _requires_ directive and the  _uses_ directive.

We might _require_ a module that provides a service we want to consume, but that service implements an interface from one of its transitive dependencies.

Instead of forcing our module to require  _all_ transitive dependencies just in case, we use the  _uses_ directive to add the required interface to the module path.

### **4.7. Provides … With**

**A module can also be a _service provider_ that other modules can consume.**

The first part of the directive is the  _provides_ keyword. Here is where we put the interface or abstract class name.

Next, we have the  _with_ directive where we provide the implementation class name that either _implements_ the interface or  _extends_ the abstract class.

Here’s what it looks like put together:
    
    
    module my.module {
        provides MyInterface with MyInterfaceImpl;
    }

### **4.8. Open**

We mentioned earlier that encapsulation was a driving motivator for the design of this module system.

Before Java 9, it was possible to use reflection to examine every type and member in a package, even the  _private_ ones. Nothing was truly encapsulated, which can open up all kinds of problems for developers of the libraries.

Because Java 9 enforces  _strong encapsulation_ , **we now have to explicitly grant permission for other modules to reflect on our classes.**

If we want to continue to allow full reflection as older versions of Java did, we can simply  _open_ the entire module up:
    
    
    open module my.module {
    }

### **4.9. Opens**

If we need to allow reflection of private types, but we don’t want all of our code exposed, **we can use the _opens_ directive to expose specific packages.**

But remember, this will open the package up to the entire world, so make sure that is what you want:
    
    
    module my.module {
      opens com.my.package;
    }

### **4.10. Opens … To**

Okay, so reflection is great sometimes, but we still want as much security as we can get from  _encapsulation_. **We can selectively open our packages to a pre-approved list of modules, in this case, using the _opens…to_ directive**:
    
    
    module my.module {
        opens com.my.package to moduleOne, moduleTwo, etc.;
    }

## **5\. Command Line Options**

By now, support for Java 9 modules has been added to Maven and Gradle, so you won’t need to do a lot of manual building of your projects. However, it’s still valuable to know  _how_ to use the module system from the command line.

We’ll be using the command line for our full example down below to help solidify how the entire system works in our minds.

  * _**module-path**_**–** We use the  _–module-path_ option to specify the module path. This is a list of one or more directories that contain your modules.
  * _**add-reads**_ – Instead of relying on the module declaration file, we can use the command line equivalent of the  _requires_ directive;  _–add-reads_.
  * _**add-exports**_**–** Command line replacement for the _exports_ directive.
  * _**add-opens**_ _–_ Replace the  _open_ clause in the module declaration file.
  * _**add-modules**_ _–_ Adds the list of modules into the default set of modules
  * _**list-modules**_ _–_ Prints a list of all modules and their version strings
  * _**patch-module**_ – Add or override classes in a modules
  * _**illegal-access=permit|warn|deny**_ – Either relax strong encapsulation by showing a single global warning, shows every warning, or fails with errors. The default is  _permit_.



## **6\. Visibility**

We should spend a little time talking about the visibility of our code.

**A lot of libraries depend on reflection to work their magic** (JUnit and Spring come to mind).

By default in Java 9, we will  _only_ have access to public classes, methods, and fields in our exported packages. Even if we use reflection to get access to non-public members and call  _setAccessible(true),_ we won’t be able to access these members.

We can use the  _open_ ,  _opens_ , and  _opens…to_ options to grant runtime-only access for reflection. Note, **this is runtime-only!**

We won’t be able to compile against private types, and we should never need to anyway.

If we must have access to a module for reflection, and we’re not the owner of that module (i.e., we can’t use the  _opens…to_ directive), then it’s possible to use the command line  _–add-opens_ option to allow own modules reflection access to the locked down module at runtime.

The only caveat here’s that you need to have access to the command line arguments that are used to run a module for this to work.

## **7\. Putting It All Together**

Now that we know what a module is and how to use them let’s go ahead and build a simple project to demonstrate all the concepts we just learned.

To keep things simple, we won’t be using Maven or Gradle. Instead, we’ll rely on the command line tools to build our modules.

### **7.1. Setting Up Our Project**

First, we need to set up our project structure. We’ll create several directories to organize our files.

Start by creating the project folder:
    
    
    mkdir module-project
    cd module-project

This is the base of our whole project, so add files in here such as Maven or Gradle build files, other source directories, and resources.

We also put a directory to hold all our project specific modules.

Next, we create a module directory:
    
    
    mkdir simple-modules

Here’s what our project structure will look like:
    
    
    module-project
    |- // src if we use the default package
    |- // build files also go at this level
    |- simple-modules
      |- hello.modules
        |- com
          |- baeldung
            |- modules
              |- hello
      |- main.app
        |- com
          |- baeldung
            |- modules
              |- main

### **7.2. Our First Module**

Now that we have the basic structure in place, let’s add our first module.

Under the  _simple-modules_ directory, create a new directory called  _hello.modules_.

**We can name this anything we want but follow package naming rules** (i.e., periods to separate words, etc.). We can even use the name of our main package as the module name if we want, but usually, we want to stick to the same name we would use to create a JAR of this module.

Under our new module, we can create the packages we want. In our case, we are going to create one package structure:
    
    
    com.baeldung.modules.hello

Next, create a new class called  _HelloModules.java_ in this package. We will keep the code simple:
    
    
    package com.baeldung.modules.hello;
    
    public class HelloModules {
        public static void doSomething() {
            System.out.println("Hello, Modules!");
        }
    }

And finally, in the  _hello.modules_ root directory, add in our module descriptor;  _module-info.java_ :
    
    
    module hello.modules {
        exports com.baeldung.modules.hello;
    }

To keep this example simple, all we are doing is exporting all public members of the  _com.baeldung.modules.hello_ package.

### **7.3. Our Second Module**

Our first module is great, but it doesn’t do anything.

We can create a second module that uses it now.

Under our  _simple-modules_ directory, create another module directory called  _main.app_. We are going to start with the module descriptor this time:
    
    
    module main.app {
        requires hello.modules;
    }

We don’t need to expose anything to the outside world. Instead, all we need to do is depend on our first module, so we have access to the public classes it exports.

Now we can create an application that uses it.

Create a new package structure:  _com.baeldung.modules.main_.

Now, create a new class file called  _MainApp.java._
    
    
    package com.baeldung.modules.main;
    
    import com.baeldung.modules.hello.HelloModules;
    
    public class MainApp {
        public static void main(String[] args) {
            HelloModules.doSomething();
        }
    }

And that is all the code we need to demonstrate modules. Our next step is to build and run this code from the command line.

### **7.4. Building Our Modules**

To build our project, we can create a simple bash script and place it at the root of our project.

Create a file called  _compile-simple-modules.sh_ :
    
    
    #!/usr/bin/env bash
    javac -d outDir --module-source-path simple-modules $(find simple-modules -name "*.java")

There are two parts to this command, the  _javac_ and  _find_ commands.

The  _find_ command is simply outputting a list of all ._java_ files under our simple-modules directory. We can then feed that list directly into the Java compiler.

The only thing we have to do differently than the older versions of Java is to provide a  _module-source-path_ parameter to inform the compiler that it’s building modules.

Once we run this command, we will have an  _outDir_ folder with two compiled modules inside.

### **7.5. Running Our Code**

And now we can finally run our code to verify modules are working correctly.

Create another file in the root of the project:  _run-simple-module-app.sh_.
    
    
    #!/usr/bin/env bash
    java --module-path outDir -m main.app/com.baeldung.modules.main.MainApp

To run a module, we must provide at least the  _module-path_ and the main class. If all works, you should see:
    
    
    >$ ./run-simple-module-app.sh 
    Hello, Modules!

### **7.6. Adding a Service**

Now that we have a basic understanding of how to build a module, let’s make it a little more complicated.

We’re going to see how to use the  _provides…with_ and  _uses_ directives.

Start by defining a new file in the  _hello.modules_ module named  _HelloInterface_ _.java_ :
    
    
    public interface HelloInterface {
        void sayHello();
    }

To make things easy, we’re going to implement this interface with our existing  _HelloModules.java_ class:
    
    
    public class HelloModules implements HelloInterface {
        public static void doSomething() {
            System.out.println("Hello, Modules!");
        }
    
        public void sayHello() {
            System.out.println("Hello!");
        }
    }

That is all we need to do to create a  _service_.

Now, we need to tell the world that our module provides this service.

Add the following to our  _module-info.java_ :
    
    
    provides com.baeldung.modules.hello.HelloInterface with com.baeldung.modules.hello.HelloModules;

As we can see, we declare the interface and which class implements it.

Next, we need to consume this  _service_. In our  _main.app_ module, let’s add the following to our  _module-info.java_ :
    
    
    uses com.baeldung.modules.hello.HelloInterface;

Finally, in our main method we can use this service via a [ServiceLoader](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/ServiceLoader.html):
    
    
    Iterable<HelloInterface> services = ServiceLoader.load(HelloInterface.class);
    HelloInterface service = services.iterator().next();
    service.sayHello();

Compile and run:
    
    
    #> ./run-simple-module-app.sh 
    Hello, Modules!
    Hello!

We use these directives to be much more explicit about how our code is to be used.

We could put the implementation into a private package while exposing the interface in a public package.

This makes our code much more secure with very little extra overhead.

Go ahead and try out some of the other directives to learn more about modules and how they work.

## 8\. Adding Modules to the Unnamed Module

**The unnamed module concept is similar to the default package.** Therefore, it’s not considered a real module, but can be viewed as the default module.

If a class is not a member of a named module, then it will be automatically considered as part of this unnamed module.

Sometimes, to ensure specific platform, library, or service-provider modules in the module graph, we need to add modules to the default root set. For example, when we try to run Java 8 programs as-is with Java 9 compiler we may need to add modules.

In general,**the option to add the named modules to the default set of root modules is** _**–add-modules <module>**(,<module>)*_ where _< module>_ is a module name.

For example, to provide access to all _java.xml.bind_ modules the syntax would be:
    
    
    --add-modules java.xml.bind

To use this in Maven, we can embed the same to the _maven-compiler-plugin_ :
    
    
    <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-compiler-plugin</artifactId>
        <version>3.8.0</version>
        <configuration>
            <source>9</source>
            <target>9</target>
            <compilerArgs>
                <arg>--add-modules</arg>
                <arg>java.xml.bind</arg>
            </compilerArgs>
        </configuration>
    </plugin>

## **9\. Conclusion**

In this extensive guide, we focused on and covered the basics of the new Java 9 Module system.

We started by talking about what a module is.

Next, we talked about how to discover which modules are included in the JDK.

We also covered the module declaration file in detail.

We rounded out the theory by talking about the various command line arguments we’ll need to build our modules.

Finally, we put all our previous knowledge into practice and created a simple application built on top of the module system.
