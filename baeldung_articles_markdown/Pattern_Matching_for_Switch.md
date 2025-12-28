# Pattern Matching for Switch

## 1\. Overview

Before pattern matching, _switch_ cases supported only simple testing of a selector expression that needs to match a constant value exactly. The Java SE 21 release introduces pattern matching for _switch_ expressions and statements ([JEP 441](https://openjdk.org/jeps/441)) as a permanent feature. Pattern matching **provides us more flexibility when defining conditions for _switch_ selector expressions and cases**.

We can use patterns (e.g., _Integer i_ , _String s_) in case labels. Furthermore, we can use a selector expression of any reference type (e.g., _ArrayList_ , _Stack_) in addition to the already supported types. Additionally, we can match _null_ in _case_ labels. We can include a _when_ clause after a case label for conditional matching. Further, when we use a _when_ clause it is called guarded pattern matching.

Java SE 24 adds support for primitive type patterns (e.g., _int i_ , _long l_) in _case_ labels as a Preview language feature.

In this tutorial, we’ll cover how we can use pattern matching in _switch_. We’ll also explore some _switch_ specifics, like covering all values, ordering subclasses, and handling null values.

## 2\. Switch Statement

We use [_switch_ ](/java-switch)in Java as a control-flow statement to transfer control to one of the several predefined _case_ statements. The _switch_ statement matches the _case_ label depending on the value of the selector expression.

In the earlier versions of Java, the**selector expression had to be a number, a string, or a constant**. Also, the _case_ labels could only contain constants:
    
    
    final String b = "B";
    switch (args[0]) {
        case "A" -> System.out.println("Parameter is A");
        case b -> System.out.println("Parameter is b");
        default -> System.out.println("Parameter is unknown");
    };

In our example, if variable b wasn’t _final_ , the compiler would throw a constant expression required error.

## 3\. Pattern Matching

Pattern matching, in general, was first introduced as a preview feature in Java SE 14. Further, a type pattern consists of a type name and the variable to bind the result to. **Applying type patterns to the _[instanceof](/java-instanceof#:~:text=instanceof%20is%20a%20binary%20operator,check%20should%20always%20be%20used.) _operator simplifies type checking and casting**. Moreover, it enables us to combine both into a single expression:
    
    
    if (o instanceof String s) {
        System.out.printf("Object is a string %s", s);
    } else if (o instanceof Number n) {
        System.out.printf("Object is a number %n", n);
    }

This built-in language enhancement helps us write less code with enhanced readability. [Pattern matching for _instanceof_](/java-pattern-matching-instanceof) became a permanent feature in Java SE 16.

## 4\. Patterns for Switch

Java SE 17 introduced pattern matching for the _switch_ expressions and statements. Subsequently, Java SE 18, 19, and 20 refined it, and Java SE 21 made it a permanent feature.

### 4.1. Type Pattern

Let’s look at how we can apply type patterns and the _instanceof_ operator in _switch_ statements. As an example, we’ll create a method that converts different types to _double_ using _if-else_ statements. Our method will simply return zero if the type is not supported:
    
    
    static double getDoubleUsingIf(Object o) {
        double result;
        if (o instanceof Integer) {
            result = ((Integer) o).doubleValue();
        } else if (o instanceof Float) {
            result = ((Float) o).doubleValue();
        } else if (o instanceof String) {
            result = Double.parseDouble(((String) o));
        } else {
            result = 0d;
        }
        return result;
    }

We can solve the same problem with less code using type patterns in _switch_ :
    
    
    static double getDoubleUsingSwitch(Object o) {
        return switch (o) {
            case Integer i -> i.doubleValue();
            case Float f -> f.doubleValue();
            case String s -> Double.parseDouble(s);
            default -> 0d;
        };
    }

In earlier versions of Java, the selector expression was limited to only a few types; integral primitive types (excluding _long_), their corresponding boxed forms, enum types, and _String_. However, with type patterns, **the _switch_ selector expression can be of any reference type in addition to the already supported types**.

### 4.2. Guarded Pattern

Type patterns help us transfer control based on a particular type. However, sometimes, we also need to **perform additional checks on the passed value**.

For example, we may use an _if_ statement to check the length of a _String_ :
    
    
    static double getDoubleValueUsingIf(Object o) {
        return switch (o) {
            case String s -> {
                if (s.length() > 0) {
                    yield Double.parseDouble(s);
                } else {
                    yield 0d;
                }
            }
            default -> 0d;
        };
    }

We can solve the same problem using guarded patterns. They use a combination of a pattern and a _when_ clause:
    
    
    static double getDoubleValueUsingGuardedPatterns(Object o) {
        return switch (o) {
            case String s when s.length() > 0 -> Double.parseDouble(s);
            default -> 0d;
        };
    }

**Guarded patterns enable us to avoid additional _if_ conditions in _switch_ statements. Instead, we can** **move our conditional logic to the case label**.

### 4.3. Primitive Type Pattern

We can use a primitive type pattern in _switch_ _case_ labels as a preview feature in Java SE 24. For example, we use primitive type patterns along with a guarded pattern:
    
    
    void primitiveTypePatternExample() {
        Random r=new Random();
        switch (r.nextInt()) {
            case 1 -> System.out.println("int is 1");
            case int i when i > 1 && i < 100 -> System.out.println("int is greater than 1 and less than 100");
            default -> System.out.println("int is greater or equal to 100");
        }
    }

We can use a selector expression of any primitive type including type _long_ , _float_ , _double_ , and _boolean_ , as well as the corresponding boxed types.

## 5\. Switch Specifics

Let’s now look at a couple of specific cases to consider while using pattern matching in _switch_.

### 5.1. Covering All Values

When using pattern matching in _switch_ , the Java **compiler will check the type coverage**.

Let’s consider an example _switch_ condition accepting any object but covering only the _String_ case:
    
    
    static double getDoubleUsingSwitch(Object o) {
        return switch (o) {
            case String s -> Double.parseDouble(s);
        };
    }

Our example will result in the following compilation error:
    
    
    [ERROR] Failed to execute goal ... Compilation failure
    [ERROR] /D:/Projects/.../HandlingNullValuesUnitTest.java:[10,16] the switch expression does not cover all possible input values

This is because the _switch_ **case labels are required to cover all possible input values; in this example all _Object_ types**.

The _default_ case label may also be applied instead of a specific selector type.

### 5.2. Ordering Subclasses

When using subclasses with pattern matching in _switch_ , the **order of the cases matters**.

Let’s consider an example where the _String_ case comes after the _CharSequence_ case.
    
    
    static double getDoubleUsingSwitch(Object o) {
        return switch (o) {
            case CharSequence c -> Double.parseDouble(c.toString());
            case String s -> Double.parseDouble(s);
            default -> 0d;
        };
    }

Since _String_ is a subclass of _CharSequence,_ our example will result in the following compilation error:
    
    
    [ERROR] Failed to execute goal ... Compilation failure
    [ERROR] /D:/Projects/.../HandlingNullValuesUnitTest.java:[12,18] this case label is dominated by a preceding case label

The reasoning behind this error is that**there is no chance that the execution goes to the second case** since any string object passed to the method would be handled in the first case itself.

### 5.3. Handling Null Values

In earlier versions of Java, each passing of a _null_ value to a _switch_ statement would result in a _NullPointerException_.

However, with type patterns, it is now possible to**apply the null check as a separate case label** :
    
    
    static double getDoubleUsingSwitch(Object o) {
        return switch (o) {
            case String s -> Double.parseDouble(s);
            case null -> 0d;
            default -> 0d;
        };
    }

We should note that a _switch_ expression cannot have both a _default_ case and a total type (selector expression type that covers all possible input values) case.

Such a _switch_ statement will result in the following compilation error:
    
    
    [ERROR] Failed to execute goal ... Compilation failure
    [ERROR] /D:/Projects/.../HandlingNullValuesUnitTest.java:[14,13] switch has both a total pattern and a default label

Finally, a _switch_ statement using pattern matching can still throw a _NullPointerException_.

However, it can do so only when the _switch_ block doesn’t have a null-matching case label.

## 6\. Conclusion

In this article,**we explored pattern matching for _switch_ expressions and statements, a new feature in _Java SE 21_** _._ We saw that by using patterns in case labels selection is determined by pattern matching rather than a simple equality check. We also discussed the support for primitive type patterns in Java SE 24.

In the examples, we covered how pattern types can be applied in _switch_ statements. Finally, we explored a couple of specific cases, including covering all values, ordering subclasses, and handling null values.

****
