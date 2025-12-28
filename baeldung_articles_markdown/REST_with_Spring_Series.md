# REST with Spring Series

**Building a REST API is not a trivial task** – from the high-level RESTful constraints down to the nitty-gritty of making everything work and work well.

Spring has made REST a first-class citizen and the platform has been maturing in leaps and bounds.

With this guide, my aim is to organize the mountains of information that are available on the subject and guide you through properly building an API.

The guide starts with **the basics** – bootstrapping the REST API, basic usage, and annotations.

It then dives into the more **advanced areas** of REST – such as error handling, pagination, testing, and documenting the API.

Last but not least, it explores how to use different **Spring REST clients** , including _RestClient_ , _RestTemplate_ , and _WebClient_.

![rest api](/wp-content/uploads/2023/03/icon_rest_api.png)

## Prerequisites

  * ![category-item-icon](/wp-content/themes/baeldung/images/long-arrow-alt-right-solid.svg) [Bootstrapping a Web Application](/bootstraping-a-web-application-with-spring-and-java-based-configuration)



![icon string api](/wp-content/uploads/2022/12/icon_string_api.png)

## REST API Basics

  * ![category-item-icon](/wp-content/themes/baeldung/images/long-arrow-alt-right-solid.svg) [Building a REST API](/building-a-restful-web-service-with-spring-and-java-based-configuration) (popular)
  * ![category-item-icon](/wp-content/themes/baeldung/images/long-arrow-alt-right-solid.svg) [Using Spring ResponseEntity to Manipulate the HTTP Response](/spring-response-entity) (popular)
  * ![category-item-icon](/wp-content/themes/baeldung/images/long-arrow-alt-right-solid.svg) [How to Read HTTP Headers in Spring REST Controllers](/spring-rest-http-headers) (popular)
  * ![category-item-icon](/wp-content/themes/baeldung/images/long-arrow-alt-right-solid.svg) [Entity To DTO Conversion for a Spring REST API](/entity-to-and-from-dto-for-a-java-spring-application) (popular)
  * ![category-item-icon](/wp-content/themes/baeldung/images/long-arrow-alt-right-solid.svg) [Error Handling for REST](/exception-handling-for-rest-with-spring) (popular)
  * ![category-item-icon](/wp-content/themes/baeldung/images/long-arrow-alt-right-solid.svg) [HTTP PUT vs. POST in REST API](/rest-http-put-vs-post)
  * ![category-item-icon](/wp-content/themes/baeldung/images/long-arrow-alt-right-solid.svg) [Custom Error Message Handling for REST API](/global-error-handler-in-a-spring-rest-api) (popular)



![icon spring examples](/wp-content/uploads/2019/09/icon_spring_examples.png)

## REST API Annotations

  * ![category-item-icon](/wp-content/themes/baeldung/images/long-arrow-alt-right-solid.svg) [Spring @Controller and @RestController Annotations](/spring-controller-vs-restcontroller) (popular)
  * ![category-item-icon](/wp-content/themes/baeldung/images/long-arrow-alt-right-solid.svg) [Spring @RequestBody and @ResponseBody Annotations](/spring-request-response-body) (popular)
  * ![category-item-icon](/wp-content/themes/baeldung/images/long-arrow-alt-right-solid.svg) [Spring @PathVariable Annotation](/spring-pathvariable) (popular)
  * ![category-item-icon](/wp-content/themes/baeldung/images/long-arrow-alt-right-solid.svg) [Spring @RequestParam Annotation](/spring-request-param) (popular)
  * ![category-item-icon](/wp-content/themes/baeldung/images/long-arrow-alt-right-solid.svg) [Spring @RequestMapping](/spring-requestmapping) (popular)
  * ![category-item-icon](/wp-content/themes/baeldung/images/long-arrow-alt-right-solid.svg) [Spring @ResponseStatus Annotation](/spring-response-status) (popular)



![rest api advanced](/wp-content/uploads/2023/03/icon_rest_api_advanced.png)

