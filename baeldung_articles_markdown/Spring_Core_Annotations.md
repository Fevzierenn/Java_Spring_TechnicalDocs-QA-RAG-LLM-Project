# Spring Core Annotations

[This article is part of a series:](javascript:void\(0\);)

• Spring Core Annotations (current article)

[• Spring Web Annotations](/spring-mvc-annotations)  
[• Spring Boot Annotations](/spring-boot-annotations)  
[• Spring Scheduling Annotations](/spring-scheduling-annotations)  
[• Spring Data Annotations](/spring-data-annotations)  
[• Spring Bean Annotations](/spring-bean-annotations)  


## 1\. Overview

We can leverage the capabilities of Spring DI engine using the annotations in the _org.springframework.beans.factory.annotation_ and  _org.springframework.context.annotation_ packages.

We often call these “Spring core annotations” and we’ll review them in this tutorial.

## 2\. DI-Related Annotations

### 2.1. _@Autowired_

We can use the _@Autowired_ to **mark a dependency which Spring is going to resolve and inject**. We can use this annotation with a constructor, setter, or field injection.

Constructor injection:
    
    
    class Car {
        Engine engine;
    
        @Autowired
        Car(Engine engine) {
            this.engine = engine;
        }
    }

Setter injection:
    
    
    class Car {
        Engine engine;
    
        @Autowired
        void setEngine(Engine engine) {
            this.engine = engine;
        }
    }

Field injection:
    
    
    class Car {
        @Autowired
        Engine engine;
    }

_@Autowired_ has a _boolean_ argument called _required_ with a default value of _true_. It tunes Spring’s behavior when it doesn’t find a suitable bean to wire. When _true_ , an exception is thrown, otherwise, nothing is wired.

Note, that if we use constructor injection, all constructor arguments are mandatory.

Starting with version 4.3, we don’t need to annotate constructors with _@Autowired_ explicitly unless we declare at least two constructors.

For more details visit our articles about [_@Autowired_](/spring-autowire) and [constructor injection](/constructor-injection-in-spring).

### 2.2. _@Bean_

_@Bean_ marks a factory method which instantiates a Spring bean:
    
    
    @Bean
    Engine engine() {
        return new Engine();
    }

**Spring calls these methods** when a new instance of the return type is required.

The resulting bean has the same name as the factory method. If we want to name it differently, we can do so with the _name_ or the _value_ arguments of this annotation (the argument _value_ is an alias for the argument _name_):
    
    
    @Bean("engine")
    Engine getEngine() {
        return new Engine();
    }

Note, that all methods annotated with _@Bean_ must be in _@Configuration_ classes.

### 2.3. _@Qualifier_

We use _@Qualifier_ along with _@Autowired_ to **provide the bean id or bean name** we want to use in ambiguous situations.

For example, the following two beans implement the same interface:
    
    
    class Bike implements Vehicle {}
    
    class Car implements Vehicle {}

If Spring needs to inject a _Vehicle_ bean, it ends up with multiple matching definitions. In such cases, we can provide a bean’s name explicitly using the _@Qualifier_ annotation.

Using constructor injection:
    
    
    @Autowired
    Biker(@Qualifier("bike") Vehicle vehicle) {
        this.vehicle = vehicle;
    }

Using setter injection:
    
    
    @Autowired
    void setVehicle(@Qualifier("bike") Vehicle vehicle) {
        this.vehicle = vehicle;
    }

Alternatively:
    
    
    @Autowired
    @Qualifier("bike")
    void setVehicle(Vehicle vehicle) {
        this.vehicle = vehicle;
    }

Using field injection:
    
    
    @Autowired
    @Qualifier("bike")
    Vehicle vehicle;

For a more detailed description, please read [this article](/spring-autowire).

### 2.4. _@Value_

We can use [_@Value_](/spring-value-annotation) for injecting property values into beans. It’s compatible with constructor, setter, and field injection.

Constructor injection:
    
    
    Engine(@Value("8") int cylinderCount) {
        this.cylinderCount = cylinderCount;
    }

Setter injection:
    
    
    @Autowired
    void setCylinderCount(@Value("8") int cylinderCount) {
        this.cylinderCount = cylinderCount;
    }

Alternatively:
    
    
    @Value("8")
    void setCylinderCount(int cylinderCount) {
        this.cylinderCount = cylinderCount;
    }

Field injection:
    
    
    @Value("8")
    int cylinderCount;

Of course, injecting static values isn’t useful. Therefore, we can use **placeholder strings** in _@Value_ to wire values **defined in external sources** , for example, in _.properties_ or _.yaml_ files.

Let’s assume the following _.properties_ file:
    
    
    engine.fuelType=petrol

We can inject the value of _engine.fuelType_ with the following:
    
    
    @Value("${engine.fuelType}")
    String fuelType;

We can use _@Value_ even with SpEL. More advanced examples can be found in our [article about _@Value_](/spring-value-annotation).

### 2.5. _@DependsOn_

We can use this annotation to make Spring **initialize other beans before the annotated one**. Usually, this behavior is automatic, based on the explicit dependencies between beans.

We only need this annotation **when the dependencies are implicit** , for example, JDBC driver loading or static variable initialization.

