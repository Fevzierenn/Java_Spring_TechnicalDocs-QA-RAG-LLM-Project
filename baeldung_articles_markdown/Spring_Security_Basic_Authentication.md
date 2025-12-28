# Spring Security Basic Authentication

## **1\. Overview**

This tutorial will explain how to set up, configure, and customize **Basic Authentication with Spring**. We’re going to build on top of the simple [Spring MVC example](/spring-mvc-tutorial "Spring MVC Tutorial"), and secure the UI of the MVC application with the Basic Auth mechanism provided by Spring Security.

## **2\. The Spring Security Configuration**

We can configure Spring Security using Java config:
    
    
    @Configuration
    @EnableWebSecurity
    public class CustomWebSecurityConfigurerAdapter {
    
        @Autowired private RestAuthenticationEntryPoint authenticationEntryPoint;
    
        @Autowired
        public void configureGlobal(AuthenticationManagerBuilder auth) throws Exception {
            auth
              .inMemoryAuthentication()
              .withUser("user1")
              .password(passwordEncoder().encode("user1Pass"))
              .authorities("ROLE_USER");
        }
    
        @Bean
        public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
            http.authorizeHttpRequests(expressionInterceptUrlRegistry ->
                            expressionInterceptUrlRegistry.requestMatchers("/securityNone").permitAll()
                                    .anyRequest().authenticated())
                .httpBasic(httpSecurityHttpBasicConfigurer -> httpSecurityHttpBasicConfigurer.authenticationEntryPoint(authenticationEntryPoint));
            http.addFilterAfter(new CustomFilter(), BasicAuthenticationFilter.class);
            return http.build();
        }
        
        @Bean
        public PasswordEncoder passwordEncoder() {
            return new BCryptPasswordEncoder();
        }
    }

Here we’re using the _httpBasic()_ element to define Basic Authentication inside the _SecurityFilterChain_ bean _._

We could achieve the same result using XML as well:
    
    
    <http pattern="/securityNone" security="none"/>
    <http use-expressions="true">
        <intercept-url pattern="/**" access="isAuthenticated()" />
        <http-basic />
    </http>
    
    <authentication-manager>
        <authentication-provider>
            <user-service>
                <user name="user1" password="{noop}user1Pass" authorities="ROLE_USER" />
            </user-service>
        </authentication-provider>
    </authentication-manager>

What’s relevant here is the _< http-basic>_ element inside the main _< http>_ element of the configuration. This is enough to enable Basic Authentication for the entire application. Since we’re not focusing on the Authentication Manager in this tutorial, we’ll use an in-memory manager with the user and password defined in plain text.

The _web.xml_ of the web application enabling Spring Security has already been discussed in the [Spring Logout tutorial](/spring-security-login#web_xml "Spring Security web.xml").

## **3\. Consuming the Secured Application**

The _curl_ command is our go-to tool for consuming the secured application.

First, let’s try to request the _/homepage.html_ without providing any security credentials:
    
    
    curl -i http://localhost:8080/spring-security-rest-basic-auth/api/foos/1

We get back the expected _401 Unauthorized_ and [the Authentication Challenge](https://datatracker.ietf.org/doc/html/rfc1945#section-10.16 "Basic Authentication Challenge"):
    
    
    HTTP/1.1 401 Unauthorized
    Server: Apache-Coyote/1.1
    Set-Cookie: JSESSIONID=E5A8D3C16B65A0A007CFAACAEEE6916B; Path=/spring-security-mvc-basic-auth/; HttpOnly
    WWW-Authenticate: Basic realm="Spring Security Application"
    Content-Type: text/html;charset=utf-8
    Content-Length: 1061
    Date: Wed, 29 May 2013 15:14:08 GMT

Normally the browser would interpret this challenge and prompt us for credentials with a simple dialog, but since we’re using _curl_ , this isn’t the case.

Now let’s request the same resource, the homepage, but **provide the credentials** to access it as well:
    
    
    curl -i --user user1:user1Pass 
      http://localhost:8080/spring-security-rest-basic-auth/api/foos/1

As a result, the response from the server is _200 OK_ along with a _Cookie_ :
    
    
    HTTP/1.1 200 OK
    Server: Apache-Coyote/1.1
    Set-Cookie: JSESSIONID=301225C7AE7C74B0892887389996785D; Path=/spring-security-mvc-basic-auth/; HttpOnly
    Content-Type: text/html;charset=ISO-8859-1
    Content-Language: en-US
    Content-Length: 90
    Date: Wed, 29 May 2013 15:19:38 GMT

From the browser, we can consume the application normally; the only difference is that a login page is no longer a hard requirement since all browsers support Basic Authentication, and use a dialog to prompt the user for credentials.

## **4\. Further Configuration – t****he Entry Point**

By default, the _BasicAuthenticationEntryPoint_ provisioned by Spring Security returns a full page for a _401 Unauthorized_ response back to the client. This HTML representation of the error renders well in a browser. Conversely, it’s not well suited for other scenarios, such as a REST API where a json representation may be preferred.

The namespace is flexible enough for this new requirement as well. To address this, the entry point can be overridden:
    
    
    <http-basic entry-point-ref="myBasicAuthenticationEntryPoint" />

The new entry point is defined as a standard bean:
    
    
    @Component
    public class MyBasicAuthenticationEntryPoint extends BasicAuthenticationEntryPoint {
    
        @Override
        public void commence(
          HttpServletRequest request, HttpServletResponse response, AuthenticationException authEx) 
          throws IOException, ServletException {
            response.addHeader("WWW-Authenticate", "Basic realm="" + getRealmName() + """);
            response.setStatus(HttpServletResponse.SC_UNAUTHORIZED);
            PrintWriter writer = response.getWriter();
            writer.println("HTTP Status 401 - " + authEx.getMessage());
        }
    
        @Override
        public void afterPropertiesSet() throws Exception {
            setRealmName("Baeldung");
            super.afterPropertiesSet();
        }
    }

By writing directly to the HTTP Response, we now have full control over the format of the response body.

## **5\. The Maven Dependencies**

The Maven dependencies for Spring Security have been discussed before in the [Spring Security with Maven article](/spring-security-with-maven "Spring Security with Maven"). We will need both _spring-security-web_ and _spring-security-config_ available at runtime.

## **6\. Conclusion**

In this article, we secured an MVC application with Spring Security and Basic Authentication. We discussed the XML configuration, and we consumed the application with simple curl commands. Finally, we took control of the exact error message format, moving from the standard HTML error page to a custom text or JSON format.

When the project runs locally, the sample HTML can be accessed at:

[http://localhost:8080/spring-security-rest-basic-auth/api/foos/1](http://localhost:8080/spring-security-mvc-basic-auth/homepage.html).
