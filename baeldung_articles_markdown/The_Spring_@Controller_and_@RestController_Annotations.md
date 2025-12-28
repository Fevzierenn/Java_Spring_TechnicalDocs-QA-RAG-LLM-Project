# The Spring @Controller and @RestController Annotations

## 1\. Overview

In this brief tutorial, we’ll discuss the difference between _@Controller_ and _@RestController_ annotations in Spring MVC.

We can use the first annotation for traditional Spring controllers, and it has been part of the framework for a very long time.

Spring 4.0 introduced the _@RestController_ annotation in order to simplify the creation of RESTful web services. **It’s a convenient annotation that combines _@Controller_ and _@ResponseBody_** , which eliminates the need to annotate every request handling method of the controller class with the _@ResponseBody_ annotation.

## 2\. Spring MVC _@Controller_

We can annotate classic controllers with the _@Controller_ annotation. This is simply a specialization of the  _@Component_ class, which allows us to auto-detect implementation classes through the classpath scanning.

We typically use _@Controller_ in combination with a _@RequestMapping_ annotation for request handling methods.

Let’s see a quick example of the Spring MVC controller:
    
    
    @Controller
    @RequestMapping("books")
    public class SimpleBookController {
    
        @GetMapping("/{id}", produces = "application/json")
        public @ResponseBody Book getBook(@PathVariable int id) {
            return findBookById(id);
        }
    
        private Book findBookById(int id) {
            // ...
        }
    }
    

We annotated the request handling method with _@ResponseBody_. This annotation enables automatic serialization of the return object into the _HttpResponse_.

## 3\. Spring MVC _@RestController_

_@RestController_ is a specialized version of the controller. It includes the _@Controller_ and _@ResponseBody_ annotations, and as a result, simplifies the controller implementation:
    
    
    @RestController
    @RequestMapping("books-rest")
    public class SimpleBookRestController {
        
        @GetMapping("/{id}", produces = "application/json")
        public Book getBook(@PathVariable int id) {
            return findBookById(id);
        }
    
        private Book findBookById(int id) {
            // ...
        }
    }
    

**The controller is annotated with the _@RestController_ annotation; therefore, the _@ResponseBody_ isn’t required.**

Every request handling method of the controller class automatically serializes return objects into _HttpResponse_.

## 4\. Conclusion

In this article, we examined the classic and specialized REST controllers available in the Spring Framework.
