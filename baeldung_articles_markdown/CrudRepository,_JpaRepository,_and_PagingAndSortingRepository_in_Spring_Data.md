# CrudRepository, JpaRepository, and PagingAndSortingRepository in Spring Data

## **1\. Overview**

In this quick article, we’ll focus on different kinds of Spring Data repository interfaces and their functionality. We’ll touch on:

  * _CrudRepository_
  * _PagingAndSortingRepository_
  * _JpaRepository_



Simply put, every repository in [Spring Data](http://projects.spring.io/spring-data/) extends the generic _Repository_ interface, but beyond that, they each have different functionality.

## **2\. Spring Data Repositories**

_Let’s start with the[ JpaRepository](https://docs.spring.io/spring-data/jpa/docs/current/api/org/springframework/data/jpa/repository/JpaRepository.html)_ – which extends _[PagingAndSortingRepository](https://docs.spring.io/spring-data/commons/docs/current/api/org/springframework/data/repository/PagingAndSortingRepository.html)_ and, in turn, the _[CrudRepository](https://docs.spring.io/spring-data/commons/docs/current/api/org/springframework/data/repository/CrudRepository.html)_.

Each of these defines its functionality:

  * _[CrudRepository](https://docs.spring.io/spring-data/data-commons/docs/2.7.9/api/org/springframework/data/repository/CrudRepository.html)_ provides CRUD functions
  * _[PagingAndSortingRepository](https://docs.spring.io/spring-data/data-commons/docs/2.7.9/api/org/springframework/data/repository/PagingAndSortingRepository.html)_ provides methods to do pagination and sorting of records
  * _[JpaRepository](https://docs.spring.io/spring-data/jpa/docs/2.7.9/api/org/springframework/data/jpa/repository/JpaRepository.html)_ provides JPA-related methods such as flushing the persistence context and deleting records in a batch



And so, because of this inheritance relationship, the **_JpaRepository_ contains the full API of _CrudRepository_ and _PagingAndSortingRepository_.**

When we don’t need the full functionality provided by _JpaRepository_ and _PagingAndSortingRepository_ , we can use the _CrudRepository_.

Let’s now look at a quick example to understand these APIs better.

We’ll start with a simple _Product_ entity:
    
    
    @Entity
    public class Product {
    
        @Id
        private long id;
        private String name;
    
        // getters and setters
    }

And let’s implement a simple operation – find a _Product_ based on its name:
    
    
    @Repository
    public interface ProductRepository extends JpaRepository<Product, Long> {
        Product findByName(String productName);
    }

That’s all. The Spring Data Repository will auto-generate the implementation based on the name we provided it.

This was a very simple example, of course; you can go deeper into Spring Data JPA [here](/the-persistence-layer-with-spring-data-jpa).

## **3._CrudRepository_**

Let’s now have a look at the code for the [_CrudRepository_](https://docs.spring.io/spring-data/data-commons/docs/2.7.9/api/org/springframework/data/repository/CrudRepository.html) interface:
    
    
    public interface CrudRepository<T, ID extends Serializable>
      extends Repository<T, ID> {
    
        <S extends T> S save(S entity);
    
        T findOne(ID primaryKey);
    
        Iterable<T> findAll();
    
        Long count();
    
        void delete(T entity);
    
        boolean exists(ID primaryKey);
    }

Notice the typical CRUD functionality:

  * _save(…) – s_ ave an _Iterable_ of entities. Here, we can pass multiple objects to save them in a batch
  * _findOne(…)_ – get a single entity based on passed primary key value
  * _findAll()_ – get an _Iterable_ of all available entities in the database
  * _count() – r_ eturn the count of total entities in a table
  * _delete(…)_ – delete an entity based on the passed object
  * exists(…) – verify if an entity exists based on the passed primary key value



This interface looks quite generic and simple, but actually, it provides all the basic query abstractions needed in an application.

## **4._PagingAndSortingRepository_**

Now, let’s have a look at another repository interface, which extends _CrudRepository_ :
    
    
    public interface PagingAndSortingRepository<T, ID extends Serializable> 
      extends CrudRepository<T, ID> {
    
        Iterable<T> findAll(Sort sort);
    
        Page<T> findAll(Pageable pageable);
    }

This interface provides a method _findAll(Pageable pageable)_ , which is the key to implementing _Pagination._

When using _Pageable_ , we create a _Pageable_ object with certain properties, and we’ve to specify at least the following:

  1. Page size
  2. Current page number
  3. Sorting



So, let’s assume that we want to show the first page of a result set sorted by _lastName,_ ascending, having no more than five records each. This is how we can achieve this using a _PageRequest_ and a _Sort_ definition:
    
    
    Sort sort = new Sort(new Sort.Order(Direction.ASC, "lastName"));
    Pageable pageable = new PageRequest(0, 5, sort);

Passing the pageable object to the Spring data query will return the results in question (the first parameter of _PageRequest_ is zero-based).

## **5._JpaRepository_**

Finally, we’ll have a look at the [_JpaRepository_](https://docs.spring.io/spring-data/jpa/docs/2.7.9/api/) interface:
    
    
    public interface JpaRepository<T, ID extends Serializable> extends
      PagingAndSortingRepository<T, ID> {
    
        List<T> findAll();
    
        List<T> findAll(Sort sort);
    
        List<T> save(Iterable<? extends T> entities);
    
        void flush();
    
        T saveAndFlush(T entity);
    
        void deleteInBatch(Iterable<T> entities);
    }

Again, let’s look at each of these methods in brief:

  * _findAll()_ – get a _List_ of all available entities in the database
  * _findAll(…)_ – get a _List_ of all available entities and sort them using the provided condition
  * _save(…) – s_ ave an _Iterable_ of entities. Here, we can pass multiple objects to save them in a batch
  * _flush() – f_ lush all pending tasks to the database
  * _saveAndFlush(…)_ – save the entity and flush changes immediately
  * deleteInBatch(…) – delete an _Iterable_ of entities. Here, we can pass multiple objects to delete them in a batch



Clearly, the above interface extends _PagingAndSortingRepository,_ which means it also has all methods present in the _CrudRepository_.

## 6\. Spring Data Repositories in Spring Data 3

In the new version of Spring Data, the internals of some Repository classes have changed slightly, adding new functionalities and providing a simpler development experience.

We now have access to the advantageous List-based CRUD repository interface. Also, the class hierarchy of some spring-data Repository classes is based on a different structure.

All details are available in our [New CRUD Repository Interfaces in Spring Data 3](/spring-data-3-crud-repository-interfaces) article.

## **7\. Downsides of Spring Data Repositories**

Beyond all the very useful advantages of these repositories, there are some basic downsides of directly depending on these as well:

  1. We couple our code to the library and to its specific abstractions, such as `Page` or `Pageable`; that’s, of course, not unique to this library – but we do have to be careful not to expose these internal implementation details
  2. By extending, e.g. _CrudRepository_ , we expose a complete set of persistence methods at once. This is probably fine in most circumstances as well, but we might run into situations where we’d like to gain more fine-grained control over the methods exposed, e.g. to create a _ReadOnlyRepository_ that doesn’t include the _save(…)_ and _delete(…)_ methods of _CrudRepository_



## **8\. Conclusion**

This article covered some brief but important differences and features of Spring Data JPA repository interfaces. For more information, have a look at the series on [Spring Persistence](/persistence-with-spring-series).
