# Spring @Component Annotation

## 1\. Overview

In this tutorial, we’ll take a comprehensive look at the [Spring _@Component_](/spring-component-repository-service) annotation and related areas. We’ll see the different ways we can integrate with some core Spring functionality and how to take advantage of its many benefits.

## 2\. Spring _ApplicationContext_

Before we can understand the value of _@Component_ , we first need to understand a little bit about the [Spring _ApplicationContext_](/spring-application-context).

Spring _ApplicationContext_ is where Spring holds instances of objects that it has identified to be managed and distributed automatically. These are called beans.

Some of Spring’s main features are bean management and the opportunity for dependency injection.

Using the [Inversion of Control principle](/inversion-control-and-dependency-injection-in-spring), **Spring collects bean instances from our application and uses them at the appropriate time.** We can show bean dependencies to Spring without handling the setup and instantiation of those objects.

The ability to use annotations like [_@Autowired_](/spring-autowire) to inject Spring-managed beans into our application is a driving force for creating powerful and scalable code in Spring.

So, how do we tell Spring about the beans we want it to manage for us? **We should take advantage of Spring’s automatic bean detection by using stereotype annotations in our classes.**

## 3\. _@Component_

_@Component_ is an annotation that allows Spring to detect our custom beans automatically.

In other words, without having to write any explicit code, Spring will:

  * Scan our application for classes annotated with _@Component_
  * Instantiate them and inject any specified dependencies into them
  * Inject them wherever needed



However, most developers prefer to use more specialized stereotype annotations to serve this function.

### 3.1. Spring Stereotype Annotations

Spring has provided a few specialized stereotype annotations: _@Controller_ , _@Service_ and _@Repository_. They all provide the same function as _@Component_.

**They all act the same because they are all composed annotations with _@Component_ as a meta-annotation for each of them.** They are like _@Component_ aliases with specialized uses and meaning outside Spring auto-detection or dependency injection.

We could theoretically use @Component exclusively for our bean auto-detection needs if we wanted to. On the flip side, we could also [compose our specialized annotations](/java-custom-annotation) that use _@Component_.

However, other areas of Spring look specifically for Spring’s specialized annotations to provide additional automation benefits. **So, we should probably stick with using the established specializations most of the time.**

Let’s assume we have an example of each of these cases in our Spring Boot project:
    
    
    @Controller
    public class ControllerExample {
    }
    
    @Service
    public class ServiceExample {
    }
    
    @Repository
    public class RepositoryExample {
    }
    
    @Component
    public class ComponentExample {
    }
    
    @Target({ElementType.TYPE})
    @Retention(RetentionPolicy.RUNTIME)
    @Component
    public @interface CustomComponent {
    }
    
    @CustomComponent
    public class CustomComponentExample {
    }

We could write a test that proves that each one is auto-detected by Spring and added to the _ApplicationContext_ :
    
    
    @SpringBootTest
    @ExtendWith(SpringExtension.class)
    public class ComponentUnitTest {
    
        @Autowired
        private ApplicationContext applicationContext;
    
        @Test
        public void givenInScopeComponents_whenSearchingInApplicationContext_thenFindThem() {
            assertNotNull(applicationContext.getBean(ControllerExample.class));
            assertNotNull(applicationContext.getBean(ServiceExample.class));
            assertNotNull(applicationContext.getBean(RepositoryExample.class));
            assertNotNull(applicationContext.getBean(ComponentExample.class));
            assertNotNull(applicationContext.getBean(CustomComponentExample.class));
        }
    }

### 3.2. _@ComponentScan_

Before we rely entirely on _@Component_ , we must understand that it’s only a plain annotation. The annotation serves the purpose of differentiating beans from other objects, such as domain objects.

However, **Spring uses the _@ComponentScan_ annotation to gather them into its _ApplicationContext_.**

If we’re writing a Spring Boot application, it is helpful to know that _@SpringBootApplication_ is a composed annotation that includes _@ComponentScan_. As long as our _@SpringBootApplication_ class is at the root of our project, it will scan every _@Component_ we define by default.

