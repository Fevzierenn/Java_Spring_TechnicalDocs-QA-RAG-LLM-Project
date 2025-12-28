# Spring Security Form Login

## **1\. Introduction**

This tutorial will focus on **Login with Spring Security**. We’re going to build on top of the [previous Spring MVC example](/spring-mvc-tutorial "MVC Tutorial"), as that’s a necessary part of setting up the web application along with the login mechanism.

## **2\. The Maven Dependencies**

When working with Spring Boot, the [_spring-boot-starter-security_](https://mvnrepository.com/artifact/org.springframework.boot/spring-boot-starter-security) starter will automatically include all dependencies, such as _spring-security-core_ , _spring-security-web_ , and _spring-security-config_ among others:
    
    
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-security</artifactId>
        <version>2.3.3.RELEASE</version>
    </dependency>

If we don’t use Spring Boot, please see the [Spring Security with Maven article](/spring-security-with-maven "Maven Spring Security tutorial"), which describes how to add all required dependencies. Both standard _spring-security-web_ and _spring-security-config_ will be required.

## **3\. Spring Security Java Configuration**

Let’s start by creating a Spring Security configuration class that creates a _SecurityFilterChain_ bean _._

By adding _@EnableWebSecurity_ , we get Spring Security and MVC integration support:
    
    
    @Configuration
    @EnableWebSecurity
    public class SecSecurityConfig {
    
        @Bean
        public InMemoryUserDetailsManager userDetailsService() {
            // InMemoryUserDetailsManager (see below)
        }
    
        @Bean
        public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
            // http builder configurations for authorize requests and form login (see below)
        }
    }

In this example, we used in-memory authentication and defined three users.

Next we’ll go through the elements we used to create the form login configuration.

Let’s start by building our Authentication Manager.

### **3.1. InMemoryUserDetailsManager**

The Authentication Provider is backed by a simple, in-memory implementation, _InMemoryUserDetailsManager_. This is useful for rapid prototyping when a full persistence mechanism is not yet necessary:
    
    
        @Bean
        public InMemoryUserDetailsManager userDetailsService() {
            UserDetails user1 = User.withUsername("user1")
                .password(passwordEncoder().encode("user1Pass"))
                .roles("USER")
                .build();
            UserDetails user2 = User.withUsername("user2")
                .password(passwordEncoder().encode("user2Pass"))
                .roles("USER")
                .build();
            UserDetails admin = User.withUsername("admin")
                .password(passwordEncoder().encode("adminPass"))
                .roles("ADMIN")
                .build();
            return new InMemoryUserDetailsManager(user1, user2, admin);
        }

Here we’ll configure three users with the username, password, and role hard-coded.

**Starting with Spring 5, we also have to define a password encoder**. In our example, we’ll use the _BCryptPasswordEncoder:_
    
    
    @Bean 
    public PasswordEncoder passwordEncoder() { 
        return new BCryptPasswordEncoder(); 
    }

Next let’s configure the _HttpSecurity._

### **3.2. Configuration to Authorize Requests**

We’ll start by doing the necessary configurations to Authorize Requests.

Here we’re allowing anonymous access on _/login_ so that users can authenticate. We’ll restrict _/admin_ to _ADMIN_ roles and securing everything else:
    
    
       @Bean
        public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
            http.csrf()
                .disable()
                .authorizeRequests()
                .antMatchers("/admin/**")
                .hasRole("ADMIN")
                .antMatchers("/anonymous*")
                .anonymous()
                .antMatchers("/login*")
                .permitAll()
                .anyRequest()
                .authenticated()
                .and()
                // ...
        }
    

Note that the order of the _antMatchers()_ elements is significant; **the more specific rules need to come first, followed by the more general ones**.

### **3.3. Configuration for Form Login**

