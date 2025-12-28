# Two Factor Auth with Spring Security

## **1\. Overview**

In this tutorial, we’re going to implement [Two Factor Authentication functionality](https://en.wikipedia.org/wiki/Multi-factor_authentication) with a Soft Token and Spring Security.

We’re going to be adding the new functionality into [an existing, simple login flow](https://github.com/Baeldung/spring-security-registration) and use the [Google Authenticator app](https://play.google.com/store/apps/details?id=com.google.android.apps.authenticator2&hl=en) to generate the tokens.

Simply put, two factor authentication is a verification process which follows the well known principle of “something the user knows and something the user has”.

And so, users provide an extra “verification token” during authentication – a one-time password verification code based on Time-based One-time Password [TOTP](https://tools.ietf.org/html/rfc6238) algorithm.

## **2\. Maven Configuration**

First, in order to use Google Authenticator in our app we need to:

  * Generate secret key
  * Provide secret key to the user via QR-code
  * Verify token entered by the user using this secret key.



We will use a simple server-side [library](https://github.com/aerogear/aerogear-otp-java) to generate/verify one-time password by adding the following dependency to our _pom.xml_ :
    
    
    <dependency>
        <groupId>org.jboss.aerogear</groupId>
        <artifactId>aerogear-otp-java</artifactId>
        <version>1.0.0</version>
    </dependency>

## **3\. User Entity**

Next, we will modify our user entity to hold extra information – as follows:
    
    
    @Entity
    public class User {
        ...
        private boolean isUsing2FA;
        private String secret;
    
        public User() {
            super();
            this.secret = Base32.random();
            ...
        }
    }

Note that:

  * We save a random secret code for each user to be used later in generating verification code
  * Our 2-step verification is optional



## **4\. Extra Login Parameter**

First, we will need to adjust our security configuration to accept extra parameter – verification token. We can accomplish that by using custom _AuthenticationDetailsSource_ :

Here is our _CustomWebAuthenticationDetailsSource_ :
    
    
    @Component
    public class CustomWebAuthenticationDetailsSource implements 
      AuthenticationDetailsSource<HttpServletRequest, WebAuthenticationDetails> {
        
        @Override
        public WebAuthenticationDetails buildDetails(HttpServletRequest context) {
            return new CustomWebAuthenticationDetails(context);
        }
    }

and here is _CustomWebAuthenticationDetails_ :
    
    
    public class CustomWebAuthenticationDetails extends WebAuthenticationDetails {
    
        private String verificationCode;
    
        public CustomWebAuthenticationDetails(HttpServletRequest request) {
            super(request);
            verificationCode = request.getParameter("code");
        }
    
        public String getVerificationCode() {
            return verificationCode;
        }
    }

And our security configuration:
    
    
    @Configuration
    @EnableWebSecurity
    public class LssSecurityConfig {
    
        @Autowired
        private CustomWebAuthenticationDetailsSource authenticationDetailsSource;
    
        @Bean
        public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
            http.formLogin()
                .authenticationDetailsSource(authenticationDetailsSource)
                ...
        } 
    }

And finally add the extra parameter to our login form:
    
    
    <labelth:text="#{label.form.login2fa}">
        Google Authenticator Verification Code
    </label>
    <input type='text' name='code'/>

Note: We need to set our custom _AuthenticationDetailsSource_ in our security configuration.

## **5\. Custom Authentication Provider**

Next, we’ll need a custom _AuthenticationProvider_ to handle extra parameter validation:
    
    
    public class CustomAuthenticationProvider extends DaoAuthenticationProvider {
    
        @Autowired
        private UserRepository userRepository;
    
        @Override
        public Authentication authenticate(Authentication auth)
          throws AuthenticationException {
            String verificationCode 
              = ((CustomWebAuthenticationDetails) auth.getDetails())
                .getVerificationCode();
            User user = userRepository.findByEmail(auth.getName());
            if ((user == null)) {
                throw new BadCredentialsException("Invalid username or password");
            }
            if (user.isUsing2FA()) {
                Totp totp = new Totp(user.getSecret());
                if (!isValidLong(verificationCode) || !totp.verify(verificationCode)) {
                    throw new BadCredentialsException("Invalid verfication code");
                }
            }
            
            Authentication result = super.authenticate(auth);
            return new UsernamePasswordAuthenticationToken(
              user, result.getCredentials(), result.getAuthorities());
        }
    
        private boolean isValidLong(String code) {
            try {
                Long.parseLong(code);
            } catch (NumberFormatException e) {
                return false;
            }
            return true;
        }
    
        @Override
        public boolean supports(Class<?> authentication) {
            return authentication.equals(UsernamePasswordAuthenticationToken.class);
        }
    }

Note that – after we verified the one-time-password verification code, we simply delegated authentication downstream.

Here is our Authentication Provider bean
    
    
    @Bean
    public DaoAuthenticationProvider authProvider() {
        CustomAuthenticationProvider authProvider = new CustomAuthenticationProvider();
        authProvider.setUserDetailsService(userDetailsService);
        authProvider.setPasswordEncoder(encoder());
        return authProvider;
    }

## **6\. Registration Process**

Now, in order for users to be able to use the application to generate the tokens, they’ll need to set things up properly when they register.

And so, we’ll need to do few simple modifications to the registration process – to allow users who have chosen to use 2-step verification to **scan the QR-code they need to login later**.

First, we add this simple input to our registration form:
    
    
    Use Two step verification <input type="checkbox" name="using2FA" value="true"/>

Then, in our _RegistrationController_ – we redirect users based on their choices after confirming registration:
    
    
    @GetMapping("/registrationConfirm")
    public String confirmRegistration(@RequestParam("token") String token, ...) {
        String result = userService.validateVerificationToken(token);
        if(result.equals("valid")) {
            User user = userService.getUser(token);
            if (user.isUsing2FA()) {
                model.addAttribute("qr", userService.generateQRUrl(user));
                return "redirect:/qrcode.html?lang=" + locale.getLanguage();
            }
            
            model.addAttribute(
              "message", messages.getMessage("message.accountVerified", null, locale));
            return "redirect:/login?lang=" + locale.getLanguage();
        }
        ...
    }

And here is our method _generateQRUrl()_ :
    
    
    public static String QR_PREFIX = 
      "https://chart.googleapis.com/chart?chs=200x200&chld=M%%7C0&cht=qr&chl=";
    
    @Override
    public String generateQRUrl(User user) {
        return QR_PREFIX + URLEncoder.encode(String.format(
          "otpauth://totp/%s:%s?secret=%s&issuer=%s", 
          APP_NAME, user.getEmail(), user.getSecret(), APP_NAME),
          "UTF-8");
    }

And here is our _qrcode.html_ :
    
    
    <html>
    <body>
    <div id="qr">
        <p>
            Scan this Barcode using Google Authenticator app on your phone 
            to use it later in login
        </p>
        <img th:src="${param.qr[0]}"/>
    </div>
    <a href="/login" class="btn btn-primary">Go to login page</a>
    </body>
    </html>

Note that:

  * _generateQRUrl()_ method is used to generate QR-code URL
  * This QR-code will be scanned by users mobile phones using Google Authenticator app
  * The app will generate a 6-digit code that is valid for only 30 seconds which is desired verification code
  * This verification code will be verified while login using our custom _AuthenticationProvider_



## **7\. Enable Two Step Verification**

Next, we will make sure that users can change their login preferences at any time – as follows:
    
    
    @PostMapping("/user/update/2fa")
    public GenericResponse modifyUser2FA(@RequestParam("use2FA") boolean use2FA) 
      throws UnsupportedEncodingException {
        User user = userService.updateUser2FA(use2FA);
        if (use2FA) {
            return new GenericResponse(userService.generateQRUrl(user));
        }
        return null;
    }

And here is _updateUser2FA()_ :
    
    
    @Override
    public User updateUser2FA(boolean use2FA) {
        Authentication curAuth = SecurityContextHolder.getContext().getAuthentication();
        User currentUser = (User) curAuth.getPrincipal();
        currentUser.setUsing2FA(use2FA);
        currentUser = repository.save(currentUser);
        
        Authentication auth = new UsernamePasswordAuthenticationToken(
          currentUser, currentUser.getPassword(), curAuth.getAuthorities());
        SecurityContextHolder.getContext().setAuthentication(auth);
        return currentUser;
    }

And here is the front-end:
    
    
    <div th:if="${#authentication.principal.using2FA}">
        You are using Two-step authentication 
        <a href="#" onclick="disable2FA()">Disable 2FA</a> 
    </div>
    <div th:if="${! #authentication.principal.using2FA}">
        You are not using Two-step authentication 
        <a href="#" onclick="enable2FA()">Enable 2FA</a> 
    </div>
    <br/>
    <div id="qr" style="display:none;">
        <p>Scan this Barcode using Google Authenticator app on your phone </p>
    </div>
    
    <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>
    <script type="text/javascript">
    function enable2FA(){
        set2FA(true);
    }
    function disable2FA(){
        set2FA(false);
    }
    function set2FA(use2FA){
        $.post( "/user/update/2fa", { use2FA: use2FA } , function( data ) {
            if(use2FA){
            	$("#qr").append('<img src="'+data.message+'" />').show();
            }else{
                window.location.reload();
            }
        });
    }
    </script>

## **8\. Conclusion**

In this quick tutorial, we illustrated how to do a two-factor authentication implementation using a Soft Token with Spring Security.
