# REST Pagination in Spring

## **1\. Overview**

This tutorial will focus on **the implementation of pagination in a REST API using Spring MVC and Spring Data.**

## **2\. Page as Resource vs Page as Representation**

The first question when designing pagination in the context of a RESTful architecture is whether to consider the **page an actual Resource or just a Representation of Resources**.

Treating the page itself as a resource introduces a host of problems, such as no longer being able to uniquely identify resources between calls. This, coupled with the fact that, in the persistence layer, the page isn’t a proper entity but a holder that’s constructed when necessary, makes the choice straightforward; **the page is part of the representation**.

The next question in the pagination design in the context of REST is **where to include the paging information** :

  * in the URI path: _/foo/page/1_
  * the URI query: _/foo?page=1_



Keeping in mind that **a page isn’t a Resource** , encoding the page information in the URI isn’t an option.

We’ll use the standard way of solving this problem by **encoding the paging information in a URI query.**

## **3\. The Controller**

Now for the implementation. **The Spring MVC Controller for pagination is straightforward** :
    
    
    @GetMapping(params = { "page", "size" })
    public List<Foo> findPaginated(@RequestParam("page") int page, 
      @RequestParam("size") int size, UriComponentsBuilder uriBuilder,
      HttpServletResponse response) {
        Page<Foo> resultPage = service.findPaginated(page, size);
        if (page > resultPage.getTotalPages()) {
            throw new MyResourceNotFoundException();
        }
        eventPublisher.publishEvent(new PaginatedResultsRetrievedEvent<Foo>(
          Foo.class, uriBuilder, response, page, resultPage.getTotalPages(), size));
    
        return resultPage.getContent();
    }

In this example, we’re injecting the two query parameters,  _size_ and _page,_ in the Controller method via _@RequestParam._

**Alternatively, we could have used a _Pageable_ object, which maps the _page_ ,  _size_ , and  _sort_ parameters automatically.** In addition, the _PagingAndSortingRepository_ entity provides out-of-the-box methods that support using _Pageable_ as a parameter.

We’re also injecting the Http Response and the _UriComponentsBuilder_ to help with Discoverability, which we’re decoupling via a custom event. If that’s not a goal of the API, we can simply remove the custom event.

