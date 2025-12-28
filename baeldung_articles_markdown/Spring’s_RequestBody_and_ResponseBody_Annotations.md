# Spring’s RequestBody and ResponseBody Annotations

## **1\. Introduction**

In this quick tutorial, we provide a concise overview of the Spring _@RequestBody_ and _@ResponseBody_ annotations.

## **2._@RequestBody_**

Simply put, **the _@RequestBody_ annotation maps the _HttpRequest_ body to a transfer or domain object, enabling automatic deserialization** of the inbound _HttpRequest_ body onto a Java object.

First, let’s have a look at a Spring controller method:
    
    
    @PostMapping("/request")
    public ResponseEntity postController(
      @RequestBody LoginForm loginForm) {
     
        exampleService.fakeAuthenticate(loginForm);
        return ResponseEntity.ok(HttpStatus.OK);
    }

Spring automatically deserializes the JSON into a Java type, assuming an appropriate one is specified.

By default, **the type we annotate with the _@RequestBody_ annotation must correspond to the JSON sent from our client-side controller:**
    
    
    public class LoginForm {
        private String username;
        private String password;
        // ...
    }

Here, the object we use to represent the _HttpRequest_ body maps to our _LoginForm_ object.

Let’s test this using CURL:
    
    
    curl -i \
    -H "Accept: application/json" \
    -H "Content-Type:application/json" \
    -X POST --data 
      '{"username": "johnny", "password": "password"}' "https://localhost:8080/spring-boot-rest/post/request"

This is all we need for a Spring REST API and an Angular client using the @_RequestBody_ annotation.

## **3._@ResponseBody_**

The _@ResponseBody_ annotation tells a controller that the object returned is automatically serialized into JSON and passed back into the _HttpResponse_ object.

Suppose we have a custom _Response_ object:
    
    
    public class ResponseTransfer {
        private String text; 
        
        // standard getters/setters
    }

Next, the associated controller can be implemented:
    
    
    @Controller
    @RequestMapping("/post")
    public class ExamplePostController {
    
        @Autowired
        ExampleService exampleService;
    
        @PostMapping("/response")
        @ResponseBody
        public ResponseTransfer postResponseController(
          @RequestBody LoginForm loginForm) {
            return new ResponseTransfer("Thanks For Posting!!!");
         }
    }

In the developer console of our browser or using a tool like Postman, we can see the following response:
    
    
    {"text":"Thanks For Posting!!!"}

**Remember, we don’t need to annotate the _@RestController-_ annotated controllers with the _@ResponseBody_ annotation** since Spring does it by default.

### 3.1. Setting the Content Type

When we use the _@ResponseBody_ annotation, we’re still able to explicitly set the content type that our method returns.

For that, **we can use the _@RequestMapping_ ‘s  _produces_ attribute.** Note that annotations like _@PostMapping_ , _@GetMapping_ , etc. define aliases for that parameter.

Let’s now add a new endpoint that sends a JSON response:
    
    
    @PostMapping(value = "/content", produces = MediaType.APPLICATION_JSON_VALUE)
    @ResponseBody
    public ResponseTransfer postResponseJsonContent(
      @RequestBody LoginForm loginForm) {
        return new ResponseTransfer("JSON Content!");
    }

In the example, we used the _MediaType.APPLICATION_JSON_VALUE_ constant. Alternatively, we can use _application/json_ directly.

Next, let’s implement a new method, mapped to the same _/content_ path, but returning XML content instead:
    
    
    @PostMapping(value = "/content", produces = MediaType.APPLICATION_XML_VALUE)
    @ResponseBody
    public ResponseTransfer postResponseXmlContent(
      @RequestBody LoginForm loginForm) {
        return new ResponseTransfer("XML Content!");
    }

Now, **depending on the value of an _Accept_ parameter sent in the request’s header, we’ll get different responses.**

Let’s see this in action:
    
    
    curl -i \ 
    -H "Accept: application/json" \ 
    -H "Content-Type:application/json" \ 
    -X POST --data 
      '{"username": "johnny", "password": "password"}' "https://localhost:8080/spring-boot-rest/post/content"

The CURL command returns a JSON response:
    
    
    HTTP/1.1 200
    Content-Type: application/json
    Transfer-Encoding: chunked
    Date: Thu, 20 Feb 2020 19:43:06 GMT
    
    {"text":"JSON Content!"}

Now, let’s change the _Accept_ parameter:
    
    
    curl -i \
    -H "Accept: application/xml" \
    -H "Content-Type:application/json" \
    -X POST --data
      '{"username": "johnny", "password": "password"}' "https://localhost:8080/spring-boot-rest/post/content"

As anticipated, we get an XML content this time:
    
    
    HTTP/1.1 200
    Content-Type: application/xml
    Transfer-Encoding: chunked
    Date: Thu, 20 Feb 2020 19:43:19 GMT
    
    <ResponseTransfer><text>XML Content!</text></ResponseTransfer>

## **4\. Conclusion**

We’ve built a simple Angular client for the Spring app that demonstrates how to use the _@RequestBody_ and _@ResponseBody_ annotations.

Additionally, we showed how to set a content type when using _@ResponseBody_.
