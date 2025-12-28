# The Spring @Qualifier Annotation

## 1\. Overview

In this tutorial, we’ll explore **what the _@Qualifier_ annotation can help us with**, which problems it solves, and how to use it.

We’ll also explain how it’s different from the _@Primary_ annotation, and from autowiring by name.

## 2\. Autowire Need for Disambiguation

The [_@Autowired_](/spring-autowire) annotation is a great way of making the need to inject a dependency in Spring explicit. Although it’s useful, there are use cases for which this annotation alone isn’t enough for Spring to understand which bean to inject.

By default, Spring resolves autowired entries by type.

**If more than one bean of the same type is available in the container, the framework will throw _NoUniqueBeanDefinitionException_** _,_ indicating that more than one bean is available for autowiring.

Let’s imagine a situation in which two possible candidates exist for Spring to inject as bean collaborators in a given instance:
    
    
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
    
    @Component
    public class FooService {
         
        @Autowired
        private Formatter formatter;
    }

If we try to load _FooService_ into our context, the Spring framework will throw a _NoUniqueBeanDefinitionException_. This is because **Spring doesn’t know which bean to inject**. To avoid this problem, there are several solutions; the _@Qualifier_ annotation is one of them.

## 3\. _@Qualifier_ Annotation

By using the _@Qualifier_ annotation, we can **eliminate the issue of which bean needs to be injected**.

Let’s revisit our previous example to see how we solve the problem by including the _@Qualifier_ annotation to indicate which bean we want to use:
    
    
    public class FooService {
         
        @Autowired
        @Qualifier("fooFormatter")
        private Formatter formatter;
    }

By including the _@Qualifier_ annotation, together with the name of the specific implementation we want to use, in this example _Foo,_ we can avoid ambiguity when Spring finds multiple beans of the same type.

We need to take into consideration that the qualifier name to be used is the one declared in the _@Component_ annotation.

Note that we could have also used the _@Qualifier_ annotation on the _Formatter_ implementing classes, instead of specifying the names in their _@Component_ annotations, to obtain the same effect:
    
    
    @Component
    @Qualifier("fooFormatter")
    public class FooFormatter implements Formatter {
        //...
    }
    
    @Component
    @Qualifier("barFormatter")
    public class BarFormatter implements Formatter {
        //...
    }
    

## 4\. _@Qualifier_ vs _@Primary_

There’s another annotation called [_@Primary_](/spring-primary) that we can use to decide which bean to inject when ambiguity is present regarding dependency injection.

This annotation **defines a preference when multiple beans of the same type are present**. The bean associated with the _@Primary_ annotation will be used unless otherwise indicated.

Let’s see an example:
    
    
    @Configuration
    public class Config {
     
        @Bean
        public Employee johnEmployee() {
            return new Employee("John");
        }
     
        @Bean
        @Primary
        public Employee tonyEmployee() {
            return new Employee("Tony");
        }
    }

In this example, both methods return the same _Employee_ type. The bean that Spring will inject is the one returned by the method _tonyEmployee_. This is because it contains the _@Primary_ annotation. This annotation is useful when we want to **specify which bean of a certain type should be injected by default**.

If we require the other bean at some injection point, we would need to specifically indicate it. We can do that via the _@Qualifier_ annotation. For instance, we could specify that we want to use the bean returned by the _johnEmployee_ method by using the _@Qualifier_ annotation.

It’s worth noting that **if both the _@Qualifier_ and _@Primary_ annotations are present, then the _@Qualifier_ annotation will have precedence.** Basically, _@Primary_ defines a default, while _@Qualifier_ is very specific.

Let’s look at another way of using the _@Primary_ annotation, this time using the initial example:
    
    
    @Component
    @Primary
    public class FooFormatter implements Formatter {
        //...
    }
    
    @Component
    public class BarFormatter implements Formatter {
        //...
    }
    

**In this case, the _@Primary_ annotation is placed in one of the implementing classes,** and will disambiguate the scenario.

## 5\. _@Qualifier_ vs Autowiring by Name

Another way to decide between multiple beans when autowiring, is by using the name of the field to inject. **This is the default in case there are no other hints for Spring**. Let’s see some code based on our initial example:
    
    
    public class FooService {
         
        @Autowired
        private Formatter fooFormatter;
    }

In this case, Spring will determine that the bean to inject is the _FooFormatter_ one, since the field name is matched to the value that we used in the _@Component_ annotation for that bean.

## 6\. Conclusion

In this article, we described the scenarios where we need to disambiguate which beans to inject. In particular, we examined the _@Qualifier_ annotation, and compared it with other similar ways of determining which beans need to be used.
