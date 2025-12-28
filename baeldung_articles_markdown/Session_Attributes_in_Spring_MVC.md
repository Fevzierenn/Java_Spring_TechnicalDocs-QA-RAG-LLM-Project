# Session Attributes in Spring MVC

## **1\. Overview**

When developing web applications, we often need to refer to the same attributes in several views. For example, we may have shopping cart contents that need to be displayed on multiple pages.

A good location to store those attributes is in the user’s session.

In this tutorial, we’ll focus on a simple example and **examine 2 different strategies for working with a session attribute** :

  * **Using a scoped proxy**
  * **Using the @_SessionAttributes_ annotation**



## **2\. Maven Setup**

We’ll use Spring Boot starters to bootstrap our project and bring in all necessary dependencies.

Our setup requires a parent declaration, web starter, and thymeleaf starter.

We’ll also include the spring test starter to provide some additional utility in our unit tests:
    
    
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <relativePath/>
    </parent>
     
    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-thymeleaf</artifactId>
         </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>

The most recent versions of these dependencies can be found [on Maven Central](https://mvnrepository.com/artifact/org.springframework.boot/spring-boot-starter-test).

## **3\. Example Use Case**

Our example will implement a simple “TODO” application. We’ll have a form for creating instances of _TodoItem_ and a list view that displays all _TodoItem_ s.

If we create a _TodoItem_ using the form, subsequent accesses of the form will be prepopulated with the values of the most recently added _TodoItem_. **We’ll use** t**his feature to demonstrate how to “remember” form values** that are stored in session scope.

Our 2 model classes are implemented as simple POJOs:
    
    
    public class TodoItem {
    
        private String description;
        private LocalDateTime createDate;
    
        // getters and setters
    }
    
    
    public class TodoList extends ArrayDeque<TodoItem>{
    
    }

Our _TodoList_ class extends _ArrayDeque_ to give us convenient access to the most recently added item via the _peekLast_ method.

We’ll need 2 controller classes: 1 for each of the strategies we’ll look at. They’ll have subtle differences but the core functionality will be represented in both. Each will have 3 _@RequestMapping_ s:

  * _**@GetMapping(“/form”)**_ – This method will be responsible for initializing the form and rendering the form view. The method will prepopulate the form with the most recently added _TodoItem_ if the _TodoList_ is not empty.
  * **_@PostMapping(“/form”)_** – This method will be responsible for adding the submitted _TodoItem_ to the _TodoList_ and redirecting to the list URL.
  * **_@GetMapping(“/todos.html”) –_** This method will simply add the _TodoList_ to the _Model_ for display and render the list view.



## **4\. Using a Scoped Proxy**

### **4.1. Setup**

In this setup, our _TodoList_ is configured as a session-scoped _@Bean_ that is backed by a proxy. The fact that the _@Bean_ is a proxy means that we are able to inject it into our singleton-scoped _@Controller_.

Since there is no session when the context initializes, Spring will create a proxy of _TodoList_ to inject as a dependency. The target instance of _TodoList_ will be instantiated as needed when required by requests.

For a more in-depth discussion of bean scopes in Spring, refer to our [article on the topic](/spring-bean-scopes).

First, we define our bean within a _@Configuration_ class:
    
    
    @Bean
    @Scope(
      value = WebApplicationContext.SCOPE_SESSION, 
      proxyMode = ScopedProxyMode.TARGET_CLASS)
    public TodoList todos() {
        return new TodoList();
    }

Next, we declare the bean as a dependency for the _@Controller_ and inject it just as we would any other dependency:
    
    
    @Controller
    @RequestMapping("/scopedproxy")
    public class TodoControllerWithScopedProxy {
    
        private TodoList todos;
    
        // constructor and request mappings
    }
    

Finally, using the bean in a request simply involves calling its methods:
    
    
    @GetMapping("/form")
    public String showForm(Model model) {
        if (!todos.isEmpty()) {
            model.addAttribute("todo", todos.peekLast());
        } else {
            model.addAttribute("todo", new TodoItem());
        }
        return "scopedproxyform";
    }

### **4.2. Unit Testing**

In order to test our implementation using the scoped proxy, **we first configure a _SimpleThreadScope_** _._ This will ensure that our unit tests accurately simulate runtime conditions of the code we are testing.

First, we define a _TestConfig_ and a _CustomScopeConfigurer_ :
    
    
    @Configuration
    public class TestConfig {
    
        @Bean
        public CustomScopeConfigurer customScopeConfigurer() {
            CustomScopeConfigurer configurer = new CustomScopeConfigurer();
            configurer.addScope("session", new SimpleThreadScope());
            return configurer;
        }
    }

Now we can start by testing that an initial request of the form contains an uninitialized _TodoItem:_
    
    
    @RunWith(SpringRunner.class) 
    @SpringBootTest
    @AutoConfigureMockMvc
    @Import(TestConfig.class) 
    public class TodoControllerWithScopedProxyIntegrationTest {
    
        // ...
    
        @Test
        public void whenFirstRequest_thenContainsUnintializedTodo() throws Exception {
            MvcResult result = mockMvc.perform(get("/scopedproxy/form"))
              .andExpect(status().isOk())
              .andExpect(model().attributeExists("todo"))
              .andReturn();
    
            TodoItem item = (TodoItem) result.getModelAndView().getModel().get("todo");
     
            assertTrue(StringUtils.isEmpty(item.getDescription()));
        }
    }
    
    

We can also confirm that our submit issues a redirect and that a subsequent form request is prepopulated with the newly added _TodoItem_ :
    
    
    @Test
    public void whenSubmit_thenSubsequentFormRequestContainsMostRecentTodo() throws Exception {
        mockMvc.perform(post("/scopedproxy/form")
          .param("description", "newtodo"))
          .andExpect(status().is3xxRedirection())
          .andReturn();
    
        MvcResult result = mockMvc.perform(get("/scopedproxy/form"))
          .andExpect(status().isOk())
          .andExpect(model().attributeExists("todo"))
          .andReturn();
        TodoItem item = (TodoItem) result.getModelAndView().getModel().get("todo");
     
        assertEquals("newtodo", item.getDescription());
    }

### **4.3. Discussion**

A key feature of using the scoped proxy strategy is that **it has no impact on request mapping method signatures.** This keeps readability on a very high level compared to the _@SessionAttributes_ strategy.

It can be helpful to recall that controllers have _singleton_ scope by default.

This is the reason why we must use a proxy instead of simply injecting a non-proxied session-scoped bean. **We can’t inject a bean with a lesser scope into a bean with greater scope.**

Attempting to do so, in this case, would trigger an exception with a message containing: _Scope ‘session’ is not active for the current thread_.

If we’re willing to define our controller with session scope, we could avoid specifying a _proxyMode_. This can have disadvantages, especially if the controller is expensive to create because a controller instance would have to be created for each user session.

Note that _TodoList_ is available to other components for injection. This may be a benefit or a disadvantage depending on the use case. If making the bean available to the entire application is problematic, the instance can be scoped to the controller instead using _@SessionAttributes_ as we’ll see in the next example.

## **5\. Using the _@SessionAttributes_ Annotation**

### **5.1. Setup**

In this setup, we don’t define _TodoList_ as a Spring-managed _@Bean_. Instead, we **declare it as a _@ModelAttribute_ and specify the _@SessionAttributes_ annotation to scope it to the session for the controller**.

The first time our controller is accessed, Spring will instantiate an instance and place it in the _Model_. Since we also declare the bean in _@SessionAttributes_ , Spring will store the instance.

For a more in-depth discussion of _@ModelAttribute_ in Spring, refer to our [article on the topic](/spring-mvc-and-the-modelattribute-annotation).

First, we declare our bean by providing a method on the controller and we annotate the method with _@ModelAttribute_ :
    
    
    @ModelAttribute("todos")
    public TodoList todos() {
        return new TodoList();
    }
    

Next, we inform the controller to treat our _TodoList_ as session-scoped by using _@SessionAttributes_ :
    
    
    @Controller
    @RequestMapping("/sessionattributes")
    @SessionAttributes("todos")
    public class TodoControllerWithSessionAttributes {
        // ... other methods
    }

Finally, to use the bean within a request, we provide a reference to it in the method signature of a _@RequestMapping_ :
    
    
    @GetMapping("/form")
    public String showForm(
      Model model,
      @ModelAttribute("todos") TodoList todos) {
     
        if (!todos.isEmpty()) {
            model.addAttribute("todo", todos.peekLast());
        } else {
            model.addAttribute("todo", new TodoItem());
        }
        return "sessionattributesform";
    }
    

In the _@PostMapping_ method, we inject _RedirectAttributes_ and call _addFlashAttribute_ before returning our _RedirectView_. This is an important difference in implementation compared to our first example:
    
    
    @PostMapping("/form")
    public RedirectView create(
      @ModelAttribute TodoItem todo, 
      @ModelAttribute("todos") TodoList todos, 
      RedirectAttributes attributes) {
        todo.setCreateDate(LocalDateTime.now());
        todos.add(todo);
        attributes.addFlashAttribute("todos", todos);
        return new RedirectView("/sessionattributes/todos.html");
    }

Spring uses a specialized _RedirectAttributes_ implementation of _Model_ for redirect scenarios to support the encoding of URL parameters. During a redirect, any attributes stored on the _Model_ would normally only be available to the framework if they were included in the URL.

**By using _addFlashAttribute_ we are telling the framework that we want our _TodoList_ to survive the redirect** without needing to encode it in the URL.

### **5.2. Unit Testing**

The unit testing of the form view controller method is identical to the test we looked at in our first example. The test of the _@PostMapping_ , however, is a little different because we need to access the flash attributes in order to verify the behavior:
    
    
    @Test
    public void whenTodoExists_thenSubsequentFormRequestContainsesMostRecentTodo() throws Exception {
        FlashMap flashMap = mockMvc.perform(post("/sessionattributes/form")
          .param("description", "newtodo"))
          .andExpect(status().is3xxRedirection())
          .andReturn().getFlashMap();
    
        MvcResult result = mockMvc.perform(get("/sessionattributes/form")
          .sessionAttrs(flashMap))
          .andExpect(status().isOk())
          .andExpect(model().attributeExists("todo"))
          .andReturn();
        TodoItem item = (TodoItem) result.getModelAndView().getModel().get("todo");
     
        assertEquals("newtodo", item.getDescription());
    }

### **5.3. Discussion**

The _@ModelAttribute_ and _@SessionAttributes_ strategy for storing an attribute in the session is a straightforward solution that **requires no additional context configuration or Spring-managed _@Bean_ s**.

Unlike our first example, it’s necessary to inject _TodoList_ in the _@RequestMapping_ methods _._

In addition, we must make use of flash attributes for redirect scenarios.

## **6\. Conclusion**

In this article, we looked at using scoped proxies and _@SessionAttributes_ as 2 strategies for working with session attributes in Spring MVC. Note that in this simple example, any attributes stored in session will only survive for the life of the session.

If we needed to persist attributes between server restarts or session timeouts, we could consider using Spring Session to transparently handle saving the information. Have a look at [our article](/spring-session) on Spring Session for more information.
