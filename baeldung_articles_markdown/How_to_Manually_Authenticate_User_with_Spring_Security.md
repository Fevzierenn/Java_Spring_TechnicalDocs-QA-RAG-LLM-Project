# How to Manually Authenticate User with Spring Security

## **1\. Overview**

In this quick article, we’ll focus on how to programmatically set an authenticated user in Spring Security and Spring MVC.

## **2\. Spring Security**

Simply put, Spring Security hold the principal information of each authenticated user in a _ThreadLocal_ – represented as an _Authentication_ object.

In order to construct and set this _Authentication_ object – we need to use the same approach Spring Security typically uses to build the object on a standard authentication.

To, let’s manually trigger authentication and then set the resulting _Authentication_ object into the current _SecurityContext_ used by the framework to hold the currently logged-in user:
    
    
    UsernamePasswordAuthenticationToken authReq
     = new UsernamePasswordAuthenticationToken(user, pass);
    Authentication auth = authManager.authenticate(authReq);
    SecurityContext sc = SecurityContextHolder.getContext();
    sc.setAuthentication(auth);

After setting the _Authentication_ in the context, we’ll now be able to check if the current user is authenticated – using _securityContext.getAuthentication().isAuthenticated()_.

## **3\. Spring MVC**

By default, Spring Security adds an additional filter in the Spring Security filter chain – which is capable of persisting the Security Context (_SecurityContextPersistenceFilter_ class).

In turn, it delegates the persistence of the Security Context to an instance of _SecurityContextRepository_ , defaulting to the _HttpSessionSecurityContextRepository_ class.

So, in order to set the authentication on the request and hence, **make it available for all subsequent requests from the client** , we need to manually set the _SecurityContext_ containing the _Authentication_ in the HTTP session:
    
    
    public void login(HttpServletRequest req, String user, String pass) { 
        UsernamePasswordAuthenticationToken authReq
          = new UsernamePasswordAuthenticationToken(user, pass);
        Authentication auth = authManager.authenticate(authReq);
        
        SecurityContext sc = SecurityContextHolder.getContext();
        sc.setAuthentication(auth);
        HttpSession session = req.getSession(true);
        session.setAttribute(SPRING_SECURITY_CONTEXT_KEY, sc);
    }

_SPRING_SECURITY_CONTEXT_KEY_ is a statically imported _HttpSessionSecurityContextRepository.SPRING_SECURITY_CONTEXT_KEY_.

It should be noted that we can’t directly use the _HttpSessionSecurityContextRepository_ – because it works in conjunction with the _SecurityContextPersistenceFilter._

That is because the filter uses the repository in order to load and store the security context before and after the execution of the rest of defined filters in the chain, but it uses a custom wrapper over the response which is passed to the chain.

So in this case, you should know the class type of the wrapper used and pass it to the appropriate save method in the repository.

## **4\. Conclusion**

In this quick tutorial, we went over how to manually set the user _Authentication_ in the Spring Security context and how it can be made available for Spring MVC purposes, focusing on the code samples that illustrate the simplest way to achieve it.
