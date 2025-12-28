# Override Properties in Spring’s Tests

## 1\. Overview

In this tutorial, we’ll look at various ways to override the properties in Spring’s tests.

Spring actually provides a number of solutions for this, so we have quite a bit to explore here.

## 2\. Dependencies

Of course, in order to work with Spring tests, we need to add a test dependency:
    
    
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-test</artifactId>
        <scope>test</scope>
    </dependency>

This dependency also includes JUnit 5 for us.

## 3\. Setup

First, we’ll create a class in the application that will use our properties:
    
    
    @Component
    public class PropertySourceResolver {
    
        @Value("${example.firstProperty}") private String firstProperty;
        @Value("${example.secondProperty}") private String secondProperty;
    
        public String getFirstProperty() {
            return firstProperty;
        }
    
        public String getSecondProperty() {
            return secondProperty;
        }
    }

Next, we’ll assign values to them. We can do this by creating the _application.properties_ in the  _src/main/resources:_
    
    
    example.firstProperty=defaultFirst
    example.secondProperty=defaultSecond

## 4\. Overriding a Property File

Now we’ll override properties by putting the property file in the test resources. **This file must be** **on the same classpath** as the default one.

Additionally, it should **contain all the property keys** specified in the default file. Therefore, we’ll add the _application.properties_ file into the _src/test/resources_ :
    
    
    example.firstProperty=file
    example.secondProperty=file

Let’s also add the test that will make use of our solution:
    
    
    @SpringBootTest
    public class TestResourcePropertySourceResolverIntegrationTest {
    
        @Autowired private PropertySourceResolver propertySourceResolver;
    
        @Test
        public void shouldTestResourceFile_overridePropertyValues() {
            String firstProperty = propertySourceResolver.getFirstProperty();
            String secondProperty = propertySourceResolver.getSecondProperty();
    
            assertEquals("file", firstProperty);
            assertEquals("file", secondProperty);
        }
    }

This method is very effective when we want to override multiple properties from the file.

And if we don’t put the _example.secondProperty_ in the file, the application context won’t discover this property.

## 5\. Spring Profiles

In this section, we’ll learn how to handle our issue by using Spring Profiles. **Unlike the previous method,** **this one merges properties from the default file and the profiled file**.

First, let’s create an _application**–** test.properties _file in the _src/test/resources:_
    
    
    example.firstProperty=profile

Then we’ll create a test that will use the _test_ profile:
    
    
    @SpringBootTest
    @ActiveProfiles("test")
    public class ProfilePropertySourceResolverIntegrationTest {
    
        @Autowired private PropertySourceResolver propertySourceResolver;
    
        @Test
        public void shouldProfiledProperty_overridePropertyValues() {
            String firstProperty = propertySourceResolver.getFirstProperty();
            String secondProperty = propertySourceResolver.getSecondProperty();
    
            assertEquals("profile", firstProperty);
            assertEquals("defaultSecond", secondProperty);
        }
    }

This approach allows us to use both default and test values. Therefore, this is a great method when we need to **override multiple properties from a file, but we still want to use the default** **ones too.**

We can learn more about Spring profiles in our [_Spring Profiles_](/spring-profiles) article.

## 6\. _@SpringBootTest_

Another way to override the property value is to use the _@SpringBootTest_ annotation:
    
    
    @SpringBootTest(properties = { "example.firstProperty=annotation" })
    public class SpringBootPropertySourceResolverIntegrationTest {
    
        @Autowired private PropertySourceResolver propertySourceResolver;
    
        @Test
        public void shouldSpringBootTestAnnotation_overridePropertyValues() {
            String firstProperty = propertySourceResolver.getFirstProperty();
            String secondProperty = propertySourceResolver.getSecondProperty();
    
            Assert.assertEquals("annotation", firstProperty);
            Assert.assertEquals("defaultSecond", secondProperty);
        }
    }

**As we can see,** **the _example.firstProperty_ has been overridden, while the _example.secondProperty_ hasn’t been**. Therefore, this is a great solution when we need to override only specific properties for the test. This is the only method that requires the use of Spring Boot.

## 7\. _TestPropertySourceUtils_

In this section, we’ll learn how to override properties by using the _TestPropertySourceUtils_ class in the _ApplicationContextInitializer._

The  _TestPropertySourceUtils_ comes with two methods that we can use to define a different property value.

Let’s create an initializer class that we’ll use in our test:
    
    
    public class PropertyOverrideContextInitializer
      implements ApplicationContextInitializer<ConfigurableApplicationContext> {
    
        static final String PROPERTY_FIRST_VALUE = "contextClass";
    
        @Override
        public void initialize(ConfigurableApplicationContext configurableApplicationContext) {
            TestPropertySourceUtils.addInlinedPropertiesToEnvironment(
              configurableApplicationContext, "example.firstProperty=" + PROPERTY_FIRST_VALUE);
    
            TestPropertySourceUtils.addPropertiesFilesToEnvironment(
              configurableApplicationContext, "context-override-application.properties");
        }
    }

Next, we’ll add the _context-override-application.properties_ file into _src/test/resources:_
    
    
    example.secondProperty=contextFile

Finally, we should create a test class that will use our initializer:
    
    
    @SpringBootTest
    @ContextConfiguration(
      initializers = PropertyOverrideContextInitializer.class,
      classes = Application.class)
    public class ContextPropertySourceResolverIntegrationTest {
    
        @Autowired private PropertySourceResolver propertySourceResolver;
    
        @Test
        public void shouldContext_overridePropertyValues() {
            final String firstProperty = propertySourceResolver.getFirstProperty();
            final String secondProperty = propertySourceResolver.getSecondProperty();
    
            assertEquals(PropertyOverrideContextInitializer.PROPERTY_FIRST_VALUE, firstProperty);
            assertEquals("contextFile", secondProperty);
        }
    }

The  _example.firstProperty_ has been overridden from the inlined method.

The _example.secondProperty_ has been overridden from the specific file in the second method. This approach allows us to define different property values when initializing the context.

## 8\. Conclusion

In this article, we focused on the multiple ways we can override properties in our tests. We also discussed when to use each solution, or in some cases, when to mix them.

Of course, we have [the _@TestPropertySource_ annotation](/spring-test-property-source) at our disposal as well.
