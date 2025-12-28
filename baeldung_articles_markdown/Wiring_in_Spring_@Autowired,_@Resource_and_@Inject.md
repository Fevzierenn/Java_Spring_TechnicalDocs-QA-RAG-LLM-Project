# Wiring in Spring: @Autowired, @Resource and @Inject

## **1\. Overview**

In this Spring Framework tutorial, we’ll demonstrate how to use annotations related to dependency injection, namely the _@Resource_ , _@Inject_ , and _@Autowired_ annotations. These annotations provide classes with a declarative way to resolve dependencies:
    
    
    @Autowired 
    ArbitraryClass arbObject;

As opposed to instantiating them directly (the imperative way):
    
    
    ArbitraryClass arbObject = new ArbitraryClass();

Two of the three annotations belong to the Java extension package: _javax.annotation.Resource_ and _javax.inject.Inject_. The _@Autowired_ annotation belongs to the _org.springframework.beans.factory.annotation_ package.

Each of these annotations can resolve dependencies either by field injection or by setter injection. We’ll use a simplified, but practical example to demonstrate the distinction between the three annotations, based on the execution paths taken by each annotation.

The examples will focus on how to use the three injection annotations during integration testing. The dependency required by the test can either be an arbitrary file or an arbitrary class.

## **2\. The _@Resource_ A****nnotation**

