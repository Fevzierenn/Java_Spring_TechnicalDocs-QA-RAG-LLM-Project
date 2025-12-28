# Checked and Unchecked Exceptions in Java

## 1\. Overview

[Java exceptions](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/Exception.html) fall into two main categories: **checked exceptions and unchecked exceptions.**

In this tutorial, we’ll provide some code samples on how to use them.

## 2\. Checked Exceptions

In general, checked exceptions represent errors outside the control of the program. For example, the constructor of [_FileInputStream_](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/io/FileInputStream.html#%3Cinit%3E\(java.io.File\)) throws _FileNotFoundException_ if the input file does not exist.

**Java verifies checked exceptions at compile-time.**

Therefore, we should use the [_throws_](/java-throw-throws) keyword to declare a checked exception:
    
    
    private static void checkedExceptionWithThrows() throws FileNotFoundException {
        File file = new File("not_existing_file.txt");
        FileInputStream stream = new FileInputStream(file);
    }

We can also use a _try-catch_ block to handle a checked exception:
    
    
    private static void checkedExceptionWithTryCatch() {
        File file = new File("not_existing_file.txt");
        try {
            FileInputStream stream = new FileInputStream(file);
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }
    }

Some [common checked exceptions](/java-common-exceptions) in Java are _IOException_ , _SQLException_ and _ParseException_.

The [_Exception_](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/Exception.html) class is the superclass of checked exceptions, so we can [create a custom checked exception](/java-new-custom-exception) by extending _Exception_ :
    
    
    public class IncorrectFileNameException extends Exception {
        public IncorrectFileNameException(String errorMessage) {
            super(errorMessage);
        }
    }
    

## 3\. Unchecked Exceptions

If a program throws an unchecked exception, it reflects some error inside the program logic.

For example, if we divide a number by 0, Java will throw _ArithmeticException_ :
    
    
    private static void divideByZero() {
        int numerator = 1;
        int denominator = 0;
        int result = numerator / denominator;
    }
    

**Java does not verify unchecked exceptions at compile-time.** Furthermore, we don’t have to declare unchecked exceptions in a method with the _throws_ keyword. And although the above code does not have any errors during compile-time, it will throw _ArithmeticException_ at runtime.

Some [common unchecked exceptions](/java-common-exceptions) in Java are _NullPointerException_ , _ArrayIndexOutOfBoundsException_ and _IllegalArgumentException_.

The _[RuntimeException](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/RuntimeException.html) _class is the superclass of all unchecked exceptions, so we can [create a custom unchecked exception](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/Exception.html) by extending _RuntimeException_ :
    
    
    public class NullOrEmptyException extends RuntimeException {
        public NullOrEmptyException(String errorMessage) {
            super(errorMessage);
        }
    }

## 4\. When to Use Checked Exceptions and Unchecked Exceptions

It’s a good practice to use exceptions in Java so that we can separate error-handling code from regular code. However, we need to decide which type of exception to throw. The [Oracle Java Documentation](https://docs.oracle.com/javase/tutorial/essential/exceptions/runtime.html) provides guidance on when to use checked exceptions and unchecked exceptions:

“If a client can reasonably be expected to recover from an exception, make it a checked exception. If a client cannot do anything to recover from the exception, make it an unchecked exception.”

For example, before we open a file, we can first validate the input file name. If the user input file name is invalid, we can throw a custom checked exception:
    
    
    if (!isCorrectFileName(fileName)) {
        throw new IncorrectFileNameException("Incorrect filename : " + fileName );
    }
    

In this way, we can recover the system by accepting another user input file name.

However, if the input file name is a null pointer or it is an empty string, it means that we have some errors in the code. In this case, we should throw an unchecked exception:
    
    
    if (fileName == null || fileName.isEmpty())  {
        throw new NullOrEmptyException("The filename is null or empty.");
    }
    

## 5\. Conclusion

In this article, we discussed the difference between checked and unchecked exceptions. We also provided some code examples to show when to use checked or unchecked exceptions.