Next we’ll extend the above configuration for form login and logout:
    
    
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
          // ...
          .and()
          .formLogin()
          .loginPage("/login.html")
          .loginProcessingUrl("/perform_login")
          .defaultSuccessUrl("/homepage.html", true)
          .failureUrl("/login.html?error=true")
          .failureHandler(authenticationFailureHandler())
          .and()
          .logout()
          .logoutUrl("/perform_logout")
          .deleteCookies("JSESSIONID")
          .logoutSuccessHandler(logoutSuccessHandler());
          return http.build();
    }

  * _loginPage()_ – the custom login page
  * _loginProcessingUrl()_ – the URL to submit the username and password to
  * _defaultSuccessUrl()_ – the landing page after a successful login
  * _failureUrl()_ – the landing page after an unsuccessful login
  * _logoutUrl()_ – the custom logout



## 4\. Add Spring Security to the Web Application

To use the above-defined Spring Security configuration, we need to attach it to the web application.

We’ll use the _WebApplicationInitializer_ , so we don’t need to provide any _web.xml:_
    
    
    public class AppInitializer implements WebApplicationInitializer {
    
        @Override
        public void onStartup(ServletContext sc) {
    
            AnnotationConfigWebApplicationContext root = new AnnotationConfigWebApplicationContext();
            root.register(SecSecurityConfig.class);
    
            sc.addListener(new ContextLoaderListener(root));
    
            sc.addFilter("securityFilter", new DelegatingFilterProxy("springSecurityFilterChain"))
              .addMappingForUrlPatterns(null, false, "/*");
        }
    }

**Note that this initializer isn’t necessary if we’re using a Spring Boot application.** For more details on how the security configuration is loaded in Spring Boot, have a look at our article on [Spring Boot security auto-configuration](/spring-boot-security-autoconfiguration).

## **5\. The Spring Security XML Configuration**

Let’s also have a look at the corresponding XML configuration.

The overall project is using Java configuration, so we need to import the XML configuration file via a Java _@Configuration_ class:
    
    
    @Configuration
    @ImportResource({ "classpath:webSecurityConfig.xml" })
    public class SecSecurityConfig {
       public SecSecurityConfig() {
          super();
       }
    }

And the Spring Security XML Configuration, _webSecurityConfig.xml_ :
    
    
    <http use-expressions="true">
        <intercept-url pattern="/login*" access="isAnonymous()" />
        <intercept-url pattern="/**" access="isAuthenticated()"/>
    
        <form-login login-page='/login.html' 
          default-target-url="/homepage.html" 
          authentication-failure-url="/login.html?error=true" />
        <logout logout-success-url="/login.html" />
    </http>
    
    <authentication-manager>
        <authentication-provider>
            <user-service>
                <user name="user1" password="user1Pass" authorities="ROLE_USER" />
            </user-service>
            <password-encoder ref="encoder" />
        </authentication-provider>
    </authentication-manager>
    
    <beans:bean id="encoder" 
      class="org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder">
    </beans:bean>

## **6\. The _web.xml_**

