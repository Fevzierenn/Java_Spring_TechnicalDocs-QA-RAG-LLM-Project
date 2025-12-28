# A Guide to JPA with Spring

## **1\. Overview**

This tutorial **shows how to set up Spring with JPA** , using Hibernate as a persistence provider.

See this [article](/bootstraping-a-web-application-with-spring-and-java-based-configuration) for a step-by-step introduction to setting up the Spring context using Java-based configuration and the basic Maven pom for the project.

We’ll start by setting up JPA in a Spring Boot project. Then we’ll look into the full configuration we need if we have a standard Spring project.

## **2\. JPA in Spring Boot**

The Spring Boot project is intended to make creating Spring applications much faster and easier. This is done using starters and auto-configuration for various Spring functionalities, JPA among them.

### 2.1. Maven Dependencies

To enable JPA in a Spring Boot application, we need the _[spring-boot-starter](https://mvnrepository.com/artifact/org.springframework.boot/spring-boot-starter)_ and _[spring-boot-starter-data-jpa](https://mvnrepository.com/artifact/org.springframework.boot/spring-boot-starter-data-jpa) _dependencies:
    
    
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter</artifactId>
        <version>3.1.0</version>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-data-jpa</artifactId>
        <version>3.1.0</version>
    </dependency>

The _spring-boot-starter_ contains the necessary auto-configuration for Spring JPA. Also, the _spring-boot-starter-jpa_ project references all the necessary dependencies, such as _hibernate-core_.

### 2.2. Configuration

**Spring Boot configures _Hibernate_ as the default JPA provider**, so it’s no longer necessary to define the _entityManagerFactory_ bean unless we want to customize it.

**Spring Boot can also auto-configure the _dataSource_ bean, depending on the database we’re using.** In the case of an in-memory database of type _H2_ , _HSQLDB_ and _Apache Derby_ , Boot automatically configures the _DataSource_ if the corresponding database dependency is present on the classpath.

For example, if we want to use an in-memory _H2_ database in a Spring Boot JPA application, we only need to add the [_h2_](https://mvnrepository.com/artifact/com.h2database/h2) dependency to the _pom.xml_ file:
    
    
    <dependency>
        <groupId>com.h2database</groupId>
        <artifactId>h2</artifactId>
        <version>2.1.214</version>
    </dependency>

This way, we don’t need to define the _dataSource_ bean, but we can if we want to customize it.

If we want to use JPA with _MySQL_ database, we need the _mysql-connector-java_ dependency. We’ll also need to define the _DataSource_ configuration.

We can do this in a _@Configuration_ class or by using standard Spring Boot properties.

The Java configuration looks the same as it does in a standard Spring project:
    
    
    @Bean
    public DataSource dataSource() {
        DriverManagerDataSource dataSource = new DriverManagerDataSource();
    
        dataSource.setDriverClassName("com.mysql.cj.jdbc.Driver");
        dataSource.setUsername("mysqluser");
        dataSource.setPassword("mysqlpass");
        dataSource.setUrl(
          "jdbc:mysql://localhost:3306/myDb?createDatabaseIfNotExist=true"); 
        
        return dataSource;
    }

**To configure the data source using a properties file, we have to set properties prefixed with _spring.datasource_** :
    
    
    spring.datasource.driver-class-name=com.mysql.cj.jdbc.Driver
    spring.datasource.username=mysqluser
    spring.datasource.password=mysqlpass
    spring.datasource.url=
      jdbc:mysql://localhost:3306/myDb?createDatabaseIfNotExist=true

Spring Boot will automatically configure a data source based on these properties.

Also, in Spring Boot 1, the default connection pool was _Tomcat_ , but it has been changed to _HikariCP_ with Spring Boot 2.

We have more examples of configuring JPA in Spring Boot in the [GitHub project](https://github.com/eugenp/tutorials/tree/master/persistence-modules/spring-jpa).

As we can see, the basic JPA configuration is fairly simple if we’re using Spring Boot.

However,**if we have a standard Spring project, we need a more explicit configuration using Java or XML.** That’s what we’ll focus on in the next sections.

## **3\. The JPA Spring Configuration With Java in a Non-Boot Project**

To use JPA in a Spring project, **we need to set up the _EntityManager_.**

This is the main part of the configuration, and we can do it via a Spring factory bean. This can be either the simpler _LocalEntityManagerFactoryBean_ or, **the more flexible _LocalContainerEntityManagerFactoryBean_.**

Let’s see how we can use the latter option:
    
    
    @Configuration
    @EnableTransactionManagement
    public class PersistenceJPAConfig {
    
       @Bean
       public LocalContainerEntityManagerFactoryBean entityManagerFactory() {
          LocalContainerEntityManagerFactoryBean em 
            = new LocalContainerEntityManagerFactoryBean();
          em.setDataSource(dataSource());
          em.setPackagesToScan("com.baeldung.persistence.model");
    
          JpaVendorAdapter vendorAdapter = new HibernateJpaVendorAdapter();
          em.setJpaVendorAdapter(vendorAdapter);
          em.setJpaProperties(additionalProperties());
    
          return em;
       }
       
       // ...
    
    }

**We also need to explicitly define the _DataSource_ bean** we’ve used above:
    
    
    @Bean
    public DataSource dataSource(){
        DriverManagerDataSource dataSource = new DriverManagerDataSource();
        dataSource.setDriverClassName("com.mysql.cj.jdbc.Driver");
        dataSource.setUrl("jdbc:mysql://localhost:3306/spring_jpa");
        dataSource.setUsername( "tutorialuser" );
        dataSource.setPassword( "tutorialmy5ql" );
        return dataSource;
    }

The final part of the configuration is the additional Hibernate properties and the _TransactionManager_ and _exceptionTranslation_ beans:
    
    
    @Bean
    public PlatformTransactionManager transactionManager() {
        JpaTransactionManager transactionManager = new JpaTransactionManager();
        transactionManager.setEntityManagerFactory(entityManagerFactory().getObject());
    
        return transactionManager;
    }
    
    @Bean
    public PersistenceExceptionTranslationPostProcessor exceptionTranslation(){
        return new PersistenceExceptionTranslationPostProcessor();
    }
    
    Properties additionalProperties() {
        Properties properties = new Properties();
        properties.setProperty("hibernate.hbm2ddl.auto", "create-drop");
        properties.setProperty("hibernate.dialect", "org.hibernate.dialect.MySQL5Dialect");
           
        return properties;
    }

## **4\. Going Full XML-less**

Usually, JPA defines a persistence unit through the _META-INF/persistence.xml_ file. **Starting with Spring 3.1, the _persistence.xml_ is no longer necessary.** The _LocalContainerEntityManagerFactoryBean_ now supports a _packagesToScan_ property where the packages to scan for _@Entity_ classes can be specified.

This file was the last piece of XML we need to remove. **We can now set up JPA fully with no XML.**

We would usually specify JPA properties in the _persistence.xml_ file.

Alternatively, we can add the properties directly to the entity manager factory bean:
    
    
    factoryBean.setJpaProperties(this.additionalProperties());

As a side note, if Hibernate is the persistence provider, this would be the way to specify Hibernate-specific properties as well.

## **5\. The Maven Configuration**

In addition to the Spring Core and persistence dependencies — shown in detail in the [Spring with Maven tutorial](/spring-with-maven "Spring Maven dependencies") — we also need to define JPA and Hibernate in the project as well as a MySQL connector:
    
    
    <dependency>
       <groupId>org.hibernate</groupId>
       <artifactId>hibernate-core</artifactId>
       <version>6.5.2.Final</version>
    </dependency>
    
    <dependency>
       <groupId>mysql</groupId>
       <artifactId>mysql-connector-java</artifactId>
       <version>8.0.19</version>
       <scope>runtime</scope>
    </dependency>

Note that the MySQL dependency is included here as an example. We need a driver to configure the data source, **but any Hibernate-supported database will do.**

## 6\. Spring Data JPA Example Project

Let’s see Spring Data JPA in action with an example project.

### 6.1. Entity Class

First, let’s create a new entity class:
    
    
    @Entity
    public class Publishers {
        @Id
        @GeneratedValue(strategy = GenerationType.IDENTITY)
        private int id;
        private String name;
        private String location;
        private int journals;
        // constructors, getters and setters
    }

Here, we create an Entity class named _Publishers_ representing a database table, the fields represent columns in the database. In this case, we have four columns and _id_ is the primary key.

### 6.2. Repository

The Spring Data JPA provides repository support to perform various database operations without boilerplate code. A repository serves as a link between an entity and the database.

Let’s create a _PublisherRepository_ interface:
    
    
    public interface PublisherRepository extends JpaRepository<Publishers, Integer> {
    }

The repository interface extends the _JpaRepository_ which provides various inbuilt methods for database operation. The common method includes:

  * _save()_ – to persist entities into the database
  * _findById()_ – to find database record by its _id_
  * _findAll()_ – to get all entities
  * _findById()_ – to get an entity by its _id_.



Also, **Spring Data JPA allows us to derive queries through methods by following a specific naming convention** :
    
    
    public interface PublisherRepository extends JpaRepository<Publishers, Integer> {
        List<Publishers> findAllByLocation(String location);
    }

In the code above, we define a method named _findAllByLocation()._ When this method is invoked on a _PublisherRepository_ object, it’s parsed and converted to an SQL query. The _findAllBy_ prefix indicates the start of the query, and the _Location_ indicates the property name corresponding to the location field in the entity class.

Also, we can use the _@Query_ annotation to define a custom query:
    
    
    @Query("SELECT p FROM Publishers p WHERE p.journals > :minJournals AND p.location = :location")
    List<Publisher> findPublishersWithMinJournalsInLocation(Integer minJournals,String location);

Here, we define a query to find all _Publishers_ based on a specific number of journals and locations.

### 6.3. Service

Furthermore, let’s create a service class to implement different logic for a typical database operation.

First, let’s inject the _PublisherRepository_ into the service class:
    
    
    @Service
    class PublisherService {
        private final PublisherRepository publisherRepository;
    
        public PublisherService(PublisherRepository publisherRepository) {
            this.publisherRepository = publisherRepository;
        }
        // ...
    }

Next, let’s create a method to insert publishers record into the database:
    
    
    public Publishers save(Publishers publishers) {
        return publisherRepository.save(publishers);
    }

Here, we use the _save()_ method to persist an entity in the database. It can either save a new entity or update an existing one, depending on whether the entity already exists in the database.

Then, let’s find all the saved publishers:
    
    
    public List<Publishers> findAll() {
        return publisherRepository.findAll();
    }

The _findAll()_ method retrieves all publisher’s records in the database and returns them as a _List_.

Also, let’s find a publisher by its _id_ :
    
    
    public Publishers findById(int id) {
        return publisherRepository.findById(id)
          .orElseThrow(() -> new RuntimeException("Publisher not found"));
    }

The method above retrieves a publisher record from the database based on the provided _id_. If no record matches the provided _id_ , it throws a _RuntimeException_.

Also, let’s use the repository method with the custom query _findPublishersWithMinJournalsLocation()._ It helps to find publishers based on a minimum number of journals and location:
    
    
    List<Publishers> findPublishersWithMinJournalsInLocation(int minJournals, String location) {
        return publisherRepository.findPublishersWithMinJournalsInLocation(minJournals, location);
    }

Now that we have defined methods for different database operations, we can use them in our test class or in a controller.

## **7\. Conclusion**

In this article, we learned how to configure JPA with Hibernate in a Spring boot and a standard Spring application. Also, we saw an example Spring Boot project that persist entities and as well as retrieve entities from the database.
