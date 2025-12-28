# Java Stream Filter with Lambda Expression

## **1\. Introduction**

In this quick tutorial, we’ll explore the use of the  _Stream.filter()_ method when we work with [_Streams_ in Java](/java-8-streams-introduction).

We’ll look at how to use it, and how to handle special cases with checked exceptions.

## **2\. Using _Stream.filter()_**

The _filter()_ method is an intermediate operation of the _Stream_ interface that allows us to filter elements of a stream that match a given _Predicate:_
    
    
    Stream<T> filter(Predicate<? super T> predicate)

To see how this works, let’s create a _Customer_ class:
    
    
    public class Customer {
        private String name;
        private int points;
        //Constructor and standard getters
    }

In addition, let’s create a collection of customers:
    
    
    Customer john = new Customer("John P.", 15);
    Customer sarah = new Customer("Sarah M.", 200);
    Customer charles = new Customer("Charles B.", 150);
    Customer mary = new Customer("Mary T.", 1);
    
    List<Customer> customers = Arrays.asList(john, sarah, charles, mary);

### **2.1. Filtering Collections**

A common use case of the  _filter()_ method is [processing collections](/java-collection-filtering).

Let’s make a list of customers with more than 100  _points._ To do that, we can use a lambda expression:
    
    
    List<Customer> customersWithMoreThan100Points = customers
      .stream()
      .filter(c -> c.getPoints() > 100)
      .collect(Collectors.toList());

We can also use a [method reference](/java-8-double-colon-operator), which is shorthand for a lambda expression:
    
    
    List<Customer> customersWithMoreThan100Points = customers
      .stream()
      .filter(Customer::hasOverHundredPoints)
      .collect(Collectors.toList());

In this case, we added the _hasOverHundredPoints_ method to our _Customer_ class:
    
    
    public boolean hasOverHundredPoints() {
        return this.points > 100;
    }

In both cases, we get the same result:
    
    
    assertThat(customersWithMoreThan100Points).hasSize(2);
    assertThat(customersWithMoreThan100Points).contains(sarah, charles);

### **2.2. Filtering Collections with Multiple Criteria**

Furthermore, we can use multiple conditions with _filter()_. For example, we can filter by _points_ and _name_ :
    
    
    List<Customer> charlesWithMoreThan100Points = customers
      .stream()
      .filter(c -> c.getPoints() > 100 && c.getName().startsWith("Charles"))
      .collect(Collectors.toList());
    
    assertThat(charlesWithMoreThan100Points).hasSize(1);
    assertThat(charlesWithMoreThan100Points).contains(charles);

## **3\. Handling Exceptions**

Until now, we’ve been using the filter with predicates that don’t throw an exception. Indeed, the **functional interfaces in Java don’t declare any checked or unchecked exceptions**.

Next we’re going to show some different ways to handle [exceptions in lambda expressions](/java-lambda-exceptions).

### **3.1. Using a Custom Wrapper**

First, we’ll start by adding a _profilePhotoUrl_ to our _Customer_ _:_
    
    
    private String profilePhotoUrl;

In addition, let’s add a simple  _hasValidProfilePhoto()_ method to check the availability of the profile:
    
    
    public boolean hasValidProfilePhoto() throws IOException {
        URL url = new URL(this.profilePhotoUrl);
        HttpsURLConnection connection = (HttpsURLConnection) url.openConnection();
        return connection.getResponseCode() == HttpURLConnection.HTTP_OK;
    }

We can see that the  _hasValidProfilePhoto()_ method throws an  _IOException_. Now if we try to filter the customers with this method:
    
    
    List<Customer> customersWithValidProfilePhoto = customers
      .stream()
      .filter(Customer::hasValidProfilePhoto)
      .collect(Collectors.toList());

We’ll see the following error:
    
    
    Incompatible thrown types java.io.IOException in functional expression

To handle it, one of the alternatives we can use is wrapping it with a try-catch block:
    
    
    List<Customer> customersWithValidProfilePhoto = customers
      .stream()
      .filter(c -> {
          try {
              return c.hasValidProfilePhoto();
          } catch (IOException e) {
              //handle exception
          }
          return false;
      })
      .collect(Collectors.toList());

If we need to throw an exception from our predicate, we can wrap it in an unchecked exception like _RuntimeException_.

### **3.2. Using ThrowingFunction**

Alternatively, we can use the ThrowingFunction library.

ThrowingFunction is an open source library that allows us to handle checked exceptions in Java functional interfaces.

Let’s start by adding the [_throwing-function_ dependency](https://mvnrepository.com/artifact/com.pivovarit/throwing-function/1.5.1) to our pom:
    
    
    <dependency>	
        <groupId>com.pivovarit</groupId>	
        <artifactId>throwing-function</artifactId>	
        <version>1.5.1</version>	
    </dependency>

To handle exceptions in predicates, this library offers us the _ThrowingPredicate_ class, which has the _unchecked()_ method to wrap checked exceptions.

Let’s see it in action:
    
    
    List customersWithValidProfilePhoto = customers
      .stream()
      .filter(ThrowingPredicate.unchecked(Customer::hasValidProfilePhoto))
      .collect(Collectors.toList());

## **4\. Conclusion**

In this article, we saw an example of how to use the  _filter()_ method to process streams. We also explored some alternatives to handle exceptions.
