# A Guide to Java HashMap

## 1\. Overview

**In this tutorial, we’ll see how to use _HashMap_ in Java, and we’ll look at how it works internally.**

A class very similar to _HashMap_ is _Hashtable_. Please refer to a couple of our other articles to learn more about the [_java.util.Hashtable_ class](/java-hash-table) itself and the [differences between _HashMap_ and _Hashtable_](/hashmap-hashtable-differences).

## 2\. Basic Usage

Let’s first look at what it means that _HashMap_ is a map. **A map is a key-value mapping, which means that every key is mapped to exactly one value and that we can use the key to retrieve the corresponding value from a map.**

One might ask why not simply add the value to a list. Why do we need a _HashMap_? The simple reason is performance. If we want to find a specific element in a list, the time complexity is _O(n)_ and if the list is sorted, it will be _O(log n)_ using, for example, a binary search.

The advantage of a _HashMap_ is that the time complexity to insert and retrieve a value is _O(1)_ on average. We’ll look at how that can be achieved later. Let’s first look at how to use _HashMap_.

### 2.1. Setup

Let’s create a simple class that we’ll use throughout the article:
    
    
    public class Product {
    
        private String name;
        private String description;
        private List<String> tags;
        
        // standard getters/setters/constructors
    
        public Product addTagsOfOtherProduct(Product product) {
            this.tags.addAll(product.getTags());
            return this;
        }
    }

### 2.2. Put

We can now create a _HashMap_ with the key of type _String_ and elements of type _Product_ :
    
    
    Map<String, Product> productsByName = new HashMap<>();
    

And add products to our _HashMap_ :
    
    
    Product eBike = new Product("E-Bike", "A bike with a battery");
    Product roadBike = new Product("Road bike", "A bike for competition");
    productsByName.put(eBike.getName(), eBike);
    productsByName.put(roadBike.getName(), roadBike);
    

### 2.3. Get

We can **retrieve a value from the map by its key:**
    
    
    Product nextPurchase = productsByName.get("E-Bike");
    assertEquals("A bike with a battery", nextPurchase.getDescription());

If we try to find a value for a key that doesn’t exist in the map, we’ll get a _null_ value:
    
    
    Product nextPurchase = productsByName.get("Car");
    assertNull(nextPurchase);

And if we insert a second value with the same key, we’ll only get the last inserted value for that key:
    
    
    Product newEBike = new Product("E-Bike", "A bike with a better battery");
    productsByName.put(newEBike.getName(), newEBike);
    assertEquals("A bike with a better battery", productsByName.get("E-Bike").getDescription());

### 2.4. Null as the Key

_HashMap_ also allows us to have _null_ as a key:
    
    
    Product defaultProduct = new Product("Chocolate", "At least buy chocolate");
    productsByName.put(null, defaultProduct);
    
    Product nextPurchase = productsByName.get(null);
    assertEquals("At least buy chocolate", nextPurchase.getDescription());

### 2.5. Values with the Same Key

Furthermore, we can insert the same object twice with a different key:
    
    
    productsByName.put(defaultProduct.getName(), defaultProduct);
    assertSame(productsByName.get(null), productsByName.get("Chocolate"));

### 2.6. Remove a Value

We can remove a key-value mapping from the _HashMap_ :
    
    
    productsByName.remove("E-Bike");
    assertNull(productsByName.get("E-Bike"));

### 2.7. Check If a Key or Value Exists in the Map

To check if a key is present in the map, we can use the _containsKey()_ method:
    
    
    productsByName.containsKey("E-Bike");

Or, to check if a value is present in the map, we can use the _containsValue()_ method:
    
    
    productsByName.containsValue(eBike);

Both method calls will return _true_ in our example. Though they look very similar, there is an important difference in performance between these two method calls.**The complexity to check if a key exists is _O(1)_ , while the complexity to check for an element is _O(n),_ as it’s necessary to loop over all the elements in the map.**

### 2.8. Iterating Over a _HashMap_

There are **three basic ways to iterate over all key-value pairs** in a _HashMap_.

We can iterate over the set of all keys:
    
    
    for(String key : productsByName.keySet()) {
        Product product = productsByName.get(key);
    }

Or we can iterate over the set of all entries:
    
    
    for(Map.Entry<String, Product> entry : productsByName.entrySet()) {
        Product product =  entry.getValue();
        String key = entry.getKey();
        //do something with the key and value
    }

