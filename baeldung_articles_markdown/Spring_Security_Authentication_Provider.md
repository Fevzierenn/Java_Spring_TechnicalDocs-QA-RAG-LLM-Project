# Spring Security Authentication Provider

## **1\. Overview**

In this tutorial, we’ll learn how to set up an **Authentication Provider in Spring Security,** allowing for additional flexibility compared to the standard scenario using a simple _UserDetailsService_.

## **2\. The Authentication Provider**

Spring Security provides a variety of options for performing authentication. These options follow a simple contract:**an _AuthenticationProvider_ processes an _Authentication_ request _,_** and a fully authenticated object with full credentials is returned.

The standard and most common implementation is the _DaoAuthenticationProvider,_ which retrieves the user details from a simple, read-only user DAO, the _UserDetailsService_. This User Details Service **only has access to the username** in order to retrieve the full user entity, which is enough for most scenarios.

More custom scenarios will still need to access the full _Authentication_ request to be able to perform the authentication process. For example, when authenticating against some external, third-party service (such as [Crowd](https://www.atlassian.com/software/crowd "Crowd - Identity Management")), **both the _username_ and _password_ from the authentication request will be necessary**.

For these more advanced scenarios, we’ll need to **define a custom Authentication Provider** :
    
    
    @Component
    public class CustomAuthenticationProvider implements AuthenticationProvider {
    
        @Override
        public Authentication authenticate(final Authentication authentication) throws AuthenticationException {
            final String name = authentication.getName();
            final String password = authentication.getCredentials().toString();
            if (!"admin".equals(name) || !"system".equals(password)) {
                return null;
            }
            return authenticateAgainstThirdPartyAndGetAuthentication(name, password);
        }
    
        @Override
        public boolean supports(Class<?> authentication) {
            return authentication.equals(UsernamePasswordAuthenticationToken.class);
        }
    }

Here, we have a generic method that returns an _Authentication_ object. Its implementation can vary based on how we want to authenticate. As an example, we can write an example of a fixed credentials method:
    
    
    private static UsernamePasswordAuthenticationToken authenticateAgainstThirdPartyAndGetAuthentication(String name, String password) {
        final List<GrantedAuthority> grantedAuths = new ArrayList<>();
        grantedAuths.add(new SimpleGrantedAuthority("ROLE_USER"));
        final UserDetails principal = new User(name, password, grantedAuths);
        return new UsernamePasswordAuthenticationToken(principal, password, grantedAuths);
    }

It is worth noting that we also add an authority to our _UserDetails_ object. In real-world scenarios, implementing the method above according to your needs is necessary as the short article may not cover all situations.

## **3\. Register the Auth Provider**

Now that we’ve defined the Authentication Provider, we need to specify it in the XML Security Configuration using the available namespace support:
    
    
    <http use-expressions="true">
        <intercept-url pattern="/**" access="isAuthenticated()"/>
        <http-basic/>
    </http>
    
    <authentication-manager>
        <authentication-provider
          ref="customAuthenticationProvider" />
    </authentication-manager>

## **4\. Java Configuration**

Next, we’ll take a look at the corresponding Java configuration:
    
    
    @Configuration
    @EnableWebSecurity
    @ComponentScan("com.baeldung.security")
    public class SecurityConfig {
    
        @Autowired
        private CustomAuthenticationProvider authProvider;
    
        @Bean
        public AuthenticationManager authManager(HttpSecurity http) throws Exception {
            AuthenticationManagerBuilder authenticationManagerBuilder = 
                http.getSharedObject(AuthenticationManagerBuilder.class);
            authenticationManagerBuilder.authenticationProvider(authProvider);
            return authenticationManagerBuilder.build();
        }
    
        @Bean
        public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
            return http.authorizeHttpRequests(request -> request.anyRequest()
                    .authenticated())
                .httpBasic(Customizer.withDefaults())
                .build();
        }
    }

Here, we configure the authentication mandatory for all the requests and configure the [Http basic authentication](/spring-security-basic-authentication) as well.

## **5\. Performing Authentication**

Requesting Authentication from the Client is basically the same with or without this custom authentication provider on the back end.

We’ll use a simple _curl_ command to send an authenticated request:
    
    
    curl --header "Accept:application/json" -i --user user1:user1Pass 
        http://localhost:8080/spring-security-custom/api/foo/1

For this example, we secured the REST API with Basic Authentication.

And we get back the expected 200 OK from the server:
    
    
    HTTP/1.1 200 OK
    Server: Apache-Coyote/1.1
    Set-Cookie: JSESSIONID=B8F0EFA81B78DE968088EBB9AFD85A60; Path=/spring-security-custom/; HttpOnly
    Content-Type: application/json;charset=UTF-8
    Transfer-Encoding: chunked
    Date: Sun, 02 Jun 2013 17:50:40 GMT

## **6\. Conclusion**

In this article, we explored an example of a custom authentication provider for Spring Security.
