# Integration Testing in Spring

## **1\. Overview**

Integration testing plays an important role in the application development cycle by verifying the end-to-end behavior of a system.

In this tutorial, we’ll learn how to leverage the [Spring MVC](/spring-mvc) test framework to write and run integration tests that test controllers without explicitly starting a Servlet container.

## **2\. Preparation**

We’ll need several Maven dependencies to run the integration tests we’ll use in this article. First and foremost, we’ll need the latest [junit-jupiter-engine](https://mvnrepository.com/artifact/org.junit.jupiter/junit-jupiter-engine), [junit-jupiter-api](https://mvnrepository.com/artifact/org.junit.jupiter/junit-jupiter-api), and [Spring test](https://search.maven.org/classic/#search%7Cgav%7C1%7Cg%3A%22org.springframework%22%20AND%20a%3A%22spring-test%22) dependencies:
    
    
    <dependency>
        <groupId>org.junit.jupiter</groupId>
        <artifactId>junit-jupiter-engine</artifactId>
        <version>5.10.2</version>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>org.junit.jupiter</groupId>
        <artifactId>junit-jupiter-api</artifactId>
        <version>5.10.2</version>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>org.springframework</groupId>
        <artifactId>spring-test</artifactId>
        <version>6.0.13</version>
        <scope>test</scope>
    </dependency>

## **3\. Spring MVC Test Configuration**

Now, let’s see how to configure and run the Spring-enabled tests.

### **3.1. Enable Spring in Tests With JUnit 5**

[JUnit 5](/junit-5) defines an extension interface through which classes can integrate with the JUnit test.

We can enable this extension **by adding the _@ExtendWith_ annotation to our test classes and specifying the extension class to load**. To run the Spring test, we use _SpringExtension.class._

We’ll also need the **_@ContextConfiguration_ annotation to load the context configuration and****bootstrap the context that our test will use**.

Let’s have a look:
    
    
    @ExtendWith(SpringExtension.class)
    @ContextConfiguration(classes = { ApplicationConfig.class })
    @WebAppConfiguration
    public class GreetControllerIntegrationTest {
        ....
    }

Notice that in _@ContextConfiguration,_ we provided the _ApplicationConfig.class_ config class, which loads the configuration we need for this particular test.

We’ll use a Java configuration class here to specify the context configuration. Similarly, we can use the XML-based configuration:
    
    
    @ContextConfiguration(locations={""})

Finally, we’ll also annotate the test with **@_WebAppConfiguration_ , which will load the web application context**.

By default, it looks for the root web application at path _src/main/webapp._ We can override this location by simply passing the _value_ attribute:
    
    
    @WebAppConfiguration(value = "")

### **3.2. The _WebApplicationContext_ Object**

_WebApplicationContext_ provides a web application configuration. It loads all the application beans and controllers into the context.

Now, we’ll be able to wire the web application context right into the test:
    
    
    @Autowired
    private WebApplicationContext webApplicationContext;

### **3.3. Mocking Web Context Beans**

_MockMvc_ provides support for Spring MVC testing.**It encapsulates all web application beans and makes them available for testing.**

Let’s see how to use it:
    
    
    private MockMvc mockMvc;
    @BeforeEach
    public void setup() throws Exception {
        this.mockMvc = MockMvcBuilders.webAppContextSetup(this.webApplicationContext).build();
    }

We’ll initialize the _mockMvc_ object in the _@BeforeEach_ annotated method so that we don’t have to initialize it inside every test.

### **3.4. Verify Test Configuration**

Let’s verify that we’re loading the _WebApplicationContext_ object (_webApplicationContext_) properly. We’ll also check that the right _servletContext_ is being attached:
    
    
    @Test
    public void givenWac_whenServletContext_thenItProvidesGreetController() {
        ServletContext servletContext = webApplicationContext.getServletContext();
        
        assertNotNull(servletContext);
        assertTrue(servletContext instanceof MockServletContext);
        assertNotNull(webApplicationContext.getBean("greetController"));
    }

Notice that we’re also checking that a _GreetController.java_ bean exists in the web context. This ensures that Spring beans are loaded properly. At this point, the setup of the integration test is done. Now, we’ll see how we can test resource methods using the _MockMvc_ object.

## **4\. Writing Integration Tests**

In this section, we’ll go over the basic operations available through the test framework.

We’ll look at how to send requests with path variables and parameters. We’ll also follow with a few examples that show how to assert that the proper view name is resolved, or that the response body is as expected.

The snippets that are shown below use static imports from the M _ockMvcRequestBuilders_ or _MockMvcResultMatchers_ classes.

### **4.1. Verify View Name**

We can invoke the _/homePage_ endpoint from our test as _:_
    
    
    http://localhost:8080/spring-mvc-test/

or
    
    
    http://localhost:8080/spring-mvc-test/homePage

First, let’s see the test code:
    
    
    @Test
    public void givenHomePageURI_whenMockMVC_thenReturnsIndexJSPViewName() {
        this.mockMvc.perform(get("/homePage")).andDo(print())
          .andExpect(view().name("index"));
    }

Let’s break it down:

  * _perform()_ method will call a GET request method, which returns the _ResultActions_. Using this result, we can have assertion expectations about the response, like its content, HTTP status, or header.
  * _andDo(print())_ will print the request and response. This is helpful to get a detailed view in case of an error.
  * _andExpect()_ will expect the provided argument. In our case, we’re expecting “index” to be returned via _MockMvcResultMatchers.view()._



### **4.2. Verify Response Body**

We’ll invoke the _/greet_ endpoint from our test as:
    
    
    http://localhost:8080/spring-mvc-test/greet

The expected output will be:
    
    
    {
        "id": 1,
        "message": "Hello World!!!"
    }

Let’s see the test code:
    
    
    @Test
    public void givenGreetURI_whenMockMVC_thenVerifyResponse() {
        MvcResult mvcResult = this.mockMvc.perform(get("/greet"))
          .andDo(print()).andExpect(status().isOk())
          .andExpect(jsonPath("$.message").value("Hello World!!!"))
          .andReturn();
        
        assertEquals("application/json;charset=UTF-8", mvcResult.getResponse().getContentType());
    }

Let’s see exactly what’s going on:

  * _andExpect(MockMvcResultMatchers.status().isOk())_ will verify that the response HTTP status is _Ok_ (_200)_. This ensures that the request is successfully executed.
  * _andExpect(MockMvcResultMatchers.jsonPath(“$.message”).value(“Hello World!!!”))_ will verify that the response content matches with the argument “ _Hello World!!!_ ” Here, we used _jsonPath_ , which extracts the response content and provides the requested value.
  * _andReturn()_ will return the _MvcResult_ object, which is used when we have to verify something that isn’t directly achievable by the library. In this case, we’ve added _assertEquals_ to match the content type of the response that is extracted from the _MvcResult_ object.



### **4.****3\. Send GET Request With Path Variable**

We’ll invoke the _/greetWithPathVariable/{name}_ endpoint from our test as:
    
    
    http://localhost:8080/spring-mvc-test/greetWithPathVariable/John

The expected output will be:
    
    
    {
        "id": 1,
        "message": "Hello World John!!!"
    }

Let’s see the test code:
    
    
    @Test
    public void givenGreetURIWithPathVariable_whenMockMVC_thenResponseOK() {
        this.mockMvc
          .perform(get("/greetWithPathVariable/{name}", "John"))
          .andDo(print()).andExpect(status().isOk())
          .andExpect(content().contentType("application/json;charset=UTF-8"))
          .andExpect(jsonPath("$.message").value("Hello World John!!!"));
    }

_MockMvcRequestBuilders.get(“/greetWithPathVariable/{name}”, “John”)_ will send a request as “ _/greetWithPathVariable/John._ ”

This becomes easier with respect to readability and knowing what parameters are dynamically set in the URL. Note that we can pass as many path parameters as needed.

### **4.4. Send GET Request With Query Parameters**

We’ll invoke the _/greetWithQueryVariable?name={name}_ endpoint from our test as:
    
    
    http://localhost:8080/spring-mvc-test/greetWithQueryVariable?name=John%20Doe

In this case, the expected output will be:
    
    
    {
        "id": 1,
        "message": "Hello World John Doe!!!"
    }

Now, let’s see the test code:
    
    
    @Test
    public void givenGreetURIWithQueryParameter_whenMockMVC_thenResponseOK() {
        this.mockMvc.perform(get("/greetWithQueryVariable")
          .param("name", "John Doe")).andDo(print()).andExpect(status().isOk())
          .andExpect(content().contentType("application/json;charset=UTF-8"))
          .andExpect(jsonPath("$.message").value("Hello World John Doe!!!"));
    }

**_param(“name”, “John Doe”)_ will append the query parameter in the GET request**. This is similar to “ _/greetWithQueryVariable?name=John%20Doe.__“_

The query parameter can also be implemented using the URI template style:
    
    
    this.mockMvc.perform(
      get("/greetWithQueryVariable?name={name}", "John Doe"));

### **4.5. Send POST Request**

We’ll invoke the _/greetWithPost_ endpoint from our test as:
    
    
    http://localhost:8080/spring-mvc-test/greetWithPost

We should obtain the output:
    
    
    {
        "id": 1,
        "message": "Hello World!!!"
    }

And our test code is:
    
    
    @Test
    public void givenGreetURIWithPost_whenMockMVC_thenVerifyResponse() {
        this.mockMvc.perform(post("/greetWithPost")).andDo(print())
          .andExpect(status().isOk()).andExpect(content()
          .contentType("application/json;charset=UTF-8"))
          .andExpect(jsonPath("$.message").value("Hello World!!!"));
    }

_**MockMvcRequestBuilders.post(“/greetWithPost”)**_**will send the POST request**. We can set path variables and query parameters in a similar way as before, whereas form data can be set only via the _param()_ method, similar to query parameters as:
    
    
    http://localhost:8080/spring-mvc-test/greetWithPostAndFormData

Then the data will be:
    
    
    id=1;name=John%20Doe

So we should get:
    
    
    {
        "id": 1,
        "message": "Hello World John Doe!!!"
    }

Let’s see our test:
    
    
    @Test
    public void givenGreetURI_whenMockMVC_thenVerifyResponse() throws Exception {
        MvcResult mvcResult = this.mockMvc.perform(MockMvcRequestBuilders.get("/greet"))
          .andDo(print())
          .andExpect(MockMvcResultMatchers.status().isOk())
          .andExpect(MockMvcResultMatchers.jsonPath("$.message").value("Hello World!!!"))
          .andReturn();
     
       assertEquals("application/json;charset=UTF-8", mvcResult.getResponse().getContentType());
    }

In the above code snippet, we’ve added two parameters: _id_ as “1” and _name_ as “John Doe.”

## 5\. _MockMvc_ Limitations

_MockMvc_ provides an elegant and easy-to-use API to call web endpoints and to inspect and assert their response at the same time. Despite all its benefits, it has a few limitations.

First of all, it does use a subclass of the  _[DispatcherServlet](https://docs.spring.io/spring/docs/current/javadoc-api/org/springframework/web/servlet/DispatcherServlet.html) _to handle test requests. To be more specific, the  _[TestDispatcherServlet](https://github.com/spring-projects/spring-framework/blob/622ccc57672ffed758220b33a08f8215334cdb2d/spring-test/src/main/java/org/springframework/test/web/servlet/TestDispatcherServlet.java#L53) _is responsible for calling controllers and performing all the familiar Spring magic.

The  _MockMvc_ class [wraps](https://github.com/spring-projects/spring-framework/blob/622ccc57672ffed758220b33a08f8215334cdb2d/spring-test/src/main/java/org/springframework/test/web/servlet/MockMvc.java#L72) this  _TestDispatcherServlet_ internally. So, every time we send a request using the _perform()_ method, _MockMvc_ will use the underlying  _TestDispatcherServlet_ directly. Therefore, no real network connections are made, and consequently, we won’t test the whole network stack while using _MockMvc_.

Also, **because Spring prepares a fake web application context to mock the HTTP requests and responses, it may not support all the features of a full-blown Spring application**.

For example, this mock setup doesn’t support [HTTP redirections](https://github.com/spring-projects/spring-boot/issues/7321). This may not seem that significant at first. However, Spring Boot handles some errors by redirecting the current request to the _/error_ endpoint. So, if we’re using the _MockMvc,_ we may not be able to test some API failures.

As an alternative to _MockMvc,_ we can set up a more real application context __ and then use _[RestTemplate](/rest-template), _or even [REST-assured](/rest-assured-tutorial), to test our application.

For instance, this is easy using Spring Boot:
    
    
    @SpringBootTest(webEnvironment = DEFINED_PORT)
    public class GreetControllerRealIntegrationTest {
    
        @Before
        public void setUp() {
            RestAssured.port = DEFAULT_PORT;
        }
    
        @Test
        public void givenGreetURI_whenSendingReq_thenVerifyResponse() {
            given().get("/greet")
              .then()
              .statusCode(200);
        }
    }

Here, we don’t even need to add the _@ExtendWith(SpringExtension.class)_.

This way, every test will make a real HTTP request to the application that listens on a random TCP port.

## **6\. Conclusion**

In this article, we implemented a few simple Spring-enabled integration tests.

We also looked at the _WebApplicationContext_ and _MockMvc_ object creation, which plays an important role in calling the endpoints of the application.

Looking further, we discussed how to send GET and POST requests with variations of parameter passing and how to verify the HTTP response status, header, and content.

Then, we evaluated some limitations of _MockMvc._ Knowing these limitations can guide us to make an informed decision about how we’re going to implement our tests.
