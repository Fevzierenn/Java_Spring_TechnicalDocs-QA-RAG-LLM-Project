# Spring Bean Annotations

[This article is part of a series:](javascript:void\(0\);)

[• Spring Core Annotations](/spring-core-annotations)  
[• Spring Web Annotations](/spring-mvc-annotations)  
[• Spring Boot Annotations](/spring-boot-annotations)  
[• Spring Scheduling Annotations](/spring-scheduling-annotations)  
[• Spring Data Annotations](/spring-data-annotations)  


• Spring Bean Annotations (current article)

## **1\. Overview**

In this tutorial, we’ll discuss the most **common Spring bean annotations** used to define different types of beans.

There are several ways to configure beans in a Spring container. Firstly, we can declare them using XML configuration. We can also declare beans using the _@Bean_ annotation in a configuration class.

Finally, we can mark the class with one of the annotations from the _org.springframework.stereotype_ package, and leave the rest to component scanning.

## **2\. Component Scanning**

Spring can automatically scan a package for beans if component scanning is enabled.

_@ComponentScan_ configures which **packages to scan for classes with annotation configuration**. We can specify the base package names directly with one of the _basePackages_ or _value_ arguments (_value_ is an alias for _basePackages_):
    
    
    @Configuration
    @ComponentScan(basePackages = "com.baeldung.annotations")
    class VehicleFactoryConfig {}

Also, we can point to classes in the base packages with the _basePackageClasses_ argument:
    
    
    @Configuration
    @ComponentScan(basePackageClasses = VehicleFactoryConfig.class)
    class VehicleFactoryConfig {}

Both arguments are arrays so that we can provide multiple packages for each.

If no argument is specified, the scanning happens from the same package where the _@ComponentScan_ annotated class is present.

_@ComponentScan_ leverages the Java 8 repeating annotations feature, which means we can mark a class with it multiple times:
    
    
    @Configuration
    @ComponentScan(basePackages = "com.baeldung.annotations")
    @ComponentScan(basePackageClasses = VehicleFactoryConfig.class)
    class VehicleFactoryConfig {}

Alternatively, we can use _@ComponentScans_ to specify multiple _@ComponentScan_ configurations:
    
    
    @Configuration
    @ComponentScans({ 
      @ComponentScan(basePackages = "com.baeldung.annotations"), 
      @ComponentScan(basePackageClasses = VehicleFactoryConfig.class)
    })
    class VehicleFactoryConfig {}

When **using XML configuration** , the configuring component scanning is just as easy:
    
    
    <context:component-scan base-package="com.baeldung" />

## **3._@Component_**

_@Component_ is a class level annotation. During the component scan, **Spring Framework automatically detects classes annotated with _@Component:_**
    
    
    @Component
    class CarUtility {
        // ...
    }

By default, the bean instances of this class have the same name as the class name with a lowercase initial. In addition, we can specify a different name using the optional _value_ argument of this annotation.

Since _@Repository_ , _@Service_ , _@Configuration_ , and _@Controller_ are all meta-annotations of _@Component_ , they share the same bean naming behavior. Spring also automatically picks them up during the component scanning process.

## **4._@Repository_**

DAO or Repository classes usually represent the database access layer in an application, and should be annotated with _@Repository:_
    
    
    @Repository
    class VehicleRepository {
        // ...
    }

One advantage of using this annotation is that **it has automatic persistence exception translation enabled**. When using a persistence framework, such as Hibernate, native exceptions thrown within classes annotated with _@Repository_ will be automatically translated into subclasses of Spring’s _DataAccessExeption_.

**To enable exception translation** , we need to declare our own _PersistenceExceptionTranslationPostProcessor_ bean:
    
    
    @Bean
    public PersistenceExceptionTranslationPostProcessor exceptionTranslation() {
        return new PersistenceExceptionTranslationPostProcessor();
    }

Note that in most cases, Spring does the above step automatically.

Or via XML configuration:
    
    
    <bean class=
      "org.springframework.dao.annotation.PersistenceExceptionTranslationPostProcessor"/>

## **5._@Service_**

The **business logic** of an application usually resides within the service layer, so we’ll use the _@Service_ annotation to indicate that a class belongs to that layer:
    
    
    @Service
    public class VehicleService {
        // ...    
    }

## **6._@Controller_**

_@Controller_ is a class level annotation, which tells the Spring Framework that this class serves as a **controller in Spring MVC** :
    
    
    @Controller
    public class VehicleController {
        // ...
    }

## 7\. _@Configuration_

_Configuration_ classes can **contain bean definition methods** annotated with _@Bean_ :
    
    
    @Configuration
    class VehicleFactoryConfig {
    
        @Bean
        Engine engine() {
            return new Engine();
        }
    
    }

## **8\. Stereotype Annotations and AOP**

When we use Spring stereotype annotations, it’s easy to create a pointcut that targets all classes that have a particular stereotype.

For instance, suppose we want to measure the execution time of methods from the DAO layer. We’ll create the following aspect (using AspectJ annotations), taking advantage of the _@Repository_ stereotype:
    
    
    @Aspect
    @Component
    public class PerformanceAspect {
        @Pointcut("within(@org.springframework.stereotype.Repository *)")
        public void repositoryClassMethods() {};
    
        @Around("repositoryClassMethods()")
        public Object measureMethodExecutionTime(ProceedingJoinPoint joinPoint) 
          throws Throwable {
            long start = System.nanoTime();
            Object returnValue = joinPoint.proceed();
            long end = System.nanoTime();
            String methodName = joinPoint.getSignature().getName();
            System.out.println(
              "Execution of " + methodName + " took " + 
              TimeUnit.NANOSECONDS.toMillis(end - start) + " ms");
            return returnValue;
        }
    }

In this example, we created a pointcut that matches all the methods in classes annotated with _@Repository_. Then we used the _@Around_ advice to target that pointcut, and determine the execution time of the intercepted methods calls.

Furthermore, using this approach, we can add logging, performance management, audit, and other behaviors to each application layer.

## **9\. Conclusion**

In this article, we examined the Spring stereotype annotations and discussed what type of semantics they each represent.

We also learned how to use component scanning to tell the container where to find annotated classes.

Finally, we learned how these annotations **lead to a clean, layered design,** and separation between the concerns of an application. They also make configuration smaller, as we no longer need to explicitly define beans manually.

**«** Previous

[Spring Data Annotations](/spring-data-annotations)
