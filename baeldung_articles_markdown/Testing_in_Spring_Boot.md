# Testing in Spring Boot

## **1\. Overview**

In this tutorial, we’ll have a look at **writing tests using the framework support in Spring Boot.** We’ll cover unit tests that can run in isolation as well as integration tests that will bootstrap Spring context before executing tests.

If you are new to Spring Boot, check out our [intro to Spring Boot](/spring-boot-start).

## **2\. Project Setup**

The application we’re going to use in this article is an API that provides some basic operations on an _Employee_ Resource. This is a typical tiered architecture — the API call is processed from the _Controller_ to _Service_ to the _Persistence_ layer.

## **3\. Maven Dependencies**

Let’s first add our testing dependencies:
    
    
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-test</artifactId>
        <scope>test</scope>
        <version>3.3.2</version>
    </dependency>
    <dependency>
        <groupId>com.h2database</groupId>
        <artifactId>h2</artifactId>
        <scope>test</scope>
    </dependency>

The [_spring-boot-starter-test_](https://mvnrepository.com/artifact/org.springframework.boot/spring-boot-starter-test) is the primary dependency that contains the majority of elements required for our tests.

The [H2 DB](https://mvnrepository.com/artifact/com.h2database/h2) is our in-memory database. It eliminates the need to configure and start an actual database for test purposes.

## **4\. Integration Testing With _@SpringBootTest_**

As the name suggests, integration tests focus on integrating different layers of the application. That also means no mocking is involved.

**Ideally, we should keep the integration tests separate from the unit tests and not run along with the unit tests.** We can do this by using a different profile to only run the integration tests. A couple of reasons for doing this could be that the integration tests are time-consuming and might need an actual database to execute.

However in this article, we won’t focus on that, and we’ll instead make use of the in-memory H2 persistence storage.

The integration tests need to start up a container to execute the test cases. Hence, some additional setup is required for this — all of this is easy in Spring Boot:
    
    
    @ExtendWith(SpringExtension.class)
    @SpringBootTest(
      webEnvironment = SpringBootTest.WebEnvironment.MOCK,
      classes = Application.class)
    @AutoConfigureMockMvc
    @TestPropertySource(
      locations = "classpath:application-integrationtest.properties")
    public class EmployeeRestControllerIntegrationTest {
    
        @Autowired
        private MockMvc mvc;
    
        @Autowired
        private EmployeeRepository repository;
    
        // write test cases here
    }

**The _@SpringBootTest_ annotation is useful when we need to bootstrap the entire container.** The annotation works by creating the _ApplicationContext_ that will be utilized in our tests.

We can use the _webEnvironment_ attribute of _@SpringBootTest_ to configure our runtime environment; we’re using _WebEnvironment.MOCK_ here so that the container will operate in a mock servlet environment.

Next, the _@TestPropertySource_ annotation helps configure the locations of properties files specific to our tests. Note that the property file loaded with _@TestPropertySource_ will override the existing _application.properties_ file.

The _application-integrationtest.properties_ contains the details to configure the persistence storage:
    
    
    spring.datasource.url = jdbc:h2:mem:test
    spring.jpa.properties.hibernate.dialect = org.hibernate.dialect.H2Dialect

If we want to run our integration tests against MySQL, we can change the above values in the properties file.

The test cases for the integration tests might look similar to the _Controller_ layer unit tests:
    
    
    @Test
    public void givenEmployees_whenGetEmployees_thenStatus200()
      throws Exception {
    
        createTestEmployee("bob");
    
        mvc.perform(get("/api/employees")
          .contentType(MediaType.APPLICATION_JSON))
          .andExpect(status().isOk())
          .andExpect(content()
          .contentTypeCompatibleWith(MediaType.APPLICATION_JSON))
          .andExpect(jsonPath("$[0].name", is("bob")));
    }

The difference from the _Controller_ layer unit tests is that here nothing is mocked and end-to-end scenarios will be executed.

## 5\. Test Configuration With  _@TestConfiguration_

As we’ve seen in the previous section, a test annotated with _@SpringBootTest_ will bootstrap the full application context, which means we can _@Autowire_ any bean that’s picked up by component scanning into our test:
    
    
    @ExtendWith(SpringExtension.class)
    @SpringBootTest
    public class EmployeeServiceImplIntegrationTest {
    
        @Autowired
        private EmployeeService employeeService;
    
        // class code ...
    }
    

However, we might want to avoid bootstrapping the real application context but use a special test configuration. We can achieve this with the  _@TestConfiguration_ annotation. There are two ways of using the annotation. Either on a static inner class in the same test class where we want to _@Autowire_ the bean:
    
    
    @ExtendWith(SpringExtension.class)
    public class EmployeeServiceImplIntegrationTest {
    
        @TestConfiguration
        static class EmployeeServiceImplTestContextConfiguration {
            @Bean
            public EmployeeService employeeService() {
                return new EmployeeService() {
                    // implement methods
                };
            }
        }
    
        @Autowired
        private EmployeeService employeeService;
    }

Alternatively, we can create a separate test configuration class:
    
    
    @TestConfiguration
    public class EmployeeServiceImplTestContextConfiguration {
        
        @Bean
        public EmployeeService employeeService() {
            return new EmployeeService() { 
                // implement methods 
            };
        }
    }

Configuration classes annotated with _@TestConfiguration_ are excluded from component scanning. Therefore, we need to import it explicitly in every test where we want to _@Autowire_ it. We can do that with the  _@Import_ annotation:
    
    
    @ExtendWith(SpringExtension.class)
    @Import(EmployeeServiceImplTestContextConfiguration.class)
    public class EmployeeServiceImplIntegrationTest {
    
        @Autowired
        private EmployeeService employeeService;
    
        // remaining class code
    }

## **6\. Mocking With _@MockBean_**

Our _Service_ layer code is dependent on our _Repository:_
    
    
    @Service
    public class EmployeeServiceImpl implements EmployeeService {
    
        @Autowired
        private EmployeeRepository employeeRepository;
    
        @Override
        public Employee getEmployeeByName(String name) {
            return employeeRepository.findByName(name);
        }
    }

However, to test the _Service_ layer, we don’t need to know or care about how the persistence layer is implemented. Ideally, we should be able to write and test our _Service_ layer code without wiring in our full persistence layer.

To achieve this, **we can use the mocking support provided by Spring Boot Test.**

Let’s have a look at the test class skeleton first:
    
    
    @ExtendWith(SpringExtension.class)
    public class EmployeeServiceImplIntegrationTest {
    
        @TestConfiguration
        static class EmployeeServiceImplTestContextConfiguration {
     
            @Bean
            public EmployeeService employeeService() {
                return new EmployeeServiceImpl();
            }
        }
    
        @Autowired
        private EmployeeService employeeService;
    
        @MockBean
        private EmployeeRepository employeeRepository;
    
        // write test cases here
    }

To check the _Service_ class, we need to have an instance of the _Service_ class created and available as a _@Bean_ so that we can _@Autowire_ it in our test class. We can achieve this configuration using the _@TestConfiguration_ annotation.

Another interesting thing here is the use of _@MockBean_. It [creates a Mock](/mockito-mock-methods) for the _EmployeeRepository_ , which can be used to bypass the call to the actual _EmployeeRepository_ :
    
    
    @BeforeEach
    public void setUp() {
        Employee alex = new Employee("alex");
    
        Mockito.when(employeeRepository.findByName(alex.getName()))
          .thenReturn(alex);
    }

With the setup complete, the test case becomes simpler:
    
    
    @Test
    public void whenValidName_thenEmployeeShouldBeFound() {
        String name = "alex";
        Employee found = employeeService.getEmployeeByName(name);
     
         assertThat(found.getName())
          .isEqualTo(name);
     }

## **7\. Integration Testing With _@DataJpaTest_**

We’re going to work with an entity named _Employee,_ which has an _id_ and a _name_ as its properties:
    
    
    @Entity
    @Table(name = "person")
    public class Employee {
    
        @Id
        @GeneratedValue(strategy = GenerationType.AUTO)
        private Long id;
    
        @Size(min = 3, max = 20)
        private String name;
    
        // standard getters and setters, constructors
    }

And here’s our repository using Spring Data JPA:
    
    
    @Repository
    public interface EmployeeRepository extends JpaRepository<Employee, Long> {
    
        public Employee findByName(String name);
    
    }

That’s it for the persistence layer code. Now let’s head toward writing our test class.

First, let’s create the skeleton of our test class:
    
    
    @ExtendWith(SpringExtension.class)
    @DataJpaTest
    public class EmployeeRepositoryIntegrationTest {
    
        @Autowired
        private TestEntityManager entityManager;
    
        @Autowired
        private EmployeeRepository employeeRepository;
    
        // write test cases here
    
    }

_@ExtendWith(SpringExtension.class)_ provides a bridge between Spring Boot test features and JUnit. Whenever we are using any Spring Boot testing features in our JUnit tests, this annotation will be required.

_@DataJpaTest_ provides some standard setup needed for testing the persistence layer:

  * configuring H2, an in-memory database
  * setting Hibernate, Spring Data, and the _DataSource_
  * performing an _@EntityScan_
  * turning on SQL logging



To carry out DB operations, we need some records already in our database. To setup this data, we can use _TestEntityManager._

**The Spring Boot _TestEntityManager_ is an alternative to the standard JPA _EntityManager_ that provides methods commonly used when writing tests.**

_EmployeeRepository_ is the component that we are going to test.

Now let’s write our first test case:
    
    
    @Test
    public void whenFindByName_thenReturnEmployee() {
        // given
        Employee alex = new Employee("alex");
        entityManager.persist(alex);
        entityManager.flush();
    
        // when
        Employee found = employeeRepository.findByName(alex.getName());
    
        // then
        assertThat(found.getName())
          .isEqualTo(alex.getName());
    }

In the above test, we’re using the _TestEntityManager_ to insert an _Employee_ in the DB and read it via the find by name API.

The _assertThat(…)_ part comes from the [Assertj library](/introduction-to-assertj), which comes bundled with Spring Boot.

## **8\. Unit Testing With _@WebMvcTest_**

Our _Controller_ depends on the _Service_ layer; let’s only include a single method for simplicity:
    
    
    @RestController
    @RequestMapping("/api")
    public class EmployeeRestController {
    
        @Autowired
        private EmployeeService employeeService;
    
        @GetMapping("/employees")
        public List<Employee> getAllEmployees() {
            return employeeService.getAllEmployees();
        }
    }

Since we’re only focused on the _Controller_ code, it’s natural to mock the _Service_ layer code for our unit tests:
    
    
    @ExtendWith(SpringExtension.class)
    @WebMvcTest(EmployeeRestController.class)
    public class EmployeeRestControllerIntegrationTest {
    
        @Autowired
        private MockMvc mvc;
    
        @MockBean
        private EmployeeService service;
    
        // write test cases here
    }

**To test the _Controllers_ , we can use _@WebMvcTest_. It will auto-configure the Spring MVC infrastructure for our unit tests.**

In most cases, @_WebMvcTest_ will be limited to bootstrap a single controller. We can also use it along with _@MockBean_ to provide mock implementations for any required dependencies.

_@WebMvcTest_ also auto-configures _MockMvc_ , which offers a powerful way of easy testing MVC controllers without starting a full HTTP server.

Having said that, let’s write our test case:
    
    
    @Test
    public void givenEmployees_whenGetEmployees_thenReturnJsonArray()
      throws Exception {
        
        Employee alex = new Employee("alex");
    
        List<Employee> allEmployees = Arrays.asList(alex);
    
        given(service.getAllEmployees()).willReturn(allEmployees);
    
        mvc.perform(get("/api/employees")
          .contentType(MediaType.APPLICATION_JSON))
          .andExpect(status().isOk())
          .andExpect(jsonPath("$", hasSize(1)))
          .andExpect(jsonPath("$[0].name", is(alex.getName())));
    }

We can replace the _get(…)_ method call with other methods corresponding to HTTP verbs like _put()_ , _post()_ , etc. Please note that we are also setting the content type in the request.

_MockMvc_ is flexible, and we can create any request using it.

## 9\. Auto-Configured Tests

One of the amazing features of Spring Boot’s auto-configured annotations is that it helps to load parts of the complete application and test-specific layers of the codebase.

In addition to the above-mentioned annotations, here’s a list of a few widely used annotations:

Annotation | Description  
---|---  
_@WebFluxTest_ | Used to test Spring WebFlux controllers. Often used with _@MockBean_ to provide mock implementations for required dependencies.  
_@JdbcTest_ | Used to test JPA applications that only require a _DataSource_. Configures an in-memory embedded database and a _JdbcTemplate_.  
_@JooqTest_ | Used to test jOOQ-related components. Configures a DSLContext.  
_@DataMongoTest_ | Used to test MongoDB applications. Configures an in-memory embedded MongoDB (if the driver is available), a _MongoTemplate_ , scans for _@Document_ classes, and configures Spring Data MongoDB repositories.  
_@DataRedisTest_ | Facilitates testing of Redis applications. Scans for _@RedisHash_ classes and configures Spring Data Redis repositories by default.  
_@DataLdapTest_ | Configures an in-memory embedded _LDAP_ (if available), a _LdapTemplate_ , scans for _@Entry_ classes, and configures Spring Data _LDAP_ repositories by default.  
_@RestClientTest_ | Used to test REST clients. Auto-configures dependencies such as Jackson, Gson, and Jsonb support; configures a _RestTemplateBuilder_ ; and adds support for _MockRestServiceServer_ by default.  
_@JsonTest_ | Initializes the Spring application context only with beans needed to test JSON serialization.  
  
We can read more about these annotations and how to further optimize integration tests in our article on [Optimizing Spring Integration Tests](/spring-tests).

## **10\. Conclusion**

In this article, we took a deep dive into the testing support in Spring Boot and showed how to write unit tests efficiently.

If you want to keep learning about testing, we have separate articles related to [integration tests](/integration-testing-in-spring), [optimizing Spring integration tests](/spring-tests), and [unit tests in JUnit 5](/junit-5).
