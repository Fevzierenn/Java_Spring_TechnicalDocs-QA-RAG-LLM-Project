# Spring Data JPA Projections

## **1\. Overview**

When using [Spring Data JPA](/the-persistence-layer-with-spring-and-jpa) to implement the persistence layer, the repository typically returns one or more instances of the root class. However, more often than not, we don’t need all the properties of the returned objects.

In such cases, we might want to retrieve data as objects of customized types. **These types reflect partial views of the root class, containing only the properties we care about.** This is where projections come in handy.

## **2\. Initial Setup**

The first step is to set up the project and populate the database.

### **2.1. Maven Dependencies**

For dependencies, please check out section 2 of [this tutorial](/spring-data-case-insensitive-queries).

### **2.2. Entity Classes**

Let’s define two entity classes:
    
    
    @Entity
    public class Address {
     
        @Id
        private Long id;
     
        @OneToOne
        private Person person;
     
        private String state;
     
        private String city;
     
        private String street;
     
        private String zipCode;
    
        // getters and setters
    }

And:
    
    
    @Entity
    public class Person {
     
        @Id
        private Long id;
     
        private String firstName;
     
        private String lastName;
     
        @OneToOne(mappedBy = "person")
        private Address address;
    
        // getters and setters
    }

The relationship between _Person_ and _Address_ entities is bidirectional one-to-one; _Address_ is the owning side, and _Person_ is the inverse side.

Notice in this tutorial, we use an embedded database, H2.

**When an embedded database is configured, Spring Boot automatically generates underlying tables for the entities we defined.**

### **2.3. SQL Scripts**

We’ll use the _projection-insert-data.sql_ script to populate both the backing tables:
    
    
    INSERT INTO person(id,first_name,last_name) VALUES (1,'John','Doe');
    INSERT INTO address(id,person_id,state,city,street,zip_code) 
      VALUES (1,1,'CA', 'Los Angeles', 'Standford Ave', '90001');

To clean up the database after each test run, we can use another script, _projection-clean-up-data.sql_ :
    
    
    DELETE FROM address;
    DELETE FROM person;

### 2.4. Test Class

Then, to confirm the projections produce the correct data, we need a test class:
    
    
    @DataJpaTest
    @RunWith(SpringRunner.class)
    @Sql(scripts = "/projection-insert-data.sql")
    @Sql(scripts = "/projection-clean-up-data.sql", executionPhase = AFTER_TEST_METHOD)
    public class JpaProjectionIntegrationTest {
        // injected fields and test methods
    }

With the given annotations, **Spring Boot creates the database, injects dependencies, and populates and cleans up tables before and after each test method’s execution.**

## **3\. Interface-Based Projections**

When projecting an entity, it’s natural to rely on an interface, as we won’t need to provide an implementation.

### **3.1. Closed Projections**

Looking back at the _Address_ class, we can see **it has many properties, yet not all of them are helpful.** For example, sometimes a zip code is enough to indicate an address.

Let’s declare a projection interface for the _Address_ class:
    
    
    public interface AddressView {
        String getZipCode();
    }

Then we’ll use it in a repository interface:
    
    
    public interface AddressRepository extends Repository<Address, Long> {
        List<AddressView> getAddressByState(String state);
    }

It’s easy to see that defining a repository method with a projection interface is pretty much the same as with an entity class.

The only difference is that **the projection interface, rather than the entity class, is used as the element type in the returned collection.**

Let’s do a quick test of the _Address_ projection:
    
    
    @Autowired
    private AddressRepository addressRepository;
    
    @Test
    public void whenUsingClosedProjections_thenViewWithRequiredPropertiesIsReturned() {
        AddressView addressView = addressRepository.getAddressByState("CA").get(0);
        assertThat(addressView.getZipCode()).isEqualTo("90001");
        // ...
    }

Behind the scenes,**Spring creates a proxy instance of the projection interface for each entity object, and all calls to the proxy are forwarded to that object.**

We can use projections recursively. For instance, here’s a projection interface for the _Person_ class:
    
    
    public interface PersonView {
        String getFirstName();
    
        String getLastName();
    }

Now we’ll add a method with the return type _PersonView,_ a nested projection, in the _Address_ projection:
    
    
    public interface AddressView {
        // ...
        PersonView getPerson();
    }

**Notice the method that returns the nested projection must have the same name as the method in the root class that returns the related entity.**

