# The Spring ApplicationContext

## 1\. Overview

In this tutorial, we’ll explore the Spring _ApplicationContext_ interface in detail.

## 2\. The _ApplicationContext_ Interface

One of the main features of the Spring framework is the IoC (Inversion of Control) container. The [Spring IoC container](/inversion-control-and-dependency-injection-in-spring) is responsible for managing the objects of an application. It uses dependency injection to achieve inversion of control.

The interfaces _[BeanFactory](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/beans/factory/BeanFactory.html) _and _[ApplicationContext](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/context/ApplicationContext.html) _**represent the Spring IoC container**. Here, _BeanFactory_ is the root interface for accessing the Spring container. It provides basic functionalities for managing beans.

On the other hand, the _ApplicationContext_ is a sub-interface of the _BeanFactory_. Therefore, it offers all the functionalities of _BeanFactory._

Furthermore, it **provides** **more enterprise-specific functionalities**. The important features of _ApplicationContext_ are **resolving messages, supporting internationalization, publishing events, and application-layer specific contexts**. This is why we use it as the default Spring container.

## 3\. What Is a Spring Bean?

Before we dive deeper into the _ApplicationContext_ container, it’s important to know about Spring beans. In Spring, a [bean](/spring-bean) is **an object that the Spring container instantiates, assembles, and manages**.

So should we configure all of the objects of our application as Spring beans? Well, as a best practice, we shouldn’t.