## REST API Documenting and Versioning

  * ![category-item-icon](/wp-content/themes/baeldung/images/long-arrow-alt-right-solid.svg) [Setting Up Swagger 2 with a Spring REST API](/swagger-2-documentation-for-spring-rest-api) (popular)
  * ![category-item-icon](/wp-content/themes/baeldung/images/long-arrow-alt-right-solid.svg) [Documenting a Spring REST API Using OpenAPI 3.0](/spring-rest-openapi-documentation) (popular)
  * ![category-item-icon](/wp-content/themes/baeldung/images/long-arrow-alt-right-solid.svg) [Swagger @Parameter vs @Schema](/swagger-parameter-vs-schema) (popular)
  * ![category-item-icon](/wp-content/themes/baeldung/images/long-arrow-alt-right-solid.svg) [Generate Spring Boot REST Client with Swagger](/spring-boot-rest-client-swagger-codegen) (popular)
  * ![category-item-icon](/wp-content/themes/baeldung/images/long-arrow-alt-right-solid.svg) [Versioning a REST API](/rest-versioning)
  * ![category-item-icon](/wp-content/themes/baeldung/images/long-arrow-alt-right-solid.svg) [@Operation vs @ApiResponse in Swagger](/swagger-operation-vs-apiresponse) (popular)
  * ![category-item-icon](/wp-content/themes/baeldung/images/long-arrow-alt-right-solid.svg) [Setting Example and Description with Swagger](/swagger-set-example-description) (popular)



![spring on web - icon](/wp-content/uploads/2019/08/icon_spring_on_web.png)

## REST API Advanced Topics

  * ![category-item-icon](/wp-content/themes/baeldung/images/long-arrow-alt-right-solid.svg) [REST Pagination](/rest-api-pagination-in-spring) (popular)
  * ![category-item-icon](/wp-content/themes/baeldung/images/long-arrow-alt-right-solid.svg) [Handling URL Encoded Form Data in Spring REST](/spring-url-encoded-form-data)
  * ![category-item-icon](/wp-content/themes/baeldung/images/long-arrow-alt-right-solid.svg) [Setting a Request Timeout for a Spring REST API](/spring-rest-timeout) (popular)
  * ![category-item-icon](/wp-content/themes/baeldung/images/long-arrow-alt-right-solid.svg) [Best Practices for REST API Error Handling](/rest-api-error-handling-best-practices) (popular)
  * ![category-item-icon](/wp-content/themes/baeldung/images/long-arrow-alt-right-solid.svg) [Get All Endpoints in Spring Boot](/spring-boot-get-all-endpoints)
  * ![category-item-icon](/wp-content/themes/baeldung/images/long-arrow-alt-right-solid.svg) [How to Make Multiple REST Calls in CompletableFuture](/rest-completablefuture-several-calls)
  * ![category-item-icon](/wp-content/themes/baeldung/images/long-arrow-alt-right-solid.svg) [Avoid Brittle Tests for the Service Layer](/testing-the-java-service-layer)



![test api](/wp-content/uploads/2023/03/icon_test_api.png)

## REST API Testing

  * ![category-item-icon](/wp-content/themes/baeldung/images/long-arrow-alt-right-solid.svg) [Test a REST API with Java](/integration-testing-a-rest-api)
  * ![category-item-icon](/wp-content/themes/baeldung/images/long-arrow-alt-right-solid.svg) [Testing Exceptions with Spring MockMvc](/spring-mvc-test-exceptions)
  * ![category-item-icon](/wp-content/themes/baeldung/images/long-arrow-alt-right-solid.svg) [REST API Testing with Cucumber](/cucumber-rest-api-testing)
  * ![category-item-icon](/wp-content/themes/baeldung/images/long-arrow-alt-right-solid.svg) [Introduction to WireMock](/introduction-to-wiremock) (popular)
  * ![category-item-icon](/wp-content/themes/baeldung/images/long-arrow-alt-right-solid.svg) [A Guide to REST-assured](/rest-assured-tutorial) (popular)
  * ![category-item-icon](/wp-content/themes/baeldung/images/long-arrow-alt-right-solid.svg) [Getting and Verifying Response Data with REST-assured](/rest-assured-response)
  * ![category-item-icon](/wp-content/themes/baeldung/images/long-arrow-alt-right-solid.svg) [Test a REST API with curl](/curl-rest) (popular)



![basics spring - icon](/wp-content/uploads/2019/08/icon_basics_spring.png)

