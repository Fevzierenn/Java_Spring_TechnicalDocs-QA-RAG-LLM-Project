# Why Choose Spring as Your Java Framework?

## 1\. Overview

In this article, we’ll go through the main value proposition of [Spring](https://spring.io/) as one of the most popular Java frameworks.

More importantly, we’ll try to understand the reasons for Spring being our framework of choice. Details of Spring and its constituent parts have been [widely covered in our previous tutorials](/spring-intro). Hence we’ll skip the introductory “how” parts and mostly focus on “why”s.

## 2\. Why Use Any Framework?

Before we begin any discussion in particular on Spring, let’s first understand why do we need to use any framework at all in the first place.

A **general purpose programming language like Java is capable of supporting a wide variety of applications**. Not to mention that Java is actively being worked upon and improving every day.

Moreover, there are countless open source and proprietary libraries to support Java in this regard.

So why do we need a framework after all? Honestly, it isn’t absolutely necessary to use a framework to accomplish a task. But, it’s often advisable to use one for several reasons:

  * Helps us **focus on the core task rather than the boilerplate** associated with it
  * Brings together years of wisdom in the form of design patterns
  * Helps us adhere to the industry and regulatory standards
  * Brings down the total cost of ownership for the application



We’ve just scratched the surface here and we must say that the benefits are difficult to ignore. But it can’t be all positives, so what’s the catch:

  * Forces us to **write an application in a specific manner**
  * Binds to a specific version of language and libraries
  * Adds to the resource footprint of the application



Frankly, there are no silver bullets in software development and frameworks are certainly no exception to that. So the choice of which framework or none should be driven from the context.

Hopefully, we’ll be better placed to make this decision with respect to Spring in Java by the end of this article.

## 3\. Brief Overview of Spring Ecosystem

Before we begin our qualitative assessment of Spring Framework, let’s have a closer look into what does Spring ecosystem looks like.

**Spring came into existence somewhere in 2003** at a time when Java Enterprise Edition was evolving fast and developing an enterprise application was exciting but nonetheless tedious!

Spring started out as [an Inversion of Control (IoC) container for Java](/inversion-control-and-dependency-injection-in-spring). We still relate Spring mostly to it and in fact, it forms the core of the framework and other projects that have been developed on top of it.

### 3.1. Spring Framework

Spring framework is [divided into modules](https://docs.spring.io/spring/docs/current/spring-framework-reference/index.html) which makes it really easy to pick and choose in parts to use in any application:

  * [Core](https://docs.spring.io/spring/docs/5.1.8.RELEASE/spring-framework-reference/core.html#spring-core): Provides core features like DI (Dependency Injection), Internationalisation, Validation, and AOP (Aspect Oriented Programming)
  * [Data Access](https://docs.spring.io/spring/docs/5.1.8.RELEASE/spring-framework-reference/data-access.html#spring-data-tier): Supports data access through JTA (Java Transaction API), JPA (Java Persistence API), and JDBC (Java Database Connectivity)
  * [Web](https://docs.spring.io/spring/docs/5.1.8.RELEASE/spring-framework-reference/web.html#spring-web): Supports both Servlet API ([Spring MVC](https://docs.spring.io/spring/docs/5.1.8.RELEASE/spring-framework-reference/web.html#spring-web)) and of recently Reactive API ([Spring WebFlux](https://docs.spring.io/spring/docs/5.1.8.RELEASE/spring-framework-reference/web-reactive.html#spring-webflux)), and additionally supports WebSockets, STOMP, and WebClient
  * [Integration](https://docs.spring.io/spring/docs/5.1.8.RELEASE/spring-framework-reference/integration.html#spring-integration): Supports integration to Enterprise Java through JMS (Java Message Service), JMX (Java Management Extension), and RMI (Remote Method Invocation)
  * [Testing](https://docs.spring.io/spring/docs/5.1.8.RELEASE/spring-framework-reference/testing.html#testing): Wide support for unit and integration testing through Mock Objects, Test Fixtures, Context Management, and Caching



### 3.2. Spring Projects

But what makes Spring much more valuable is **a strong ecosystem that has grown around it over the years and that continues to evolve actively**. These are structured as [Spring projects](https://spring.io/projects) which are developed on top of the Spring framework.

Although the list of Spring projects is a long one and it keeps changing, there are a few worth mentioning:

  * [Boot](/spring-boot): Provides us with a set of highly opinionated but extensible template for creating various projects based on Spring in almost no time. It makes it really easy to create standalone Spring applications with embedded Tomcat or a similar container.
  * [Cloud](/spring-cloud-series): Provides support to easily develop some of the common distributed system patterns like service discovery, circuit breaker, and API gateway. It helps us cut down the effort to deploy such boilerplate patterns in local, remote or even managed platforms.
  * [Security](/security-spring): Provides a robust mechanism to develop authentication and authorization for projects based on Spring in a highly customizable manner. With minimal declarative support, we get protection against common attacks like session fixation, click-jacking, and cross-site request forgery.
  * [Mobile](/spring-mobile): Provides capabilities to detect the device and adapt the application behavior accordingly. Additionally, supports device-aware view management for optimal user experience, site preference management, and site switcher.
  * [Batch](/introduction-to-spring-batch): Provides a lightweight framework for developing batch applications for enterprise systems like data archival. Has intuitive support for scheduling, restart, skipping, collecting metrics, and logging. Additionally, supports scaling up for high-volume jobs through optimization and partitioning.



Needless to say that this is quite an abstract introduction to what Spring has to offer. But it provides us enough ground with respect to Spring’s organization and breadth to take our discussion further.

## 4\. Spring in Action

It is customary to add a hello-world program to understand any new technology.

Let’s see how **Spring can make it a cakewalk to write a program which does more than just hello-world**. We’ll create an application that will expose CRUD operations as REST APIs for a domain entity like Employee backed by an in-memory database. What’s more, we’ll protect our mutation endpoints using basic auth. Finally, no application can really be complete without good, old unit tests.

### 4.1. Project Set-up

We’ll set up our Spring Boot project using [Spring Initializr](https://start.spring.io/), which is a convenient online tool to bootstrap projects with the right dependencies. We’ll add Web, JPA, H2, and Security as project dependencies to get the Maven configuration set-up correctly.

More [details on bootstrapping](/spring-boot-start) are available in one of our previous articles.

### 4.2. Domain Model and Persistence

With so little to be done, we are already ready to define our domain model and persistence.

Let’s first define the _Employee_ as a simple JPA entity:
    
    
    @Entity
    public class Employee {
        @Id
        @GeneratedValue(strategy = GenerationType.AUTO)
        private Long id;
        @NotNull
        private String firstName;
        @NotNull
        private String lastName;
        // Standard constructor, getters and setters
    }

Note the auto-generated id we’ve included in our entity definition.

Now we have to define a JPA repository for our entity. This is where Spring makes it really simple:
    
    
    public interface EmployeeRepository 
      extends CrudRepository<Employee, Long> {
        List<Employee> findAll();
    }

All we have to do is define an interface like this, and **Spring JPA will provide us with an implementation fleshed out with default and custom operations**. Quite neat! Find more details on [working with Spring Data JPA](/the-persistence-layer-with-spring-data-jpa) in our other articles.

### 4.3. Controller

Now we have to define a web controller to route and handle our incoming requests:
    
    
    @RestController
    public class EmployeeController {
        @Autowired
        private EmployeeRepository repository;
        @GetMapping("/employees")
        public List<Employee> getEmployees() {
            return repository.findAll();
        }
        // Other CRUD endpoints handlers
    }

Really, all we had to do was **annotate the class and define routing meta information** along with each handler method.

Working with [Spring REST controllers](/building-a-restful-web-service-with-spring-and-java-based-configuration) is covered in great details in our previous article.

### 4.4. Security

So we have defined everything now, but what about securing operations like create or delete employees? We don’t want unauthenticated access to those endpoints!

Spring Security really shines in this area:
    
    
    @EnableWebSecurity
    public class WebSecurityConfig {
     
        @Bean
        public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
            http
              .authorizeRequests()
                .antMatchers(HttpMethod.GET, "/employees", "/employees/**")
                .permitAll()
              .anyRequest()
                .authenticated()
              .and()
                .httpBasic();
            return http.build();
        }
        // other necessary beans and definitions
    }

There are [more details here which require attention](/spring-security-basic-authentication) to understand but the most important point to note is **the declarative manner in which we have only allowed GET operations unrestricted**.

### 4.5. Testing

Now we’ have done everything, but wait, how do we test this?

Let’s see if Spring can make it easy to write unit tests for REST controllers:
    
    
    @RunWith(SpringRunner.class)
    @SpringBootTest(webEnvironment = WebEnvironment.RANDOM_PORT)
    @AutoConfigureMockMvc
    public class EmployeeControllerTests {
        @Autowired
        private MockMvc mvc;
        @Test
        @WithMockUser()
        public void givenNoEmployee_whenCreateEmployee_thenEmployeeCreated() throws Exception {
            mvc.perform(post("/employees").content(
                new ObjectMapper().writeValueAsString(new Employee("First", "Last"))
                .with(csrf()))
              .contentType(MediaType.APPLICATION_JSON)
              .accept(MediaType.APPLICATION_JSON))
              .andExpect(MockMvcResultMatchers.status()
                .isCreated())
              .andExpect(jsonPath("$.firstName", is("First")))
              .andExpect(jsonPath("$.lastName", is("Last")));
        }
        // other tests as necessary
    }

As we can see, **Spring provides us with the necessary infrastructure to write simple unit and integration tests** which otherwise depend on the Spring context to be initialized and configured.

### 4.6. Running the Application

Finally, how do we run this application? This is another interesting aspect of Spring Boot. Although we can package this as a regular application and deploy traditionally on a Servlet container.

But where is fun this that! **Spring Boot comes with an embedded Tomcat server** :
    
    
    @SpringBootApplication
    public class Application {
        public static void main(String[] args) {
            SpringApplication.run(Application.class, args);
        }
    }

This is a class which comes pre-created as part of the bootstrap and has all the necessary details to start this application using the embedded server.

Moreover, [this is highly customizable](/spring-boot-application-configuration).

## 5\. Alternatives to Spring

While choosing to use a framework is relatively easier, choosing between frameworks can often be daunting with the choices we have. But for that, we must have at least a rough understanding of what alternatives are there for the features that Spring has to offer.

As we discussed previously, **the Spring framework together with its projects offer a wide choice for an enterprise developer to pick from**. If we do a quick assessment of contemporary Java frameworks, they don’t even come close to the ecosystem that Spring provides us.

However, for specific areas, they do form a compelling argument to pick as alternatives:

  * [Guice](/guice): Offers a robust IoC container for Java applications
  * [Play](/java-intro-to-the-play-framework): Quite aptly fits in as a Web framework with reactive support
  * [Hibernate](/hibernate-4-spring): An established framework for data access with JPA support



Other than these there are some recent additions that offer wider support than a specific domain but still do not cover everything that Spring has to offer:

  * [Micronaut](/micronaut): A JVM-based framework tailored towards cloud-native microservices
  * [Quarkus](/quarkus-io): A new age Java stack which promises to deliver faster boot time and a smaller footprint



Obviously, it’s neither necessary nor feasible to iterate over the list completely but we do get the broad idea here.

## 6\. So, Why Choose Spring?

Finally, we’ve built all the required context to address our central question, why Spring? We understand the ways a framework can help us in developing complex enterprise applications.

Moreover, we do understand the options we’ve got for specific concerns like web, data access, integration in terms of framework, especially for Java.

Now, where does Spring shine among all these? Let’s explore.

### 6.1. Usability

One of the key aspects of any framework’s popularity is how easy it is for developers to use it. Spring through multiple configuration options and Convention over Configuration makes it **really easy for developers to start and then configure exactly what they need**.

Projects like **Spring Boot have made bootstrapping a complex Spring project almost trivial**. Not to mention, it has excellent documentation and tutorials to help anyone get on-boarded.

### 6.2. Modularity

Another key aspect of Spring’s popularity is its highly modular nature. We’ve options to use the entire Spring framework or just the modules necessary. Moreover, we can**optionally include one or more Spring projects** depending upon the need.

What’s more, we’ve got the option to use other frameworks like Hibernate or Struts as well!

### 6.3. Conformance

Although Spring **does not support all of Jakarta EE specifications, it supports all of its technologies** , often improving the support over the standard specification where necessary. For instance, Spring supports JPA based repositories and hence makes it trivial to switch providers.

Moreover, Spring supports industry specifications like [Reactive Stream](https://www.reactive-streams.org/) under Spring Web Reactive and HATEOAS under [Spring HATEOAS](/spring-hateoas-tutorial).

### 6.4. Testability

Adoption of any framework largely also depends on the fact that how easy it is to test the application built on top of it. Spring at the core **advocates and supports Test Driven Development** (TDD).

Spring application is mostly composed of POJOs which naturally makes unit testing relatively much simpler. However, Spring does provide Mock Objects for scenarios like MVC where unit testing gets complicated otherwise.

### 6.5. Maturity

Spring has a long history of innovation, adoption, and standardization. Over the years, it’s become **mature enough to become a default solution for most common problems** faced in the development of large scale enterprise applications.

What’s even more exciting is how actively it’s being developed and maintained. Support for new language features and enterprise integration solutions are being developed every day.

### 6.6. Community Support

Last but not least, any framework or even library survive the industry through innovation and there’s no better place for innovation than the community. Spring is an open source **led by Pivotal Software and backed by a large consortium of organizations and individual developers**.

This has meant that it remains contextual and often futuristic, as evident by the number of projects under its umbrella.

## 7\. Reasons _Not_ to Use Spring

There is a wide variety of application which can benefit from a different level of Spring usage, and that is changing as fast as Spring is growing.

However, we must understand that Spring like any other framework is helpful in managing the complexity of application development. It helps us to avoid common pitfalls and keeps the application maintainable as it grows over time.

This **comes at the cost of an additional resource footprint and learning curve** , however small that may be. If there is really an application which is simple enough and not expected to grow complex, perhaps it may benefit more to not use any framework at all!

## 8\. Conclusion

In this article, we discussed the benefits of using a framework in application development. We further discussed briefly Spring Framework in particular.

While on the subject, we also looked into some of the alternate frameworks available for Java.

Finally, we discussed the reasons which can compel us to choose Spring as the framework of choice for Java.

We should end this article with a note of advice, though. However compelling it may sound, **there is usually no single, one-size-fits-all solution** in software development.

Hence, we must apply our wisdom in selecting the simplest of solutions for the specific problems we target to solve.