As per [Spring documentation](https://docs.spring.io/spring/docs/current/spring-framework-reference/core.html#beans-factory-metadata) in general, we should define beans for service layer objects, data access objects (DAOs), presentation objects, infrastructure objects such as Hibernate _SessionFactories,_ JMS Queues, and so forth.

Also, typically, we shouldn’t configure fine-grained domain objects in the container. It’s usually the responsibility of DAOs and business logic to create and load domain objects.

Now let’s define a simple Java class that we’ll use as a Spring bean in this tutorial:
    
    
    public class AccountService {
    
      @Autowired
      private AccountRepository accountRepository;
    
      // getters and setters
    }

## 4\. Configuring Beans in the Container

As we know, the primary job of the _ApplicationContext_ is to manage beans.

As such, an application must provide the bean configuration to the _ApplicationContext_ container. A Spring bean configuration consists of one or more bean definitions. In addition, Spring supports different ways of configuring beans.

### 4.1. Java-Based Configuration

First, we’ll start with Java-based configuration as it’s the newest and most preferred way of bean configuration. It’s available from Spring 3.0 onward.

Java configuration typically uses **_@Bean_ -annotated methods within a _@Configuration_ class**. The _@Bean_ annotation on a method indicates that the method creates a Spring bean. Moreover, a class annotated with _@Configuration_ indicates that it contains Spring bean configurations.

Now let’s create a configuration class to define our _AccountService_ class as a Spring bean:
    
    
    @Configuration
    public class AccountConfig {
    
      @Bean
      public AccountService accountService() {
        return new AccountService(accountRepository());
      }
    
      @Bean
      public AccountRepository accountRepository() {
        return new AccountRepository();
      }
    }

### 4.2. Annotation-Based Configuration

Spring 2.5 introduced annotation-based configuration as the first step to enable bean configurations in Java.

In this approach, we first enable annotation-based configuration via XML configuration. Then we use a set of annotations on our Java classes, methods, constructors, or fields to configure beans. Some examples of these annotations are _@Component_ , _@Controller_ , _@Service_ , _@Repository_ , _@Autowired_ , and _@Qualifier_.

Notably, we use these annotations with Java-based configuration as well. Also worth mentioning, Spring keeps on adding more capabilities to these annotations with each release.

Now let’s see a simple example of this configuration.

First, we’ll create the XML configuration, _user-bean-config.xml_ , to enable annotations:
    
    
    <?xml version="1.0" encoding="UTF-8"?>
    <beans xmlns="http://www.springframework.org/schema/beans"
      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xmlns:context="http://www.springframework.org/schema/context"
      xsi:schemaLocation="http://www.springframework.org/schema/beans
        http://www.springframework.org/schema/beans/spring-beans.xsd
        http://www.springframework.org/schema/context
        http://www.springframework.org/schema/context/spring-context.xsd">
      
      <context:annotation-config/>
      <context:component-scan base-package="com.baeldung.applicationcontext"/>
    
    </beans>

Here, **the _annotation-config_ tag enables annotation-based mappings**. The _component-scan_ tag also tells Spring where to look for annotated classes.

Second, we’ll create the _UserService_ class and define it as a Spring bean using the _@Component_ annotation:
    
    
    @Component
    public class UserService {
      // user service code
    }

Then we’ll write a simple test case to test this configuration:
    
    
    ApplicationContext context = new ClassPathXmlApplicationContext("applicationcontext/user-bean-config.xml");
    UserService userService = context.getBean(UserService.class);
    assertNotNull(userService);

### 4.3. XML-Based Configuration

Finally, let’s take a look at XML-based configuration. This is the traditional way of configuring beans in Spring.

Obviously, in this approach, we do all **bean mappings in an XML configuration file**.

So let’s create an XML configuration file, _account-bean-config.xml_ , and define beans for our _AccountService_ class:
    
    
    <?xml version="1.0" encoding="UTF-8"?>
    <beans xmlns="http://www.springframework.org/schema/beans"
      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xsi:schemaLocation="
        http://www.springframework.org/schema/beans 
        http://www.springframework.org/schema/beans/spring-beans.xsd">
    	  
      <bean id="accountService" class="com.baeldung.applicationcontext.AccountService">
        <constructor-arg name="accountRepository" ref="accountRepository" />
      </bean>
    	
      <bean id="accountRepository" class="com.baeldung.applicationcontext.AccountRepository" />
    </beans>

## 5\. Types of _ApplicationContext_

Spring provides different types of _ApplicationContext_ containers suitable for different requirements. These are implementations of the _ApplicationContext_ interface. So let’s take a look at some of the common types of _ApplicationContext_.

### 5.1. _AnnotationConfigApplicationContext_

First, let’s see the [_AnnotationConfigApplicationContext_ ](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/context/annotation/AnnotationConfigApplicationContext.html)class, which was introduced in Spring 3.0. It can take **classes annotated with _@Configuration_ , **_**@Component** ,_ and JSR-330 metadata as input.

So let’s see a simple example of using the _AnnotationConfigApplicationContext_ container with our Java-based configuration:
    
    
    ApplicationContext context = new AnnotationConfigApplicationContext(AccountConfig.class);
    AccountService accountService = context.getBean(AccountService.class);

### 5.2. _AnnotationConfigWebApplicationContext_

[_**AnnotationConfigWebApplicationContext**_ ](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/web/context/support/AnnotationConfigWebApplicationContext.html)**is a web-based variant** of _AnnotationConfigApplicationContext_.

We may use this class when we configure Spring’s _ContextLoaderListener_ servlet listener or a Spring MVC _DispatcherServlet_ in a _web.xml_ file.

Moreover, from Spring 3.0 onward, we can also configure this application context container programmatically. All we need to do is implement the [_WebApplicationInitializer_](https://docs.spring.io/spring/docs/current/javadoc-api/org/springframework/web/WebApplicationInitializer.html) interface:
    
    
    public class MyWebApplicationInitializer implements WebApplicationInitializer {
    
      public void onStartup(ServletContext container) throws ServletException {
        AnnotationConfigWebApplicationContext context = new AnnotationConfigWebApplicationContext();
        context.register(AccountConfig.class);
        context.setServletContext(container);
    
        // servlet configuration
      }
    }

### 5.3. _XmlWebApplicationContext_

If we use the **XML based configuration in a web application** , we can use the [_XmlWebApplicationContext_](https://docs.spring.io/spring/docs/current/javadoc-api/org/springframework/web/context/support/XmlWebApplicationContext.html) class.

As a matter of fact, configuring this container is like the _AnnotationConfigWebApplicationContext_ class only, which means we can configure it in _web.xml,_ or implement the _WebApplicationInitializer_ interface:
    
    
    public class MyXmlWebApplicationInitializer implements WebApplicationInitializer {
    
      public void onStartup(ServletContext container) throws ServletException {
        XmlWebApplicationContext context = new XmlWebApplicationContext();
        context.setConfigLocation("/WEB-INF/spring/applicationContext.xml");
        context.setServletContext(container);
    
        // Servlet configuration
      }
    }

### 5.4. _FileSystemXMLApplicationContext_

We use the [_FileSystemXMLApplicationContext_ ](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/context/support/FileSystemXmlApplicationContext.html)class to **load an XML-based Spring configuration file from the file system** or from URLs. This class is useful when we need to load the _ApplicationContext_ programmatically. In general, test harnesses and standalone applications are some of the possible use cases for this.

For example, let’s see how we can create this Spring container and load the beans for our XML-based configuration:
    
    
    String path = "C:/myProject/src/main/resources/applicationcontext/account-bean-config.xml";
    
    ApplicationContext context = new FileSystemXmlApplicationContext(path);
    AccountService accountService = context.getBean("accountService", AccountService.class);

### 5.5. _ClassPathXmlApplicationContext_

In case we want to **load an XML configuration file from the classpath** , we can use the [_ClassPathXmlApplicationContext_](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/context/support/ClassPathXmlApplicationContext.html) class. Similar to _FileSystemXMLApplicationContext,_ it’s useful for test harnesses, as well as application contexts embedded within JARs.

So let’s see an example of using this class:
    
    
    ApplicationContext context = new ClassPathXmlApplicationContext("applicationcontext/account-bean-config.xml");
    AccountService accountService = context.getBean("accountService", AccountService.class);

## 6\. Multiple _ApplicationContext_ in Spring

Moreover, there may be scenarios where multiple _ApplicationContext_ instances are needed within a single application.

### 6.1. Modular Applications

In a large modular application, each module might have its own context. **This helps isolate the configurations of each module, preventing bean naming conflicts and making it easier to maintain.**

For a modular application, each module can load its own _ApplicationContext_ :
    
    
    // Module 1 Context
    ApplicationContext module1Context = new AnnotationConfigApplicationContext(Module1Config.class);
    
    // Module 2 Context
    ApplicationContext module2Context = new AnnotationConfigApplicationContext(Module2Config.class);
    

Each context can manage its beans independently without interfering with other module contexts.

### 6.2. Hierarchical Application Contexts

Spring allows for hierarchical contexts, where a parent context can define beans that are available to all child contexts, but child contexts can have beans that are specific to their module. **This is useful in cases like having a shared core configuration in the parent context.**

Here’s an example of parent-child context:
    
    
    // Parent ApplicationContext
    ApplicationContext parentContext = new AnnotationConfigApplicationContext(ParentConfig.class);
    
    // Child ApplicationContext
    AnnotationConfigApplicationContext childContext = new AnnotationConfigApplicationContext();
    childContext.setParent(parentContext);
    childContext.register(ChildConfig.class);
    childContext.refresh();
    

In this example, the _parentContext_ is loaded first. The _childContext_ is created and linked to the _parentContext_ using the _setParent()_ method. **Beans defined in _ParentConfig_ will be available in _childContext_.**

### 6.3. Isolation for Testing

We can use different _ApplicationContext_ instances to simulate different parts of the application during testing. **This allows testing one part of the application without affecting another.**

For unit or integration testing, we might want to create specific contexts for each test scenario:
    
    
    @RunWith(SpringJUnit4ClassRunner.class)
    @ContextConfiguration(classes = { Module1Config.class })
    public class TestClass1 {
        @Autowired
        ApplicationContext context1;
    
        // Test cases
    }
    
    @RunWith(SpringJUnit4ClassRunner.class)
    @ContextConfiguration(classes = { Module2Config.class })
    public class TestClass2 {
        @Autowired
        ApplicationContext context2;
    
        // Test cases
    }

This ensures that the test classes are isolated and have their own context configuration.

## 7\. Additional Features of _ApplicationContext_

### 7.1. Message Resolution

The _ApplicationContext_ interface **supports message resolution** and internationalization **by extending the _MessageSource_ interface**. Furthermore, Spring provides two _MessageSource_ implementations, [_ResourceBundleMessageSource_ ](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/context/support/ResourceBundleMessageSource.html)and [_StaticMessageSource_](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/context/support/StaticMessageSource.html).

We can use the _StaticMessageSource_ to programmatically add messages to the source; however, it supports basic internationalization and is more suitable for tests than production use.

On the other hand, **_ResourceBundleMessageSource_ is the most common implementation of _MessageSource_**. It relies on the underlying JDK’s [_ResouceBundle_](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/ResourceBundle.html) implementation. It also uses the JDK’s standard message parsing provided by [_MessageFormat_](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/text/MessageFormat.html).

Now let’s see how can we use the _MessageSource_ to read the messages from a properties file.

First, we’ll create the _messages.properties_ file on the classpath:
    
    
    account.name=TestAccount

Second, we’ll add a bean definition in our _AccountConfig_ class:
    
    
    @Bean
    public MessageSource messageSource() {
      ResourceBundleMessageSource messageSource = new ResourceBundleMessageSource();
      messageSource.setBasename("config/messages");
      return messageSource;
    }

Third, we’ll inject the _MessageSource_ in the _AccountService_ :
    
    
    @Autowired
    private MessageSource messageSource;

Finally, we can use the _getMessage_ method anywhere in the _AccountService_ to read the message:
    
    
    messageSource.getMessage("account.name", null, Locale.ENGLISH);

Spring also provides the [_ReloadableResourceBundleMessageSource_ ](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/context/support/ReloadableResourceBundleMessageSource.html)class, which allows for reading files from any Spring resource location, and supports hot reloading of bundle property files.

### 7.2. Event Handling

_ApplicationContext_ supports event handling**with the help of the _ApplicationEvent_ class and the _ApplicationListener_ interface**. It supports [built-in events](/spring-context-events) like _ContextStartedEvent_ , _ContextStoppedEvent_ , _ContextClosedEvent_ , and _RequestHandledEvent_. Moreover, it also supports [custom events](/spring-events) for business use cases.

## 8\. Conclusion

In this article, we discussed various aspects of the _ApplicationContext_ container in Spring. We also explored different examples of how to configure Spring beans in an _AppicationContext_. Finally, we learned how to create and use different types of _ApplicationContext_.