Finally, note that the focus of this article is only the REST and web layer; to go deeper into the data access part of pagination, we can [check out this article](http://www.petrikainulainen.net/programming/spring-framework/spring-data-jpa-tutorial-part-seven-pagination/ "Data Acceess for Pagination") about Pagination with Spring Data.

## **4\. Discoverability for REST Pagination**

Within the scope of pagination, satisfying the **HATEOAS constraint of REST** means enabling the client of the API to discover the _next_ and _previous_ pages based on the current page in the navigation. For this purpose, **we’ll use the _Link_ HTTP header, coupled with the “ _next,_ ” “ _prev,_ ” “ _first,_ ” and “ _last_ ” link relation types**.

In REST, **Discoverability is a cross-cutting concern** , applicable not only to specific operations, but to types of operations. For example, each time a Resource is created, the URI of that Resource should be discoverable by the client. Since this requirement is relevant for the creation of ANY Resource, we’ll handle it separately.

We’ll decouple these concerns using events, as we discussed in the [previous article focusing on Discoverability](/rest-api-discoverability-with-spring "How to make REST Discoverable") of a REST Service. In the case of pagination, the event, _PaginatedResultsRetrievedEvent,_ is fired in the controller layer. Then we’ll implement discoverability with a custom listener for this event.

In short, the listener will check if the navigation allows for _next_ ,  _previous_ ,  _first_ and  _last_ pages. If it does, it’ll **add the relevant URIs to the response as a ‘Link’ HTTP Header**.

Now let’s go step by step. The _UriComponentsBuilder_ passed from the controller contains only the base URL (the host, the port and the context path). Therefore, we’ll have to add the remaining sections:
    
    
    void addLinkHeaderOnPagedResourceRetrieval(
     UriComponentsBuilder uriBuilder, HttpServletResponse response,
     Class clazz, int page, int totalPages, int size ){
    
       String resourceName = clazz.getSimpleName().toString().toLowerCase();
       uriBuilder.path( "/admin/" + resourceName );
    
        // ...
       
    }

Next, we’ll use a _StringJoiner_ to concatenate each link. We’ll use the _uriBuilder_ to generate the URIs. Let’s see how we proceed with the link to the _next_ page:
    
    
    StringJoiner linkHeader = new StringJoiner(", ");
    if (hasNextPage(page, totalPages)){
        String uriForNextPage = constructNextPageUri(uriBuilder, page, size);
        linkHeader.add(createLinkHeader(uriForNextPage, "next"));
    }

Let’s have a look at the logic of the  _constructNextPageUri_ method:
    
    
    String constructNextPageUri(UriComponentsBuilder uriBuilder, int page, int size) {
        return uriBuilder.replaceQueryParam(PAGE, page + 1)
          .replaceQueryParam("size", size)
          .build()
          .encode()
          .toUriString();
    }

We’ll proceed similarly for the rest of the URIs that we want to include.

Finally, we’ll add the output as a response header:
    
    
    response.addHeader("Link", linkHeader.toString());

Note that, for brevity, only a partial code sample is included, and [the full code is here](https://gist.github.com/1622997 "PaginatedResultsRetrievedEventDiscoverabilityListener").

## **5\. Test Driving Pagination**

Both the main logic of pagination and discoverability are covered by small, focused integration tests. As in the [previous article](/restful-web-service-discoverability "Testing REST Dsicoverability"), we’ll use the [REST-assured library](https://github.com/rest-assured/rest-assured "rest-assured official project page") to consume the REST service and verify the results.

These are a few examples of pagination integration tests; for a full test suite, check out the GitHub project (link at the end of the article):
    
    
    @Test
    public void whenResourcesAreRetrievedPaged_then200IsReceived(){
        Response response = RestAssured.get(paths.getFooURL() + "?page=0&size=2");
    
        assertThat(response.getStatusCode(), is(200));
    }
    @Test
    public void whenPageOfResourcesAreRetrievedOutOfBounds_then404IsReceived(){
        String url = getFooURL() + "?page=" + randomNumeric(5) + "&size=2";
        Response response = RestAssured.get.get(url);
    
        assertThat(response.getStatusCode(), is(404));
    }
    @Test
    public void givenResourcesExist_whenFirstPageIsRetrieved_thenPageContainsResources(){
       createResource();
       Response response = RestAssured.get(paths.getFooURL() + "?page=0&size=2");
    
       assertFalse(response.body().as(List.class).isEmpty());
    }

## **6\. Test Driving Pagination Discoverability**

Testing that pagination is discoverable by a client is relatively straightforward, although there’s a lot of ground to cover.

**The tests will focus on the position of the current page in navigation,** and the different URIs that should be discoverable from each position:
    
    
    @Test
    public void whenFirstPageOfResourcesAreRetrieved_thenSecondPageIsNext(){
       Response response = RestAssured.get(getFooURL()+"?page=0&size=2");
    
       String uriToNextPage = extractURIByRel(response.getHeader("Link"), "next");
       assertEquals(getFooURL()+"?page=1&size=2", uriToNextPage);
    }
    @Test
    public void whenFirstPageOfResourcesAreRetrieved_thenNoPreviousPage(){
       Response response = RestAssured.get(getFooURL()+"?page=0&size=2");
    
       String uriToPrevPage = extractURIByRel(response.getHeader("Link"), "prev");
       assertNull(uriToPrevPage );
    }
    @Test
    public void whenSecondPageOfResourcesAreRetrieved_thenFirstPageIsPrevious(){
       Response response = RestAssured.get(getFooURL()+"?page=1&size=2");
    
       String uriToPrevPage = extractURIByRel(response.getHeader("Link"), "prev");
       assertEquals(getFooURL()+"?page=0&size=2", uriToPrevPage);
    }
    @Test
    public void whenLastPageOfResourcesIsRetrieved_thenNoNextPageIsDiscoverable(){
       Response first = RestAssured.get(getFooURL()+"?page=0&size=2");
       String uriToLastPage = extractURIByRel(first.getHeader("Link"), "last");
    
       Response response = RestAssured.get(uriToLastPage);
    
       String uriToNextPage = extractURIByRel(response.getHeader("Link"), "next");
       assertNull(uriToNextPage);
    }

Note that the full low-level code for _extractURIByRel,_ responsible for extracting the URIs by _rel_ relation, [is here](https://gist.github.com/eugenp/8269915).

## **7\. Getting All Resources**

On the same topic of pagination and discoverability, **the choice must be made if a client is allowed to retrieve all the Resources in the system at once, or if the client must ask for them paginated**.

If it’s decided that the client can’t retrieve all Resources with a single request, and pagination is required, then several options are available for the response to get a request. One option is to return a 404 (_Not Found_) and use the _Link_ header to make the first page discoverable:

> _Link= <http://localhost:8080/rest/api/admin/foo?page=0&size=2>; rel=”first”, <http://localhost:8080/rest/api/admin/foo?page=103&size=2>; rel=”last”_

Another option is to return a redirect, 303 _(See Other_), to the first page. A more conservative route would be to simply return to the client a 405 (_Method Not Allowed)_ for the GET request.

## **8\. REST Paging With _Range_ HTTP Headers**

A relatively different way of implementing pagination is to work with the **HTTP _Range_ headers,** _Range_ , _Content-Range_ , _If-Range_ , _Accept-Ranges,_ and **HTTP status codes,** 206 (_Partial Content_), 413 (_Request Entity Too Large_), and 416 (_Requested Range Not Satisfiable_).

One view of this approach is that the HTTP Range extensions aren’t intended for pagination, and they should be managed by the Server, not by the Application. Implementing pagination based on the HTTP Range header extensions is technically possible, although not nearly as common as the implementation discussed in this article.

## 9\. Spring Data REST Pagination

In Spring Data, if we need to return a few results from the complete data set, we can use any _Pageable_ repository method, as it will always return a _Page._ The results will be returned based on the page number, page size, and sorting direction.

**[Spring Data REST](/spring-data-rest-intro) automatically recognizes URL parameters like _page, size, sort_ etc.**

To use paging methods of any repository, we need to extend _PagingAndSortingRepository:_
    
    
    public interface SubjectRepository extends PagingAndSortingRepository<Subject, Long>{}

If we call  _http://localhost:8080/subjects,_ Spring automatically adds the _page, size, sort_ parameter suggestions with the API:
    
    
    "_links" : {
      "self" : {
        "href" : "http://localhost:8080/subjects{?page,size,sort}",
        "templated" : true
      }
    }

By default, the page size is 20, but we can change it by calling something like _http://localhost:8080/subjects?page=10._

If we want to implement paging into our own custom repository API, we need to pass an additional _Pageable_ parameter and make sure that API returns a _Page:_
    
    
    @RestResource(path = "nameContains")
    public Page<Subject> findByNameContaining(@Param("name") String name, Pageable p);

Whenever we add a custom API, a _/search_ endpoint gets added to the generated links. So if we call  _http://localhost:8080/subjects/search,_ we’ll see a pagination capable endpoint:
    
    
    "findByNameContaining" : {
      "href" : "http://localhost:8080/subjects/search/nameContains{?name,page,size,sort}",
      "templated" : true
    }

All APIs that implement  _PagingAndSortingRepository_ will return a _Page._ If we need to return the list of the results from the _Page,_ the _getContent()_ API of _Page_ provides the list of records fetched as a result of the Spring Data REST API.

## 10\. Convert a _List_ into a _Page_

Let’s suppose that we have a _Pageable_ object as input, but the information that we need to retrieve is contained in a list instead of a _PagingAndSortingRepository_. In these cases, we may need to **convert a _List_ into a _Page_**.

For example, imagine that we have a list of results from a [SOAP](/spring-boot-soap-web-service) service:
    
    
    List<Foo> list = getListOfFooFromSoapService();

We need to access the list in the specific positions specified by the _Pageable_ object sent to us. So let’s define the start index:
    
    
    int start = (int) pageable.getOffset();

And the end index:
    
    
    int end = (int) ((start + pageable.getPageSize()) > fooList.size() ? fooList.size()
      : (start + pageable.getPageSize()));

Having these two in place, we can create a _Page_ to obtain the list of elements between them:
    
    
    Page<Foo> page 
      = new PageImpl<Foo>(fooList.subList(start, end), pageable, fooList.size());

That’s it! We can now return _page_ as a valid result.

And note that if we also want to give support for [sorting](/java-8-sort-lambda), we need to **sort the list before sub-listing** it.

## **11\. Conclusion**

This article illustrated how to implement Pagination in a REST API using Spring, and discussed how to set up and test Discoverability.

If we want to go in depth on pagination in the persistence level, we can check out the [JPA](/jpa-pagination "JPA Pagination") or [Hibernate](/hibernate-pagination "Hibernate Pagination") pagination tutorials.
