# Spring RequestMapping

## **1\. Overview**

In this tutorial, we’ll focus on one of the main annotations in **Spring MVC:_@RequestMapping._**

Simply put, the annotation is used to map web requests to Spring Controller methods.

## **2\. @_RequestMapping_ Basics**

We start with a simple example: mapping an HTTP request to a method using some basic criteria. Let’s consider that Spring serves content on the root [context path](/spring-boot-context-path) (“/”) by default. All the CURL requests in this article rely on the default root context path.

### **2.1._@RequestMapping_ — by Path**
    
    
    @RequestMapping(value = "/ex/foos", method = RequestMethod.GET)
    @ResponseBody
    public String getFoosBySimplePath() {
        return "Get some Foos";
    }

To test out this mapping with a simple _curl_ command, run:
    
    
    curl -i http://localhost:8080/ex/foos

### **2.2._@RequestMapping_ — the HTTP Method**

The HTTP _method_ parameter has **no default.** So, if we don’t specify a value, it’s going to map to any HTTP request.

Here’s a simple example, similar to the previous one, but this time mapped to an HTTP POST request:
    
    
    @RequestMapping(value = "/ex/foos", method = POST)
    @ResponseBody
    public String postFoos() {
        return "Post some Foos";
    }

To test the POST via a _curl_ command:
    
    
    curl -i -X POST http://localhost:8080/ex/foos

## **3._RequestMapping_ and HTTP Headers**

### **3.1._@RequestMapping_ With the _headers_ Attribute**

The mapping can be narrowed even further by specifying a header for the request:
    
    
    @RequestMapping(value = "/ex/foos", headers = "key=val", method = GET)
    @ResponseBody
    public String getFoosWithHeader() {
        return "Get some Foos with Header";
    }

To test the operation, we’re going to use the _curl_ header support:
    
    
    curl -i -H "key:val" http://localhost:8080/ex/foos

and even multiple headers via the _headers_ attribute of _@RequestMapping_ :
    
    
    @RequestMapping(
      value = "/ex/foos", 
      headers = { "key1=val1", "key2=val2" }, method = GET)
    @ResponseBody
    public String getFoosWithHeaders() {
        return "Get some Foos with Header";
    }

We can test this with the command:
    
    
    curl -i -H "key1:val1" -H "key2:val2" http://localhost:8080/ex/foos

Note that for the _curl_ syntax, a colon separates the header key and the header value, the same as in the HTTP spec, while in Spring, the equals sign is used.

### **3.2._@RequestMapping_ Consumes and Produces**

Mapping **media types produced by a controller** method is worth special attention.

We can map a request based on its _Accept_ header via the _@RequestMapping_ _headers_ attribute introduced above:
    
    
    @RequestMapping(
      value = "/ex/foos", 
      method = GET, 
      headers = "Accept=application/json")
    @ResponseBody
    public String getFoosAsJsonFromBrowser() {
        return "Get some Foos with Header Old";
    }

The matching for this way of defining the _Accept_ header is flexible — it uses contains instead of equals, so a request such as the following would still map correctly:
    
    
    curl -H "Accept:application/json,text/html" 
      http://localhost:8080/ex/foos

Starting with Spring 3.1, the **_@RequestMapping_ annotation now has the _produces_ and _consumes_ attributes**, specifically for this purpose:
    
    
    @RequestMapping(
      value = "/ex/foos", 
      method = RequestMethod.GET, 
      produces = "application/json"
    )
    @ResponseBody
    public String getFoosAsJsonFromREST() {
        return "Get some Foos with Header New";
    }

Also, the old type of mapping with the _headers_ attribute will automatically be converted to the new _produces_ mechanism starting with Spring 3.1, so the results will be identical.

This is consumed via _curl_ in the same way:
    
    
    curl -H "Accept:application/json" 
      http://localhost:8080/ex/foos