We can use _@DependsOn_ on the dependent class specifying the names of the dependency beans. The annotation’s _value_ argument needs an array containing the dependency bean names:
    
    
    @DependsOn("engine")
    class Car implements Vehicle {}

Alternatively, if we define a bean with the _@Bean_ annotation, the factory method should be annotated with _@DependsOn_ :
    
    
    @Bean
    @DependsOn("fuel")
    Engine engine() {
        return new Engine();
    }

### 2.6. _@Lazy_

We use [_@Lazy_](/spring-lazy-annotation) when we want to initialize our bean lazily. By default, Spring creates all singleton beans eagerly at the startup/bootstrapping of the application context.

However, there are cases when**we need to create a bean when we request it, not at application startup**.

This annotation behaves differently depending on where we exactly place it. We can put it on:

  * a _@Bean_ annotated bean factory method, to delay the method call (hence the bean creation)
  * a @_Configuration_ class and all contained _@Bean_ methods will be affected
  * a _@Component_ class, which is not a _@Configuration_ class, this bean will be initialized lazily
  * an _@Autowired_ constructor, setter, or field, to load the dependency itself lazily (via proxy)



This annotation has an argument named _value_ with the default value of _true_. It is useful to override the default behavior.

For example, marking beans to be eagerly loaded when the global setting is lazy, or configure specific _@Bean_ methods to eager loading in a _@Configuration_ class marked with _@Lazy_ :
    
    
    @Configuration
    @Lazy
    class VehicleFactoryConfig {
    
        @Bean
        @Lazy(false)
        Engine engine() {
            return new Engine();
        }
    }

For further reading, please visit [this article](/spring-lazy-annotation).

### 2.7. _@Lookup_

A method annotated with _@Lookup_ tells Spring to return an instance of the method’s return type when we invoke it.

Detailed information about the annotation [can be found in this article](/spring-lookup).

### 2.8. _@Primary_

Sometimes we need to define multiple beans of the same type. In these cases, the injection will be unsuccessful because Spring has no clue which bean we need.

We already saw an option to deal with this scenario: marking all the wiring points with _@Qualifier_ and specify the name of the required bean.

However, most of the time we need a specific bean and rarely the others. We can use _@Primary_ to simplify this case: if **we mark the most frequently used bean with _@Primary_** it will be chosen on unqualified injection points:
    
    
    @Component
    @Primary
    class Car implements Vehicle {}
    
    @Component
    class Bike implements Vehicle {}
    
    @Component
    class Driver {
        @Autowired
        Vehicle vehicle;
    }
    
    @Component
    class Biker {
        @Autowired
        @Qualifier("bike")
        Vehicle vehicle;
    }

In the previous example _Car_ is the primary vehicle. Therefore, in the _Driver_ class, Spring injects a _Car_ bean. Of course, in the _Biker_ bean, the value of the field _vehicle_ will be a _Bike_ object because it’s qualified.

### 2.9. _@Scope_

We use _@Scope_ to define the [scope](/spring-bean-scopes) of a _@Component_ class or a _@Bean_ definition _._ It can be either _singleton, prototype, request, session, globalSession_ or some custom scope.

For example:
    
    
    @Component
    @Scope("prototype")
    class Engine {}

## 3\. Context Configuration Annotations

We can configure the application context with the annotations described in this section.

### 3.1. _@Profile_

If we want Spring to **use a _@Component_ class or a _@Bean_ method only when a specific profile is active**, we can mark it with _@Profile_. We can configure the name of the profile with the _value_ argument of the annotation:
    
    
    @Component
    @Profile("sportDay")
    class Bike implements Vehicle {}

You can read more about profiles in [this article](/spring-profiles).

### 3.2. _@Import_

We can use **specific _@Configuration_ classes without component scanning** with this annotation. We can provide those classes with _@Import_ ‘s _value_ argument:
    
    
    @Import(VehiclePartSupplier.class)
    class VehicleFactoryConfig {}

### 3.3. _@ImportResource_

We can **import XML configurations** with this annotation. We can specify the XML file locations with the _locations_ argument, or with its alias, the _value_ argument:
    
    
    @Configuration
    @ImportResource("classpath:/annotations.xml")
    class VehicleFactoryConfig {}

### 3.4. _@PropertySource_

With this annotation, we can **define property files for application settings** :
    
    
    @Configuration
    @PropertySource("classpath:/annotations.properties")
    class VehicleFactoryConfig {}

_@PropertySource_ leverages the Java 8 repeating annotations feature, which means we can mark a class with it multiple times:
    
    
    @Configuration
    @PropertySource("classpath:/annotations.properties")
    @PropertySource("classpath:/vehicle-factory.properties")
    class VehicleFactoryConfig {}

### 3.5. _@PropertySources_

We can use this annotation to specify multiple _@PropertySource_ configurations:
    
    
    @Configuration
    @PropertySources({ 
        @PropertySource("classpath:/annotations.properties"),
        @PropertySource("classpath:/vehicle-factory.properties")
    })
    class VehicleFactoryConfig {}

Note, that since Java 8 we can achieve the same with the repeating annotations feature as described above.

## 4\. Conclusion

In this article, we saw an overview of the most common Spring core annotations. We saw how to configure bean wiring and application context, and how to mark classes for component scanning.

Next **»**

[Spring Web Annotations](/spring-mvc-annotations)
