# The transient Keyword in Java

## 1\. Introduction

In this article, we’ll first understand the _transient_ keyword and then see its behavior through examples for different data types on how they behave.

## 2\. Usage of _transient_

Let’s first understand the serialization before moving to _transient_ as it is used in the context of serialization.

**[Serialization](/java-serialization) is the process of converting an object into a byte stream, and de-serialization is the opposite of it**.

**When we mark any variable as _transient,_ then that variable is not serialized**. Since _transient_ fields aren’t present in the serialized form of an object, the de-serialization process would use the default values (which are null or 0) for such fields when creating an object out of the serialized form.8

The _transient_ keyword is useful in a few scenarios:

  * We can use it for derived fields
  * It is useful for fields that do not represent the state of the object
  * We use it for any non-serializable references
  * When we want to store sensitive information and don’t want to send it through the network



## 3\. Example

To see it in action, let’s first create a _Book_ class whose object we would like to serialize:
    
    
    public class Book implements Serializable {
        private static final long serialVersionUID = -2936687026040726549L;
        private String bookName;
        private transient String description;
        private transient int copies;
        
        // getters and setters
    }

Here, we have marked _description_ and _copies_ as _transient_ fields.

After creating the class, we’ll create an object of this class:
    
    
    Book book = new Book();
    book.setBookName("Java Reference");
    book.setDescription("will not be saved");
    book.setCopies(25);

Now, we’ll serialize the object into a file:
    
    
    public static void serialize(Book book) throws Exception {
        FileOutputStream file = new FileOutputStream(fileName);
        ObjectOutputStream out = new ObjectOutputStream(file);
        out.writeObject(book);
        out.close();
        file.close();
    }

Let’s deserialize the object now from the file:
    
    
    public static Book deserialize() throws Exception {
        FileInputStream file = new FileInputStream(fileName);
        ObjectInputStream in = new ObjectInputStream(file);
        Book book = (Book) in.readObject();
        in.close();
        file.close();
        return book;
    }

Finally, we’ll verify the values of the _book_ object:
    
    
    assertEquals("Java Reference", book.getBookName());
    assertNull(book.getDescription());
    assertEquals(0, book.getCopies());

Here we see that _bookName_ has been properly persisted. On the other hand, the _copies_ field has value _0_ and the _description_ is _null –_ the default values for their respective data types – instead of the original values.

## 4\. Behavior With _final_

Now, let’s see a case where we’ll use _transient_ with the _final_ keyword. For that, first, we’ll add a _final transient_ element in our _Book_ class and then create an empty _Book_ object:
    
    
    public class Book implements Serializable {
        // existing fields    
        
        private final transient String bookCategory = "Fiction";
    
        // getters and setters
    }
    
    
    Book book = new Book();

**The final modifier makes no difference when it has literal initialization.** When a variable of type String is declared as final and transient, its value is determined at compile-time and is stored in the class’s constant pool. Since it is final, it’s value can’t be change after it’s initialization. Hence, its value will be taken from the class and not null.

_For more information on String pool, head over to our article[Guide to Java String Pool](/java-string-pool)._
    
    
    assertEquals("Fiction", book.getBookCategory());

## 4.1. Behavior With _final String U_ sing _new_ Operator __

Now let’s see a case where we’ll use transient with the final keyword. For that, we’ll create a variable String with final and transient and using new operator in our Book class and then create an empty Book object:
    
    
    public class Book implements Serializable {
        // existing fields    
        
        private final transient String bookCategoryNewOperator = new String("Fiction with new Operator");
    
        // getters and setters
    }
    
    
    Book book = new Book();

In this case, using a **new operator** to initialize a String will create the object in the Heap memory and the default value for this object when we deserialize will be **null**.
    
    
    assertNull(book.getBookCategoryNewOperator());

## 5\. Conclusion

In this article, we saw the usage of the _transient_ keyword and its behavior in serialization and de-serialization, with some useful examples that contain examples that are not obvious, e.g Strings with transient.