Additionally, _produces_ supports multiple values as well:
    
    
    @RequestMapping(
      value = "/ex/foos", 
      method = GET,
      produces = { "application/json", "application/xml" }
    )

Keep in mind that these — the old and new ways of specifying the _Accept_ header — are basically the same mapping, so Spring won’t allow them together.

Having both these methods active would result in:
    
    
    Caused by: java.lang.IllegalStateException: Ambiguous mapping found. 
    Cannot map 'fooController' bean method 
    java.lang.String 
    org.baeldung.spring.web.controller
      .FooController.getFoosAsJsonFromREST()
    to 
    { [/ex/foos],
      methods=[GET],params=[],headers=[],
      consumes=[],produces=[application/json],custom=[]
    }: 
    There is already 'fooController' bean method
    java.lang.String 
    org.baeldung.spring.web.controller
      .FooController.getFoosAsJsonFromBrowser() 
    mapped.

A final note on the new _produces_ and _consumes_ mechanisms, which behave differently from most other annotations: When specified at the type level, **the method-level annotations do not complement but override** the type-level information.

And of course, if you want to dig deeper into building a REST API with Spring, [check out**the new REST with Spring course**](/rest-with-spring-course).

## **4._RequestMapping_ With Path Variables**

Parts of the mapping URI can be bound to variables via the _@PathVariable_ annotation.

### **4.1. Single _@PathVariable_**

A simple example with a single path variable:
    
    
    @RequestMapping(value = "/ex/foos/{id}", method = GET)
    @ResponseBody
    public String getFoosBySimplePathWithPathVariable(
      @PathVariable("id") long id) {
        return "Get a specific Foo with id=" + id;
    }

This can be tested with _curl_ :
    
    
    curl http://localhost:8080/ex/foos/1

If the name of the method parameter matches the name of the path variable exactly, then this can be simplified by **using _@PathVariable_ with no value**:
    
    
    @RequestMapping(value = "/ex/foos/{id}", method = GET)
    @ResponseBody
    public String getFoosBySimplePathWithPathVariable(
      @PathVariable String id) {
        return "Get a specific Foo with id=" + id;
    }

Note that _@PathVariable_ benefits from automatic type conversion, so we could have also declared the _id_ as:
    
    
    @PathVariable long id

### **4.2. Multiple _@PathVariable_**

A more complex URI may need to map multiple parts of the URI to **multiple values** :
    
    
    @RequestMapping(value = "/ex/foos/{fooid}/bar/{barid}", method = GET)
    @ResponseBody
    public String getFoosBySimplePathWithPathVariables
      (@PathVariable long fooid, @PathVariable long barid) {
        return "Get a specific Bar with id=" + barid + 
          " from a Foo with id=" + fooid;
    }

This is easily tested with a _curl_ in the same way:
    
    
    curl http://localhost:8080/ex/foos/1/bar/2

### **4.3._@PathVariable_ With Regex**

Regular expressions can also be used when mapping the _@PathVariable._

For example, we will restrict the mapping to only accept numerical values for the _id_ :
    
    
    @RequestMapping(value = "/ex/bars/{numericId:[\\d]+}", method = GET)
    @ResponseBody
    public String getBarsBySimplePathWithPathVariable(
      @PathVariable long numericId) {
        return "Get a specific Bar with id=" + numericId;
    }

This will mean that the following URIs will match:
    
    
    http://localhost:8080/ex/bars/1

But this will not:
    
    
    http://localhost:8080/ex/bars/abc

## **5._RequestMapping_ With Request Parameters**

@RequestMapping allows easy **mapping of URL parameters with the _@RequestParam_ annotation**. **_  
_**

We are now mapping a request to a URI:
    
    
    http://localhost:8080/ex/bars?id=100
    
    
    @RequestMapping(value = "/ex/bars", method = GET)
    @ResponseBody
    public String getBarBySimplePathWithRequestParam(
      @RequestParam("id") long id) {
        return "Get a specific Bar with id=" + id;
    }

