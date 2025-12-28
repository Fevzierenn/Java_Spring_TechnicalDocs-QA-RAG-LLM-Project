# Guide to Spring @Autowired

## 1\. Overview

Starting with Spring 2.5, the framework introduced annotations-driven _Dependency Injection_. The main annotation of this feature is _@Autowired_ _._ **It allows Spring to resolve and inject collaborating beans into our bean.**

In this tutorial, we’ll first take a look at how to enable autowiring and the __ various __ ways to autowire beans. Afterward, we’ll talk about **resolving bean conflicts using _@Qualifier_ annotation,** as well as potential exception scenarios.

## 2\. Enabling _@Autowired_ Annotations

The Spring framework enables automatic dependency injection. In other words, **by declaring all the bean dependencies in a Spring configuration file, Spring container can autowire relationships between collaborating beans**. This is called **_Spring bean autowiring_**.

To use Java-based configuration in our application, let’s enable annotation-driven injection __ to load our Spring configuration:
    
    
    @Configuration
    @ComponentScan("com.baeldung.autowire.sample")
    public class AppConfig {}

Alternatively, the [_< context:annotation-config>_ annotation](/spring-contextannotation-contextcomponentscan#:~:text=The%20%3Ccontext%3Aannotation%2Dconfig,annotation%2Dconfig%3E%20can%20resolve.) is mainly used to activate the dependency injection annotations in Spring XML files.

Moreover,**Spring Boot introduces the[ _@SpringBootApplication_](/spring-boot-annotations#spring-boot-application)annotation**. This single annotation is equivalent to using _@Configuration_ , _@EnableAutoConfiguration_ , and  _@ComponentScan_.

Let’s use this annotation in the main class of the application:
    
    
    @SpringBootApplication
    public class App {
        public static void main(String[] args) {
            SpringApplication.run(App.class, args);
        }
    }

As a result, when we run this Spring Boot application, **it will automatically scan the components in the current package and its sub-packages**. Thus it will register them in Spring’s Application Context, and allow us to inject beans using _@Autowired_.

## 3\. Using _@Autowired_

After enabling annotation injection,**we can use autowiring on properties, setters, and constructors**.

### **3.1._@Autowired_ on Properties**

Let’s see how we can annotate a property using _@Autowired_. This eliminates the need for getters and setters.

First, let’s define a _fooFormatter_ bean:
    
    
    @Component("fooFormatter")
    public class FooFormatter {
        public String format() {
            return "foo";
        }
    }

Then, we’ll inject this bean into the _FooService_ bean using _@Autowired_ on the field definition:
    
    
    @Component
    public class FooService {  
        @Autowired
        private FooFormatter fooFormatter;
    }

As a result, Spring injects _fooFormatter_ when _FooService_ is created.

### **3.2._@Autowired_ on Setters**

Now let’s try adding _@Autowired_ annotation on a setter method.

In the following example, the setter method is called with the instance of _FooFormatter_ when _FooService_ is created:
    
    
    public class FooService {
        private FooFormatter fooFormatter;
        @Autowired
        public void setFormatter(FooFormatter fooFormatter) {
            this.fooFormatter = fooFormatter;
        }
    }
    

### **3.3._@Autowired_ on Constructors**

Finally, let’s use _@Autowired_ on a constructor.

We’ll see that an instance of _FooFormatter_ is injected by Spring as an argument to the _FooService_ constructor:
    
    
    public class FooService {
        private FooFormatter fooFormatter;
        @Autowired
        public FooService(FooFormatter fooFormatter) {
            this.fooFormatter = fooFormatter;
        }
    }

## 4\. _@Autowired_ and Optional Dependencies

When a bean is being constructed, the _@Autowired_ dependencies should be available. Otherwise, **if Spring cannot resolve a bean for wiring, it will throw an exception**.

Consequently, it prevents the Spring container from launching successfully with an exception of the form:
    
    
    Caused by: org.springframework.beans.factory.NoSuchBeanDefinitionException: 
    No qualifying bean of type [com.autowire.sample.FooDAO] found for dependency: 
    expected at least 1 bean which qualifies as autowire candidate for this dependency. 
    Dependency annotations: 
    {@org.springframework.beans.factory.annotation.Autowired(required=true)}

To fix this, we need to declare a bean of the required type:
    
    
    public class FooService {
        @Autowired(required = false)
        private FooDAO dataAccessor; 
    }

## 5\. Autowire Disambiguation

By default, Spring resolves _@Autowired_ entries by type. **If more than one bean of the same type is available in the container, the framework will throw a fatal exception**.

To resolve this conflict, we need to tell Spring explicitly which bean we want to inject.

### **5.1. Autowiring by _@Qualifier_**

For instance, let’s see how we can use the [_@Qualifier_](/spring-qualifier-annotation) annotation to indicate the required bean.

First, we’ll define 2 beans of type _Formatter_ :
    
    
    @Component("fooFormatter")
    public class FooFormatter implements Formatter {
        public String format() {
            return "foo";
        }
    }
    
    
    @Component("barFormatter")
    public class BarFormatter implements Formatter {
        public String format() {
            return "bar";
        }
    }

Now let’s try to inject a _Formatter_ bean into the _FooService_ class:
    
    
    public class FooService {
        @Autowired
        private Formatter formatter;
    }

In our example, there are two concrete implementations of _Formatter_ available for the Spring container. As a result, **Spring will throw a _NoUniqueBeanDefinitionException_ exception when constructing the _FooService_** :_  
_
    
    
    Caused by: org.springframework.beans.factory.NoUniqueBeanDefinitionException: 
    No qualifying bean of type [com.autowire.sample.Formatter] is defined: 
    expected single matching bean but found 2: barFormatter,fooFormatter
    

**We can avoid this by narrowing the implementation using a _@Qualifier_ annotation:**
    
    
    public class FooService {
        @Autowired
        @Qualifier("fooFormatter")
        private Formatter formatter;
    }

When there are multiple beans of the same type, it’s a good idea to**use _@Qualifier_ to avoid ambiguity.**

Please note that the value of the _@Qualifier_ annotation matches with the name declared in the _@Component_ annotation of our _FooFormatter_ implementation.

### **5.2. Autowiring by Custom Qualifier**

Spring also allows us to **create our own custom _@Qualifier_ annotation**. To do so, we should provide the _@Qualifier_ annotation with the definition:
    
    
    @Qualifier
    @Target({
      ElementType.FIELD, ElementType.METHOD, ElementType.TYPE, ElementType.PARAMETER})
    @Retention(RetentionPolicy.RUNTIME)
    public @interface FormatterType {  
        String value();
    }

Then we can use the _FormatterType_ within various implementations to specify a custom value:
    
    
    @FormatterType("Foo")
    @Component
    public class FooFormatter implements Formatter {
        public String format() {
            return "foo";
        }
    }
    
    
    @FormatterType("Bar")
    @Component
    public class BarFormatter implements Formatter {
        public String format() {
            return "bar";
        }
    }

Finally, our custom Qualifier annotation is ready to use for autowiring:
    
    
    @Component
    public class FooService {  
        @Autowired
        @FormatterType("Foo")
        private Formatter formatter;
    }
    

The value specified in the **_@Target_ meta-annotation restricts where to apply the qualifier, **which in our example is fields, methods, types, and parameters.

### **5.3. Autowiring by Name**

**Spring uses the bean’s name as a default qualifier value.** It will inspect the container and look for a bean with the exact name as the property to autowire it.

Hence, in our example, Spring matches the _fooFormatter_ property name to the _FooFormatter_ implementation. Therefore, it injects that specific implementation when constructing _FooService_ :
    
    
    public class FooService {
     @Autowired 
    private Formatter fooFormatter; 
    }

## 6\. Conclusion

In this article, we discussed autowiring and the different ways to use it. We also examined ways to solve two common autowiring exceptions caused by either a missing bean or an ambiguous bean injection.
