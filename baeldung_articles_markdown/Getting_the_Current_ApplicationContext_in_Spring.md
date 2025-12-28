# Getting the Current ApplicationContext in Spring

## 1\. Overview

In this short tutorial, we’ll see how to get the current [_ApplicationContext_](/spring-application-context) in a Spring application.

## 2\. _ApplicationContext_

_ApplicationContext_ represents the Spring IoC container that holds all the beans created by the application. It is responsible for instantiating, configuring, and creating the beans. Additionally, it gets the beans’ information from configuration metadata provided in XML or Java.

_ApplicationContext_ represents the sub-interface of _[BeanFactory](https://docs.spring.io/spring-framework/docs/1.2.9/javadoc-api/org/springframework/beans/factory/BeanFactory.html)_. In addition to the functionalities of _BeanFactory_ , it includes features like message resolving and internationalization, resource loading, and event publishing. Furthermore, it has the functionality of loading multiple contexts.

**Each bean is instantiated after the container has been started since it uses eager loading.**

We may want to use this container to access other beans and resources in our application. We’ll learn two ways to get the current _ApplicationContext_ reference in the Spring application.

## 3\. _ApplicationContext_ Bean

**The simplest way to get the current _ApplicationContext_ is by injecting it into our beans using the [_@Autowired_ annotation](/spring-autowire).**

Firstly, let’s declare the instance variable and annotate it with the _@Autowired_ annotation:
    
    
    @Component
    public class MyBean {
    
        @Autowired
        private ApplicationContext applicationContext;
    
        public ApplicationContext getApplicationContext() {
            return applicationContext;
        }
    }

Instead of _@Autowired_ , we could use the _@Inject_ annotation.

To verify the container was properly injected, let’s create a test:
    
    
    @Test
    void whenGetApplicationContext_thenReturnApplicationContext(){
        assertNotNull(myBean);
        ApplicationContext context = myBean.getApplicationContext();
        assertNotNull(context);
    }

## 4\. _ApplicationContextAware_ Interface

Another way to get the current context is by implementing the [_ApplicationContextAware_](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/context/ApplicationContextAware.html) interface. It contains the _setApplicationContext()_ method, which Spring calls after creating _ApplicationContext_.

**Furthermore, when an application starts, Spring automatically detects this interface and injects a reference to _ApplicationContext_.**

Now, let’s create the _ApplicationContextProvider_ class that implements the _ApplicationContextAware_ interface:
    
    
    @Component
    public class ApplicationContextProvider implements ApplicationContextAware {
        private static ApplicationContext applicationContext;
    
        @Override
        public void setApplicationContext(ApplicationContext applicationContext) throws BeansException {
            ApplicationContextProvider.applicationContext = applicationContext;
        }
    
        public static ApplicationContext getApplicationContext() {
            return applicationContext;
        }
    }

We declared the _applicationContext_ instance variable as _static_ so we can access it in any class. Additionally, we created a static method for retrieving the reference to _ApplicationContext_.

Now, we can get the current _ApplicationContext_ object by calling the static _getApplicationContext()_ method:
    
    
    @Test
    void whenGetApplicationContext_thenReturnApplicationContext() {
        ApplicationContext context = ApplicationContextProvider.getApplicationContext();
        assertNotNull(context);
    }

Furthermore, by implementing the interface, a bean can obtain a reference to _ApplicationContext_ and access other beans or resources.

To accomplish this, firstly, let’s create the _ItemService_ class:
    
    
    @Service
    public class ItemService {
        // ...
    }

Secondly, to get the _ItemService_ bean from the context, let’s call the _getBean()_ method on _ApplicationContext_ :
    
    
    @Test
    void whenGetBean_thenReturnItemServiceReference() {
        ApplicationContext context = ApplicationContextProvider.getApplicationContext();
        assertNotNull(context);
    
        ItemService itemService = context.getBean(ItemService.class);
        assertNotNull(context);
    }

## 5\. Conclusion

In this short article, we learned how to get the current _ApplicationContext_ in our Spring Boot application. To summarize, we could inject the _ApplicationContext_ bean directly or implement the _ApplicationContextAware_ interface.
