# Quick Guide to Spring Bean Scopes

## **1\. Overview**

In this quick tutorial, we’ll learn about the different types of bean scopes in the Spring framework.

The scope of a bean defines the life cycle and visibility of that bean in the contexts we use it.

The latest version of the Spring framework defines 6 types of scopes:

  * singleton
  * prototype
  * request
  * session
  * application
  * websocket



The last four scopes mentioned, _request, session, application_ and _websocket_ , are only available in a web-aware application.

## **2\. Singleton Scope**

When we define a bean with the _singleton_ scope, the container creates a single instance of that bean; all requests for that bean name will return the same object, which is cached. Any modifications to the object will be reflected in all references to the bean. This scope is the default value if no other scope is specified.

Let’s create a _Person_ entity to exemplify the concept of scopes:
    
    
    public class Person {
        private String name;
    
        // standard constructor, getters and setters
    }

Afterwards, we define the bean with the _singleton_ scope by using the _@Scope_ annotation:
    
    
    @Bean
    @Scope("singleton")
    public Person personSingleton() {
        return new Person();
    }

We can also use a constant instead of the _String_ value in the following manner:
    
    
    @Scope(value = ConfigurableBeanFactory.SCOPE_SINGLETON)

Now we can proceed to write a test that shows that two objects referring to the same bean will have the same values, even if only one of them changes their state, as they are both referencing the same bean instance:
    
    
    private static final String NAME = "John Smith";
    
    @Test
    public void givenSingletonScope_whenSetName_thenEqualNames() {
        ApplicationContext applicationContext = 
          new ClassPathXmlApplicationContext("scopes.xml");
    
        Person personSingletonA = (Person) applicationContext.getBean("personSingleton");
        Person personSingletonB = (Person) applicationContext.getBean("personSingleton");
    
        personSingletonA.setName(NAME);
        Assert.assertEquals(NAME, personSingletonB.getName());
    
        ((AbstractApplicationContext) applicationContext).close();
    }

The _scopes.xml_ file in this example should contain the xml definitions of the beans used:
    
    
    <?xml version="1.0" encoding="UTF-8"?>
    <beans xmlns="http://www.springframework.org/schema/beans"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://www.springframework.org/schema/beans 
        http://www.springframework.org/schema/beans/spring-beans.xsd">
    
        <bean id="personSingleton" class="org.baeldung.scopes.Person" scope="singleton"/>    
    </beans>

## **3\. Prototype Scope**

A bean with the _prototype_ scope will return a different instance every time it is requested from the container. It is defined by setting the value _prototype_ to the _@Scope_ annotation in the bean definition:
    
    
    @Bean
    @Scope("prototype")
    public Person personPrototype() {
        return new Person();
    }

We can also use a constant like we did for the _singleton_ scope:
    
    
    @Scope(value = ConfigurableBeanFactory.SCOPE_PROTOTYPE)

We will now write a similar test as before that shows two objects requesting the same bean name with the  _prototype_ scope. They will have different states as they are no longer referring to the same bean instance:
    
    
    private static final String NAME = "John Smith";
    private static final String NAME_OTHER = "Anna Jones";
    
    @Test
    public void givenPrototypeScope_whenSetNames_thenDifferentNames() {
        ApplicationContext applicationContext = 
          new ClassPathXmlApplicationContext("scopes.xml");
    
        Person personPrototypeA = (Person) applicationContext.getBean("personPrototype");
        Person personPrototypeB = (Person) applicationContext.getBean("personPrototype");
    
        personPrototypeA.setName(NAME);
        personPrototypeB.setName(NAME_OTHER);
    
        Assert.assertEquals(NAME, personPrototypeA.getName());
        Assert.assertEquals(NAME_OTHER, personPrototypeB.getName());
    
        ((AbstractApplicationContext) applicationContext).close();
    }
    

The _scopes.xml_ file is similar to the one presented in the previous section while adding the xml definition for the bean with the _prototype_ scope:
    
    
    <bean id="personPrototype" class="org.baeldung.scopes.Person" scope="prototype"/>

## **4\. Web Aware Scopes**

As previously mentioned, there are four additional scopes that are only available in a web-aware application context. We use these less often in practice.

The _request_ scope creates a bean instance for a single HTTP request, while the s _ession_ scope creates a bean instance for an HTTP Session.

The _application_ scope creates the bean instance for the lifecycle of a _ServletContext_ , and the _websocket_ scope creates it for a particular _WebSocket_ session.

Let’s create a class to use for instantiating the beans:
    
    
    public class HelloMessageGenerator {
        private String message;
        
        // standard getter and setter
    }

### **4.1. Request Scope**

We can define the bean with the _request_ scope using the _@Scope_ annotation:
    
    
    @Bean
    @Scope(value = WebApplicationContext.SCOPE_REQUEST, proxyMode = ScopedProxyMode.TARGET_CLASS)
    public HelloMessageGenerator requestScopedBean() {
        return new HelloMessageGenerator();
    }

