# A Quick Guide to Spring @Value

## 1\. Overview

In this quick tutorial, we’re going to **have a look at the _@Value_ Spring annotation.**

This annotation can be used for injecting values into fields in Spring-managed beans, and it can be applied at the field or constructor/method parameter level.

## 2\. Setting Up the Application

To describe different kinds of usage for this annotation, we need to configure a simple Spring application configuration class.

Naturally, **we’ll need a properties file** to define the values we want to inject with the _@Value_ annotation. And so, we’ll first need to define a _@PropertySource_ in our configuration class — with the properties file name.

Let’s define the properties file:
    
    
    value.from.file=Value got from the file
    priority=high
    listOfValues=A,B,C

## 3\. Usage Examples

As a basic and mostly useless example, we can only inject “string value” from the annotation to the field:
    
    
    @Value("string value")
    private String stringValue;

Using the _@PropertySource_ annotation allows us to work with values from properties files with the _@Value_ annotation.

In the following example, we get _Value got from the file_ assigned to the field:
    
    
    @Value("${value.from.file}")
    private String valueFromFile;

We can also set the value from system properties with the same syntax.

Let’s assume that we have defined a system property named _systemValue_ :
    
    
    @Value("${systemValue}")
    private String systemValue;

Default values can be provided for properties that might not be defined. Here, the value _some default_ will be injected:
    
    
    @Value("${unknown.param:some default}")
    private String someDefault;

If the same property is defined as a system property and in the properties file, then the system property would be applied.

Suppose we had a property _priority_ defined as a system property with the value _System property_ and defined as something else in the properties file. The value would be _System property_ :
    
    
    @Value("${priority}")
    private String prioritySystemProperty;

Sometimes, we need to inject a bunch of values. It would be convenient to define them as comma-separated values for the single property in the properties file or as a system property and to inject into an array.

In the first section, we defined comma-separated values in the _listOfValues_ of the properties file _,_ so the array values would be _[“A”, “B”, “C”]:_
    
    
    @Value("${listOfValues}")
    private String[] valuesArray;

## 4\. Advanced Examples With SpEL

We can also use SpEL expressions to get the value.

If we have a system property named _priority,_ then its value will be applied to the field:
    
    
    @Value("#{systemProperties['priority']}")
    private String spelValue;

If we have not defined the system property, then the _null_ value will be assigned.

To prevent this, we can provide a default value in the SpEL expression. We get _some default_ value for the field if the system property is not defined:
    
    
    @Value("#{systemProperties['unknown'] ?: 'some default'}")
    private String spelSomeDefault;

Furthermore, we can use a field value from other beans. Suppose we have a bean named _someBean_ with a field _someValue_ equal to _10_. Then, _10_ will be assigned to the field:
    
    
    @Value("#{someBean.someValue}")
    private Integer someBeanValue;

We can manipulate properties to get a _List_ of values, here, a list of string values A, B, and C:
    
    
    @Value("#{'${listOfValues}'.split(',')}")
    private List<String> valuesList;

## 5\. Using _@Value_ With _Maps_

We can also use the _@Value_ annotation to inject a _Map_ property.

First, we’ll need to define the property in the _{key: ‘value’ }_ form in our properties file:
    
    
    valuesMap={key1: '1', key2: '2', key3: '3'}

**Note that the values in the _Map_ must be in single quotes.**

Now we can inject this value from the property file as a _Map_ :
    
    
    @Value("#{${valuesMap}}")
    private Map<String, Integer> valuesMap;

If we need **to get the value of a specific key** in the _Map_ , all we have to do is **add the key’s name in the expression** :
    
    
    @Value("#{${valuesMap}.key1}")
    private Integer valuesMapKey1;

If we’re not sure whether the _Map_ contains a certain key, we should choose **a safer expression that will not throw an exception but set the value to _null_** when the key is not found:
    
    
    @Value("#{${valuesMap}['unknownKey']}")
    private Integer unknownMapKey;

We can also **set default values for the properties or keys that might not exist** :
    
    
    @Value("#{${unknownMap : {key1: '1', key2: '2'}}}")
    private Map<String, Integer> unknownMap;
    
    @Value("#{${valuesMap}['unknownKey'] ?: 5}")
    private Integer unknownMapKeyWithDefaultValue;

**_Map_ entries can also be filtered** before injection.

Let’s assume we need to get only those entries whose values are greater than one:
    
    
    @Value("#{${valuesMap}.?[value>'1']}")
    private Map<String, Integer> valuesMapFiltered;

We can also use the _@Value_ annotation to **inject all current system properties** :
    
    
    @Value("#{systemProperties}")
    private Map<String, String> systemPropertiesMap;

## 6\. Using _@Value_ With Constructor Injection

When we use the _@Value_ annotation, we’re not limited to a field injection. **We can also use it together with constructor injection.**

Let’s see this in practice:
    
    
    @Component
    @PropertySource("classpath:values.properties")
    public class PriorityProvider {
    
        private String priority;
    
        @Autowired
        public PriorityProvider(@Value("${priority:normal}") String priority) {
            this.priority = priority;
        }
    
        // standard getter
    }

In the above example, we inject a _priority_ directly into our _PriorityProvider_ ‘s constructor.

Note that we also provide a default value in case the property isn’t found.

## 7\. Using _@Value_ With Setter Injection

Analogous to the constructor injection, **we can also use _@Value_ with setter injection.**

Let’s take a look:
    
    
    @Component
    @PropertySource("classpath:values.properties")
    public class CollectionProvider {
    
        private List<String> values = new ArrayList<>();
    
        @Autowired
        public void setValues(@Value("#{'${listOfValues}'.split(',')}") List<String> values) {
            this.values.addAll(values);
        }
    
        // standard getter
    }

We use the SpEL expression to inject a list of values into the _setValues_ method.

## 8\. Using _@Value_ With Records

Java 14 introduced [records](/java-record-keyword) to facilitate the creation of an immutable class. **The Spring framework supports _@Value_ for record injection since version 6.0.6:**
    
    
    @Component
    @PropertySource("classpath:values.properties")
    public record PriorityRecord(@Value("${priority:normal}") String priority) {}

Here, we inject the value directly into the record’s constructor.

## 9\. Conclusion

In this article, we examined the various possibilities of using the _@Value_ annotation with simple properties defined in the file, with system properties, and with properties calculated with SpEL expressions.
