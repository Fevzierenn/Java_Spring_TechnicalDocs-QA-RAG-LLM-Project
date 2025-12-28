# Spring PostConstruct and PreDestroy Annotations

## 1\. Introduction

Spring allows us to attach custom actions to [bean creation and destruction](/running-setup-logic-on-startup-in-spring). We can, for example, do it by implementing the [ _InitializingBean_](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/beans/factory/InitializingBean.html) and [_DisposableBean_](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/beans/factory/DisposableBean.html) interfaces.

In this quick tutorial, we’ll look at a second possibility, the _@PostConstruct_ and _@PreDestroy_ annotations.

## 2\. _@PostConstruct_

**Spring calls the methods annotated with _@PostConstruct_ only once, just after the initialization of bean properties**. Keep in mind that these methods will run even if there’s nothing to initialize.

The method annotated with _@PostConstruct_ can have any access level, but it can’t be static.

One possible use of _@PostConstruct_ is populating a database. For instance, during development, we might want to create some default users:
    
    
    @Component
    public class DbInit {
    
        @Autowired
        private UserRepository userRepository;
    
        @PostConstruct
        private void postConstruct() {
            User admin = new User("admin", "admin password");
            User normalUser = new User("user", "user password");
            userRepository.save(admin, normalUser);
        }
    }

The above example will first initialize _UserRepository_ and then run the _@PostConstruct_ method.

## 3\. _@PreDestroy_

A method annotated with _@PreDestroy_ runs only once, just before Spring removes our bean from the application context.

Same as with _@PostConstruct_ , the methods annotated with _@PreDestroy_ can have any access level, but can’t be static.
    
    
    @Component
    public class UserRepository {
    
        private DbConnection dbConnection;
        @PreDestroy
        public void preDestroy() {
            dbConnection.close();
        }
    }

The purpose of this method should be to release resources or perform other cleanup tasks, such as closing a database connection, before the bean gets destroyed.

## 4\. _javax.annotation_ or _jakarta.annotation_

From JDK 6 to JDK 8, the _@PostConstruct_ and _@PreDestroy_ annotations were part of the standard Java libraries under the _javax.annotation_ package. However, [**with JDK 9, the entire _javax.annotation_ package was removed from the core Java modules and fully eliminated in JDK 11**](/java-enterprise-evolution). In Jakarta EE 9, this package has been relocated to _jakarta.annotation._

So, sometimes, we may ask, “Should I use the annotations from _javax.annotation_ or _jakarta annotation_?” **This depends on the Spring version we use.** To quickly understand the compatibilities among Spring, JDK, _javax_ , and _jakarta_ namespaces, let’s summarize them in a table:

Spring Version | JDK Version | Java / Jakatar Namespace  
---|---|---  
6.1.x | JDK 17 to JDK 23 | jakarta  
6.0.x | JDK 17 to JDK 21 | jakarta  
5.3.x | JDK 8 to JDK 21 | javax  
  
As the table above shows, with Spring 6.0.x and 6.1.x, we should use the _jakarta_ namespace. However, **if our project uses Spring 5.3.x and JDK 9 or a later version, since Spring 5.3.x only supports the _javax_ namespace, we must explicitly add the [_javax.annotation-api_ dependency](https://mvnrepository.com/artifact/javax.annotation/javax.annotation-api) to our project:**
    
    
    <dependency>
        <groupId>javax.annotation</groupId>
        <artifactId>javax.annotation-api</artifactId>
        <version>1.3.2</version>
    </dependency>

The above XML shows an example of adding the _javax.annotation-api_ dependency to a Maven project’s _pom.xml._

## 5\. Conclusion

In this brief article, we learned how to use the _@PostConstruct_ and _@PreDestroy_ annotations.