We are then extracting the value of the _id_ parameter using the _@RequestParam(“id”)_ annotation in the controller method signature.

To send a request with the _id_ parameter, we’ll use the parameter support in _curl_ :
    
    
    curl -i http://localhost:8080/ex/bars --get -d id=100

In this example, the parameter was bound directly without having been declared first.

For more advanced scenarios, **_@RequestMapping_ can optionally define the parameters** as yet another way of narrowing the request mapping:
    
    
    @RequestMapping(value = "/ex/bars", params = "id", method = GET)
    @ResponseBody
    public String getBarBySimplePathWithExplicitRequestParam(
      @RequestParam("id") long id) {
        return "Get a specific Bar with id=" + id;
    }

Even more flexible mappings are allowed. Multiple _params_ values can be set, and not all of them have to be used:
    
    
    @RequestMapping(
      value = "/ex/bars", 
      params = { "id", "second" }, 
      method = GET)
    @ResponseBody
    public String getBarBySimplePathWithExplicitRequestParams(
      @RequestParam("id") long id) {
        return "Narrow Get a specific Bar with id=" + id;
    }

And of course, a request to a URI such as:
    
    
    http://localhost:8080/ex/bars?id=100&second=something

will always be mapped to the best match — which is the narrower match, which defines both the _id_ and the _second_ parameter.

## **6._RequestMapping_ Corner Cases**

### **6.1._@RequestMapping_ — Multiple Paths Mapped to the Same Controller Method**

Although a single _@RequestMapping_ path value is usually used for a single controller method (just good practice, not a hard and fast rule), there are some cases where mapping multiple requests to the same method may be necessary.

In that case, **the _value_ attribute of _@RequestMapping_ does accept multiple mappings**, not just a single one:
    
    
    @RequestMapping(
      value = { "/ex/advanced/bars", "/ex/advanced/foos" }, 
      method = GET)
    @ResponseBody
    public String getFoosOrBarsByPath() {
        return "Advanced - Get some Foos or Bars";
    }

Now both of these _curl_ commands should hit the same method:
    
    
    curl -i http://localhost:8080/ex/advanced/foos
    curl -i http://localhost:8080/ex/advanced/bars

### **6.2._@RequestMapping_ — Multiple HTTP Request Methods to the Same Controller Method**

Multiple requests using different HTTP verbs can be mapped to the same controller method:
    
    
    @RequestMapping(
      value = "/ex/foos/multiple", 
      method = { RequestMethod.PUT, RequestMethod.POST }
    )
    @ResponseBody
    public String putAndPostFoos() {
        return "Advanced - PUT and POST within single method";
    }

With _curl_ , both of these will now hit the same method:
    
    
    curl -i -X POST http://localhost:8080/ex/foos/multiple
    curl -i -X PUT http://localhost:8080/ex/foos/multiple

### **6.3._@RequestMapping_ — a Fallback for All Requests**

To implement a simple fallback for all requests using a particular HTTP method, for example, for a GET:
    
    
    @RequestMapping(value = "*", method = RequestMethod.GET)
    @ResponseBody
    public String getFallback() {
        return "Fallback for GET Requests";
    }

or even for all requests:
    
    
    @RequestMapping(
      value = "*", 
      method = { RequestMethod.GET, RequestMethod.POST ... })
    @ResponseBody
    public String allFallback() {
        return "Fallback for All Requests";
    }

### **6.4. Ambiguous Mapping Error**

The ambiguous mapping error occurs when Spring evaluates two or more request mappings to be the same for different controller methods. A request mapping is the same when it has the same HTTP method, URL, parameters, headers, and media type.

For example, this is an ambiguous mapping:
    
    
    @GetMapping(value = "foos/duplicate" )
    public String duplicate() {
        return "Duplicate";
    }
    
    @GetMapping(value = "foos/duplicate" )
    public String duplicateEx() {
        return "Duplicate";
    }

