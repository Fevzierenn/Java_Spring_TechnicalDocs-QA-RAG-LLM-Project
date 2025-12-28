# Java equals() and hashCode() Contracts

## **1\. Overview**

In this tutorial, we’ll introduce two methods that closely belong together: ._equals()_ and ._hashCode()_. We’ll focus on their relationship with each other, how to correctly override them, and why we should override both or neither.

## **2\. The ._equals()_ Method**

By default**, the _Object_ class defines both the ._equals()_ and ._hashCode()_ methods**. As a result, every Java class implicitly has these two methods.:
    
    
    class Money {
        int amount;
        String currencyCode;
    }
    
    
    Money income = new Money(55, "USD");
    Money expenses = new Money(55, "USD");
    boolean balanced = income.equals(expenses)

We would expect _income.equals(expenses)_ to return _true,_ but with the current implementation of the _Money_ class, it won’t.

**The default implementation of _equals()_ in the _Object_ class compares the identity of the object**. In our example, the _income_ and _expenses_ instances of the _Money_ class have two different identities. Therefore, comparing them with the ._equals()_ method returns false.

To change this behavior we must override this method.

### **2.1. Overriding _equals()_**

Let’s override the ._equals()_ method so that it doesn’t consider only object identity but also the value of the two relevant properties:
    
    
    @Override
    public boolean equals(Object o) {
        if (o == this)
            return true;
        if (!(o instanceof Money))
            return false;
        Money other = (Money)o;
        boolean currencyCodeEquals = (this.currencyCode == null && other.currencyCode == null)
          || (this.currencyCode != null && this.currencyCode.equals(other.currencyCode));
        return this.amount == other.amount && currencyCodeEquals;
    }

Above, we have three conditions to check whether the _Money_ instance is the same as any other object. First, if the object is equal to itself it will return true. Second, if it is not an instance of _Money_ it will return false. Third, we compare it with the attributes of another  _Money_ class instance. In detail, we ensure that all attributes of the compared class match those of the comparing class.

### **2.2. The ._equals()_ Contract**

**Java SE defines the contract that our implementation of the _equals()_ method must fulfill**. In short, most criteria follow common sense but we can define the formal rules that the  _equals()_ method must follow. It must be:

  * _reflexive_ : an object must equal itself
  * _symmetric_ : _x.equals(y)_ must return the same result as _y.equals(x)_
  * _transitive_ : if _x.equals(y)_ and _y.equals(z),_ then also _x.equals(z)_
  * _consistent_ : the value of ._equals()_ should change only if a property that is contained in ._equals()_ changes (no randomness allowed)



We can look up the exact criteria in the [Java SE Docs for the _Object_ class](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/Object.html).

### **2.3. Violating _equals()_ Symmetry With Inheritance**

If the criteria for ._equals()_ is such common sense, then how can we violate it at all? Well, **violations of the _.equals()_ contract are more likely to occur when we extend a class that has overridden the ._equals()_ method as well**. Let’s consider a _Voucher_ class that extends our _Money_ class:
    
    
    class WrongVoucher extends Money {
    
        private String store;
    
        @Override
        public boolean equals(Object o) {
            if (o == this)
                return true;
            if (!(o instanceof WrongVoucher))
                return false;
            WrongVoucher other = (WrongVoucher)o;
            boolean currencyCodeEquals = (this.currencyCode == null && other.currencyCode == null)
              || (this.currencyCode != null && this.currencyCode.equals(other.currencyCode));
            boolean storeEquals = (this.store == null && other.store == null)
              || (this.store != null && this.store.equals(other.store));
            return this.amount == other.amount && currencyCodeEquals && storeEquals;
        }
    
        // other methods
    }

At first glance, the _Voucher_ class and its override for ._equals()_ seem to be correct. Both ._equals()_ methods behave correctly as long as we compare _Money_ to _Money_ or _Voucher_ to _Voucher_. But what happens if we compare these two objects:
    
    
    Money cash = new Money(42, "USD");
    WrongVoucher voucher = new WrongVoucher(42, "USD", "Amazon");
    
    voucher.equals(cash) => false // As expected.
    cash.equals(voucher) => true // That's wrong.

Thus, we have a violation of the symmetry criteria.

### 2.4**. Fixing _equals()_ Symmetry With Composition**

**To avoid making mistakes, we should favor composition over inheritance.**

Instead of subclassing _Money_ , let’s create a _Voucher_ class with a _Money_ property:
    
    
    class Voucher {
    
        private Money value;
        private String store;
    
        Voucher(int amount, String currencyCode, String store) {
            this.value = new Money(amount, currencyCode);
            this.store = store;
        }
    
        @Override
        public boolean equals(Object o) {
            if (o == this)
                return true;
            if (!(o instanceof Voucher))
                return false;
            Voucher other = (Voucher) o;
            boolean valueEquals = (this.value == null && other.value == null)
              || (this.value != null && this.value.equals(other.value));
            boolean storeEquals = (this.store == null && other.store == null)
              || (this.store != null && this.store.equals(other.store));
            return valueEquals && storeEquals;
        }
    
        // other methods
    }

Now ._equals()_ will work symmetrically as the contract requires.

## **3\. The ._hashCode()_ Method**

**The _.hashCode()_ method returns an integer representing the current instance of the class**. We should calculate this value consistently with the class definition of equality.

For more details, check out our [guide to ._hashCode()_](/java-hashcode).

### **3.1. The ._hashCode()_ Contract**

