# Spring Data Annotations

[This article is part of a series:](javascript:void\(0\);)

[• Spring Core Annotations](/spring-core-annotations)  
[• Spring Web Annotations](/spring-mvc-annotations)  
[• Spring Boot Annotations](/spring-boot-annotations)  
[• Spring Scheduling Annotations](/spring-scheduling-annotations)  


• Spring Data Annotations (current article)

[• Spring Bean Annotations](/spring-bean-annotations)  


## 1\. Introduction

Spring Data provides an abstraction over data storage technologies. Therefore, our business logic code can be much more independent of the underlying persistence implementation. Also, Spring simplifies the handling of implementation-dependent details of data storage.

In this tutorial, we’ll see the most common annotations of the Spring Data, Spring Data JPA, and Spring Data MongoDB projects.

## 2\. Common Spring Data Annotations

### 2.1. _@Transactional_

When we want to **configure the transactional behavior of a method** , we can do it with:
    
    
    @Transactional
    void pay() {}

If we apply this annotation on class level, then it works on all methods inside the class. However, we can override its effects by applying it to a specific method.

It has many configuration options, which can be found in [this article](/transaction-configuration-with-jpa-and-spring).

### 2.2. _@NoRepositoryBean_

**Sometimes we want to create repository interfaces with the only goal of providing common methods for the child repositories**.

Of course, we don’t want Spring to create a bean of these repositories since we won’t inject them anywhere. _@NoRepositoryBean_ does exactly this: when we mark a child interface of _org.springframework.data.repository.Repository_ , Spring won’t create a bean out of it.

For example, if we want an _Optional <T> findById(ID id) _method in all of our repositories, we can create a base repository:
    
    
    @NoRepositoryBean
    interface MyUtilityRepository<T, ID extends Serializable> extends CrudRepository<T, ID> {
        Optional<T> findById(ID id);
    }

This annotation doesn’t affect the child interfaces; hence Spring will create a bean for the following repository interface:
    
    
    @Repository
    interface PersonRepository extends MyUtilityRepository<Person, Long> {}

Note, that the example above isn’t necessary since Spring Data version 2 which includes this method replacing the older _T findOne(ID id)_.

### 2.3. _@Param_

We can pass named parameters to our queries using _@Param_ :
    
    
    @Query("FROM Person p WHERE p.name = :name")
    Person findByName(@Param("name") String name);

Note, that we refer to the parameter with the _:name_ syntax.

For further examples, please visit [this article](/spring-data-jpa-query).

### 2.4. _@Id_

_@Id_ marks a field in a model class as the primary key:
    
    
    class Person {
    
        @Id
        Long id;
    
        // ...
        
    }

Since it’s implementation-independent, it makes a model class easy to use with multiple data store engines.

### 2.5. _@Transient_

We can use this annotation to mark a field in a model class as transient. Hence the data store engine won’t read or write this field’s value:
    
    
    class Person {
    
        // ...
    
        @Transient
        int age;
    
        // ...
    
    }

Like _@Id_ , _@Transient_ is also implementation-independent, which makes it convenient to use with multiple data store implementations.

### 2.6. _@CreatedBy_ , _@LastModifiedBy_ , _@CreatedDate_ , _@LastModifiedDate_

With these annotations, we can audit our model classes: Spring automatically populates the annotated fields with the principal who created the object, last modified it, and the date of creation, and last modification:
    
    
    public class Person {
    
        // ...
    
        @CreatedBy
        User creator;
        
        @LastModifiedBy
        User modifier;
        
        @CreatedDate
        Date createdAt;
        
        @LastModifiedDate
        Date modifiedAt;
    
        // ...
    
    }

Note, that if we want Spring to populate the principals, we need to use Spring Security as well.

For a more thorough description, please visit [this article](/database-auditing-jpa).

## 3\. Spring Data JPA Annotations

### 3.1. _@Query_

With _@Query_ , we can provide a JPQL implementation for a repository method:
    
    
    @Query("SELECT COUNT(*) FROM Person p")
    long getPersonCount();

Also, we can use named parameters:
    
    
    @Query("FROM Person p WHERE p.name = :name")
    Person findByName(@Param("name") String name);

Besides, we can use native SQL queries, if we set the _nativeQuery_ argument to _true_ :
    
    
    @Query(value = "SELECT AVG(p.age) FROM person p", nativeQuery = true)
    int getAverageAge();

For more information, please visit [this article](/spring-data-jpa-query).

### 3.2. _@Procedure_

