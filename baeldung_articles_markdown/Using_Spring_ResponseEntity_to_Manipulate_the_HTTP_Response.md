# Using Spring ResponseEntity to Manipulate the HTTP Response

## 1\. Introduction

Using Spring, we usually have many ways to achieve the same goal, including fine-tuning HTTP responses.

In this short tutorial, we’ll see how to set the body, status, and headers of an HTTP response using _ResponseEntity_.

## 2\. _ResponseEntity_

_ResponseEntity_ **represents the whole HTTP response: status code, headers, and body**. As a result, we can use it to fully configure the HTTP response.

If we want to use it, we have to return it from the endpoint; Spring takes care of the rest.

_ResponseEntity_ is a generic type. Consequently, we can use any type as the response body:
    
    
    @GetMapping("/hello")
    ResponseEntity<String> hello() {
        return new ResponseEntity<>("Hello World!", HttpStatus.OK);
    }

Since we specify the response status programmatically, we can return with different status codes for different scenarios:
    
    
    @GetMapping("/age")
    ResponseEntity<String> age(
      @RequestParam("yearOfBirth") int yearOfBirth) {
     
        if (isInFuture(yearOfBirth)) {
            return new ResponseEntity<>(
              "Year of birth cannot be in the future", 
              HttpStatus.BAD_REQUEST);
        }
    
        return new ResponseEntity<>(
          "Your age is " + calculateAge(yearOfBirth), 
          HttpStatus.OK);
    }

Additionally, we can set HTTP headers:
    
    
    @GetMapping("/customHeader")
    ResponseEntity<String> customHeader() {
        HttpHeaders headers = new HttpHeaders();
        headers.add("Custom-Header", "foo");
            
        return new ResponseEntity<>(
          "Custom header set", headers, HttpStatus.OK);
    }

Furthermore, _ResponseEntity_ **provides two nested builder interfaces** : _HeadersBuilder_ and its subinterface, _BodyBuilder_. Therefore, we can access their capabilities through the static methods of _ResponseEntity_.

The simplest case is a response with a body and HTTP 200 response code:
    
    
    @GetMapping("/hello")
    ResponseEntity<String> hello() {
        return ResponseEntity.ok("Hello World!");
    }

For the most popular [HTTP status codes](/cs/http-status-codes) we get static methods:
    
    
    BodyBuilder accepted();
    BodyBuilder badRequest();
    BodyBuilder created(java.net.URI location);
    HeadersBuilder<?> noContent();
    HeadersBuilder<?> notFound();
    BodyBuilder ok();

In addition, we can use the _BodyBuilder status(HttpStatus status)_ and the _BodyBuilder status(int status)_ methods to set any HTTP status.

Finally, with _ResponseEntity <T> BodyBuilder.body(T body)_ we can set the HTTP response body:
    
    
    @GetMapping("/age")
    ResponseEntity<String> age(@RequestParam("yearOfBirth") int yearOfBirth) {
        if (isInFuture(yearOfBirth)) {
            return ResponseEntity.badRequest()
                .body("Year of birth cannot be in the future");
        }
    
        return ResponseEntity.status(HttpStatus.OK)
            .body("Your age is " + calculateAge(yearOfBirth));
    }

We can also set custom headers:
    
    
    @GetMapping("/customHeader")
    ResponseEntity<String> customHeader() {
        return ResponseEntity.ok()
            .header("Custom-Header", "foo")
            .body("Custom header set");
    }

Since _BodyBuilder.body()_ returns a _ResponseEntity_ instead of _BodyBuilder,_ it should be the last call.

Note that with _HeaderBuilder_ we can’t set any properties of the response body.

While returning _ResponseEntity <T> _object from the controller, we might get an exception or error while processing the request and would like to **return error-related information to the user represented as some other type, let’s say E**.

Spring 3.2 brings support for a global ** _@ExceptionHandler_ with the new  _@ControllerAdvice_ annotation, **which handles these kinds of scenarios. For in-depth details, refer to our existing article [here](/exception-handling-for-rest-with-spring).

**While _ResponseEntity_ is very powerful, we shouldn’t overuse it.** In simple cases, there are other options that satisfy our needs and they result in much cleaner code.

## 3\. Alternatives

### 3.1. _@ResponseBody_

In classic Spring MVC applications, endpoints usually return rendered HTML pages. Sometimes we only need to return the actual data; for example, when we use the endpoint with AJAX.

In such cases, we can mark the request handler method with _@ResponseBody_ , and **Spring treats the result value of the method as the HTTP response body** itself.

For more information, [this article is a good place to start](/spring-request-response-body).

### 3.2. _@ResponseStatus_

When an endpoint returns successfully, Spring provides an HTTP 200 (OK) response. If the endpoint throws an exception, Spring looks for an exception handler that tells which HTTP status to use.

We can mark these methods with @ResponseStatus, and therefore, Spring **returns with a custom HTTP status**.

For more examples, please visit our article about [custom status codes](/spring-response-status).

### 3.3. Manipulate the Response Directly

Spring also lets us access the _jakarta.servlet.http.HttpServletResponse_ object directly; we only have to declare it as a method argument:
    
    
    @GetMapping("/manual")
    void manual(HttpServletResponse response) throws IOException {
        response.setHeader("Custom-Header", "foo");
        response.setStatus(200);
        response.getWriter().println("Hello World!");
    }

Since Spring provides abstractions and additional capabilities above the underlying implementation, **we shouldn’t manipulate the response this way**.

## 4\. Conclusion

In this article, we discussed multiple ways to manipulate the HTTP response in Spring, and examined their benefits and drawbacks.
