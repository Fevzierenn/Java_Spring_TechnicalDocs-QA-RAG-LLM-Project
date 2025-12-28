# Introduction to Spring AOP

## **1\. Introduction**

In this tutorial, we’ll introduce AOP (Aspect Oriented Programming) with Spring, and learn how we can use this powerful tool in practical scenarios.

It’s also possible to leverage [AspectJ’s annotations](/aspectj) when developing with Spring AOP, but in this article, we’ll focus on the core Spring AOP XML-based configuration.  


## **2\. Overview**

**AOP is a programming paradigm that aims to increase modularity by allowing the separation of cross-cutting concerns.** It does this by adding additional behavior to existing code without modifying the code itself.

Instead, we can declare the new code and the new behaviors separately.

Spring’s [AOP framework](https://docs.spring.io/spring/docs/current/spring-framework-reference/core.html#aop) helps us implement these cross-cutting concerns.

## **3\. Maven Dependencies**

Let’s start by adding Spring’s AOP library dependency in the _pom.xml_ :
    
    
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
    </parent>
     
    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-aop</artifactId>
        </dependency>
    </dependencies>

The latest version of the dependency can be checked [here](https://mvnrepository.com/artifact/org.springframework.boot/spring-boot-starter-aop).

## **4\. AOP Concepts and Terminology**

Let’s briefly go over the concepts and terminology specific to AOP:

[![Program Execution](/wp-content/uploads/2017/11/Program_Execution.jpg)](/wp-content/uploads/2017/11/Program_Execution.jpg)

### **4.1. Business Object**

A business object is a normal class that has a normal business logic. Let’s look at a simple example of a business object where we just add two numbers:
    
    
    public class SampleAdder {
        public int add(int a, int b) {
            return a + b;
        }
    }
    

Note that this class is a normal class with business logic, without any Spring-related annotations.

### **4.2. Aspect**

An aspect is a modularization of a concern that cuts across multiple classes. Unified logging can be an example of such cross-cutting concern.

Let’s see how we define a simple Aspect:
    
    
    public class AdderAfterReturnAspect {
        private Logger logger = LoggerFactory.getLogger(this.getClass());
        public void afterReturn(Object returnValue) throws Throwable {
            logger.info("value return was {}",  returnValue);
        }
    }
    

In the above example, we defined a simple Java class that has a method called _afterReturn,_ which takes one argument of type _Object_ and logs in that value. Note that even our _AdderAfterReturnAspect_ is a standard class, free of any Spring annotations.

In the next sections, we’ll see how we can wire this Aspect to our Business Object.

### **4.3._Joinpoint_**

**A _Joinpoint_ is a point during the execution of a program, such as the execution of a method or the handling of an exception.**

In Spring AOP, a _JoinPoint_ always represents a method execution.

### **4.4._Pointcut_**

A _Pointcut_ is a predicate that helps match an _Advice_ to be applied by an _Aspect_ at a particular _JoinPoint_.

We often associate the _Advice_ with a _Pointcut_ expression, and it runs at any _Joinpoint_ matched by the _Pointcut_.

### **4.5._Advice_**

An _Advice_ is an action taken by an aspect at a particular _Joinpoint_. Different types of advice include _“around,” “before,”_ and _“after.”_

In Spring, an _Advice_ is modelled as an interceptor, maintaining a chain of interceptors around the _Joinpoint_.

### **4.6. Wiring Business Object and Aspect**

Now let’s look at how we can wire a Business Object to an Aspect with an After-Returning advice.

Below is the config excerpt that we’d place in a standard Spring config in the _“ <beans>”_ tag:
    
    
    <bean id="sampleAdder" class="org.baeldung.logger.SampleAdder" />
    <bean id="doAfterReturningAspect" 
      class="org.baeldung.logger.AdderAfterReturnAspect" />
    <aop:config>
        <aop:aspect id="aspects" ref="doAfterReturningAspect">
           <aop:pointcut id="pointCutAfterReturning" expression=
             "execution(* org.baeldung.logger.SampleAdder+.*(..))"/>
           <aop:after-returning method="afterReturn"
             returning="returnValue" pointcut-ref="pointCutAfterReturning"/>
        </aop:aspect>
    </aop:config>
    

As we can see, we defined a simple bean called _simpleAdder,_ which represents an instance of a Business Object. In addition, we created an instance of an Aspect called _AdderAfterReturnAspect_.

Of course, XML isn’t our only option here; as mentioned before, [AspectJ](/aspectj) annotations are fully supported as well.

### **4.7. Configuration at Glance**

We can use tag _aop:config_ for defining AOP-related configuration. **Within the _config_ tag, we define the class that represents an aspect.** Then we give it a reference of _“doAfterReturningAspect,”_ an aspect bean that we created.

Next we define a Pointcut using the _pointcut_ tag. The pointcut used in the example above is _execution(* org.baeldung.logger.SampleAdder+.*(..)),_ which means apply an advice on any method within the _SampleAdder_ class that accepts any number of arguments and returns any value type.

Then we define which advice we want to apply. In the above example, we applied the after-returning advice. We defined this in our Aspect _AdderAfterReturnAspect_ by executing the _afterReturn_ method that we defined using the attribute method.

This advice within Aspect takes one parameter of type _Object._ The parameter gives us an opportunity to take an action before and/or after the target method call. In this case, we just log the method’s return value.

Spring AOP supports multiple types of advice using annotation-based config. This and more examples can be found [here](/spring-aop-advice-tutorial) and [here](/spring-aop-pointcut-tutorial).

## **5\. Conclusion**

In this article, we illustrated the concepts used in AOP. We also looked at examples of using the AOP module of Spring. If we want to learn more about AOP, we can look at the following resources:

  * [An introduction to AspectJ](/aspectj)
  * [Implementing a Custom Spring AOP Annotation](/spring-aop-annotation)
  * [An introduction to Pointcut Expressions in Spring](/spring-aop-pointcut-tutorial)
  * [Comparing Spring AOP and AspectJ](/spring-aop-vs-aspectj)
  * [An introduction to Advice Types in Spring](/spring-aop-advice-tutorial)


