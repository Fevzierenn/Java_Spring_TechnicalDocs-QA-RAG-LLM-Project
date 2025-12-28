# Object Type Casting in Java

## **1\. Overview**

The Java type system is made up of two kinds of types: primitives and references.

We covered primitive conversions in [this article](/java-primitive-conversions), and we’ll focus on references casting here to get a good understanding of how Java handles types.

## **2\. Primitive vs Reference**

Although primitive conversions and reference variable casting may look similar, they’re quite [different concepts](https://docs.oracle.com/javase/specs/jls/se8/html/jls-4.html#jls-4.1).

In both cases, we’re “turning” one type into another. But, in a simplified way, a primitive variable contains its value, and conversion of a primitive variable means irreversible changes in its value:
    
    
    double myDouble = 1.1;
    int myInt = (int) myDouble;
            
    assertNotEquals(myDouble, myInt);

After the conversion in the above example, _myInt_ variable is _1_ , and we can’t restore the previous value _1.1_ from it.

**Reference variables are different** ; the reference variable only refers to an object but doesn’t contain the object itself.

And casting a reference variable doesn’t touch the object it refers to but only labels this object in another way, expanding or narrowing opportunities to work with it. **Upcasting narrows the list of methods and properties available to this object, and downcasting can extend it.**

A reference is like a remote control to an object. The remote control has more or fewer buttons depending on its type, and the object itself is stored in a heap. When we do casting, we change the type of the remote control but don’t change the object itself.

## **3\. Upcasting**

**Casting from a subclass to a superclass is called upcasting.** Typically, the upcasting is implicitly performed by the compiler.

Upcasting is closely related to inheritance — another core concept in Java. It’s common to use reference variables to refer to a more specific type. And every time we do this, implicit upcasting takes place.

To demonstrate upcasting, let’s define an _Animal_ class:
    
    
    public class Animal {
    
        public void eat() {
            // ... 
        }
    }

Now let’s extend _Animal_ :
    
    
    public class Cat extends Animal {
    
        public void eat() {
             // ... 
        }
    
        public void meow() {
             // ... 
        }
    }

Now we can create an object of _Cat_ class and assign it to the reference variable of type _Cat_ :
    
    
    Cat cat = new Cat();

And we can also assign it to the reference variable of type _Animal_ :
    
    
    Animal animal = cat;

In the above assignment, implicit upcasting takes place.

We could do it explicitly:
    
    
    animal = (Animal) cat;

But there is no need to do explicit cast up the inheritance tree. The compiler knows that _cat_ is an _Animal_ and doesn’t display any errors.

Note that reference can refer to any subtype of the declared type.

Using upcasting, we’ve restricted the number of methods available to _Cat_ instance but haven’t changed the instance itself. Now we can’t do anything that is specific to _Cat_ — we can’t invoke _meow()_ on the _animal_ variable.

Although _Cat_ object remains _Cat_ object, calling _meow()_ would cause the compiler error:
    
    
    // animal.meow(); The method meow() is undefined for the type Animal

To invoke _meow()_ we need to downcast _animal_ , and we’ll do this later.

But now we’ll describe what gives us the upcasting. Thanks to upcasting, we can take advantage of polymorphism.

### **3.1. Polymorphism**

Let’s define another subclass of _Animal_ , a _Dog_ class:
    
    
    public class Dog extends Animal {
    
        public void eat() {
             // ... 
        }
    }

Now we can define the _feed()_ method, which treats all cats and dogs like _animals_ :
    
    
    public class AnimalFeeder {
    
        public void feed(List<Animal> animals) {
            animals.forEach(animal -> {
                animal.eat();
            });
        }
    }

We don’t want _AnimalFeeder_ to care about which _animal_ is on the list — a _Cat_ or a _Dog_. In the _feed()_ method they are all _animals_.

Implicit upcasting occurs when we add objects of a specific type to the _animals_ list:
    
    
    List<Animal> animals = new ArrayList<>();
    animals.add(new Cat());
    animals.add(new Dog());
    new AnimalFeeder().feed(animals);

We add cats and dogs, and they are upcast to _Animal_ type implicitly. Each _Cat_ is an _Animal_ and each _Dog_ is an _Animal_. They’re polymorphic.

By the way, all Java objects are polymorphic because each object is an _Object_ at least. We can assign an instance of _Animal_ to the reference variable of _Object_ type and the compiler won’t complain:
    
    
    Object object = new Animal();

That’s why all Java objects we create already have _Object_ -specific methods, for example _toString()_.

Upcasting to an interface is also common.

We can create _Mew_ interface and make _Cat_ implement it:
    
    
    public interface Mew {
        public void meow();
    }
    
    public class Cat extends Animal implements Mew {
        
        public void eat() {
             // ... 
        }
    
        public void meow() {
             // ... 
        }
    }

Now any _Cat_ object can also be upcast to _Mew_ :
    
    
    Mew mew = new Cat();

_Cat_ is a _Mew_ ; upcasting is legal and done implicitly.

Therefore, _Cat_ is a _Mew_ , _Animal_ , _Object_ and _Cat_. It can be assigned to reference variables of all four types in our example.

### **3.2. Overriding**

In the example above, the _eat()_ method is overridden. This means that although _eat()_ is called on the variable of the _Animal_ type, the work is done by methods invoked on real objects — cats and dogs:
    
    
    public void feed(List<Animal> animals) {
        animals.forEach(animal -> {
            animal.eat();
        });
    }

If we add some logging to our classes, we’ll see that _Cat_ and _Dog_ methods are called:
    
    
    web - 2018-02-15 22:48:49,354 [main] INFO com.baeldung.casting.Cat - cat is eating
    web - 2018-02-15 22:48:49,363 [main] INFO com.baeldung.casting.Dog - dog is eating
    

**To sum up:**

  * A reference variable can refer to an object if the object is of the same type as a variable or if it is a subtype.
  * Upcasting happens implicitly.
  * All Java objects are polymorphic and can be treated as objects of supertype due to upcasting.



## **4\. Downcasting**

What if we want to use the variable of type _Animal_ to invoke a method available only to _Cat_ class? Here comes the downcasting.**It’s the casting from a superclass to a subclass.**

Let’s look at an example:
    
    
    Animal animal = new Cat();

We know that _animal_ variable refers to the instance of _Cat_. And we want to invoke _Cat_ ’s _meow()_ method on the _animal_. But the compiler complains that _meow()_ method doesn’t exist for the type _Animal_.

To call _meow()_ we should downcast _animal_ to _Cat_ :
    
    
    ((Cat) animal).meow();

The inner parentheses and the type they contain are sometimes called the cast operator. Note that external parentheses are also needed to compile the code.

Let’s rewrite the previous _AnimalFeeder_ example with _meow()_ method:
    
    
    public class AnimalFeeder {
    
        public void feed(List<Animal> animals) {
            animals.forEach(animal -> {
                animal.eat();
                if (animal instanceof Cat) {
                    ((Cat) animal).meow();
                }
            });
        }
    }

Now we gain access to all methods available to _Cat_ class. Look at the log to make sure that _meow()_ is actually called:
    
    
    web - 2018-02-16 18:13:45,445 [main] INFO com.baeldung.casting.Cat - cat is eating
    web - 2018-02-16 18:13:45,454 [main] INFO com.baeldung.casting.Cat - meow
    web - 2018-02-16 18:13:45,455 [main] INFO com.baeldung.casting.Dog - dog is eating

Note that in the above example we’re trying to downcast only those objects that are really instances of _Cat_. To do this, we use the operator _instanceof_.

### **4.1._instanceof_ Operator**

We often use _instanceof_ operator before downcasting to check if the object belongs to the specific type:
    
    
    if (animal instanceof Cat) {
        ((Cat) animal).meow();
    }

### **4.2._ClassCastException_**

If we hadn’t checked the type with the _instanceof_ operator, the compiler wouldn’t have complained. But at runtime, there would be an exception.

To demonstrate this, let’s remove the _instanceof_ operator from the above code:
    
    
    public void uncheckedFeed(List<Animal> animals) {
        animals.forEach(animal -> {
            animal.eat();
            ((Cat) animal).meow();
        });
    }

This code compiles without issues. But if we try to run it, we’ll see an exception:

_java.lang.ClassCastException: com.baeldung.casting.Dog_ cannot be cast to _com.baeldung.casting.Cat_

This means that we are trying to convert an object that is an instance of _Dog_ into a _Cat_ instance.

_ClassCastException_ is always thrown at runtime if the type we downcast to doesn’t match the type of the real object.

Note that if we try to downcast to an unrelated type, the compiler won’t allow this:
    
    
    Animal animal;
    String s = (String) animal;

The compiler says “Cannot cast from Animal to String.”

For the code to compile, both types should be in the same inheritance tree.

Let’s sum up:

  * Downcasting is necessary to gain access to members specific to subclass.
  * Downcasting is done using cast operator.
  * To downcast an object safely, we need _instanceof_ operator.
  * If the real object doesn’t match the type we downcast to, then _ClassCastException_ will be thrown at runtime.



## **5._cast()_ Method**

There’s another way to cast objects using the methods of _Class_ :
    
    
    public void whenDowncastToCatWithCastMethod_thenMeowIsCalled() {
        Animal animal = new Cat();
        if (Cat.class.isInstance(animal)) {
            Cat cat = Cat.class.cast(animal);
            cat.meow();
        }
    }

In the above example, _cast(_) and _isInstance()_ methods are used instead of cast and _instanceof_ operators correspondingly.

It’s common to use _cast()_ and _isInstance()_ methods with generic types.

Let’s create _AnimalFeederGeneric <T>_ class with _feed()_ method that “feeds” only one type of animal, cats or dogs, depending on the value of the type parameter:
    
    
    public class AnimalFeederGeneric<T> {
        private Class<T> type;
    
        public AnimalFeederGeneric(Class<T> type) {
            this.type = type;
        }
    
        public List<T> feed(List<Animal> animals) {
            List<T> list = new ArrayList<T>();
            animals.forEach(animal -> {
                if (type.isInstance(animal)) {
                    T objAsType = type.cast(animal);
                    list.add(objAsType);
                }
            });
            return list;
        }
    
    }

The _feed()_ method checks each animal and returns only those that are instances of _T_.

Note that the _Class_ instance should also be passed to the generic class, as we can’t get it from the type parameter _T_. In our example, we pass it in the constructor.

Let’s make _T_ equal to _Cat_ and make sure that the method returns only cats:
    
    
    @Test
    public void whenParameterCat_thenOnlyCatsFed() {
        List<Animal> animals = new ArrayList<>();
        animals.add(new Cat());
        animals.add(new Dog());
        AnimalFeederGeneric<Cat> catFeeder
          = new AnimalFeederGeneric<Cat>(Cat.class);
        List<Cat> fedAnimals = catFeeder.feed(animals);
    
        assertTrue(fedAnimals.size() == 1);
        assertTrue(fedAnimals.get(0) instanceof Cat);
    }

## **6\. Conclusion**

In this foundational tutorial, we’ve explored upcasting, downcasting, how to use them and how these concepts can help you take advantage of polymorphism.
