# How to Make a Deep Copy of an Object in Java

## **1\. Introduction**

When we want to copy an object in Java, there are two possibilities that we need to consider, [a shallow copy and a deep copy](/cs/deep-vs-shallow-copy).

For the shallow copy approach, we only copy field values, therefore the copy might be dependant on the original object. In the deep copy approach, we make sure that all the objects in the tree are deeply copied, so the copy isn’t dependant on any earlier existing object that might ever change.

In this tutorial, we’ll compare these two approaches, and learn four methods to implement the deep copy.

## **2\. Maven Setup**

We’ll use three Maven dependencies, Gson, Jackson, and Apache Commons Lang, to test different ways of performing a deep copy.

Let’s add these dependencies to our _pom.xml_ :
    
    
    <dependency>
        <groupId>com.google.code.gson</groupId>
        <artifactId>gson</artifactId>
        <version>2.10.1</version>
    </dependency>
    <dependency>
        <groupId>org.apache.commons</groupId>
        <artifactId>commons-lang3</artifactId>
        <version>3.14.0</version>
    </dependency>
    <dependency>
        <groupId>com.fasterxml.jackson.core</groupId>
        <artifactId>jackson-databind</artifactId>
        <version>2.17.2</version>
    </dependency>

The latest versions of [Gson](https://mvnrepository.com/artifact/com.google.code.gson/gson), [Jackson](https://mvnrepository.com/artifact/com.fasterxml.jackson.core/jackson-databind), and [Apache Commons Lang](https://mvnrepository.com/artifact/commons-lang/commons-lang) can be found on Maven Central.

## **3\. Model**

To compare different methods of copying Java objects, we’ll need two classes to work on:
    
    
    class Address {
    
        private String street;
        private String city;
        private String country;
    
        // standard constructors, getters and setters
    }
    
    
    class User {
    
        private String firstName;
        private String lastName;
        private Address address;
    
        // standard constructors, getters and setters
    }

## **4\. Shallow Copy**

A shallow copy is one in which **we only copy values of fields** from one object to another:
    
    
    @Test
    public void whenShallowCopying_thenObjectsShouldNotBeSame() {
    
        Address address = new Address("Downing St 10", "London", "England");
        User pm = new User("Prime", "Minister", address);
        
        User shallowCopy = new User(
          pm.getFirstName(), pm.getLastName(), pm.getAddress());
    
        assertThat(shallowCopy)
          .isNotSameAs(pm);
    }

In this case, _pm != shallowCopy_ , which means that **they’re different objects; however, the problem is that when we change any of the original _address’_ properties, this will also affect the _shallowCopy_ ‘s address**.

We wouldn’t bother with it if _Address_ was immutable, but it’s not:
    
    
    @Test
    public void whenModifyingOriginalObject_ThenCopyShouldChange() {
     
        Address address = new Address("Downing St 10", "London", "England");
        User pm = new User("Prime", "Minister", address);
        User shallowCopy = new User(
          pm.getFirstName(), pm.getLastName(), pm.getAddress());
    
        address.setCountry("Great Britain");
        assertThat(shallowCopy.getAddress().getCountry())
          .isEqualTo(pm.getAddress().getCountry());
    }

## **5\. Deep Copy**

A deep copy is an alternative that solves this problem. Its advantage is that **each mutable object in the object graph is recursively copied**.

Since the copy isn’t dependent on any mutable object that was created earlier, it won’t get modified by accident like we saw with the shallow copy.

In the following sections, we’ll discuss several deep copy implementations and demonstrate this advantage.

### **5.1. Copy Constructor**

The first implementation we’ll examine is based on copy constructors:
    
    
    public Address(Address that) {
        this(that.getStreet(), that.getCity(), that.getCountry());
    }
    
    
    public User(User that) {
        this(that.getFirstName(), that.getLastName(), new Address(that.getAddress()));
    }

In the above implementation of the deep copy, we haven’t created new _Strings_ in our copy constructor because _String_ is an immutable class.

As a result, they can’t be modified by accident. Let’s see if this works:
    
    
    @Test
    public void whenModifyingOriginalObject_thenCopyShouldNotChange() {
        Address address = new Address("Downing St 10", "London", "England");
        User pm = new User("Prime", "Minister", address);
        User deepCopy = new User(pm);
    
        address.setCountry("Great Britain");
        assertNotEquals(
          pm.getAddress().getCountry(), 
          deepCopy.getAddress().getCountry());
    }

### **5.2. Cloneable Interface**

The second implementation is based on the clone method inherited from _Object_. It’s protected, but we need to override it as _public_.

We’ll also add a marker interface, _Cloneable,_ to the classes to indicate that the classes are actually cloneable.

Let’s add the _clone()_ method to the _Address_ class:
    
    
    @Override
    public Object clone() {
        try {
            return (Address) super.clone();
        } catch (CloneNotSupportedException e) {
            return new Address(this.street, this.getCity(), this.getCountry());
        }
    }

Now let’s implement _clone()_ for the _User_ class:
    
    
    @Override
    public Object clone() {
        User user = null;
        try {
            user = (User) super.clone();
        } catch (CloneNotSupportedException e) {
            user = new User(
              this.getFirstName(), this.getLastName(), this.getAddress());
        }
        user.address = (Address) this.address.clone();
        return user;
    }

**Note that the _super.clone()_ call returns a shallow copy of an object, but we set deep copies of mutable fields manually, so the result is correct:**
    
    
    @Test
    public void whenModifyingOriginalObject_thenCloneCopyShouldNotChange() {
        Address address = new Address("Downing St 10", "London", "England");
        User pm = new User("Prime", "Minister", address);
        User deepCopy = (User) pm.clone();
    
        address.setCountry("Great Britain");
    
        assertThat(deepCopy.getAddress().getCountry())
          .isNotEqualTo(pm.getAddress().getCountry());
    }

## **6\. External Libraries**

The above examples look easy, but sometimes they don’t work as a solution **when we can’t add an additional constructor or override the clone method**.

This might happen when we don’t own the code, or when the object graph is so complicated that we wouldn’t finish our project on time if we focused on writing additional constructors or implementing the _clone_ method on all classes in the object graph.

So what can we do then? In that case, we can use an external library. To achieve a deep copy, **we can serialize an object and then deserialize it to a new object**.

Let’s look at a few examples.

### **6.1. Apache Commons Lang**

Apache Commons Lang has _SerializationUtils#clone,_ which performs a deep copy when all classes in the object graph implement the _Serializable_ interface.

**If the method encounters a class that isn’t serializable, it’ll fail and throw an unchecked _SerializationException_.**

Consequently, we need to add the _Serializable_ interface to our classes:
    
    
    @Test
    public void whenModifyingOriginalObject_thenCommonsCloneShouldNotChange() {
        Address address = new Address("Downing St 10", "London", "England");
        User pm = new User("Prime", "Minister", address);
        User deepCopy = (User) SerializationUtils.clone(pm);
    
        address.setCountry("Great Britain");
    
        assertThat(deepCopy.getAddress().getCountry())
          .isNotEqualTo(pm.getAddress().getCountry());
    }

### **6.2. JSON Serialization With Gson**

The other way to serialize is to use JSON serialization. Gson is a library that’s used for converting objects into JSON and vice versa.

Unlike Apache Commons Lang, **GSON does not need the _Serializable_ interface to make the conversions**. Additionally, _[transient](/java-transient-keyword)_ fields are not permitted with Gson.

Let’s have a quick look at an example:
    
    
    @Test
    public void whenModifyingOriginalObject_thenGsonCloneShouldNotChange() {
        Address address = new Address("Downing St 10", "London", "England");
        User pm = new User("Prime", "Minister", address);
        Gson gson = new Gson();
        User deepCopy = gson.fromJson(gson.toJson(pm), User.class);
    
        address.setCountry("Great Britain");
    
        assertThat(deepCopy.getAddress().getCountry())
          .isNotEqualTo(pm.getAddress().getCountry());
    }

### **6.3. JSON Serialization With Jackson**

Jackson is another library that supports JSON serialization. This implementation will be very similar to the one using Gson, but **we need to add the default constructor to our classes**.

Let’s see an example:
    
    
    @Test
    public void whenModifyingOriginalObject_thenJacksonCopyShouldNotChange() 
      throws IOException {
        Address address = new Address("Downing St 10", "London", "England");
        User pm = new User("Prime", "Minister", address);
        ObjectMapper objectMapper = new ObjectMapper();
        
        User deepCopy = objectMapper
          .readValue(objectMapper.writeValueAsString(pm), User.class);
    
        address.setCountry("Great Britain");
    
        assertThat(deepCopy.getAddress().getCountry())
          .isNotEqualTo(pm.getAddress().getCountry());
    }

## **7\. Conclusion**

Which implementation should we use when making a deep copy? The final decision will often depend on the classes we’ll copy, and whether we own the classes in the object graph.
