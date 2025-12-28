# A Guide to Java Enums

## 1\. Overview

In this tutorial, we’ll learn what Java enums are, what problems they solve, and how some of their design patterns can be used in practice.

**Java 5 first introduced the _enum_ keyword.** It denotes a special type of class that always extends the _java.lang.Enum_ class. For the official documentation on usage, we can head over to the [documentation](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/Enum.html).

Constants defined this way make the code more readable, allow for compile-time checking, document the list of accepted values upfront, and avoid unexpected behavior due to invalid values being passed in.

Here’s a quick and simple example of an enum that defines the status of a pizza order; the order status can be _ORDERED_ , _READY_ or _DELIVERED_ :
    
    
    public enum PizzaStatus {
        ORDERED,
        READY, 
        DELIVERED; 
    }

Additionally, enums come with many useful methods that we would otherwise need to write if we were using traditional public static final constants.

## **2\. Custom Enum Methods**

Now that we have a basic understanding of what enums are and how we can use them, we’ll take our previous example to the next level by defining some extra API methods on the enum:
    
    
    public class Pizza {
        private PizzaStatus status;
        public enum PizzaStatus {
            ORDERED,
            READY,
            DELIVERED;
        }
    
        public boolean isDeliverable() {
            if (getStatus() == PizzaStatus.READY) {
                return true;
            }
            return false;
        }
        
        // Methods that set and get the status variable.
    }
    

## **3\. Comparing Enum Types Using “==” Operator**

Since enum types ensure that only one instance of the constants exist in the JVM, we can safely use the “==” operator to compare two variables, like we did in the above example. Furthermore, the “==” operator provides compile-time and run-time safety.

First, we’ll look **at run-time safety** in the following snippet, where we’ll use the “==” operator to compare statuses. Either value can be  _null_ and we won’t get a  _NullPointerException._ Conversely, if we use the equals method, we will get a _NullPointerException_ :
    
    
    if(testPz.getStatus().equals(Pizza.PizzaStatus.DELIVERED)); 
    if(testPz.getStatus() == Pizza.PizzaStatus.DELIVERED); 
    

As for **compile-time safety** , let’s look at an example where we’ll determine that an enum of a different type is equal by comparing it using the _equals_ method. This is because the values of the enum and the _getStatus_ method coincidentally are the same; however, logically the comparison should be false. We avoid this issue by using the “==” operator.

The compiler will flag the comparison as an incompatibility error:
    
    
    if(testPz.getStatus().equals(TestColor.GREEN));
    if(testPz.getStatus() == TestColor.GREEN);
    

## **4\. Using Enum Types in Switch Statements**

We can use enum types in _switch_ statements also:
    
    
    public int getDeliveryTimeInDays() {
        switch (status) {
            case ORDERED: return 5;
            case READY: return 2;
            case DELIVERED: return 0;
        }
        return 0;
    }

## **5\. Fields, Methods and Constructors in Enums**

We can define constructors, methods, and fields inside enum types, which makes them very powerful.

Next, let’s extend the example above by implementing the transition from one stage of a pizza order to another. We’ll see how we can get rid of the _if_ and _switch_ statements used before:
    
    
    public class Pizza {
    
        private PizzaStatus status;
        public enum PizzaStatus {
            ORDERED (5){
                @Override
                public boolean isOrdered() {
                    return true;
                }
            },
            READY (2){
                @Override
                public boolean isReady() {
                    return true;
                }
            },
            DELIVERED (0){
                @Override
                public boolean isDelivered() {
                    return true;
                }
            };
    
            private int timeToDelivery;
    
            public boolean isOrdered() {return false;}
    
            public boolean isReady() {return false;}
    
            public boolean isDelivered(){return false;}
    
            public int getTimeToDelivery() {
                return timeToDelivery;
            }
    
            PizzaStatus (int timeToDelivery) {
                this.timeToDelivery = timeToDelivery;
            }
        }
    
        public boolean isDeliverable() {
            return this.status.isReady();
        }
    
        public void printTimeToDeliver() {
            System.out.println("Time to delivery is " + 
              this.getStatus().getTimeToDelivery());
        }
        
        // Methods that set and get the status variable.
    }
    

The test snippet below demonstrates how this works:
    
    
    @Test
    public void givenPizaOrder_whenReady_thenDeliverable() {
        Pizza testPz = new Pizza();
        testPz.setStatus(Pizza.PizzaStatus.READY);
        assertTrue(testPz.isDeliverable());
    }

## 6\. _EnumSet_ and _EnumMap_

### **6.1._EnumSet_**

The _EnumSet_ is a specialized _Set_ implementation that’s meant to be used with _Enum_ types.

Compared to a _HashSet,_ it’s a very efficient and compact representation of a particular _Set_ of _Enum_ constants, owing to the internal _Bit Vector Representation_ that’s used. It also provides a type-safe alternative to traditional _int_ -based “bit flags,” allowing us to write concise code that’s more readable and maintainable.