Finally, we can iterate over all values:
    
    
    List<Product> products = new ArrayList<>(productsByName.values());

## 3\. The Key

**We can use any class as the key in our _HashMap_. However, for the map to work properly, we need to provide an implementation for _equals()_ and **_**hashCode().** _Let’s say we want to have a map with the product as the key and the price as the value:
    
    
    HashMap<Product, Integer> priceByProduct = new HashMap<>();
    priceByProduct.put(eBike, 900);

Let’s implement the _equals()_ and _hashCode()_ methods:
    
    
    @Override
    public boolean equals(Object o) {
        if (this == o) {
            return true;
        }
        if (o == null || getClass() != o.getClass()) {
            return false;
        }
    
        Product product = (Product) o;
        return Objects.equals(name, product.name) &&
          Objects.equals(description, product.description);
    }
    
    @Override
    public int hashCode() {
        return Objects.hash(name, description);
    }

**Note that _hashCode()_ and _equals()_ need to be overridden only for classes that we want to use as map keys, not for classes that are only used as values in a map.** We’ll see why this is necessary in section 5 of this article.

## 4\. Additional Methods as of Java 8

Java 8 added several functional-style methods to _HashMap_. In this section, we’ll look at some of these methods.

**For each method, we’ll look at two examples.** The first example shows how to use the new method, and the second example shows how to achieve the same in earlier versions of Java.

As these methods are quite straightforward, we won’t look at more detailed examples.

### 4.1. _forEach()_

The _forEach_ method is the functional-style way to iterate over all elements in the map:
    
    
    productsByName.forEach( (key, product) -> {
        System.out.println("Key: " + key + " Product:" + product.getDescription());
        //do something with the key and value
    });
    

Prior to Java 8:
    
    
    for(Map.Entry<String, Product> entry : productsByName.entrySet()) {
        Product product =  entry.getValue();
        String key = entry.getKey();
        //do something with the key and value
    }

Our article [Guide to the Java 8 _forEach_](/foreach-java) covers the _forEach_ loop in greater detail.

### 4.2. _getOrDefault()_

Using the _getOrDefault()_ method, we can get a value from the map or return a default element in case there is no mapping for the given key:
    
    
    Product chocolate = new Product("chocolate", "something sweet");
    Product defaultProduct = productsByName.getOrDefault("horse carriage", chocolate); 
    Product bike = productsByName.getOrDefault("E-Bike", chocolate);

Prior to Java 8:
    
    
    Product bike2 = productsByName.containsKey("E-Bike") 
        ? productsByName.get("E-Bike") 
        : chocolate;
    Product defaultProduct2 = productsByName.containsKey("horse carriage") 
        ? productsByName.get("horse carriage") 
        : chocolate;
    

### 4.3. _putIfAbsent()_

With this method, we can add a new mapping, but only if there is not yet a mapping for the given key:
    
    
    productsByName.putIfAbsent("E-Bike", chocolate);
    

Prior to Java 8:
    
    
    if(!productsByName.containsKey("E-Bike")) {
        productsByName.put("E-Bike", chocolate);
    }

Our article [Merging Two Maps with Java 8](/java-merge-maps) takes a closer look at this method.

### 4.4. _merge()_

And with _[merge()](/java-merge-maps),_ we can modify the value for a given key if a mapping exists, or add a new value otherwise:
    
    
    Product eBike2 = new Product("E-Bike", "A bike with a battery");
    eBike2.getTags().add("sport");
    productsByName.merge("E-Bike", eBike2, Product::addTagsOfOtherProduct);

Prior to Java 8:
    
    
    if(productsByName.containsKey("E-Bike")) {
        productsByName.get("E-Bike").addTagsOfOtherProduct(eBike2);
    } else {
        productsByName.put("E-Bike", eBike2);
    }
    

### 4.5. _compute()_

With the _compute()_ method, we can compute the value for a given key:
    
    
    productsByName.compute("E-Bike", (k,v) -> {
        if(v != null) {
            return v.addTagsOfOtherProduct(eBike2);
        } else {
            return eBike2;
        }
    });

Prior to Java 8:
    
    
    if(productsByName.containsKey("E-Bike")) {    
        productsByName.get("E-Bike").addTagsOfOtherProduct(eBike2); 
    } else {
        productsByName.put("E-Bike", eBike2); 
    }
    

