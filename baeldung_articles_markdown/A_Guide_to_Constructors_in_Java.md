# A Guide to Constructors in Java

## 1\. Introduction

Constructors are the gatekeepers of [_object-oriented design_](/java-polymorphism).

In this tutorial, we’ll see how they act as a single location from which to initialize [the internal state](/java-inheritance-composition) of the object being created.

Let’s forge ahead and create a simple object that represents a bank account.

## 2\. Setting Up a Bank Account

Imagine that we need to create a class that represents a bank account. It’ll contain a Name, Date of Creation and Balance.

Also, let’s override the _toString_ method to print the details to the console:
    
    
    class BankAccount {
        String name;
        LocalDateTime opened;
        double balance;
        
        @Override
        public String toString() {
            return String.format("%s, %s, %f", 
              this.name, this.opened.toString(), this.balance);
        }
    }
    

Now, this class contains all of the necessary fields required to store information about a bank account, but it doesn’t contain a constructor yet.

**This means that if we create a new object, the field values wouldn’t be initialized:**
    
    
    BankAccount account = new BankAccount();
    account.toString();
    

Running the _toString_ method above will result in an exception because the objects _name_ and _opened_ are still _null_ :
    
    
    java.lang.NullPointerException
        at com.baeldung.constructors.BankAccount.toString(BankAccount.java:12)
        at com.baeldung.constructors.ConstructorUnitTest
          .givenNoExplicitContructor_whenUsed_thenFails(ConstructorUnitTest.java:23)
    

## 3\. A No-Argument Constructor

Let’s fix that with a constructor:
    
    
    class BankAccount {
        public BankAccount() {
            this.name = "";
            this.opened = LocalDateTime.now();
            this.balance = 0.0d;
        }
    }
    

Notice a few things about the constructor which we just wrote. First, it’s a method, but it has no return type. That’s because a constructor implicitly returns the type of the object that it creates. Calling _new BankAccount()_ now will call the constructor above.

Secondly, it takes no arguments. This particular kind of constructor is called a n _o-argument constructor_.

Why didn’t we need it for the first time, though? It’s because when we **don’t explicitly write any constructor, the compiler adds a default, no-argument constructor**.

This is why we were able to construct the object the first time, even though we didn’t write a constructor explicitly. The default, no argument constructor will simply set all members to their [default values](https://docs.oracle.com/javase/tutorial/java/nutsandbolts/datatypes.html).

For objects, that’s _null,_ which resulted in the exception that we saw earlier.

## 4\. A Parameterized Constructor

Now, a real benefit of constructors is that they help us maintain _encapsulation_ when injecting state into the object.

So, to do something really useful with this bank account, we need to be able to actually inject some initial values into the object.

To do that, **let’s write a _parameterized constructor_ , that is, a constructor that takes some arguments**:
    
    
    class BankAccount {
        public BankAccount() { ... }
        public BankAccount(String name, LocalDateTime opened, double balance) {
            this.name = name;
            this.opened = opened;
            this.balance = balance;
        }
    }
    

Now we can do something useful with our _BankAccount_ class:
    
    
        LocalDateTime opened = LocalDateTime.of(2018, Month.JUNE, 29, 06, 30, 00);
        BankAccount account = new BankAccount("Tom", opened, 1000.0f); 
        account.toString();
    

Notice, that our class now has 2 constructors. An explicit, no argument constructor and a parameterized constructor.

We can create as many constructors as we like, but we probably would like not to create too many. This would be a little confusing.

If we find too many constructors in our code, a few [Creational Design Patterns](/creational-design-patterns) might be helpful.

## 5\. A Copy Constructor

Constructors need not be limited to initialization alone. They can also be used to create objects in other ways. **Imagine that we need to be able to create a new account from an existing one.**

The new account should have the same name as the old account, today’s date of creation and no funds. **We can do that using a _copy constructor_ :**
    
    
    public BankAccount(BankAccount other) {
        this.name = other.name;
        this.opened = LocalDateTime.now();
        this.balance = 0.0f;
    }
    

Now we have the following behavior:
    
    
    LocalDateTime opened = LocalDateTime.of(2018, Month.JUNE, 29, 06, 30, 00);
    BankAccount account = new BankAccount("Tim", opened, 1000.0f);
    BankAccount newAccount = new BankAccount(account);
    
    assertThat(account.getName()).isEqualTo(newAccount.getName());
    assertThat(account.getOpened()).isNotEqualTo(newAccount.getOpened());
    assertThat(newAccount.getBalance()).isEqualTo(0.0f);
    

## 6\. A Chained Constructor

Of course, we may be able to infer some of the constructor parameters or **give some of them default values.**

For example, we could just create a new bank account with only the name.

So, let’s create a constructor with a _name_ parameter and give the other parameters default values:
    
    
    public BankAccount(String name, LocalDateTime opened, double balance) {
        this.name = name;
        this.opened = opened;
        this.balance = balance;
    }
    public BankAccount(String name) {
        this(name, LocalDateTime.now(), 0.0f);
    }

With the keyword _this,_ we’re calling the other constructor.

We have to remember that**if we want to chain a superclass constructor we have to use _super_ instead of _this_.**

Also, remember that **_this_ or _super_ expression should always be the first statement.**

## 7\. Value Types

An interesting use of constructors in Java is in the creation of _Value Objects_. **A value object is an object that does not change its internal state after initialization.**

**That is, the object is immutable**. Immutability in Java is a bit [nuanced](/java-immutable-object) and care should be taken when crafting objects.

Let’s go ahead and create an immutable class:
    
    
    class Transaction {
        final BankAccount bankAccount;
        final LocalDateTime date;
        final double amount;
    
        public Transaction(BankAccount account, LocalDateTime date, double amount) {
            this.bankAccount = account;
            this.date = date;
            this.amount = amount;
        }
    }
    

Notice, that we now use the _final_ keyword when defining the members of the class. This means that each of those members can only be initialized within the constructor of the class. They cannot be reassigned later on inside any other method. We can read those values, but not change them.

**If we create multiple constructors for the _Transaction_ class, each constructor will need to initialize every final variable.** Not doing so will result in a compilation error.

## 8\. Conclusion

We’ve taken a tour through the different ways in which constructors build objects. When used judiciously, constructs form the basic building blocks of Object-Oriented design in Java.