**Before the introduction of Spring 4** , we used to configure Spring Security in the _web.xml;_ only an additional filter added to the standard Spring MVC _web.xml_ :
    
    
    <display-name>Spring Secured Application</display-name>
    
    <!-- Spring MVC -->
    <!-- ... -->
    
    <!-- Spring Security -->
    <filter>
        <filter-name>springSecurityFilterChain</filter-name>
        <filter-class>org.springframework.web.filter.DelegatingFilterProxy</filter-class>
    </filter>
    <filter-mapping>
        <filter-name>springSecurityFilterChain</filter-name>
        <url-pattern>/*</url-pattern>
    </filter-mapping>

The filter –  _DelegatingFilterProxy_ – simply delegates to a Spring-managed bean – the  _FilterChainProxy_ – which itself is able to benefit from full Spring bean life-cycle management and such.

## **7\. The Login Form**

The login form page is going to be registered with Spring MVC using the straightforward mechanism to [map views names to URLs](/spring-mvc-tutorial#configviews "Spring MVC View Configuration"). Furthermore, there is no need for an explicit controller in between:
    
    
    registry.addViewController("/login.html");

This, of course, corresponds to the _login.jsp_ :
    
    
    <html>
    <head></head>
    <body>
       <h1>Login</h1>
       <form name='f' action="login" method='POST'>
          <table>
             <tr>
                <td>User:</td>
                <td><input type='text' name='username' value=''></td>
             </tr>
             <tr>
                <td>Password:</td>
                <td><input type='password' name='password' /></td>
             </tr>
             <tr>
                <td><input name="submit" type="submit" value="submit" /></td>
             </tr>
          </table>
      </form>
    </body>
    </html>

The **Spring Login form** has the following relevant artifacts:

  * _login_ – the URL where the form is POSTed to trigger the authentication process
  * _username_ – the username
  * _password_ – the password



## **8\. Further Configuring Spring Login**

We briefly discussed a few configurations of the login mechanism when we introduced the Spring Security Configuration above. Now let’s go into some greater detail.

One reason to override most of the defaults in Spring Security is to **hide that the application is secured with Spring Security.** We also want to minimize the information a potential attacker knows about the application.

Fully configured, the login element looks like this:
    
    
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http.formLogin()
          .loginPage("/login.html")
          .loginProcessingUrl("/perform_login")
          .defaultSuccessUrl("/homepage.html",true)
          .failureUrl("/login.html?error=true")
        return http.build();
    }

Or the corresponding XML configuration:
    
    
    <form-login 
      login-page='/login.html' 
      login-processing-url="/perform_login" 
      default-target-url="/homepage.html"
      authentication-failure-url="/login.html?error=true" 
      always-use-default-target="true"/>

### **8.1. The Login Page**

Next we’ll configure a custom login page using the _loginPage() method:_
    
    
    http.formLogin()
      .loginPage("/login.html")

Similarly, we can use the XML configuration:
    
    
    login-page='/login.html'

If we don’t specify this, Spring Security will generate a very basic Login Form at the _/login_ URL.

### **8.2. The POST URL for Login**

The default URL where the Spring Login will POST to trigger the authentication process is _/login,_ which used to be _/j_spring_security_check_ before [Spring Security 4](http://docs.spring.io/spring-security/site/migrate/current/3-to-4/html5/migrate-3-to-4-xml.html#m3to4-xmlnamespace-form-login).

We can use the _loginProcessingUrl_ method to override this URL:
    
    
    http.formLogin()
      .loginProcessingUrl("/perform_login")

We can also use the XML configuration:
    
    
    login-processing-url="/perform_login"

By overriding this default URL, we’re concealing that the application is actually secured with Spring Security. This information should not be available externally.

### **8.3. The Landing Page on Success**

After successfully logging in, we will be redirected to a page that by default is the root of the web application.

We can override this via the _defaultSuccessUrl()_ method:
    
    
    http.formLogin()
      .defaultSuccessUrl("/homepage.html")

Or with XML configuration:
    
    
    default-target-url="/homepage.html"

If the _always-use-default-target_ attribute is set to true, then the user is always redirected to this page. If that attribute is set to false, then the user will be redirected to the previous page they wanted to visit before being prompted to authenticate.

### **8.4. The Landing Page on Failure**

Similar to the Login Page, the Login Failure Page is autogenerated by Spring Security at _/login?_ error by default.

To override this, we can use the  _failureUrl()_ method:
    
    
    http.formLogin()
      .failureUrl("/login.html?error=true")

Or with XML:
    
    
    authentication-failure-url="/login.html?error=true"

## **9\. Conclusion**

In this **Spring Login Example** , we configured a simple authentication process. We also discussed the Spring Security Login Form, the Security Configuration, and some of the more advanced customizations available.

When the project runs locally, the sample HTML can be accessed at:
    
    
    http://localhost:8080/spring-security-mvc-login/login.html