We’ll verify nested projections by adding a few statements to the test method we’ve just written:
    
    
    // ...
    PersonView personView = addressView.getPerson();
    assertThat(personView.getFirstName()).isEqualTo("John");
    assertThat(personView.getLastName()).isEqualTo("Doe");

Note that **recursive projections only work if we traverse from the owning side to the inverse side.** If we do it the other way around, the nested projection would be set to _null_.

### 3.2. Nested JPA Projection Using _Interface_ and Custom Query

In the previous section, we explored nested JPA projection using an _Interface_ with a derived query. We can also achieve this using a custom query:
    
    
    @Query("SELECT c.zipCode as zipCode, c.person as person FROM Address c WHERE c.state = :state")
    List<AddressView> getViewAddressByState(@Param("state") String state);

In the code above, we write a custom query to fetch an _Address_ by zip code and include the associated _Person_. Spring maps the query result to the _AddressView_ and _PersonView_ interfaces based on matching field names.

Let’s write a unit test for the nested JPA projection:
    
    
    @Test
    void whenUsingCustomQueryForNestedProjection_thenViewWithRequiredPropertiesIsReturned() {
        AddressView addressView = addressRepository.getViewAddressByState("CA").get(0);
        assertThat(addressView.getZipCode()).isEqualTo("90001");
    
        PersonView personView = addressView.getPerson();
        assertThat(personView.getFirstName()).isEqualTo("John");
        assertThat(personView.getLastName()).isEqualTo("Doe");
    }

In the test above, we invoke the custom repository method on _AddressRepository_ to fetch an address and the corresponding person. Then we assert that the return result is equal to the expected result.

Additionally, custom queries allow us to specify the type of join operation, potentially improving database lookup and preventing [N+1 problems](/cs/orm-n-plus-one-select-problem).

### **3.3. Open Projections**

Up to this point, we’ve gone through closed projections, which indicate projection interfaces whose methods exactly match the names of entity properties.

There’s also another sort of interface-based projection, open projections. **These projections enable us to define interface methods with unmatched names and with return values computed at runtime.**

Let’s go back to the _Person_ projection interface and add a new method:
    
    
    public interface PersonView {
        // ...
    
        @Value("#{target.firstName + ' ' + target.lastName}")
        String getFullName();
    }

The argument to the _@Value_ annotation is a SpEL expression, in which the _target_ designator indicates the backing entity object.

Now we’ll define another repository interface:
    
    
    public interface PersonRepository extends Repository<Person, Long> {
        PersonView findByLastName(String lastName);
    }

To make it simple, we’ll only return a single projection object instead of a collection.

This test confirms the open projections work as expected:
    
    
    @Autowired
    private PersonRepository personRepository;
    
    @Test 
    public void whenUsingOpenProjections_thenViewWithRequiredPropertiesIsReturned() {
        PersonView personView = personRepository.findByLastName("Doe");
     
        assertThat(personView.getFullName()).isEqualTo("John Doe");
    }

Open projections do have a drawback though; Spring Data can’t optimize query execution, as it doesn’t know in advance which properties will be used. Thus, **we should only use open projections when closed projections aren’t capable of handling our requirements.**

## **4\. Class-Based Projections**

Instead of using proxies Spring Data creates from projection interfaces, **we can define our own projection classes.**

For example, here’s a projection class for the _Person_ entity:
    
    
    public class PersonDto {
        private String firstName;
        private String lastName;
    
        public PersonDto(String firstName, String lastName) {
            this.firstName = firstName;
            this.lastName = lastName;
        }
    
        // getters, equals and hashCode
    }

**For a projection class to work in tandem with a repository interface, the parameter names of its constructor must match the properties of the root entity class.**

We must also define _equals_ and _hashCode_ implementations; they allow Spring Data to process projection objects in a collection.

The requirements above can be addressed by java _records_ , thus making our code more precise and expressive:
    
    
    public record PersonDto(String firstName, String lastName) {
    
    }

Now let’s add a method to the _Person_ repository:
    
    
    public interface PersonRepository extends Repository<Person, Long> {
        // ...
    
        PersonDto findByFirstName(String firstName);
    }

This test verifies our class-based projection:
    
    
    @Test
    public void whenUsingClassBasedProjections_thenDtoWithRequiredPropertiesIsReturned() {
        PersonDto personDto = personRepository.findByFirstName("John");
     
        assertThat(personDto.getFirstName()).isEqualTo("John");
        assertThat(personDto.getLastName()).isEqualTo("Doe");
    }

**Notice with the class-based approach, we can’t use nested projections.**

### 4.1. Nested Projection Using Classes

