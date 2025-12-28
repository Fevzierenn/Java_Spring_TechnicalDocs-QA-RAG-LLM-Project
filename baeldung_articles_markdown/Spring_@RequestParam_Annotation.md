# Spring @RequestParam Annotation

## **1\. Overview**

In this quick tutorial, we’ll explore Spring’s _@RequestParam_ annotation and its attributes.

**Simply put, we can use _@RequestParam_ to extract query parameters, form parameters, and even files from the request.**

## **2\. A Simple Mapping**

Let’s say that we have an endpoint _/api/foos_ that takes a query parameter called  _id_ :
    
    
    @GetMapping("/api/foos")
    @ResponseBody
    public String getFoos(@RequestParam String id) {
        return "ID: " + id;
    }

In this example, we used _@RequestParam_ to extract the _id_ query parameter.

A simple GET request would invoke _getFoos_ :
    
    
    http://localhost:8080/spring-mvc-basics/api/foos?id=abc
    ----
    ID: abc

Next, **let’s have a look at the annotation’s attributes:_name_ ,  _value_ ,_required_ , and _defaultValue_.**

## **3\. Specifying the Request Parameter Name**

In the previous example, both the variable name and the parameter name are the same.

**Sometimes we want these to be different, though.** Or, if we aren’t using Spring Boot, we may need to do special compile-time configuration or the parameter names won’t actually be in the bytecode.

Fortunately, **we can configure the _@RequestParam_ name using the _name_ attribute**:
    
    
    @PostMapping("/api/foos")
    @ResponseBody
    public String addFoo(@RequestParam(name = "id") String fooId, @RequestParam String name) { 
        return "ID: " + fooId + " Name: " + name;
    }

We can also do  _@RequestParam(value = “id”)_ or just _@RequestParam(“id”)._

## **4\. Optional Request Parameters**

Method parameters annotated with  _@RequestParam_ are required by default.

This means that if the parameter isn’t present in the request, we’ll get an error:
    
    
    GET /api/foos HTTP/1.1
    -----
    400 Bad Request
    Required String parameter 'id' is not present

**We can configure our _@RequestParam_ to be optional, though, with the _required_ attribute:**
    
    
    @GetMapping("/api/foos")
    @ResponseBody
    public String getFoos(@RequestParam(required = false) String id) { 
        return "ID: " + id;
    }

In this case, both:
    
    
    http://localhost:8080/spring-mvc-basics/api/foos?id=abc
    ----
    ID: abc

and
    
    
    http://localhost:8080/spring-mvc-basics/api/foos
    ----
    ID: null

will correctly invoke the method.

**When the parameter isn’t specified, the method parameter is bound to _null_.**

### 4.1. Using Java 8 _Optional_

Alternatively, we can wrap the parameter in  _[Optional](/java-optional)_ :
    
    
    @GetMapping("/api/foos")
    @ResponseBody
    public String getFoos(@RequestParam Optional<String> id){
        return "ID: " + id.orElseGet(() -> "not provided");
    }

In this case, **we don’t need to specify the _required_ attribute.**

And the default value will be used if the request parameter is not provided:
    
    
    http://localhost:8080/spring-mvc-basics/api/foos 
    ---- 
    ID: not provided

## **5\. A Default Value for the Request Parameter**

We can also set a default value to the _@RequestParam_ by using the _defaultValue_ attribute:
    
    
    @GetMapping("/api/foos")
    @ResponseBody
    public String getFoos(@RequestParam(defaultValue = "test") String id) {
        return "ID: " + id;
    }

**This is like _required=false,_ in that the user no longer needs to supply the parameter**:
    
    
    http://localhost:8080/spring-mvc-basics/api/foos
    ----
    ID: test

Although, we are still okay to provide it:
    
    
    http://localhost:8080/spring-mvc-basics/api/foos?id=abc
    ----
    ID: abc

Note that when we set the  _defaultValue_ attribute,  _required_ is indeed set to _false_.

## **6\. Mapping All Parameters**

**We can also have multiple parameters without defining their names** or count by just using a _Map_ :
    
    
    @PostMapping("/api/foos")
    @ResponseBody
    public String updateFoos(@RequestParam Map<String,String> allParams) {
        return "Parameters are " + allParams.entrySet();
    }

which will then reflect back any parameters sent:
    
    
    curl -X POST -F 'name=abc' -F 'id=123' http://localhost:8080/spring-mvc-basics/api/foos
    -----
    Parameters are {[name=abc], [id=123]}

## **7\. Mapping a Multi-Value Parameter**

A single _@RequestParam_ can have multiple values:
    
    
    @GetMapping("/api/foos")
    @ResponseBody
    public String getFoos(@RequestParam List<String> id) {
        return "IDs are " + id;
    }

**And Spring MVC will map a comma-delimited _id_ parameter**:
    
    
    http://localhost:8080/spring-mvc-basics/api/foos?id=1,2,3
    ----
    IDs are [1,2,3]

**or a list of separate _id_ parameters**:
    
    
    http://localhost:8080/spring-mvc-basics/api/foos?id=1&id=2
    ----
    IDs are [1,2]

## **8\. Conclusion**

In this article, we learned how to use _@RequestParam._