**With Spring Data JPA we can easily call stored procedures from repositories.**

First, we need to declare the repository on the entity class using standard JPA annotations:
    
    
    @NamedStoredProcedureQueries({ 
        @NamedStoredProcedureQuery(
            name = "count_by_name", 
            procedureName = "person.count_by_name", 
            parameters = { 
                @StoredProcedureParameter(
                    mode = ParameterMode.IN, 
                    name = "name", 
                    type = String.class),
                @StoredProcedureParameter(
                    mode = ParameterMode.OUT, 
                    name = "count", 
                    type = Long.class) 
                }
        ) 
    })
    
    class Person {}

After this, we can refer to it in the repository with the name we declared in the _name_ argument:
    
    
    @Procedure(name = "count_by_name")
    long getCountByName(@Param("name") String name);

### 3.3. _@Lock_

We can configure the lock mode when we execute a repository query method:
    
    
    @Lock(LockModeType.NONE)
    @Query("SELECT COUNT(*) FROM Person p")
    long getPersonCount();

The available lock modes:

  * _READ_
  * _WRITE_
  * _OPTIMISTIC_
  * _OPTIMISTIC_FORCE_INCREMENT_
  * _PESSIMISTIC_READ_
  * _PESSIMISTIC_WRITE_
  * _PESSIMISTIC_FORCE_INCREMENT_
  * _NONE_



### 3.4. _@Modifying_

We can modify data with a repository method if we annotate it with _@Modifying_ :
    
    
    @Modifying
    @Query("UPDATE Person p SET p.name = :name WHERE p.id = :id")
    void changeName(@Param("id") long id, @Param("name") String name);

For more information, please visit [this article](/spring-data-jpa-query).

### 3.5. _@EnableJpaRepositories_

To use JPA repositories, we have to indicate it to Spring. We can do this with _@EnableJpaRepositories._

Note, that we have to use this annotation with _@Configuration_ :
    
    
    @Configuration
    @EnableJpaRepositories
    class PersistenceJPAConfig {}

Spring will look for repositories in the sub packages of this _@Configuration_ class.

We can alter this behavior with the _basePackages_ argument:
    
    
    @Configuration
    @EnableJpaRepositories(basePackages = "com.baeldung.persistence.dao")
    class PersistenceJPAConfig {}

Also note, that Spring Boot does this automatically if it finds Spring Data JPA on the classpath.

## 4\. Spring Data Mongo Annotations

Spring Data makes working with MongoDB much easier. In the next sections, we’ll explore the most basic features of Spring Data MongoDB.

For more information, please visit our [article about Spring Data MongoDB](/spring-data-mongodb-tutorial).

### 4.1. _@Document_

This annotation marks a class as being a domain object that we want to persist to the database:
    
    
    @Document
    class User {}

It also allows us to choose the name of the collection we want to use:
    
    
    @Document(collection = "user")
    class User {}

Note, that this annotation is the Mongo equivalent of _@Entity_ in JPA.

### 4.2. _@Field_

With _@Field_ , we can configure the name of a field we want to use when MongoDB persists the document:
    
    
    @Document
    class User {
    
        // ...
    
        @Field("email")
        String emailAddress;
    
        // ...
    
    }

Note, that this annotation is the Mongo equivalent of _@Column_ in JPA.

### 4.3. _@Query_

With _@Query_ , we can provide a finder query on a MongoDB repository method:
    
    
    @Query("{ 'name' : ?0 }")
    List<User> findUsersByName(String name);

### 4.4. _@EnableMongoRepositories_

To use MongoDB repositories, we have to indicate it to Spring. We can do this with _@EnableMongoRepositories._

Note, that we have to use this annotation with _@Configuration_ :
    
    
    @Configuration
    @EnableMongoRepositories
    class MongoConfig {}

Spring will look for repositories in the sub packages of this _@Configuration_ class. We can alter this behavior with the _basePackages_ argument:
    
    
    @Configuration
    @EnableMongoRepositories(basePackages = "com.baeldung.repository")
    class MongoConfig {}

Also note, that Spring Boot does this automatically if it finds Spring Data MongoDB on the classpath.

## 5\. Conclusion

In this article, we saw which are the most important annotations we need to deal with data in general, using Spring. In addition, we looked into the most common JPA and MongoDB annotations.

Next **»**

[Spring Bean Annotations](/spring-bean-annotations)

**«** Previous

[Spring Scheduling Annotations](/spring-scheduling-annotations)