Furthermore, we can use nested DTO classes to map associated entities together:
    
    
    class AddressDto {
        private final String zipCode;
        private final PersonDto person;
    
        public AddressDto(String zipCode, PersonDto person) {
            this.zipCode = zipCode;
            this.person = person;
        }
    }

Here, we declare the _PersonDto_ as a field in the _AddressDto_ and pass it to the constructor. Notably, the constructor parameter names must match the DTO class fields.

Then, we can use a derived query or a custom query for the database lookup:
    
    
    @Query("SELECT new com.baeldung.jpa.projection.view.AddressDto(a.zipCode," +
      "new com.baeldung.jpa.projection.view.PersonDto(p.firstName, p.lastName)) " +
      "FROM Address a JOIN a.person p WHERE a.state = :state")
    List<AddressDto> findAddressByState(@Param("state") String state);

In our query, we use the _new_ keyword with a fully qualified class name of the DTOs to invoke their constructors. This is essential for creating DTO instances during a database lookup.

In the case of a derived query, we only need to ensure that the query method name ends with a valid entity field:
    
    
    List<AddressDto> findAddressByState(String state);

However, custom query provides flexibility, allowing complex join operations and more refined data retrieval.

### 4.2. With JPA Native Queries

JPA native queries allow us to write SQL queries directly instead of using JPQL. We can also map the result from the native query to the DTO class.

_@__NamedNativeQuery_ is used to define the SQL query with the _resultSetMapping_ param which is set to the mapped DTO annotation. _@SqlResultSetMapping_ annotation is used to define the mapping of the query results to the DTO class:
    
    
    @Entity
    @NamedNativeQuery(
      name = "person_native_query_dto",
      query = "SELECT p.first_name, p.last_name From Person p where p.first_name LIKE :firstNameLike",
      resultSetMapping = "person_query_dto"
    )
    @SqlResultSetMapping(
      name = "person_query_dto", 
      classes = @ConstructorResult(
        targetClass = PersonDto.class, 
        columns = { 
            @ColumnResult(name = "first_name", type = String.class), 
            @ColumnResult(name = "last_name", type = String.class), 
        }
      )
    )
    public class Person {
       // properties, getters and setters
    }

In the above logic, we map the result of the native query to _PersonDto_ class, where we define _columns_ that are mapped to the property on the _PersonDto_ class _._

Once we’ve annotated our entity, we can define the repository method:
    
    
    public interface PersonRepository extends Repository<Person, Long> {
        @Query(name = "person_native_query_dto", nativeQuery = true)
        List<PersonDto> findByFirstNameLike(@Param("firstNameLike") String firstNameLike);
    }

In the _findByFirstNameLike()_ method, we annotate with _@Query,_ which receives the name of the native query we defined on the entity.

We can write a simple unit test to verify the result:
    
    
    @Test
    void whenUsingClassBasedProjectionsAndJPANativeQuery_thenDtoWithRequiredPropertiesIsReturned() {
        List<PersonDto> personDtos = personRepository.findByFirstNameLike("Jo%");
        assertThat(personDtos.size()).isEqualTo(2);
        assertThat(personDtos).isEqualTo(Arrays.asList(new PersonDto("John", "Doe"), new PersonDto("Job", "Doe")));
    }

## **5\. Dynamic Projections**

An entity class may have many projections. In some cases, we may use a certain type, but in other cases, we may need another type. Sometimes, we also need to use the entity class itself.

Defining separate repository interfaces or methods just to support multiple return types is cumbersome. To deal with this problem, Spring Data provides a better solution, dynamic projections.

**We can apply dynamic projections just by declaring a repository method with a _Class_ parameter:**
    
    
    public interface PersonRepository extends Repository<Person, Long> {
        // ...
    
        <T> T findByLastName(String lastName, Class<T> type);
    }

By passing a projection type or the entity class to such a method, we can retrieve an object of the desired type:
    
    
    @Test
    public void whenUsingDynamicProjections_thenObjectWithRequiredPropertiesIsReturned() {
        Person person = personRepository.findByLastName("Doe", Person.class);
        PersonView personView = personRepository.findByLastName("Doe", PersonView.class);
        PersonDto personDto = personRepository.findByLastName("Doe", PersonDto.class);
    
        assertThat(person.getFirstName()).isEqualTo("John");
        assertThat(personView.getFirstName()).isEqualTo("John");
        assertThat(personDto.getFirstName()).isEqualTo("John");
    }

## **6\. Conclusion**

In this article, we discussed various types of Spring Data JPA projections.