The _@Resource_ annotation is part of the [JSR-250](https://jcp.org/en/jsr/detail?id=250) annotation collection, and is packaged with Jakarta EE. This annotation has the following execution paths, listed by precedence:

  1. Match by Name
  2. Match by Type
  3. Match by Qualifier



These execution paths are applicable to both setter and field injection.

### **2.1. Field Injection**

We can resolve dependencies by field injection by annotating an instance variable with the _@Resource_ annotation.

**2.1.1. Match by Name**

We’ll use the following integration test to demonstrate match-by-name field injection:
    
    
    @RunWith(SpringJUnit4ClassRunner.class)
    @ContextConfiguration(
      loader=AnnotationConfigContextLoader.class,
      classes=ApplicationContextTestResourceNameType.class)
    public class FieldResourceInjectionIntegrationTest {
    
        @Resource(name="namedFile")
        private File defaultFile;
    
        @Test
        public void givenResourceAnnotation_WhenOnField_ThenDependencyValid(){
            assertNotNull(defaultFile);
            assertEquals("namedFile.txt", defaultFile.getName());
        }
    }

Let’s go through the code. In the _FieldResourceInjectionTest_ integration test, at line 7, we resolved the dependency by name by passing in the bean name as an attribute value to the _@Resource_ annotation:
    
    
    @Resource(name="namedFile")
    private File defaultFile;

This configuration will resolve dependencies using the match-by-name execution path. We must define the bean _namedFile_ in the _ApplicationContextTestResourceNameType_ application context.

Note that the bean id and the corresponding reference attribute value must match:
    
    
    @Configuration
    public class ApplicationContextTestResourceNameType {
    
        @Bean(name="namedFile")
        public File namedFile() {
            File namedFile = new File("namedFile.txt");
            return namedFile;
        }
    }

If we fail to define the bean in the application context, it will result in an _org.springframework.beans.factory.NoSuchBeanDefinitionException_ being thrown. We can demonstrate this by changing the attribute value passed into the _@Bean_ annotation in the _ApplicationContextTestResourceNameType_ application context, or changing the attribute value passed into the _@Resource_ annotation in the _FieldResourceInjectionTest_ integration test.

#### **2.1.2. Match by Type**

To demonstrate the match-by-type execution path, we just remove the attribute value at line 7 of the _FieldResourceInjectionTest_ integration test:
    
    
    @Resource
    private File defaultFile;

Then we run the test again.

The test will still pass because if the _@Resource_ annotation doesn’t receive a bean name as an attribute value, the Spring Framework will proceed with the next level of precedence, match-by-type, in order to try resolve the dependency.

#### **2.1.3. Match by Qualifier**

To demonstrate the match-by-qualifier execution path, the integration testing scenario will be modified so that there are two beans defined in the _ApplicationContextTestResourceQualifier_ application context:
    
    
    @Configuration
    public class ApplicationContextTestResourceQualifier {
    
        @Bean(name="defaultFile")
        public File defaultFile() {
            File defaultFile = new File("defaultFile.txt");
            return defaultFile;
        }
    
        @Bean(name="namedFile")
        public File namedFile() {
            File namedFile = new File("namedFile.txt");
            return namedFile;
        }
    }

We’ll use the _QualifierResourceInjectionTest_ integration test to demonstrate match-by-qualifier dependency resolution. In this scenario, a specific bean dependency needs to be injected into each reference variable:
    
    
    @RunWith(SpringJUnit4ClassRunner.class)
    @ContextConfiguration(
      loader=AnnotationConfigContextLoader.class,
      classes=ApplicationContextTestResourceQualifier.class)
    public class QualifierResourceInjectionIntegrationTest {
    
        @Resource
        private File dependency1;
    	
        @Resource
        private File dependency2;
    
        @Test
        public void givenResourceAnnotation_WhenField_ThenDependency1Valid(){
            assertNotNull(dependency1);
            assertEquals("defaultFile.txt", dependency1.getName());
        }
    
        @Test
        public void givenResourceQualifier_WhenField_ThenDependency2Valid(){
            assertNotNull(dependency2);
            assertEquals("namedFile.txt", dependency2.getName());
        }
    }

When we run the integration test, an _org.springframework.beans.factory.NoUniqueBeanDefinitionException_ will be thrown. This will happen because the application context will find two bean definitions of type _File_ , and won’t know which bean should resolve the dependency.

To resolve this issue, we need to refer to line 7 to line 10 of the _QualifierResourceInjectionTest_ integration test:
    
    
    @Resource
    private File dependency1;
    
    @Resource
    private File dependency2;

We have to add the following lines of code:
    
    
    @Qualifier("defaultFile")
    
    @Qualifier("namedFile")

So that the code block looks as follows:
    
    
    @Resource
    @Qualifier("defaultFile")
    private File dependency1;
    
    @Resource
    @Qualifier("namedFile")
    private File dependency2;

When we run the integration test again, it should pass. Our test demonstrates that even if we define multiple beans in an application context, we can use the _@Qualifier_ annotation to clear any confusion by allowing us to inject specific dependencies into a class.

### **2.2. Setter Injection**

The execution paths taken when injecting dependencies on a field are applicable to setter-based injection as well.

#### **2.2.1. Match by Name**

The only difference is the _MethodResourceInjectionTest_ integration test has a setter method:
    
    
    @RunWith(SpringJUnit4ClassRunner.class)
    @ContextConfiguration(
      loader=AnnotationConfigContextLoader.class,
      classes=ApplicationContextTestResourceNameType.class)
    public class MethodResourceInjectionIntegrationTest {
    
        private File defaultFile;
    
        @Resource(name="namedFile")
        protected void setDefaultFile(File defaultFile) {
            this.defaultFile = defaultFile;
        }
    
        @Test
        public void givenResourceAnnotation_WhenSetter_ThenDependencyValid(){
            assertNotNull(defaultFile);
            assertEquals("namedFile.txt", defaultFile.getName());
        }
    }

We resolve dependencies by setter injection by annotating a reference variable’s corresponding setter method. Then we pass the name of the bean dependency as an attribute value to the _@Resource_ annotation:
    
    
    private File defaultFile;
    
    @Resource(name="namedFile")
    protected void setDefaultFile(File defaultFile) {
        this.defaultFile = defaultFile;
    }

We’ll reuse the _namedFile_ bean dependency in this example. The bean name and the corresponding attribute value must match.

When we run the integration test, it will pass.

In order for us to verify that the match-by-name execution path resolved the dependency, we need to change the attribute value passed to the _@Resource_ annotation to a value of our choice and run the test again. This time, the test will fail with a _NoSuchBeanDefinitionException_.

#### **2.2.2. Match by Type**

To demonstrate setter-based, match-by-type execution, we will use the _MethodByTypeResourceTest_ integration test:
    
    
    @RunWith(SpringJUnit4ClassRunner.class)
    @ContextConfiguration(
      loader=AnnotationConfigContextLoader.class,
      classes=ApplicationContextTestResourceNameType.class)
    public class MethodByTypeResourceIntegrationTest {
    
        private File defaultFile;
    
        @Resource
        protected void setDefaultFile(File defaultFile) {
            this.defaultFile = defaultFile;
        }
    
        @Test
        public void givenResourceAnnotation_WhenSetter_ThenValidDependency(){
            assertNotNull(defaultFile);
            assertEquals("namedFile.txt", defaultFile.getName());
        }
    }

When we run this test, it will pass.

In order for us to verify that the match-by-type execution path resolved the _File_ dependency, we need to change the class type of the _defaultFile_ variable to another class type like _String_. Then we can execute the _MethodByTypeResourceTest_ integration test again, and this time a _NoSuchBeanDefinitionException_ will be thrown.

The exception verifies that match-by-type was indeed used to resolve the _File_ dependency. The _NoSuchBeanDefinitionException_ confirms that the reference variable name doesn’t need to match the bean name. Instead, dependency resolution depends on the bean’s class type matching the reference variable’s class type.

#### **2.2.3. Match by Qualifier**

We will use the _MethodByQualifierResourceTest_ integration test to demonstrate the match-by-qualifier execution path:
    
    
    @RunWith(SpringJUnit4ClassRunner.class)
    @ContextConfiguration(
      loader=AnnotationConfigContextLoader.class,
      classes=ApplicationContextTestResourceQualifier.class)
    public class MethodByQualifierResourceIntegrationTest {
    
        private File arbDependency;
        private File anotherArbDependency;
    
        @Test
        public void givenResourceQualifier_WhenSetter_ThenValidDependencies(){
          assertNotNull(arbDependency);
            assertEquals("namedFile.txt", arbDependency.getName());
            assertNotNull(anotherArbDependency);
            assertEquals("defaultFile.txt", anotherArbDependency.getName());
        }
    
        @Resource
        @Qualifier("namedFile")
        public void setArbDependency(File arbDependency) {
            this.arbDependency = arbDependency;
        }
    
        @Resource
        @Qualifier("defaultFile")
        public void setAnotherArbDependency(File anotherArbDependency) {
            this.anotherArbDependency = anotherArbDependency;
        }
    }

Our test demonstrates that even if we define multiple bean implementations of a particular type in an application context, we can use a _@Qualifier_ annotation together with the _@Resource_ annotation to resolve a dependency.

Similar to field-based dependency injection, if we define multiple beans in an application context, we must use a  _@Qualifier_ annotation to specify which bean to use to resolve dependencies, or a _NoUniqueBeanDefinitionException_ will be thrown.

## **3\. The _@Inject_ Annotation**

The _@Inject_ annotation belongs to the [JSR-330](https://jcp.org/en/jsr/detail?id=330) annotations collection. This annotation has the following execution paths, listed by precedence:

  1. Match by Type
  2. Match by Qualifier
  3. Match by Name



These execution paths are applicable to both setter and field injection. In order for us to access the _@Inject_ annotation, we have to declare the _javax.inject_ library as a Gradle or Maven dependency.

For Gradle:
    
    
    testCompile group: 'javax.inject', name: 'javax.inject', version: '1'

For Maven:
    
    
    <dependency>
        <groupId>javax.inject</groupId>
        <artifactId>javax.inject</artifactId>
        <version>1</version>
    </dependency>

### **3.1. Field Injection**

#### **3.1.1. Match by Type**

We’ll modify the integration test example to use another type of dependency, namely the _ArbitraryDependency_ class. The _ArbitraryDependency_ class dependency merely serves as a simple dependency and holds no further significance:
    
    
    @Component
    public class ArbitraryDependency {
    
        private final String label = "Arbitrary Dependency";
    
        public String toString() {
            return label;
        }
    }

Here’s the _FieldInjectTest_ integration test in question:
    
    
    @RunWith(SpringJUnit4ClassRunner.class)
    @ContextConfiguration(
      loader=AnnotationConfigContextLoader.class,
      classes=ApplicationContextTestInjectType.class)
    public class FieldInjectIntegrationTest {
    
        @Inject
        private ArbitraryDependency fieldInjectDependency;
    
        @Test
        public void givenInjectAnnotation_WhenOnField_ThenValidDependency(){
            assertNotNull(fieldInjectDependency);
            assertEquals("Arbitrary Dependency",
              fieldInjectDependency.toString());
        }
    }

Unlike the _@Resource_ annotation, which resolves dependencies by name first, the default behavior of the _@Inject_ annotation is to resolve dependencies by type.

This means that even if the class reference variable name differs from the bean name, the dependency will still be resolved, provided that the bean is defined in the application context. Note how the reference variable name in the following test:
    
    
    @Inject
    private ArbitraryDependency fieldInjectDependency;

differs from the bean name configured in the application context:
    
    
    @Bean
    public ArbitraryDependency injectDependency() {
        ArbitraryDependency injectDependency = new ArbitraryDependency();
        return injectDependency;
    }

When we execute the test, we’re able to resolve the dependency.

#### **3.1.2. Match by Qualifier**

What if there are multiple implementations of a particular class type, and a certain class requires a specific bean? Let’s modify the integration testing example so that it requires another dependency.

In this example, we subclass the _ArbitraryDependency_ class, used in the match-by-type example, to create the _AnotherArbitraryDependency_ class:
    
    
    public class AnotherArbitraryDependency extends ArbitraryDependency {
    
        private final String label = "Another Arbitrary Dependency";
    
        public String toString() {
            return label;
        }
    }

The objective of each test case is to ensure that we inject each dependency correctly into each reference variable:
    
    
    @Inject
    private ArbitraryDependency defaultDependency;
    
    @Inject
    private ArbitraryDependency namedDependency;

We can use the _FieldQualifierInjectTest_ integration test to demonstrate match by qualifier:
    
    
    @RunWith(SpringJUnit4ClassRunner.class)
    @ContextConfiguration(
      loader=AnnotationConfigContextLoader.class,
      classes=ApplicationContextTestInjectQualifier.class)
    public class FieldQualifierInjectIntegrationTest {
    
        @Inject
        private ArbitraryDependency defaultDependency;
    
        @Inject
        private ArbitraryDependency namedDependency;
    
        @Test
        public void givenInjectQualifier_WhenOnField_ThenDefaultFileValid(){
            assertNotNull(defaultDependency);
            assertEquals("Arbitrary Dependency",
              defaultDependency.toString());
        }
    
        @Test
        public void givenInjectQualifier_WhenOnField_ThenNamedFileValid(){
            assertNotNull(defaultDependency);
            assertEquals("Another Arbitrary Dependency",
              namedDependency.toString());
        }
    }

If we have multiple implementations of a particular class in an application context, and the _FieldQualifierInjectTest_ integration test attempts to inject the dependencies in the manner listed below, a _NoUniqueBeanDefinitionException_ will be thrown:
    
    
    @Inject 
    private ArbitraryDependency defaultDependency;
    
    @Inject 
    private ArbitraryDependency namedDependency;

Throwing this exception is the Spring Framework’s way of pointing out that there are multiple implementations of a certain class and it is confused about which one to use. In order to elucidate the confusion, we can go to line 7 and 10 of the _FieldQualifierInjectTest_ integration test:
    
    
    @Inject
    private ArbitraryDependency defaultDependency;
    
    @Inject
    private ArbitraryDependency namedDependency;

We can pass the required bean name to the _@Qualifier_ annotation, which we use together with the _@Inject_ annotation. This is how the code block will now look:
    
    
    @Inject
    @Qualifier("defaultFile")
    private ArbitraryDependency defaultDependency;
    
    @Inject
    @Qualifier("namedFile")
    private ArbitraryDependency namedDependency;

The _@Qualifier_ annotation expects a strict match when receiving a bean name. We must ensure that the bean name is passed to the _Qualifier_ correctly, otherwise, a _NoUniqueBeanDefinitionException_ will be thrown. If we run the test again, it should pass.

#### **3.1.3. Match by Name**

The _FieldByNameInjectTest_ integration test used to demonstrate match by name is similar to the match by type execution path. The only difference is now we require a specific bean, as opposed to a specific type. In this example, we subclass the _ArbitraryDependency_ class again to produce the _YetAnotherArbitraryDependency_ class:
    
    
    public class YetAnotherArbitraryDependency extends ArbitraryDependency {
    
        private final String label = "Yet Another Arbitrary Dependency";
    
        public String toString() {
            return label;
        }
    }

In order to demonstrate the match-by-name execution path, we will use the following integration test:
    
    
    @RunWith(SpringJUnit4ClassRunner.class)
    @ContextConfiguration(
      loader=AnnotationConfigContextLoader.class,
      classes=ApplicationContextTestInjectName.class)
    public class FieldByNameInjectIntegrationTest {
    
        @Inject
        @Named("yetAnotherFieldInjectDependency")
        private ArbitraryDependency yetAnotherFieldInjectDependency;
    
        @Test
        public void givenInjectQualifier_WhenSetOnField_ThenDependencyValid(){
            assertNotNull(yetAnotherFieldInjectDependency);
            assertEquals("Yet Another Arbitrary Dependency",
              yetAnotherFieldInjectDependency.toString());
        }
    }

We list the application context:
    
    
    @Configuration
    public class ApplicationContextTestInjectName {
    
        @Bean
        public ArbitraryDependency yetAnotherFieldInjectDependency() {
            ArbitraryDependency yetAnotherFieldInjectDependency =
              new YetAnotherArbitraryDependency();
            return yetAnotherFieldInjectDependency;
        }
    }

If we run the integration test, it will pass.

In order to verify that we injected the dependency by the match-by-name execution path, we need to change the value, _yetAnotherFieldInjectDependency_ , that was passed in to the _@Named_ annotation to another name of our choice. When we run the test again, a _NoSuchBeanDefinitionException_ will be thrown.

### **3.2. Setter Injection**

Setter-based injection for the _@Inject_ annotation is similar to the approach used for the _@Resource_ setter-based injection. Instead of annotating the reference variable, we annotate the corresponding setter method. The execution paths followed by field-based dependency injection also apply to setter based injection.

## **4\. The _@Autowired_ Annotation**

The behaviour of the _@Autowired_ annotation is similar to the _@Inject_ annotation. The only difference is that the _@Autowired_ annotation is part of the Spring framework. This annotation has the same execution paths as the _@Inject_ annotation, listed in order of precedence:

  1. Match by Type
  2. Match by Qualifier
  3. Match by Name



These execution paths are applicable to both setter and field injection.

### **4.1. Field Injection**

#### **4.1.1. Match by Type**

The integration testing example used to demonstrate the _@Autowired_ match-by-type execution path will be similar to the test used to demonstrate the _@Inject_ match-by-type execution path. We use the following _FieldAutowiredTest_ integration test to demonstrate match-by-type using the _@Autowired_ annotation:
    
    
    @RunWith(SpringJUnit4ClassRunner.class)
    @ContextConfiguration(
      loader=AnnotationConfigContextLoader.class,
      classes=ApplicationContextTestAutowiredType.class)
    public class FieldAutowiredIntegrationTest {
    
        @Autowired
        private ArbitraryDependency fieldDependency;
    
        @Test
        public void givenAutowired_WhenSetOnField_ThenDependencyResolved() {
            assertNotNull(fieldDependency);
            assertEquals("Arbitrary Dependency", fieldDependency.toString());
        }
    }

We list the application context for this integration test:
    
    
    @Configuration
    public class ApplicationContextTestAutowiredType {
    
        @Bean
        public ArbitraryDependency autowiredFieldDependency() {
            ArbitraryDependency autowiredFieldDependency =
              new ArbitraryDependency();
            return autowiredFieldDependency;
        }
    }

We use this integration test to demonstrate that match-by-type takes first precedence over the other execution paths. Notice the reference variable name on line 8 of the _FieldAutowiredTest_ integration test:
    
    
    @Autowired
    private ArbitraryDependency fieldDependency;

This is different than the bean name in the application context:
    
    
    @Bean
    public ArbitraryDependency autowiredFieldDependency() {
        ArbitraryDependency autowiredFieldDependency =
          new ArbitraryDependency();
        return autowiredFieldDependency;
    }

When we run the test, it should pass.

In order to confirm that the dependency was indeed resolved using the match-by-type execution path, we need to change the type of the _fieldDependency_ reference variable and run the integration test again. This time, the _FieldAutowiredTest_ integration test will fail, with a _NoSuchBeanDefinitionException_ being thrown. This verifies that we used match-by-type to resolve the dependency.

#### **4.1.2. Match by Qualifier**

What if we’re faced with a situation where we’ve defined multiple bean implementations in the application context:
    
    
    @Configuration
    public class ApplicationContextTestAutowiredQualifier {
    
        @Bean
        public ArbitraryDependency autowiredFieldDependency() {
            ArbitraryDependency autowiredFieldDependency =
              new ArbitraryDependency();
            return autowiredFieldDependency;
        }
    
        @Bean
        public ArbitraryDependency anotherAutowiredFieldDependency() {
            ArbitraryDependency anotherAutowiredFieldDependency =
              new AnotherArbitraryDependency();
            return anotherAutowiredFieldDependency;
        }
    }

If we execute the following _FieldQualifierAutowiredTest_ integration test, a _NoUniqueBeanDefinitionException_ will be thrown:
    
    
    @RunWith(SpringJUnit4ClassRunner.class)
    @ContextConfiguration(
      loader=AnnotationConfigContextLoader.class,
      classes=ApplicationContextTestAutowiredQualifier.class)
    public class FieldQualifierAutowiredIntegrationTest {
    
        @Autowired
        private ArbitraryDependency fieldDependency1;
    
        @Autowired
        private ArbitraryDependency fieldDependency2;
    
        @Test
        public void givenAutowiredQualifier_WhenOnField_ThenDep1Valid(){
            assertNotNull(fieldDependency1);
            assertEquals("Arbitrary Dependency", fieldDependency1.toString());
        }
    
        @Test
        public void givenAutowiredQualifier_WhenOnField_ThenDep2Valid(){
            assertNotNull(fieldDependency2);
            assertEquals("Another Arbitrary Dependency",
              fieldDependency2.toString());
        }
    }

The exception is due to the ambiguity caused by the two beans defined in the application context. The Spring Framework doesn’t know which bean dependency should be autowired to which reference variable. We can resolve this issue by adding the _@Qualifier_ annotation to lines 7 and 10 of the _FieldQualifierAutowiredTest_ integration test:
    
    
    @Autowired
    private FieldDependency fieldDependency1;
    
    @Autowired
    private FieldDependency fieldDependency2;

so that the code block looks as follows:
    
    
    @Autowired
    @Qualifier("autowiredFieldDependency")
    private FieldDependency fieldDependency1;
    
    @Autowired
    @Qualifier("anotherAutowiredFieldDependency")
    private FieldDependency fieldDependency2;

When we run the test again, it will pass.

#### **4.1.3. Match by Name**

We’ll use the same integration test scenario to demonstrate the match-by-name execution path using the _@Autowired_ annotation to inject a field dependency. When autowiring dependencies by name, the _@ComponentScan_ annotation must be used with the application context, _ApplicationContextTestAutowiredName_ :
    
    
    @Configuration
    @ComponentScan(basePackages={"com.baeldung.dependency"})
        public class ApplicationContextTestAutowiredName {
    }

We use the _@ComponentScan_ annotation to search packages for Java classes that have been annotated with the _@Component_ annotation. For example, in the application context, the _com.baeldung.dependency_ package will be scanned for classes that have been annotated with the _@Component_ annotation. In this scenario, the Spring Framework must detect the _ArbitraryDependency_ class, which has the _@Component_ annotation:
    
    
    @Component(value="autowiredFieldDependency")
    public class ArbitraryDependency {
    
        private final String label = "Arbitrary Dependency";
    
        public String toString() {
            return label;
        }
    }

The attribute value, _autowiredFieldDependency_ , passed into the _@Component_ annotation, tells the Spring Framework that the _ArbitraryDependency_ class is a component named _autowiredFieldDependency_. In order for the _@Autowired_ annotation to resolve dependencies by name, the component name must correspond with the field name defined in the _FieldAutowiredNameTest_ integration test; please refer to line 8:
    
    
    @RunWith(SpringJUnit4ClassRunner.class)
    @ContextConfiguration(
      loader=AnnotationConfigContextLoader.class,
      classes=ApplicationContextTestAutowiredName.class)
    public class FieldAutowiredNameIntegrationTest {
    
        @Autowired
        private ArbitraryDependency autowiredFieldDependency;
    
        @Test
        public void givenAutowired_WhenSetOnField_ThenDependencyResolved(){
            assertNotNull(autowiredFieldDependency);
            assertEquals("Arbitrary Dependency",
              autowiredFieldDependency.toString());
    	}
    }

When we run the _FieldAutowiredNameTest_ integration test, it will pass.

But how do we know that the _@Autowired_ annotation really did invoke the match-by-name execution path? We can change the name of the reference variable _autowiredFieldDependency_ to another name of our choice, then run the test again.

This time, the test will fail and a _NoUniqueBeanDefinitionException_ is thrown. A similar check would be to change the _@Component_ attribute value, _autowiredFieldDependency_ , to another value of our choice and run the test again. A _NoUniqueBeanDefinitionException_ will also be thrown.

This exception is proof that if we use an incorrect bean name, no valid bean will be found. That’s how we know the match-by-name execution path was invoked.

### **4.2. Setter Injection**

Setter-based injection for the _@Autowired_ annotation is similar to the approach demonstrated for the _@Resource_ setter-based injection. Instead of annotating the reference variable with the _@Inject_ annotation, we annotate the corresponding setter. The execution paths followed by field-based dependency injection also apply to setter-based injection.

## **5\. Applying These Annotations**

This raises the question of which annotation should be used and under what circumstances. The answer to these questions depends on the design scenario faced by the application in question, and how the developer wishes to leverage polymorphism based on the default execution paths of each annotation.

### **5.1. Application-Wide Use of Singletons Through Polymorphism**

If the design is such that application behaviors are based on implementations of an interface or an abstract class, and these behaviors are used throughout the application, then we can use either the _@Inject_ or _@Autowired_ annotation.

The benefit of this approach is that when we upgrade the application, or apply a patch in order to fix a bug, classes can be swapped out with minimal negative impact to the overall application behavior. In this scenario, the primary default execution path is match-by-type.

### **5.2. Fine-Grained Application Behavior Configuration Through Polymorphism**

If the design is such that the application has complex behavior, each behavior is based on different interfaces/abstract classes, and the usage of each of these implementations varies across the application, then we can use the _@Resource_ annotation. In this scenario, the primary default execution path is match-by-name.

### **5.3. Dependency Injection Should Be Handled Solely by the Jakarta EE Platform**

If there is a design mandate for all dependencies to be injected by the Jakarta EE Platform as opposed to Spring, then the choice is between the _@Resource_ annotation and the _@Inject_ annotation. We should narrow down the final decision between the two annotations based on which default execution path is required.

### **5.4. Dependency Injection Should Be Handled Solely by the Spring Framework**

If the mandate is for all dependencies to be handled by the Spring Framework, the only choice is the _@Autowired_ annotation.

### **5.5. Discussion Summary**

The table below summarizes our discussion.

Scenario | @Resource | @Inject | @Autowired  
---|---|---|---  
Application-wide use of singletons through polymorphism | ✗ | ✔ | ✔  
Fine-grained application behavior configuration through polymorphism | ✔ | ✗ | ✗  
Dependency injection should be handled solely by the Jakarta EE platform | ✔ | ✔ | ✗  
Dependency injection should be handled solely by the Spring Framework | ✗ | ✗ | ✔  
  
## **6\. Conclusion**

In this article, we aimed to provide a deeper insight into the behavior of each annotation. Understanding how each annotation behaves will contribute to better overall application design and maintenance.
