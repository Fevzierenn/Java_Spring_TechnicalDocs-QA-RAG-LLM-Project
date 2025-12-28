# Transactions with Spring and JPA

## **1\. Overview**

This tutorial will discuss **the right way to configure Spring Transactions** , how to use the _@Transactional_ annotation and common pitfalls.

For a more in-depth discussion on the core persistence configuration, check out the [Spring with JPA tutorial](/the-persistence-layer-with-spring-and-jpa "Spring 3 and JPA with Hibernate").

Basically, there are two distinct ways to configure Transactions, annotations and AOP, each with its own advantages. We’re going to discuss the more common annotation config here.

## **2\. Configure Transactions**

Spring 3.1 introduces **the _@EnableTransactionManagement_ annotation** that we can use in a _@Configuration_ class to enable transactional support:
    
    
    @Configuration
    @EnableTransactionManagement
    public class PersistenceJPAConfig{
    
       @Bean
       public LocalContainerEntityManagerFactoryBean entityManagerFactory() {
           //...
       }
    
       @Bean
       public PlatformTransactionManager transactionManager() {
          JpaTransactionManager transactionManager = new JpaTransactionManager();
          transactionManager.setEntityManagerFactory(entityManagerFactory().getObject());
          return transactionManager;
       }
    }

However, **if we’re using a Spring Boot project and have a spring-data-* or spring-tx dependencies on the classpath, then transaction management will be enabled by default**.

## **3\. Configure Transactions With XML**

For versions before 3.1, or if Java is not an option, here is the XML configuration using _annotation-driven_ and namespace support:
    
    
    <bean id="txManager" class="org.springframework.orm.jpa.JpaTransactionManager">
       <property name="entityManagerFactory" ref="myEmf" />
    </bean>
    <tx:annotation-driven transaction-manager="txManager" />

## **4\. The _@Transactional_ Annotation**

With transactions configured, we can now annotate a bean with _@Transactional_ either at the class or method level:
    
    
    @Service
    @Transactional
    public class FooService {
        //...
    }

The annotation supports **further configuration** as well:

  * the _Propagation Type_ of the transaction
  * the _Isolation Level_ of the transaction
  * a _Timeout_ for the operation wrapped by the transaction
  * a _readOnly flag_ – a hint for the persistence provider that the transaction should be read only
  * the _Rollback_ rules for the transaction



Note that by default, rollback happens for runtime, unchecked exceptions only. **The checked exception does not trigger a rollback** of the transaction. We can, of course, configure this behavior with the _rollbackFor_ and _noRollbackFor_ annotation parameters.

## **5\. Potential Pitfalls**

### **5.1. Transactions and Proxies**

At a high level, **Spring creates proxies for all the classes annotated with _@Transactional_** , either on the class or on any of the methods. The proxy allows the framework to inject transactional logic before and after the running method, mainly for starting and committing the transaction.

What’s important to keep in mind is that, if the transactional bean is implementing an interface, by default the proxy will be a Java Dynamic Proxy. This means that only external method calls that come in through the proxy will be intercepted. **Any self-invocation calls will not start any transaction,** even if the method has the _@Transactional_ annotation.

Another caveat of using proxies is that **only public methods should be annotated with _@Transactional._** Methods of any other visibilities will simply ignore the annotation silently as these are not proxied.

### **5.2. Changing the Isolation Level**
    
    
    courseDao.createWithRuntimeException(course);

We can also change the transaction isolation level:
    
    
    @Transactional(isolation = Isolation.SERIALIZABLE)

Note that this has actually been [introduced](https://jira.spring.io/browse/SPR-5012) in Spring 4.1; if we run the above example before Spring 4.1, it will result in:
    
    
    org.springframework.transaction.InvalidIsolationLevelException: Standard JPA does not support custom isolation levels – use a special JpaDialect for your JPA implementation

### **5.3. Read-Only Transactions**

The _readOnly_ flag usually generates confusion, especially when working with JPA. From the Javadoc:
    
    
    This just serves as a hint for the actual transaction subsystem; it will not necessarily cause failure of write access attempts. A transaction manager which cannot interpret the read-only hint will not throw an exception when asked for a read-only transaction.

The fact is that **we can’t be sure that an insert or update won’t occur when the _readOnly_ flag is set.** This behavior is vendor-dependent, whereas JPA is vendor agnostic.

It’s also important to understand that**the _readOnly_ flag is only relevant inside a transaction.** If an operation occurs outside of a transactional context, the flag is simply ignored. A simple example of that would call a method annotated with:
    
    
    @Transactional(propagation = Propagation.SUPPORTS, readOnly = true)

From a non-transactional context, a transaction will not be created and the _readOnly_ flag will be ignored.

### **5.4. Transaction Logging**

A helpful method to understand transactional-related issues is fine-tuning logging in the transactional packages. The relevant package in Spring is “ _org.springframework.transaction”_ , which should be configured with a logging level of _TRACE._

### 5.5. Transaction Rollback

The _@Transactional_ annotation is the metadata that specifies the semantics of the transactions on a method. We have two ways to rollback a transaction: declarative and programmatic.

In the **declarative approach, we annotate the methods with the _@_**_**Transactional**_**annotation**. The _@Transactional_ annotation makes use of the attributes _rollbackFor_ or _rollbackForClassName_ to rollback the transactions, and the attributes _noRollbackFor_ or _noRollbackForClassName_ to avoid rollback on listed exceptions.

The default rollback behavior in the declarative approach will rollback on runtime exceptions. 

Let’s see a simple example using the declarative approach to rollback a transaction for runtime exceptions or errors:
    
    
    @Transactional
    public void createCourseDeclarativeWithRuntimeException(Course course) {
        courseDao.create(course);
        throw new DataIntegrityViolationException("Throwing exception for demoing Rollback!!!");
    }

Next, we’ll use the declarative approach to rollback a transaction for the listed checked exceptions. The rollback in our example is on _SQLException_ :
    
    
    @Transactional(rollbackFor = { SQLException.class })
    public void createCourseDeclarativeWithCheckedException(Course course) throws SQLException {
        courseDao.create(course);
        throw new SQLException("Throwing exception for demoing rollback");
    }

Let’s see a simple use of attribute _noRollbackFor_ in the declarative approach to prevent rollback of the transaction for the listed exception:
    
    
    @Transactional(noRollbackFor = { SQLException.class })
    public void createCourseDeclarativeWithNoRollBack(Course course) throws SQLException {
        courseDao.create(course);
        throw new SQLException("Throwing exception for demoing rollback");
    }

In the **programmatic approach****, we rollback the transactions using _TransactionAspectSupport_** :
    
    
    public void createCourseDefaultRatingProgramatic(Course course) {
        try {
           courseDao.create(course);
        } catch (Exception e) {
           TransactionAspectSupport.currentTransactionStatus().setRollbackOnly();
        }
    }

The **d****eclarative rollback s trategy should be favored over the programmatic rollback strategy**. 

## **6\. Conclusion**

In this article, we covered the basic configuration of transactional semantics using both Java and XML. We also learned how to use _@Transactional,_ and the best practices of a Transactional Strategy.
