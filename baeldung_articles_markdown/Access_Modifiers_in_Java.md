# Access Modifiers in Java

## **1\. Overview**

In this tutorial, we’ll discuss access modifiers in Java, which are used for setting the access level to classes, variables, methods, and constructors.

**Simply put, there are four access modifiers:** _public_ , _private_ , _protected,_ and _default_ (no keyword).

Before we begin, please note that a top-level class can only use _public_ or _default_ access modifiers. At the member level, we can use all four.

## **2\. Default**

When we don’t use any keyword explicitly, Java will set a _default_ access to a given class, method, or property. The default access modifier is also called _package-private_ , which means that**all members are visible within the same package,** but aren’t accessible from other packages:
    
    
    package com.baeldung.accessmodifiers;
    
    public class SuperPublic {
        static void defaultMethod() {
            ...
        }
    }

_defaultMethod()_ is accessible in another class of the same package:
    
    
    package com.baeldung.accessmodifiers;
    
    public class Public {
        public Public() {
            SuperPublic.defaultMethod(); // Available in the same package.
        }
    }

However, it’s not available in other packages.

## **3\. Public**

If we add the  _public_ keyword to a class, method, or property, then **we’re making it available to the whole world** (i.e. all other classes in all packages will be able to use it). This is the least restrictive access modifier:
    
    
    package com.baeldung.accessmodifiers;
    
    public class SuperPublic {
        public static void publicMethod() {
            ...
        }
    }

_publicMethod()_ is available in another package:
    
    
    package com.baeldung.accessmodifiers.another;
    
    import com.baeldung.accessmodifiers.SuperPublic;
    
    public class AnotherPublic {
        public AnotherPublic() {
            SuperPublic.publicMethod(); // Available everywhere. Let's note different package.
        }
    }

For more details on how the _public_ keyword behaves when applied to a class, interface, nested public class, or interface and method, see this [dedicated article](/java-public-keyword).

## **4\. Private**

Any method, property, or constructor with the _private_ keyword **is accessible from the same class only**. This is the most restrictive access modifier, and is core to the concept of encapsulation. All data will be hidden from the outside world:
    
    
    package com.baeldung.accessmodifiers;
    
    public class SuperPublic {
        static private void privateMethod() {
            ...
        }
        
         private void anotherPrivateMethod() {
             privateMethod(); // available in the same class only.
        }
    }

This more [detailed article](/java-private-keyword) will show how the _private_ keyword behaves when applied to a field, constructor, method, or inner class.

## **5\. Protected**

Between _public_ and _private_ access levels, there’s the  _protected_ access modifier.

If we declare a method, property, or constructor with the _protected_ keyword, we can access the member from the **same package (as with _package-private_ access level), as well as from all subclasses of its class**, even if they lie in other packages:
    
    
    package com.baeldung.accessmodifiers;
    
    public class SuperPublic {
        static protected void protectedMethod() {
            ...
        }
    }

_protectedMethod()_ is available in subclasses (regardless of the package):
    
    
    package com.baeldung.accessmodifiers.another;
    
    import com.baeldung.accessmodifiers.SuperPublic;
    
    public class AnotherSubClass extends SuperPublic {
        public AnotherSubClass() {
            SuperPublic.protectedMethod(); // Available in subclass. Let's note different package.
        }
    }

This [dedicated article](/java-protected-access-modifier) describes more about the keyword when used in a field, method, constructor, and inner class, as well as the accessibility in the same package or a different package.

## **6\. Comparison**

The table below summarizes the available access modifiers. We can see that a class, regardless of the access modifiers used, always has access to its members:

Modifier | Class | Package | Subclass | World  
---|---|---|---|---  
public | Y | Y | Y | Y  
protected | Y | Y | Y | N  
default | Y | Y | N | N  
private | Y | N | N | N  
  
## 7\. Canonical Order of Modifiers

The order of modifiers isn’t strictly enforced in Java. However, the Java Language Specification (JLS) recommends a standard canonical order. This recommended order can ensure consistency across codebases and improve readability.

The canonical order applies to the field, methods, classes, and modules. Here’s a customary recommendation for field modifiers:

  * Annotation
  * _public_ /_protected_ /_private_
  * _static_
  * _final_
  * _transient_
  * _volatile_



The annotation comes first, then one of the access modifiers and other keywords. For example, let’s declare a constant with value of _1_ :
    
    
    @Id
    private static final long ID = 1;

The code above adopts the [canonical order](/java-static-final-order) as specified in the JLS.

Also, the JLS makes a recommendation for specifying class modifiers:

  * Annotation
  * _public_ /_protected_ /_private_
  * _abstract_
  * _static_
  * _final_
  * _strictfp_



Like field modifiers, the annotation comes first, then the access modifier and other keywords.

Finally, here’s the canonical order of modifiers for method declaration as recommended by JLS:

  * Annotation
  * _public_ /_protected_ /_private_
  * _abstract_
  * _static_
  * _final_
  * _synchronized_
  * _native_
  * _strictfp_



Importantly, not all modifiers can be used together. For instance, _public_ , _protected_ , and _private_ are mutually exclusive.

Also, IDEs like [IntelliJ](/intellij-basics) can automatically arrange modifiers in the canonical order when we apply formatting. This feature helps maintain consistency and adheres to the JLS recommendation.

## **8\. Conclusion**

In this brief article, we focused on access modifiers in Java.

It’s good practice to use the most restrictive access level possible for any given member to prevent misuse. We should always use the  _private_ access modifier unless there’s a good reason not to.

_Public_ access level should only be used if a member is part of an API.