It’s worth noting that the **methods _merge()_ and _compute()_ are quite similar.** The _compute() method_ accepts two arguments: the _key_ and a _BiFunction_ for the remapping. And _merge()_ accepts three parameters: the _key_ , a _default value_ to add to the map if the key doesn’t exist yet, and a _BiFunction_ for the remapping.

## 5\. How to Avoid Casting _HashMap <String, Object>_ Value

The _java.util.HashMap <K,V>_ class is a hash table based implementation of the _Map_ interface. Let’s discuss how we can avoid casting an instance of type _HashMap <String, Object>_.

### 5.1. When We Need Casting

First, let’s introduce when we need casting. Consider the _Product_ class example. When creating a collection of _Product_ s using a _HashMap_ we’ve got the option of initializing the collection using _HashMap <String, Object>_:
    
    
    HashMap<String,Object> objectMap  = new HashMap<String,Object>();

After initializing, we can add instances of the _Product_ class. However, when we want to create an instance of _HashMap <String, Product>_ to access the field values of a _Product_ instance, we can’t mix instance types. To demonstrate, let’s try to assign the instance we created to a variable of type _HashMap <String, Product>_:
    
    
    HashMap<String,Product> productMap =objectMap;

We get an error message _error: incompatible types: HashMap <String,Object> cannot be converted to HashMap<String,Product>_. Therefore, we must iterate over the _HashMap <String, Object>_ collection and cast _Object_ to _Product_ for each value to create a type  _HashMap <String, Product>_ collection. Let’s use a JUnit 5 test to confirm that we can access the fields of the resulting collection directly:
    
    
    @Test
    public void whenUsingObjectAsHashMapGenericParameter_ShouldRequireCast() throws Exception {
    
        try { 
            HashMap<String,Object> objectMap  = new HashMap<String,Object>();  
    
            Product eBike = new Product("E-Bike", "A bike with a battery");
            Product roadBike = new Product("Road bike", "A bike for competition");
    
            objectMap.put("E-Bike", eBike);
            objectMap.put("Road bike", roadBike);
    
            HashMap<String,Product> productMap =new HashMap<String,Product>();
    
            for (Map.Entry<String, Object> entry : objectMap.entrySet()) {
                if(entry.getValue() instanceof Product){
                    productMap.put(entry.getKey(), (Product) entry.getValue());
                }
            }
    
            Product product = productMap.get("E-Bike"); 
              
            String actualDescription = product.getDescription();
            String expectedDescription = new String("A bike with a battery");
    
            Assertions.assertTrue(actualDescription.equals(expectedDescription));   
     
        } catch (ClassCastException e){
            System.out.println(e.getMessage());
        }
    }

The JUnit test passes when we correctly convert the _Object_ type values to _Product_ type values.

### 5.2. How to Avoid Casting

Although casting is an option, we can avoid it for a more concise code. We avoid casting by using appropriate generics parameters when initializing a _HashMap_. If the _HashMap_ value is of type _Product_ we parameterize using _Product_ instead of the superclass _Object_ :
    
    
    HashMap<String,Product> objectMap  = new HashMap<String,Product>();

Let’s use JUnit 5 test to confirm that no casting is required, and the resulting object can be assigned to a variable of type _HashMap <String,Product>_:
    
    
    @Test
    public void whenUsingProperHashMapGenericParameters_ShouldNotRequireCast() throws Exception {
        HashMap<String,Product> productMap  = new HashMap<String,Product>(); 
    
        Product eBike = new Product("E-Bike", "A bike with a battery");
        Product roadBike = new Product("Road bike", "A bike for competition");
    
        productMap.put(eBike.getName(), eBike);
        productMap.put(roadBike.getName(), roadBike);
    
        Product product = productMap.get("E-Bike"); 
    
        String actualDescription = product.getDescription();
        String expectedDescription = new String("A bike with a battery");
        
        Assertions.assertTrue(actualDescription.equals(expectedDescription));
    
        HashMap<String,Product> objectMap = productMap;
        
        Assertions.assertSame(objectMap, productMap);
    }

The two JUnit tests should pass, confirming that we can avoid casting.

## 6\. _HashMap_ Internals

In this section, we’ll look at how _HashMap_ works internally and what are the benefits of using _HashMap_ instead of a simple list, for example.