**Java SE also defines a contract for the ._hashCode()_ method**. A thorough look at this contract reveals how closely related ._hashCode()_ and ._equals()_ are.

All three criteria in the ._hashCode()_ contract mention the ._equals()_ method in some way**:**

  * _internal consistency_ : the value of _hashCode()_ may only change if a property that is in  _equals()_ changes
  * _equals consistency_ : objects that are equal to each other must return the same hashCode
  * _collisions_ : unequal objects may have the same hashCode



### **3.2. Violating the Consistency of _hashCode()_ and _equals()_**

The second criterion of the _.hashCode()_ contract has an important consequence: **If we override _equals()_ , we must also override _hashCode()_**. This is by far the most widespread violation regarding the _equals()_ and _hashCode()_ methods contracts.

Let’s see such an example:
    
    
    class Team {
    
        String city;
        String department;
    
        @Override
        public final boolean equals(Object o) {
            // implementation
        }
    }

The _Team_ class overrides only _equals()_ , but it still implicitly uses the default implementation of _hashCode()_ as defined in the _Object_ class. Consequently, it will return a different hashCode() for every instance of the class and violate the second rule**.**

Now, if we create two _Team_ objects, both with city “New York” and department “marketing,” they will be equal, but they’ll return different hashCodes**.**

### **3.3._HashMap_ Key With an Inconsistent _hashCode()_**

But why is the contract violation in our _Team_ class a problem? Well, the trouble starts when some hash-based collections are involved. Let’s try to use our _Team_ class as a key of a _HashMap_ :
    
    
    Map<Team,String> leaders = new HashMap<>();
    leaders.put(new Team("New York", "development"), "Anne");
    leaders.put(new Team("Boston", "development"), "Brian");
    leaders.put(new Team("Boston", "marketing"), "Charlie");
    
    Team myTeam = new Team("New York", "development");
    String myTeamLeader = leaders.get(myTeam);

We would expect _myTeamLeader_ to return “Anne,” but with the current code, it doesn’t.

If we want to use instances of the _Team_ class as _HashMap_ keys, we have to override the _hashCode()_ method so that it adheres to the contract; **equal objects return the same hashCode _._**

Let’s see an example implementation:
    
    
    @Override
    public final int hashCode() {
        int result = 17;
        if (city != null) {
            result = 31 * result + city.hashCode();
        }
        if (department != null) {
            result = 31 * result + department.hashCode();
        }
        return result;
    }

After this change, _leaders.get(myTeam)_ returns “Anne” as expected.

## **4\. When Do We Override ._equals()_ and ._hashCode()_?**

**Generally, we want to override either both _.equals() and .hashCode()_ or neither of them.** We just saw in Section 3 the undesired consequences if we ignore this rule.

Domain-driven design can help us decide circumstances when we should leave them be. For entity classes, for objects having an intrinsic identity, the default implementation often makes sense.

However, **for value objects, we usually prefer equality based on their properties**. Thus, we want to override ._equals()_ and ._hashCode()_. Remember our _Money_ class from Section 2: 55 USD equals 55 USD, even if they’re two separate instances.

## **5\. Implementation Helpers**

We typically don’t write the implementation of these methods by hand. As we’ve seen, there are quite a few pitfalls.

One common option is to [let our IDE](/java-eclipse-equals-and-hashcode) generate the ._equals()_ and ._hashCode()_ methods.

[Apache Commons Lang](/java-commons-lang-3) and [Google Guava](/whats-new-in-guava-19) have helper classes to simplify writing using both methods.

[Project Lombok](/intro-to-project-lombok) also provides an _@EqualsAndHashCode_ annotation. **Note again how ._equals()_ and ._hashCode()_ “go together” and even have a common annotation.**

## **6\. Verifying the Contracts**

If we want to check whether our implementations adhere to the Java SE contracts and best practices, we can use the EqualsVerifier library.

Let’s add the [EqualsVerifier](https://mvnrepository.com/artifact/nl.jqno.equalsverifier/equalsverifier) Maven test dependency:
    
    
    <dependency>
        <groupId>nl.jqno.equalsverifier</groupId>
        <artifactId>equalsverifier</artifactId>
        <version>3.15.3</version>
        <scope>test</scope>
    </dependency>

Now let’s verify that our _Team_ class follows the  _equals()_ and _hashCode()_ contracts:
    
    
    @Test
    public void equalsHashCodeContracts() {
        EqualsVerifier.forClass(Team.class).verify();
    }

It’s worth noting that  _EqualsVerifier_ tests both the _equals()_ and _hashCode()_ methods.

**_EqualsVerifier_ is much stricter than the Java SE contract.** For example, it makes sure that our methods can’t throw a _NullPointerException._ Also, it enforces that both methods, or the class itself, are final.

It’s important to realize that **the _EqualsVerifier_ ‘s default configuration allows only immutable fields**. This is a stricter check than what the Java SE contract allows. It adheres to a recommendation of Domain-Driven Design to make value objects immutable.

If we find some of the built-in constraints unnecessary, we can add a  _suppress(Warning.SPECIFIC_WARNING)_ to our  _EqualsVerifier_ call.

## **7\. Conclusion**

In this article, we discussed the _equals()_ and _hashCode()_ contracts. We should remember to:

  * Always override _hashCode()_ if we override _equals()_
  * Override  _equals()_ and _hashCode()_ for value objects
  * Be aware of the traps of extending classes that have overridden _equals()_ and _hashCode()_
  * Consider using an IDE or a third-party library for generating the _equals()_ and _hashCode()_ methods
  * Consider using EqualsVerifier to test our implementation


