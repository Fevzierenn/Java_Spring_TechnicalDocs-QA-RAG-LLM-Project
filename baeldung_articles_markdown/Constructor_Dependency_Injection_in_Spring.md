# Constructor Dependency Injection in Spring

## **1\. Introduction**

Arguably one of the most important development principles of modern software design is _Dependency Injection (DI),_ which quite naturally flows out of another critically important principle: _Modularity._

This quick tutorial will explore a specific type of DI technique within Spring called _Constructor-Based Dependency Injection,_ which simply put, means that we pass the required components into a class at the time of instantiation.

To get started, we need to import the _spring-boot-starter-web_ dependency in our _pom.xml_ :
    
    
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
     </dependency>

Then we need to set up a _Configuration_ file. This file can be either a POJO or an XML file, based on preference.

## **2\. Annotation Based Configuration**

Java configuration files look similar to Java objects with some additional annotations:
    
    
    @Configuration
    @ComponentScan("com.baeldung.constructordi")
    public class Config {
    
        @Bean
        public Engine engine() {
            return new Engine("v8", 5);
        }
    
        @Bean
        public Transmission transmission() {
            return new Transmission("sliding");
        }
    }
    

Here we’re using annotations to notify Spring runtime that this class provides bean definitions (_@Bean_ annotation), and that the package _com.baeldung.spring_ needs to perform a context scan for additional beans. Next, we define a _Car_ class:
    
    
    @Component
    public class Car {
    
        @Autowired
        public Car(Engine engine, Transmission transmission) {
            this.engine = engine;
            this.transmission = transmission;
        }
    }

Spring will encounter our _Car_ class while doing a package scan, and will initialize its instance by calling the _@Autowired_ annotated constructor.

By calling the _@Bean_ annotated methods of the _Config_ class, we will obtain instances of _Engine and Transmission_. Finally, we need to bootstrap an _ApplicationContext_ using our POJO configuration:
    
    
    ApplicationContext context = new AnnotationConfigApplicationContext(Config.class);
    Car car = context.getBean(Car.class);

## **3\. Implicit Constructor Injection**

Classes with a single constructor can omit the _@Autowired_ annotation. This is a nice little bit of convenience and boilerplate removal.

On top of that, also starting with 4.3, we can leverage the constructor-based injection in _@Configuration_ annotated classes. In addition, if such a class has only one constructor, we can omit the _@Autowired_ annotation as well.

## 4\. Pros and Cons

Constructor injection has a few advantages compared to field injection.

**The first benefit is testability.** Suppose we’re going to unit test a Spring bean that uses field injection:
    
    
    public class UserService {
        
        @Autowired 
        private UserRepository userRepository;
    }

During the construction of a _UserService_ instance, we can’t initialize the _userRepository_ state. The only way to achieve this is through [the Reflection API](/java-reflection), which completely breaks encapsulation. Also, the resulting code will be less safe compared to a simple constructor call.

Additionally, **with** **field injection, we can’t enforce class-level invariants,**_s_ o it’s possible to have a  _UserService_ instance without a properly initialized _userRepository_. Therefore, we may experience random  _NullPointerException_ s here and there. Also, with constructor injection, it’s easier to build immutable components.

Moreover, **using constructors to create object instances is more natural from the OOP standpoint.**

On the other hand, the main disadvantage of constructor injection is its verbosity, especially when a bean has a handful of dependencies. Sometimes it can be a blessing in disguise, as we may try harder to keep the number of dependencies minimal.

## **5\. Conclusion**

This brief article has showcased the basics of two distinct ways to use _Constructor-Based Dependency Injection_ using the Spring framework.