The _proxyMode_ attribute is necessary because at the moment of the instantiation of the web application context, there is no active request. Spring creates a proxy to be injected as a dependency, and instantiates the target bean when it is needed in a request.

We can also use a _@RequestScope_ composed annotation that acts as a shortcut for the above definition:
    
    
    @Bean
    @RequestScope
    public HelloMessageGenerator requestScopedBean() {
        return new HelloMessageGenerator();
    }

Next we can define a controller that has an injected reference to the _requestScopedBean_. We need to access the same request twice in order to test the web specific scopes.

If we display the _message_ each time the request is run, we can see that the value is reset to _null_ , even though it is later changed in the method. This is because of a different bean instance being returned for each request.
    
    
    @Controller
    public class ScopesController {
        @Resource(name = "requestScopedBean")
        HelloMessageGenerator requestScopedBean;
    
        @RequestMapping("/scopes/request")
        public String getRequestScopeMessage(final Model model) {
            model.addAttribute("previousMessage", requestScopedBean.getMessage());
            requestScopedBean.setMessage("Good morning!");
            model.addAttribute("currentMessage", requestScopedBean.getMessage());
            return "scopesExample";
        }
    }

### **4.2. Session Scope**

We can define the bean with the _session_ scope in a similar manner:
    
    
    @Bean
    @Scope(value = WebApplicationContext.SCOPE_SESSION, proxyMode = ScopedProxyMode.TARGET_CLASS)
    public HelloMessageGenerator sessionScopedBean() {
        return new HelloMessageGenerator();
    }

There’s also a dedicated composed annotation we can use to simplify the bean definition:
    
    
    @Bean
    @SessionScope
    public HelloMessageGenerator sessionScopedBean() {
        return new HelloMessageGenerator();
    }

Next we define a controller with a reference to the _sessionScopedBean_. Again, we need to run two requests in order to show that the value of the _message_ field is the same for the session.

In this case, when the request is made for the first time, the value _message_ is _null._ However, once it is changed, that value is retained for subsequent requests as the same instance of the bean is returned for the entire session.
    
    
    @Controller
    public class ScopesController {
        @Resource(name = "sessionScopedBean")
        HelloMessageGenerator sessionScopedBean;
    
        @RequestMapping("/scopes/session")
        public String getSessionScopeMessage(final Model model) {
            model.addAttribute("previousMessage", sessionScopedBean.getMessage());
            sessionScopedBean.setMessage("Good afternoon!");
            model.addAttribute("currentMessage", sessionScopedBean.getMessage());
            return "scopesExample";
        }
    }

### **4.3. Application Scope**

The _application_ scope creates the bean instance for the lifecycle of a _ServletContext._

This is similar to the _singleton_ scope, but there is a very important difference with regards to the scope of the bean.

When beans are _application_ scoped, the same instance of the bean is shared across multiple servlet-based applications running in the same _ServletContext_ , while _singleton_ scoped beans are scoped to a single application context only.

Let’s create the bean with the _application_ scope:
    
    
    @Bean
    @Scope(
      value = WebApplicationContext.SCOPE_APPLICATION, proxyMode = ScopedProxyMode.TARGET_CLASS)
    public HelloMessageGenerator applicationScopedBean() {
        return new HelloMessageGenerator();
    }

Analogous to the _request_ and _session_ scopes, we can use a shorter version:
    
    
    @Bean
    @ApplicationScope
    public HelloMessageGenerator applicationScopedBean() {
        return new HelloMessageGenerator();
    }

Now let’s create a controller that references this bean:
    
    
    @Controller
    public class ScopesController {
        @Resource(name = "applicationScopedBean")
        HelloMessageGenerator applicationScopedBean;
    
        @RequestMapping("/scopes/application")
        public String getApplicationScopeMessage(final Model model) {
            model.addAttribute("previousMessage", applicationScopedBean.getMessage());
            applicationScopedBean.setMessage("Good afternoon!");
            model.addAttribute("currentMessage", applicationScopedBean.getMessage());
            return "scopesExample";
        }
    }

In this case, once set in the _applicationScopedBean_ , the value _message_ will be retained for all subsequent requests, sessions and even for different servlet applications that will access this bean, provided it is running in the same _ServletContext._

### **4.4. WebSocket Scope**

Finally, let’s create the bean with the _websocket_ scope:
    
    
    @Bean
    @Scope(scopeName = "websocket", proxyMode = ScopedProxyMode.TARGET_CLASS)
    public HelloMessageGenerator websocketScopedBean() {
        return new HelloMessageGenerator();
    }

When first accessed, _WebSocket_ scoped beans are stored in the _WebSocket_ session attributes. The same instance of the bean is then returned whenever that bean is accessed during the entire _WebSocket_ session.

We can also say that it exhibits singleton behavior, but limited to a _W_ _ebSocket_ session only.

## **5\. Conclusion**

In this article, we discussed the different bean scopes provided by Spring and what their intended uses are.