The _EnumSet_ is an abstract class that has two implementations, _RegularEnumSet_ and _JumboEnumSet_ , one of which is chosen depending on the number of constants in the enum at the time of instantiation.

Therefore, it’s a good idea to use this set whenever we want to work with a collection of enum constants in most scenarios (like subsetting, adding, removing, and bulk operations like _containsAll_ and _removeAll_), and use _Enum.values()_ if we just want to iterate over all possible constants.

In the code snippet below, we can see how to use _EnumSet_ to create a subset of constants:
    
    
    public class Pizza {
    
        private static EnumSet<PizzaStatus> undeliveredPizzaStatuses =
          EnumSet.of(PizzaStatus.ORDERED, PizzaStatus.READY);
    
        private PizzaStatus status;
    
        public enum PizzaStatus {
            ...
        }
    
        public boolean isDeliverable() {
            return this.status.isReady();
        }
    
        public void printTimeToDeliver() {
            System.out.println("Time to delivery is " + 
              this.getStatus().getTimeToDelivery() + " days");
        }
    
        public static List<Pizza> getAllUndeliveredPizzas(List<Pizza> input) {
            return input.stream().filter(
              (s) -> undeliveredPizzaStatuses.contains(s.getStatus()))
                .collect(Collectors.toList());
        }
    
        public void deliver() { 
            if (isDeliverable()) { 
                PizzaDeliverySystemConfiguration.getInstance().getDeliveryStrategy()
                  .deliver(this); 
                this.setStatus(PizzaStatus.DELIVERED); 
            } 
        }
        
        // Methods that set and get the status variable.
    }
    

Executing the following test demonstrates the power of the _EnumSet_ implementation of the _Set_ interface:
    
    
    @Test
    public void givenPizaOrders_whenRetrievingUnDeliveredPzs_thenCorrectlyRetrieved() {
        List<Pizza> pzList = new ArrayList<>();
        Pizza pz1 = new Pizza();
        pz1.setStatus(Pizza.PizzaStatus.DELIVERED);
    
        Pizza pz2 = new Pizza();
        pz2.setStatus(Pizza.PizzaStatus.ORDERED);
    
        Pizza pz3 = new Pizza();
        pz3.setStatus(Pizza.PizzaStatus.ORDERED);
    
        Pizza pz4 = new Pizza();
        pz4.setStatus(Pizza.PizzaStatus.READY);
    
        pzList.add(pz1);
        pzList.add(pz2);
        pzList.add(pz3);
        pzList.add(pz4);
    
        List<Pizza> undeliveredPzs = Pizza.getAllUndeliveredPizzas(pzList); 
        assertTrue(undeliveredPzs.size() == 3); 
    }

### **6.2. EnumMap**

_EnumMap_ is a specialized _Map_ implementation meant to be used with enum constants as keys. Compared to its counterpart _HashMap,_ it’s an efficient and compact implementation that’s internally represented as an array:
    
    
    EnumMap<Pizza.PizzaStatus, Pizza> map;
    

Let’s look at an example of how we can use it in practice:
    
    
    public static EnumMap<PizzaStatus, List<Pizza>> 
      groupPizzaByStatus(List<Pizza> pizzaList) {
        EnumMap<PizzaStatus, List<Pizza>> pzByStatus = 
          new EnumMap<PizzaStatus, List<Pizza>>(PizzaStatus.class);
        
        for (Pizza pz : pizzaList) {
            PizzaStatus status = pz.getStatus();
            if (pzByStatus.containsKey(status)) {
                pzByStatus.get(status).add(pz);
            } else {
                List<Pizza> newPzList = new ArrayList<Pizza>();
                newPzList.add(pz);
                pzByStatus.put(status, newPzList);
            }
        }
        return pzByStatus;
    }
    

Executing the following test demonstrates the power of the _EnumMap_ implementation of the _Map_ interface:
    
    
    @Test
    public void givenPizaOrders_whenGroupByStatusCalled_thenCorrectlyGrouped() {
        List<Pizza> pzList = new ArrayList<>();
        Pizza pz1 = new Pizza();
        pz1.setStatus(Pizza.PizzaStatus.DELIVERED);
    
        Pizza pz2 = new Pizza();
        pz2.setStatus(Pizza.PizzaStatus.ORDERED);
    
        Pizza pz3 = new Pizza();
        pz3.setStatus(Pizza.PizzaStatus.ORDERED);
    
        Pizza pz4 = new Pizza();
        pz4.setStatus(Pizza.PizzaStatus.READY);
    
        pzList.add(pz1);
        pzList.add(pz2);
        pzList.add(pz3);
        pzList.add(pz4);
    
        EnumMap<Pizza.PizzaStatus,List<Pizza>> map = Pizza.groupPizzaByStatus(pzList);
        assertTrue(map.get(Pizza.PizzaStatus.DELIVERED).size() == 1);
        assertTrue(map.get(Pizza.PizzaStatus.ORDERED).size() == 2);
        assertTrue(map.get(Pizza.PizzaStatus.READY).size() == 1);
    }

## 7\. Implement Design Patterns Using Enums

### **7.1. Singleton Pattern**

