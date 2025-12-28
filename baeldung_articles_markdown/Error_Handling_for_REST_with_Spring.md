# Error Handling for REST with Spring

## **1\. Overview**

This tutorial will illustrate **how to implement Exception Handling with Spring for a REST API.** We’ll learn that there are various possibilities for that. All of these do have one thing in common: They deal with the **separation of concerns** very well. The app can throw exceptions normally to indicate a failure of some kind, which will then be handled separately.

## **2._@ExceptionHandler_**

We can use _@ExceptionHandler_ to annotate methods that Spring automatically invokes when the given exception occurs. We can specify the exception either with the annotation or by declaring it as a method parameter, which allows us to read out details from the exception object to handle it correctly. The method itself is handled as a Controller method, so:

  * It can return an object that is rendered into the response body, or a complete _ResponseEntity_. Content Negotiation is allowed here [since Spring 6.2](https://spring.io/blog/2024/06/13/spring-framework-6-2-0-m4-available-now#web-and-messaging).
  * It can return a _ProblemDetail_ object. Spring will set the _Content-Type_ header automatically to “ _application/problem+json_ “.
  * We can specify a return code with [_@ResponseStatus_](/spring-response-status).



The simplest exception handler that returns a 400 status code could be:
    
    
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    @ExceptionHandler(CustomException1.class)
    public void handleException1() { }

We could also declare the handled exception as a method parameter, for example, to read out exception details and create an [RFC-9457-compliant](https://www.rfc-editor.org/rfc/rfc9457.html) problem details object:
    
    
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    @ExceptionHandler
    public ProblemDetail handleException2(CustomException2 ex) {
        // ...
    }

Since Spring 6.2, we can write different exception handlers for different content types:
    
    
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    @ExceptionHandler( produces = MediaType.APPLICATION_JSON_VALUE )
    public CustomExceptionObject handleException3Json(CustomException3 ex) {
        // ...
    }
    
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    @ExceptionHandler( produces = MediaType.TEXT_PLAIN_VALUE )
    public String handleException3Text(CustomException3 ex) {
        // ...
    }

And, we could also write exception handlers for different types of exceptions. If we need details in the handler method, we use the shared superclass of all exception types as a method parameter:
    
    
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    @ExceptionHandler({ 
        CustomException4.class, 
        CustomException5.class
    })
    public ResponseEntity<CustomExceptionObject> handleException45(Exception ex) {
        // ...
    }

### 2.1. Local Exception Handling (Controller-Level)

We can place such handler methods in the controller class:
    
    
    @RestController
    public class FooController {
        //...
    
        @ResponseStatus(HttpStatus.BAD_REQUEST)
        @ExceptionHandler(CustomException1.class)
        public void handleException() {
            // ...
        }
    }

We could use this approach whenever we need controller-specific exception handling. But it has the drawback that **we cannot use it in multiple controllers unless we put it in a base class and use inheritance**. But there’s another approach that fits better in the sense of composition over inheritance.

### 2.2. Global Exception Handling

A _@ControllerAdvice_ contains code that is shared between multiple controllers. It’s a special kind of Spring component. Especially for REST APIs, where each method’s return value should be rendered into the response body, there’s a _@RestControllerAdvice_.

So, to handle a particular exception for all controllers of the application, we could write a simple class:
    
    
    @RestControllerAdvice
    public class MyGlobalExceptionHandler {
        @ResponseStatus(HttpStatus.BAD_REQUEST)
        @ExceptionHandler(CustomException1.class)
        public void handleException() {
            // ...
        }
    }

We should know that there’s also a base class (_ResponseEntityExceptionHandler_) that we could inherit from to use common pre-defined functionality like _ProblemDetails_ generation. We could also inherit methods for handling typical MVC exceptions:
    
    
    @ControllerAdvice
    public class MyCustomResponseEntityExceptionHandler 
      extends ResponseEntityExceptionHandler {
    
        @ExceptionHandler({ 
            IllegalArgumentException.class, 
            IllegalStateException.class
        })
        ResponseEntity<Object> handleConflict(RuntimeException ex, WebRequest request) {
            String bodyOfResponse = "This should be application specific";
            return super.handleExceptionInternal(ex, bodyOfResponse, 
              new HttpHeaders(), HttpStatus.CONFLICT, request);
        }
    
        @Override
        protected ResponseEntity<Object> handleHttpMediaTypeNotAcceptable(
          HttpMediaTypeNotAcceptableException ex, HttpHeaders headers, HttpStatusCode status, WebRequest request {
            // ... (customization, maybe invoking the overridden method)
        }
    }

Note that, in the above example, there’s no need to add the _@RestControllerAdvice_ annotation to the class since all methods return a _ResponseEntity_ , so we’ve used the vanilla _@ControllerAdvice_ annotation here.

## 3\. Annotate Exceptions Directly

Another simple approach is to directly annotate our custom exception with _@ResponseStatus_ :
    
    
    @ResponseStatus(value = HttpStatus.NOT_FOUND)
    public class MyResourceNotFoundException extends RuntimeException {
        // ...
    }

The same as the _DefaultHandlerExceptionResolver_ , this resolver is limited in the way it deals with the body of the response — it does map the Status Code on the response, but the body is still _null._ We can only use it for our custom exceptions because we cannot annotate existing, already compiled classes. And, in a layered architecture, **we should use this approach only for boundary-specific exceptions**.

By the way, we should note that **exceptions in this context typically are derived from _RuntimeException_** because we don’t need compiler checks here. Otherwise, this would lead to unnecessary _throws_ declarations in our code.

## 4\. **_ResponseStatusException_**

A controller could also throw a _ResponseStatusException_. We can create an instance of it providing an _HttpStatus_ and, optionally, a _reason_ and a _cause_ :
    
    
    @GetMapping(value = "/{id}")
    public Foo findById(@PathVariable("id") Long id) {
        try {
            // ...
         }
        catch (MyResourceNotFoundException ex) {
             throw new ResponseStatusException(
               HttpStatus.NOT_FOUND, "Foo Not Found", ex);
        }
    }

What are the benefits of using _ResponseStatusException_?

  * Excellent for prototyping: We can implement a basic solution quite fast.
  * One type, multiple status codes: One exception type can lead to multiple different responses. **This reduces tight coupling compared to the _@ExceptionHandler_.**
  * We won’t have to create as many custom exception classes.
  * We have**more control over exception handling** since the exceptions can be created programmatically.



And what about the tradeoffs?

  * There’s no unified way of exception handling: It’s more difficult to enforce some application-wide conventions as opposed to _@ControllerAdvice_ , which provides a global approach.
  * Code duplication: We may find ourselves replicating code in multiple controllers.
  * In layered architectures, we should only throw those exceptions in the controller. As shown in the code sample, we might need exception wrapping for exceptions from underlying layers.



For more details and further examples, see our [tutorial on _ResponseStatusException_](/spring-response-status-exception).

## **5._HandlerExceptionResolver_**

Another solution is to define a custom _HandlerExceptionResolver._ This will resolve any exception thrown by the application. It will also allow us to implement a **uniform exception handling mechanism** in our REST API.

### 5.1. Existing Implementations

There are already existing implementations that are enabled by default in the _DispatcherServlet_ :

  * _ExceptionHandlerExceptionResolver_ is actually the core component of how the @_ExceptionHandler_ mechanism presented earlier works.
  * _ResponseStatusExceptionResolver_ is actually the core component of how the _@ResponseStatus_ mechanism presented earlier works.
  * _DefaultHandlerExceptionResolver_ is used to resolve standard Spring exceptions to their corresponding [HTTP Status Codes](/cs/http-status-codes), namely Client error _4xx_ and Server error _5xx_ status codes. [Here’s the full list](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/web/servlet/mvc/support/DefaultHandlerExceptionResolver.html "Handling Standard Spring MVC Exceptions") of the Spring Exceptions it handles and how they map to status codes. While it does set the Status Code of the Response properly, one **limitation is that it doesn’t set anything to the body of the Response.**



### **5.2.****Custom _HandlerExceptionResolver_**

The combination of _DefaultHandlerExceptionResolver_ and _ResponseStatusExceptionResolver_ goes a long way toward providing a good error handling mechanism for a Spring RESTful Service. The downside is, as mentioned before, we have **no control over the body of the response.**

Ideally, we’d like to be able to output either JSON or XML, depending on what format the client has asked for (via the _Accept_ header).

This alone justifies creating **a new, custom exception resolver** :
    
    
    @Component
    public class RestResponseStatusExceptionResolver extends AbstractHandlerExceptionResolver {
        @Override
        protected ModelAndView doResolveException(
          HttpServletRequest request, 
          HttpServletResponse response, 
          Object handler, 
          Exception ex) {
            try {
                if (ex instanceof IllegalArgumentException) {
                    return handleIllegalArgument(
                      (IllegalArgumentException) ex, response, handler);
                }
                // ...
            } catch (Exception handlerException) {
                logger.warn("Handling of [" + ex.getClass().getName() + "] 
                  resulted in Exception", handlerException);
            }
            return null;
        }
    
        private ModelAndView handleIllegalArgument(
          IllegalArgumentException ex, HttpServletResponse response) throws IOException {
            response.sendError(HttpServletResponse.SC_CONFLICT);
            String accept = request.getHeader(HttpHeaders.ACCEPT);
            // ...
            return new ModelAndView();
        }
    }

One detail to notice here is that we have access to the _request_ itself, so we can consider the value of the _Accept_ header sent by the client.

For example, if the client asks for _application/json_ , then, in the case of an error condition, we’d want to make sure we return a response body encoded with _application/json_.

The other important implementation detail is that **we return a _ModelAndView_ — this is the body of the response**, and it will allow us to set whatever is necessary on it.

This approach is a consistent and easily configurable mechanism for the error handling of a Spring REST Service.

It does, however, have limitations: It interacts with the low-level _HtttpServletResponse_ and fits into the old MVC model that uses _ModelAndView_.

## 6\. Further Notes

### **6.1. Handling Existing Exceptions**

There are several exceptions that we often deal with in typical REST implementations:

  * _AccessDeniedException_ occurs when an authenticated user tries to access resources that he doesn’t have enough authority to access. For example, this could happen when we use method-level security annotations like _@PreAuthorize_ , _@PostAuthorize_ , and _@Secure_.
  * _ValidationException_ and _ConstraintViolationException_ occur when we use [Bean Validation](/spring-boot-bean-validation).
  * _PersistenceException_ and _DataAccessException_ occur when we use [Spring Data JPA](/the-persistence-layer-with-spring-data-jpa).



Of course, we’ll use the global exception handling mechanism that we discussed earlier to handle the _AccessDeniedException_ as well:
    
    
    @RestControllerAdvice
    public class MyGlobalExceptionHandler {
        @ResponseStatus(value = HttpStatus.FORBIDDEN)
        @ExceptionHandler( AccessDeniedException.class )
        public void handleAccessDeniedException() {
            // ...
        }
    }

### **6.2. Spring Boot Support**

**Spring Boot provides an _ErrorController_ implementation to handle errors in a sensible way.**

In a nutshell, it serves as a fallback error page for browsers (a.k.a. the Whitelabel Error Page) and a JSON response for RESTful, non-HTML requests:
    
    
    {
        "timestamp": "2019-01-17T16:12:45.977+0000",
        "status": 500,
        "error": "Internal Server Error",
        "message": "Error processing the request!",
        "path": "/my-endpoint-with-exceptions"
    }

As usual, Spring Boot allows configuring these features with properties:

  * _server.error.whitelabel.enabled_ : can be used to disable the Whitelabel Error Page and rely on the servlet container to provide an HTML error message
  * _server.error.include-stacktrace_ : with an _always_ value, it includes the stacktrace in both the HTML and the JSON default response
  * _server.error.include-message:_ since version 2.3, Spring Boot hides the  _message_ field in the response to avoid leaking sensitive information; we can use this property with an  _always_ value to enable it



Apart from these properties,**we can provide our own view-resolver mapping for /_error,_ overriding the Whitelabel Page.**

We can also customize the attributes that we want to show in the response by including an  _ErrorAttributes_ bean in the context. We can extend the  _DefaultErrorAttributes_ class provided by Spring Boot to make things easier:
    
    
    @Component
    public class MyCustomErrorAttributes extends DefaultErrorAttributes {
        @Override
        public Map<String, Object> getErrorAttributes(
          WebRequest webRequest, ErrorAttributeOptions options) {
            Map<String, Object> errorAttributes = super.getErrorAttributes(webRequest, options);
            errorAttributes.put("locale", webRequest.getLocale().toString());
            errorAttributes.remove("error");
    
            //...
    
            return errorAttributes;
        }
    }

If we want to go further and define (or override) how the application will handle errors for a particular content type, we can register an  _ErrorController_ bean.

Again, we can make use of the default  _BasicErrorController_ provided by Spring Boot to help us out.

For example, imagine we want to customize how our application handles errors triggered in XML endpoints. All we have to do is define a public method using the  _@RequestMapping_ , and state that it produces _application/xml_ media type:
    
    
    @Component
    public class MyErrorController extends BasicErrorController {
        public MyErrorController(
          ErrorAttributes errorAttributes, ServerProperties serverProperties) {
            super(errorAttributes, serverProperties.getError());
        }
    
        @RequestMapping(produces = MediaType.APPLICATION_XML_VALUE)
        public ResponseEntity<Map<String, Object>> xmlError(HttpServletRequest request) {
            // ...
        }
    }

Note: Here, we’re still relying on the _server.error.*_ Spring Boot properties we might have defined in our project that are bound to the _ServerProperties_ bean.

## **7\. Conclusion**

In this article, we discussed several ways to implement an exception handling mechanism for a REST API in Spring. We compared them in terms of their use cases.

We should note that it’s possible to combine different approaches within one application. For example, we can implement a  _@ControllerAdvice_ globally but also  _ResponseStatusException_ s locally.

****

****