But in case our _@SpringBootApplication_ class can’t be at the root of our project or we want to scan outside sources, [we can configure _@ComponentScan_](/spring-component-scanning#component-scan) explicitly to look in whatever package we specify, as long as it exists on the classpath.

Let’s define an out-of-scope _@Component_ bean:
    
    
    package com.baeldung.component.scannedscope;
    
    @Component
    public class ScannedScopeExample {
    }

Next, we can include it via explicit instructions to our _@ComponentScan_ annotation:
    
    
    package com.baeldung.component.inscope;
    
    @SpringBootApplication
    @ComponentScan({"com.baeldung.component.inscope", "com.baeldung.component.scannedscope"})
    public class ComponentApplication {
        //public static void main(String[] args) {...}
    }

Finally, we can test that it exists:
    
    
    @Test
    public void givenScannedScopeComponent_whenSearchingInApplicationContext_thenFindIt() {
        assertNotNull(applicationContext.getBean(ScannedScopeExample.class));
    }

This is more likely to happen when we want to scan for an outside dependency included in our project.

### 3.3. _@Component_ Limitations

There are some scenarios where we want a specific object to become a Spring-managed bean when we can’t use _@Component_.

Let’s define an object annotated with _@Component_ in a package outside of our project:
    
    
    package com.baeldung.component.outsidescope;
    
    @Component
    public class OutsideScopeExample {
    }

Here is a test that proves that the _ApplicationContext_ does not include the outside component:
    
    
    @Test
    public void givenOutsideScopeComponent_whenSearchingInApplicationContext_thenFail() {
        assertThrows(NoSuchBeanDefinitionException.class, () -> applicationContext.getBean(OutsideScopeExample.class));
    }

Also, we may not have access to the source code because it comes from a third-party source, and we’re unable to add the _@Component_ annotation. Or perhaps we want to conditionally use one bean implementation over another, depending on the environment we’re running in. **Auto-detection is usually sufficient, but when it’s not, we can use _@Bean_.**

## 4\. _@Component_ vs _@Bean_

_@Bean_ is also an annotation that Spring uses to gather beans at runtime, but it’s not used at the class level. Instead,**we annotate methods with _@Bean_ so that Spring can store the method’s result as a Spring bean.**

We’ll first create a POJO that has no annotations:
    
    
    public class BeanExample {
    }

Inside our class annotated with _@Configuration_ , we can create a bean-generating method:
    
    
    @Bean
    public BeanExample beanExample() {
        return new BeanExample();
    }

_BeanExample_ might represent a local class, or it might be an external class. It doesn’t matter because we need to return an instance of it.

We can then write a test that verifies Spring did pick up the bean:
    
    
    @Test
    public void givenBeanComponents_whenSearchingInApplicationContext_thenFindThem() {
        assertNotNull(applicationContext.getBean(BeanExample.class));
    }

We should note some important implications because of the differences between _@Component_ and _@Bean_.

  * _@Component_ is a class-level annotation, but _@Bean_ is at the method level, so _@Component_ is only an option when a class’s source code is editable. _@Bean_ can always be used, but it’s more verbose.
  * _@Component_ is compatible with Spring’s auto-detection, but _@Bean_ requires manual class instantiation.
  * Using _@Bean,_ decouples the instantiation of the bean from its class definition. This is why we can use it to make third-party classes into Spring beans. It also means we can introduce logic to decide which of several possible instance options for a bean to use.



## 5\. Conclusion

We’ve just explored the Spring _@Component_ annotation and other relevant topics. First, we discussed the various Spring stereotype annotations, which are just specialized versions of _@Component_.

Then we learned that _@Component_ doesn’t do anything unless @ComponentScan can find it.

Finally, since it’s not possible to use _@Component_ on classes because we don’t have the source code, we learned how to use the _@Bean_ annotation instead.