Normally, implementing a class using the Singleton pattern is quite non-trivial. Enums provide a quick and easy way of implementing singletons.

In addition, since the enum class implements the _Serializable_ interface under the hood, the class is guaranteed to be a singleton by the JVM. This is unlike the conventional implementation, where we have to ensure that no new instances are created during deserialization.

In the code snippet below, we see how we can implement a singleton pattern:
    
    
    public enum PizzaDeliverySystemConfiguration {
        INSTANCE;
        PizzaDeliverySystemConfiguration() {
            // Initialization configuration which involves
            // overriding defaults like delivery strategy
        }
    
        private PizzaDeliveryStrategy deliveryStrategy = PizzaDeliveryStrategy.NORMAL;
    
        public static PizzaDeliverySystemConfiguration getInstance() {
            return INSTANCE;
        }
    
        public PizzaDeliveryStrategy getDeliveryStrategy() {
            return deliveryStrategy;
        }
    }

### **7.2. Strategy Pattern**

Conventionally, the Strategy pattern is written by having an interface that is implemented by different classes.

Adding a new strategy means adding a new implementation class. With enums, we can achieve this with less effort, and adding a new implementation means simply defining another instance with some implementation.

The code snippet below shows how to implement the Strategy pattern:
    
    
    public enum PizzaDeliveryStrategy {
        EXPRESS {
            @Override
            public void deliver(Pizza pz) {
                System.out.println("Pizza will be delivered in express mode");
            }
        },
        NORMAL {
            @Override
            public void deliver(Pizza pz) {
                System.out.println("Pizza will be delivered in normal mode");
            }
        };
    
        public abstract void deliver(Pizza pz);
    }

Then we add the following method to the _Pizza_ class:
    
    
    public void deliver() {
        if (isDeliverable()) {
            PizzaDeliverySystemConfiguration.getInstance().getDeliveryStrategy()
              .deliver(this);
            this.setStatus(PizzaStatus.DELIVERED);
        }
    }
    
    
    @Test
    public void givenPizaOrder_whenDelivered_thenPizzaGetsDeliveredAndStatusChanges() {
        Pizza pz = new Pizza();
        pz.setStatus(Pizza.PizzaStatus.READY);
        pz.deliver();
        assertTrue(pz.getStatus() == Pizza.PizzaStatus.DELIVERED);
    }

## 8\. Java 8 and Enums

We can rewrite the _Pizza_ class in Java 8, and see how the methods _getAllUndeliveredPizzas()_ and _groupPizzaByStatus()_ become so concise with the use of lambdas and the _Stream_ APIs:
    
    
    public static List<Pizza> getAllUndeliveredPizzas(List<Pizza> input) {
        return input.stream().filter(
          (s) -> !deliveredPizzaStatuses.contains(s.getStatus()))
            .collect(Collectors.toList());
    }
    
    
    
    
    public static EnumMap<PizzaStatus, List<Pizza>> 
      groupPizzaByStatus(List<Pizza> pzList) {
        EnumMap<PizzaStatus, List<Pizza>> map = pzList.stream().collect(
          Collectors.groupingBy(Pizza::getStatus,
          () -> new EnumMap<>(PizzaStatus.class), Collectors.toList()));
        return map;
    }

## 9\. JSON Representation of Enum

Using Jackson libraries, it’s possible to have a JSON representation of enum types as if they’re POJOs. In the code snippet below, we’ll see how we can use the Jackson annotations for the same:
    
    
    @JsonFormat(shape = JsonFormat.Shape.OBJECT)
    public enum PizzaStatus {
        ORDERED (5){
            @Override
            public boolean isOrdered() {
                return true;
            }
        },
        READY (2){
            @Override
            public boolean isReady() {
                return true;
            }
        },
        DELIVERED (0){
            @Override
            public boolean isDelivered() {
                return true;
            }
        };
    
        private int timeToDelivery;
    
        public boolean isOrdered() {return false;}
    
        public boolean isReady() {return false;}
    
        public boolean isDelivered(){return false;}
    
        @JsonProperty("timeToDelivery")
        public int getTimeToDelivery() {
            return timeToDelivery;
        }
    
        private PizzaStatus (int timeToDelivery) {
            this.timeToDelivery = timeToDelivery;
        }
    }
    

We can use the _Pizza_ and _PizzaStatus_ as follows:
    
    
    Pizza pz = new Pizza();
    pz.setStatus(Pizza.PizzaStatus.READY);
    System.out.println(Pizza.getJsonString(pz));
    

This will generate the following JSON representation of the _Pizza_ s status:
    
    
    {
      "status" : {
        "timeToDelivery" : 2,
        "ready" : true,
        "ordered" : false,
        "delivered" : false
      },
      "deliverable" : true
    }

For more information on JSON serializing/deserializing (including customization) of enum types, we can refer to the [Jackson – Serialize Enums as JSON Objects](/jackson-serialize-enums).

## 10\. Conclusion

In this article, we explored the Java enum, from the language basics to more advanced and interesting real-world use cases.