As we’ve seen, we can retrieve an element from a _HashMap_ using its key. One approach would be to use a list, iterate over all elements, and return when we find an element for which the key matches. Both the time and space complexity of this approach would be _O(n)_.

**With _HashMap_ , we can achieve an average time complexity of _O(1)_ for the _put_ and _get_ operations and space complexity of _O(n)_.** Let’s see how that works.

### 6.1. The Hash Code and Equals

**Instead of iterating over all its elements,_HashMap_ attempts to calculate the position of a value based on its key. **

The naive approach would be to have a list that can contain as many elements as there are keys possible. As an example, let’s say our key is a lower-case character. Then it’s sufficient to have a list of size 26, and if we want to access the element with key ‘c’, we’d know that it’s the one at position 3, and we can retrieve it directly.

However, this approach would not be very effective if we have a much bigger keyspace. For example, let’s say our key was an integer. In this case, the size of the list would have to be 2,147,483,647. In most cases, we would also have far fewer elements, so a big part of the allocated memory would remain unused.

**_HashMap_ stores elements in so-called buckets and the number of buckets is called _capacity_.**

When we put a value in the map, the key’s _hashCode()_ method is used to determine the bucket in which the value will be stored.

To retrieve the value, _HashMap_ calculates the bucket in the same way – using _hashCode()_. Then it iterates through the objects found in that bucket and use key’s _equals()_ method to find the exact match.

### 6.2. Keys’ Immutability

**In most cases, we should use immutable keys. Or at least, we must be aware of the consequences of using mutable keys.**

Let’s see what happens when our key changes after we used it to store a value in a map.

For this example, we’ll create the _MutableKey_ :
    
    
    public class MutableKey {
        private String name;
    
        // standard constructor, getter and setter
    
        @Override
        public boolean equals(Object o) {
            if (this == o) {
                return true;
            }
            if (o == null || getClass() != o.getClass()) {
                return false;
            }
            MutableKey that = (MutableKey) o;
            return Objects.equals(name, that.name);
        }
    
        @Override
        public int hashCode() {
            return Objects.hash(name);
        }
    }

And here goes the test:
    
    
    MutableKey key = new MutableKey("initial");
    
    Map<MutableKey, String> items = new HashMap<>();
    items.put(key, "success");
    
    key.setName("changed");
    
    assertNull(items.get(key));

As we can see, we’re no longer able to get the corresponding value once the key has changed, instead, _null_ is returned. **This is because _HashMap_ is searching in the wrong bucket.**

The above test case may be surprising if we don’t have a good understanding of how _HashMap_ works internally.

### 6.3. Collisions

**For this to work correctly, equal keys must have the same hash, however, different keys can have the same hash**. If two different keys have the same hash, the two values belonging to them will be stored in the same bucket. Inside a bucket, values are stored in a list and retrieved by looping over all elements. The cost of this is _O(n)_.

As of Java 8 (see [JEP 180](https://openjdk.java.net/jeps/180)), the data structure in which the values inside one bucket are stored is changed from a list to a balanced tree if a bucket contains 8 or more values, and it’s changed back to a list if, at some point, only 6 values are left in the bucket. This improves the performance to be _O(log n)_.

### 6.4. Capacity and Load Factor

To avoid having many buckets with multiple values, the capacity is doubled if 75% (the load factor) of the buckets become non-empty. The default value for the load factor is 75%, and the default initial capacity is 16. Both can be set in the constructor.

### 6.5. Summary of _put_ and _get_ Operations

Let’s summarize how the _put_ and _get_ operations work.

**When we add an element to the map,** _HashMap_ calculates the bucket. If the bucket already contains a value, the value is added to the list (or tree) belonging to that bucket. If the load factor becomes bigger than the maximum load factor of the map, the capacity is doubled.

**When we want to get a value from the map,** _HashMap_ calculates the bucket and gets the value with the same key from the list (or tree).

## 7\. Conclusion

In this article, we saw how to use a _HashMap_ and how it works internally. Along with _ArrayList_ , _HashMap_ is one of the most frequently used data structures in Java, so it’s very handy to have good knowledge of how to use it and how it works under the hood. Our article [The Java HashMap Under the Hood](/java-hashmap-advanced) covers the internals of _HashMap_ in more detail.
