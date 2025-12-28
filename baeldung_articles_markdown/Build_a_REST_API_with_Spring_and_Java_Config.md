# Build a REST API with Spring and Java Config

## **1\. Overview**

In this tutorial, we’ll learn how to **set up[REST](/cs/rest-architecture) in Spring,** including the Controller and HTTP response codes, configuration of payload marshalling, and content negotiation.

## 2\. Dependencies

To create a REST API when using Spring Boot, we need the [Spring Boot Starter Web](https://mvnrepository.com/artifact/org.springframework.boot/spring-boot-starter-web) dependency, which bundles libraries for building web applications, handling HTTP requests, and JSON serialization: Simply include the following dependency in our _pom.xml_ :
    
    
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>

Spring Boot automatically sets up Jackson as the default serializer and deserializer for converting between Java objects and JSON.

## 3\. **The Controller**

**The _@RestController_ is the central artifact in the entire Web Tier of the RESTful API.** For the purpose of this article, the controller is modeling a simple REST resource, _Foo_ :
    
    
    @RestController
    @RequestMapping("/foos")
    class FooController {
    
        @Autowired
        private IFooService service;
    
        @GetMapping
        public List<Foo> findAll() {
            return service.findAll();
        }
    
        @GetMapping(value = "/{id}")
        public Foo findById(@PathVariable("id") Long id) {
            return RestPreconditions.checkFound(service.findById(id));
        }
    
        @PostMapping
        @ResponseStatus(HttpStatus.CREATED)
        public Long create(@RequestBody Foo resource) {
            Preconditions.checkNotNull(resource);
            return service.create(resource);
        }
    
        @PutMapping(value = "/{id}")
        @ResponseStatus(HttpStatus.OK)
        public void update(@PathVariable( "id" ) Long id, @RequestBody Foo resource) {
            Preconditions.checkNotNull(resource);
            RestPreconditions.checkNotNull(service.getById(resource.getId()));
            service.update(resource);
        }
    
        @DeleteMapping(value = "/{id}")
        @ResponseStatus(HttpStatus.OK)
        public void delete(@PathVariable("id") Long id) {
            service.deleteById(id);
        }
    
    }

As we can see, we’re using a straightforward, Guava-style _RestPreconditions_ utility:
    
    
    public class RestPreconditions {
        public static <T> T checkFound(T resource) {
            if (resource == null) {
                throw new MyResourceNotFoundException();
            }
            return resource;
        }
    }

**The Controller implementation is non-public because it doesn’t need to be.**

Usually, the controller is the last in the chain of dependencies. It receives HTTP requests from the Spring front controller (the _DispatcherServlet_) and simply delegates them forward to a service layer. If there’s no use case where the controller has to be injected or manipulated through a direct reference, then we may prefer not to declare it as public.

The request mappings are straightforward.**As with any controller, the actual _value_ of the mapping, as well as the HTTP method, determines the target method for the request.** @_RequestBody_ will bind the parameters of the method to the body of the HTTP request, whereas _@ResponseBody_ does the same for the response and return type.

**The _@RestController_ is a [shorthand](/spring-controller-vs-restcontroller) to include both the  _@ResponseBody_ and the _@Controller_ annotations in our class _._**

They also ensure that the resource will be marshalled and unmarshalled using the correct HTTP converter. Content negotiation will take place to choose which one of the active converters will be used, based mostly on the _Accept_ header, although other HTTP headers may be used to determine the representation as well.

## **4\. Testing the Spring Context**

When testing a Spring Boot application, the process is much easier thanks to Spring Boot’s autoconfiguration and testing annotations.

If we want to test the full application context without starting the server, we can use the _@SpringBootTest_ annotation.

With that in place, we can then add the _@AutoConfigureMockMvc_ to inject a  _MockMvc_ instance and send HTTP requests _:_
    
    
    @RunWith(SpringRunner.class)
    @SpringBootTest
    @AutoConfigureMockMvc
    public class FooControllerAppIntegrationTest {
    
        @Autowired
        private MockMvc mockMvc;
    
        @Test
        public void whenTestApp_thenEmptyResponse() throws Exception {
            this.mockMvc.perform(get("/foos")
              .andExpect(status().isOk())
              .andExpect(...);
        }
    
    }

To test only the web layer and avoid loading unnecessary parts of the application, we can use the _@WebMvcTest_ annotation:
    
    
    @RunWith(SpringRunner.class)
    @WebMvcTest(FooController.class)
    public class FooControllerWebLayerIntegrationTest {
    
        @Autowired
        private MockMvc mockMvc;
    
        @MockBean
        private IFooService service;
    
        @Test()
        public void whenTestMvcController_thenRetrieveExpectedResult() throws Exception {
            // ...
    
            this.mockMvc.perform(get("/foos")
              .andExpect(...);
        }
    }

By using _@WebMvcTest_ , we focus only on testing the MVC layer, with Spring Boot automatically setting up the context for just the controller layer and dependencies (like mock services).

## **5\. Mapping the HTTP Response Codes**

The status codes of the HTTP response are one of the most important parts of the REST service, and the subject can quickly become very complicated. Getting these right can be what makes or breaks the service.

### **5.1. Unmapped Requests**

If Spring MVC receives a request which doesn’t have a mapping, it considers the request not allowed, and returns a 405 METHOD NOT ALLOWED back to the client.

It’s also good practice to include the _Allow_ HTTP header when returning a _405_ to the client to specify which operations are allowed. This is the standard behavior of Spring MVC and doesn’t require any additional configuration.

### **5.2. Valid Mapped Requests**

For any request that does have a mapping, Spring MVC considers the request valid and responds with 200 OK, if no other status code is otherwise specified.

It’s because of this that the controller declares different _@ResponseStatus_ for the _create_ , _update,_ and _delete_ actions, but not for _get_ , which should indeed return the default 200 OK.

### **5.3. Client Error**

**In the case of a client error, custom exceptions are defined and mapped to the appropriate error codes.**

Simply throwing these exceptions from any of the layers of the web tier will ensure Spring maps the corresponding status code on the HTTP response:
    
    
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public class BadRequestException extends RuntimeException {
       //
    }
    @ResponseStatus(HttpStatus.NOT_FOUND)
    public class ResourceNotFoundException extends RuntimeException {
       //
    }

These exceptions are part of the REST API, and as such, we should only use them in the appropriate layers corresponding to REST; for instance, if a DAO/DAL layer exists, it shouldn’t use the exceptions directly.

Note also that these aren’t checked exceptions, but runtime exceptions in line with Spring practices and idioms.

### **5.4. Using _@ExceptionHandler_**

Another option to map custom exceptions on specific status codes is to use the _@ExceptionHandler_ annotation in the controller. The problem with that approach is that the annotation only applies to the controller in which it’s defined. This means that we need to declare them in each controller individually.

Of course, there are more [ways to handle errors](/exception-handling-for-rest-with-spring) in both Spring and Spring Boot that offer more flexibility.

## **6\. Conclusion**

This article illustrated how to implement and configure a REST Service using Spring and Java-based configuration.

In the next articles in the series, we’ll focus on the [Discoverability of the API](/restful-web-service-discoverability "HATEOAS for the API"), advanced content negotiation, and working with additional representations of a _Resource._
