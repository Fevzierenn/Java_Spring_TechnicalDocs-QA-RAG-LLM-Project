# @Component vs @Repository and @Service in Spring

## **1\. Introduction**

In this quick tutorial, we’re going to learn about the differences between the _@Component, @Repository,_ and _@Service_ annotations in the Spring Framework.

## 2\. Spring Annotations

In most typical applications, we have distinct layers like data access, presentation, service, business, etc.

Additionally, in each layer we have various beans. To detect these beans automatically, **Spring uses classpath scanning annotations**.

Then it registers each bean in the _ApplicationContext_.

Here’s a quick overview of a few of these annotations:

  * _@Component_ is a generic stereotype for any Spring-managed component.
  * _@Service_ annotates classes at the service layer.
  * _@Repository_ annotates classes at the persistence layer, which will act as a database repository.



We already have an [extended article](/spring-bean-annotations) about these annotations, so we’ll keep the focus here to the differences between them.

## **3\. What’s Different?**

**The major difference between these stereotypes is that they are used for different classifications.** When we annotate a class for auto-detection, we should use the respective stereotype.

Now let’s go through them in more detail.

### **3.1._@Component_**

**We can use @Component across the application to mark the beans as Spring’s managed components**. Spring will only pick up and register beans with _@Component,_ and doesn’t look for _@Service_ and  _@Repository_ in general.

They are registered in _ApplicationContext_ because they are annotated with _@Component_ :
    
    
    @Component
    public @interface Service {
    }
    
    
    
    @Component
    public @interface Repository {
    }
    

_@Service_ and  _@Repository_ are special cases of _@Component_. They are technically the same, but we use them for the different purposes.

### **3.2._@Repository_**

**_@Repository_ ’s job is to catch persistence-specific exceptions and re-throw them as one of Spring’s unified unchecked exceptions**.

For this, Spring provides _PersistenceExceptionTranslationPostProcessor_ , which we are required to add in our application context (already included if we’re using Spring Boot):
    
    
    <bean class=
      "org.springframework.dao.annotation.PersistenceExceptionTranslationPostProcessor"/>

This bean post processor adds an advisor to any bean that’s annotated with  _@Repository._

### **3.3._@Service_**

**We mark beans with @Service to indicate that they’re holding the business logic**. Besides being used in the service layer, there isn’t any other special use for this annotation.

## **4\. Conclusion**

**In this article, we learned about the differences between the _@Component, @Repository,_ and _@Service_ annotations**. We examined each annotation separately to understand their areas of use.

In conclusion, it’s always a good idea to choose the annotation based on their layer conventions.