## RestTemplate

  * ![category-item-icon](/wp-content/themes/baeldung/images/long-arrow-alt-right-solid.svg) [The Guide to RestTemplate](/rest-template) (popular)
  * ![category-item-icon](/wp-content/themes/baeldung/images/long-arrow-alt-right-solid.svg) [A Guide to RestClient in Spring Boot](/spring-boot-restclient) (popular)
  * ![category-item-icon](/wp-content/themes/baeldung/images/long-arrow-alt-right-solid.svg) [RestTemplate Post Request with JSON](/spring-resttemplate-post-json) (popular)
  * ![category-item-icon](/wp-content/themes/baeldung/images/long-arrow-alt-right-solid.svg) [Get and Post Lists of Objects with RestTemplate](/spring-rest-template-list)
  * ![category-item-icon](/wp-content/themes/baeldung/images/long-arrow-alt-right-solid.svg) [Spring RestTemplate Error Handling](/spring-rest-template-error-handling) (popular)
  * ![category-item-icon](/wp-content/themes/baeldung/images/long-arrow-alt-right-solid.svg) [Uploading MultipartFile with Spring RestTemplate](/spring-rest-template-multipart-upload) (popular)
  * ![category-item-icon](/wp-content/themes/baeldung/images/long-arrow-alt-right-solid.svg) [RestTemplate with Basic Authentication](/how-to-use-resttemplate-with-basic-authentication-in-spring)
  * ![category-item-icon](/wp-content/themes/baeldung/images/long-arrow-alt-right-solid.svg) [Configure a RestTemplate with RestTemplateBuilder](/spring-rest-template-builder)
  * ![category-item-icon](/wp-content/themes/baeldung/images/long-arrow-alt-right-solid.svg) [Spring RestTemplate Request/Response Logging](/spring-resttemplate-logging) (popular)
  * ![category-item-icon](/wp-content/themes/baeldung/images/long-arrow-alt-right-solid.svg) [Access HTTPS REST Service Using Spring RestTemplate](/spring-resttemplate-secure-https-service) (popular)



![spring other tech - icon](/wp-content/uploads/2019/08/icon_spring_other_tech.png)

## WebClient

  * ![category-item-icon](/wp-content/themes/baeldung/images/long-arrow-alt-right-solid.svg) [Spring WebClient](/spring-5-webclient) (popular)
  * ![category-item-icon](/wp-content/themes/baeldung/images/long-arrow-alt-right-solid.svg) [Spring WebClient Requests with Parameters](/webflux-webclient-parameters) (popular)
  * ![category-item-icon](/wp-content/themes/baeldung/images/long-arrow-alt-right-solid.svg) [Spring WebClient Filters](/spring-webclient-filters)
  * ![category-item-icon](/wp-content/themes/baeldung/images/long-arrow-alt-right-solid.svg) [Get List of JSON Objects with WebClient](/spring-webclient-json-list)
  * ![category-item-icon](/wp-content/themes/baeldung/images/long-arrow-alt-right-solid.svg) [Spring WebClient and OAuth2 Support](/spring-webclient-oauth2) (popular)
  * ![category-item-icon](/wp-content/themes/baeldung/images/long-arrow-alt-right-solid.svg) [Simultaneous Spring WebClient Calls](/spring-webclient-simultaneous-calls)
  * ![category-item-icon](/wp-content/themes/baeldung/images/long-arrow-alt-right-solid.svg) [Spring WebClient vs. RestTemplate](/spring-webclient-resttemplate) (popular)



![other spring tutorials](/wp-content/uploads/2023/03/icon_other_spring_tutorials.png)

## Other Spring Tutorials

  * ![category-item-icon](/wp-content/themes/baeldung/images/long-arrow-alt-right-solid.svg) [Spring Boot Tutorial](/spring-boot) (popular) (Series) Get started with Spring Boot and learn how to customize a Spring Boot application
  * ![category-item-icon](/wp-content/themes/baeldung/images/long-arrow-alt-right-solid.svg) [Spring Persistence Tutorial](/persistence-with-spring-series) (popular) (Series) Learn how to work with Spring Data JPA and other Spring persistence technologies
  * ![category-item-icon](/wp-content/themes/baeldung/images/long-arrow-alt-right-solid.svg) [Spring Security OAuth2 Guides](/security-spring) (popular) (Series) Learn how to secure a REST API using Spring OAuth2 support


