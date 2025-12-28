# Create a Custom Exception in Java

## **1\. Overview**

In this tutorial, we’ll cover **how to create a custom exception in Java.**

We’ll show how user-defined exceptions are implemented and used for both checked and unchecked exceptions.

## **2\. The Need for Custom Exceptions**

Java exceptions cover almost all general exceptions that are bound to happen in programming.

However, we sometimes need to supplement these standard exceptions with our own.

These are the main reasons for introducing custom exceptions:

  * Business logic exceptions – exceptions that are specific to the business logic and workflow. These help the application users or the developers understand what the exact problem is.
  * To catch and provide specific treatment to a subset of existing Java exceptions



Java exceptions can be checked and unchecked. In the next sections, we’ll cover both of these cases.

## **3\. Custom Checked Exception**

Checked exceptions are exceptions that need to be treated explicitly.

Let’s consider a piece of code that returns the first line of the file:
    
    
    try (Scanner file = new Scanner(new File(fileName))) {
        if (file.hasNextLine()) return file.nextLine();
    } catch(FileNotFoundException e) {
        // Logging, etc 
    }
    

The code above is a classic way of handling Java checked exceptions. While the code throws _FileNotFoundException_ , it’s not clear what the exact cause is — whether the file doesn’t exist or the file name is invalid.

**To create a custom exception, we have to extend the _java.lang.Exception_ class.**

Let’s see an example of this by creating a custom checked exception called _IncorrectFileNameException_ :
    
    
    public class IncorrectFileNameException extends Exception { 
        public IncorrectFileNameException(String errorMessage) {
            super(errorMessage);
        }
    }
    

Note that we also have to provide a constructor that takes a _String_ as the error message and called the parent class constructor.

**This is all we need to do to define a custom exception.**

Next, let’s see how we can use the custom exception in our example:
    
    
    try (Scanner file = new Scanner(new File(fileName))) {
        if (file.hasNextLine())
            return file.nextLine();
    } catch (FileNotFoundException e) {
        if (!isCorrectFileName(fileName)) {
            throw new IncorrectFileNameException("Incorrect filename : " + fileName );
        }
        //...
    }
    

We’ve created and used a custom exception, so the user can now know what the exact exception is.

Is this enough? We are consequently **losing the root cause of the exception.**

To fix this, we can also add a  _java.lang.Throwable_ parameter to the constructor. This way, we can pass the root exception to the method call:
    
    
    public IncorrectFileNameException(String errorMessage, Throwable err) {
        super(errorMessage, err);
    }
    

Now the _IncorrectFileNameException_ is used along with the root cause of the exception:
    
    
    try (Scanner file = new Scanner(new File(fileName))) {
        if (file.hasNextLine()) {
            return file.nextLine();
        }
    } catch (FileNotFoundException err) {
        if (!isCorrectFileName(fileName)) {
            throw new IncorrectFileNameException(
              "Incorrect filename : " + fileName , err);
        }
        // ...
    }
    

This is how we can use custom exceptions **without losing the root cause from which they occurred.**

## **4\. Custom Unchecked Exception**

In our same example, let’s assume that we need a custom exception if the file name doesn’t contain any extension.

In this case, we’ll need a custom unchecked exception similar to the previous one, as this error will only be detected during runtime.

**To create a custom unchecked exception, we need to extend the _java.lang.RuntimeException_ class**:
    
    
    public class IncorrectFileExtensionException 
      extends RuntimeException {
        public IncorrectFileExtensionException(String errorMessage, Throwable err) {
            super(errorMessage, err);
        }
    }
    

This way, we can use this custom unchecked exception in our example:
    
    
    try (Scanner file = new Scanner(new File(fileName))) {
        if (file.hasNextLine()) {
            return file.nextLine();
        } else {
            throw new IllegalArgumentException("Non readable file");
        }
    } catch (FileNotFoundException err) {
        if (!isCorrectFileName(fileName)) {
            throw new IncorrectFileNameException(
              "Incorrect filename : " + fileName , err);
        }
        
        //...
    } catch(IllegalArgumentException err) {
        if(!containsExtension(fileName)) {
            throw new IncorrectFileExtensionException(
              "Filename does not contain extension : " + fileName, err);
        }
        
        //...
    }
    

## **5\. Conclusion**

Custom exceptions are very useful when we need to handle specific exceptions related to the business logic. When used properly, they can serve as a practical tool for better exception handling and logging.