The exception thrown usually does have error messages along these lines:
    
    
    Caused by: java.lang.IllegalStateException: Ambiguous mapping.
      Cannot map 'fooMappingExamplesController' method 
      public java.lang.String org.baeldung.web.controller.FooMappingExamplesController.duplicateEx()
      to {[/ex/foos/duplicate],methods=[GET]}:
      There is already 'fooMappingExamplesController' bean method
      public java.lang.String org.baeldung.web.controller.FooMappingExamplesController.duplicate() mapped.

A careful reading of the error message points to the fact that Spring is unable to map the method  _org.baeldung.web.controller.FooMappingExamplesController.duplicateEx(),_ as it has a conflicting mapping with an already mapped  _org.baeldung.web.controller.FooMappingExamplesController.duplicate()._

**The code snippet below will not result in ambiguous mapping error because both methods return different content types** :
    
    
    @GetMapping(value = "foos/duplicate", produces = MediaType.APPLICATION_XML_VALUE)
    public String duplicateXml() {
        return "<message>Duplicate</message>";
    }
        
    @GetMapping(value = "foos/duplicate", produces = MediaType.APPLICATION_JSON_VALUE)
    public String duplicateJson() {
        return "{\"message\":\"Duplicate\"}";
    }

This differentiation allows our controller to return the correct data representation based on the  _Accepts_ header supplied in the request.

Another way to resolve this is to update the URL assigned to either of the two methods involved.

## **7\. New Request Mapping Shortcuts**

Spring Framework 4.3 introduced [a few new](/spring-new-requestmapping-shortcuts) HTTP mapping annotations, all based on _@RequestMapping_ :

  * _@GetMapping_
  * _@PostMapping_
  * _@PutMapping_
  * _@DeleteMapping_
  * _@PatchMapping_



These new annotations can improve the readability and reduce the verbosity of the code. 

Let’s look at these new annotations in action by creating a RESTful API that supports CRUD operations:
    
    
    @GetMapping("/{id}")
    public ResponseEntity<?> getBazz(@PathVariable String id){
        return new ResponseEntity<>(new Bazz(id, "Bazz"+id), HttpStatus.OK);
    }
    
    @PostMapping
    public ResponseEntity<?> newBazz(@RequestParam("name") String name){
        return new ResponseEntity<>(new Bazz("5", name), HttpStatus.OK);
    }
    
    @PutMapping("/{id}")
    public ResponseEntity<?> updateBazz(
      @PathVariable String id,
      @RequestParam("name") String name) {
        return new ResponseEntity<>(new Bazz(id, name), HttpStatus.OK);
    }
    
    @DeleteMapping("/{id}")
    public ResponseEntity<?> deleteBazz(@PathVariable String id){
        return new ResponseEntity<>(new Bazz(id), HttpStatus.OK);
    }

A deep dive into these can be found [here](/spring-new-requestmapping-shortcuts).

## **8\. Spring Configuration**

The Spring MVC Configuration is simple enough, considering that our _FooController_ is defined in the following package:
    
    
    package org.baeldung.spring.web.controller;
    
    @Controller
    public class FooController { ... }

We simply need a _@Configuration_ class to enable the full MVC support and configure classpath scanning for the controller:
    
    
    @Configuration
    @EnableWebMvc
    @ComponentScan({ "org.baeldung.spring.web.controller" })
    public class MvcConfig {
        //
    }

## **9\. Conclusion**

This article focused on the **_@RequestMapping_ annotation in Spring**, discussing a simple use case, the mapping of HTTP headers, binding parts of the URI with _@PathVariable_ , and working with URI parameters and the _@RequestParam_ annotation.

If you’d like to learn how to use another core annotation in Spring MVC, you can explore [the _@ModelAttribute_ annotation here](/spring-mvc-and-the-modelattribute-annotation).
