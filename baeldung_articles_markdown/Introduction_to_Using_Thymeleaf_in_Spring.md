# Introduction to Using Thymeleaf in Spring

## **1\. Overview**

[Thymeleaf](http://www.thymeleaf.org/) is a Java template engine for processing and creating HTML, XML, JavaScript, CSS and text.

In this tutorial, we will discuss **how to use Thymeleaf with Spring** along with some basic use cases in the view layer of a Spring MVC application.

The library is extremely extensible, and its natural templating capability ensures we can prototype templates without a back end. This makes development very fast when compared with other popular template engines such as JSP.

## **2\. Integrating Thymeleaf With Spring**

First, let’s see the configurations required to integrate with Spring. The _thymeleaf-spring_ library is required for the integration.

We’ll add the following dependencies to our Maven POM file:
    
    
    <dependency>
        <groupId>org.thymeleaf</groupId>
        <artifactId>thymeleaf</artifactId>
        <version>3.1.2.RELEASE</version>
    </dependency>
    <dependency>
        <groupId>org.thymeleaf</groupId>
        <artifactId>thymeleaf-spring5</artifactId>
        <version>3.1.2.RELEASE</version>
    </dependency>

Note that, for a Spring 4 project, we have to use the _thymeleaf-spring4_ library instead of _thymeleaf-spring5_.

The _SpringTemplateEngine_ class performs all of the configuration steps.

We can configure this class as a bean in the Java configuration file:
    
    
    @Bean
    @Description("Thymeleaf Template Resolver")
    public ServletContextTemplateResolver templateResolver() {
        ServletContextTemplateResolver templateResolver = new ServletContextTemplateResolver();
        templateResolver.setPrefix("/WEB-INF/views/");
        templateResolver.setSuffix(".html");
        templateResolver.setTemplateMode("HTML5");
    
        return templateResolver;
    }
    
    @Bean
    @Description("Thymeleaf Template Engine")
    public SpringTemplateEngine templateEngine() {
        SpringTemplateEngine templateEngine = new SpringTemplateEngine();
        templateEngine.setTemplateResolver(templateResolver());
        templateEngine.setTemplateEngineMessageSource(messageSource());
        return templateEngine;
    }

The _templateResolver_ bean properties _prefix_ and _suffix_ indicate the location of the view pages within the _webapp_ directory and their filename extension, respectively.

The _ViewResolver_ interface in Spring MVC maps the view names returned by a controller to actual view objects. _ThymeleafViewResolver_ implements the _ViewResolver_ interface, and it’s used to determine which Thymeleaf views to render, given a view name.

The final step in the integration is to add the _ThymeleafViewResolver_ as a bean:
    
    
    @Bean
    @Description("Thymeleaf View Resolver")
    public ThymeleafViewResolver viewResolver() {
        ThymeleafViewResolver viewResolver = new ThymeleafViewResolver();
        viewResolver.setTemplateEngine(templateEngine());
        viewResolver.setOrder(1);
        return viewResolver;
    }

## 3\. **Thymeleaf in Spring Boot**

_Spring Boot_ provides auto-configuration for _Thymeleaf_ by adding the [_spring-boot-starter-thymeleaf_](https://mvnrepository.com/search?q=spring-boot-starter-thymeleaf) dependency:
    
    
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-thymeleaf</artifactId>
        <version>2.3.3.RELEASE</version>
    </dependency>
    

No explicit configuration is necessary. By default, HTML files should be placed in the _resources/templates_ location.

## **4\. Displaying Values From Message Source (Property Files)**

We can use the _th:text=”#{key}”_ tag attribute to display values from property files.

For this to work, we need to configure the property file as a _messageSource_ bean:
    
    
    @Bean
    @Description("Spring Message Resolver")
    public ResourceBundleMessageSource messageSource() {
        ResourceBundleMessageSource messageSource = new ResourceBundleMessageSource();
        messageSource.setBasename("messages");
        return messageSource;
    }

Here is the Thymeleaf HTML code to display the value associated with the key _welcome.message_ :
    
    
    <span th:text="#{welcome.message}" />

## **5\. Displaying Model Attributes**

### **5.1. Simple Attributes**

We can use the _th:text=”${attributename}”_ tag attribute to display the value of model attributes.

Let’s add a model attribute with the name _serverTime_ in the controller class:
    
    
    model.addAttribute("serverTime", dateFormat.format(new Date()));

And here’s the HTML code to display the value of _serverTime_ attribute:
    
    
    Current time is <span th:text="${serverTime}" />

### **5.2. Collection Attributes**

If the model attribute is a collection of objects, we can use the _th:each_ tag attribute to iterate over it.

Let’s define a _Student_ model class with two fields, _id_ and _name_ :
    
    
    public class Student implements Serializable {
        private Integer id;
        private String name;
        // standard getters and setters
    }

Now we will add a list of students as model attribute in the controller class:
    
    
    List<Student> students = new ArrayList<Student>();
    // logic to build student data
    model.addAttribute("students", students);

Finally, we can use Thymeleaf template code to iterate over the list of students and display all field values:
    
    
    <tbody>
        <tr th:each="student: ${students}">
            <td th:text="${student.id}" />
            <td th:text="${student.name}" />
        </tr>
    </tbody>

## **6\. Conditional Evaluation**

### **6.1._if_ and _unless_**

We use the _th:if=”${condition}”_ attribute to display a section of the view if the condition is met. And we use the _th:unless=”${condition}”_ attribute to display a section of the view if the condition is not met.

Let’s add a _gender_ field to the _Student_ model:
    
    
    public class Student implements Serializable {
        private Integer id;
        private String name;
        private Character gender;
        
        // standard getters and setters
    }

Suppose this field has two possible values (M or F) to indicate the student’s gender.

If we wish to display the words “Male” or “Female” instead of the single character, we could do this using this Thymeleaf code:
    
    
    <td>
        <span th:if="${student.gender} == 'M'" th:text="Male" /> 
        <span th:unless="${student.gender} == 'M'" th:text="Female" />
    </td>

### **6.2._switch_ and _case_**

We use the _th:switch_ and _th:case_ attributes to display content conditionally using the switch statement structure.

Let’s rewrite the previous code using the _th:switch_ and _th:case_ attributes:
    
    
    <td th:switch="${student.gender}">
        <span th:case="'M'" th:text="Male" /> 
        <span th:case="'F'" th:text="Female" />
    </td>

## **7\. Handling User Input**

We can handle form input using the _th:action=”@{url}”_ and _th:object=”${object}”_ attributes. We use _th:action_ to provide the form action URL and _th:object_ to specify an object to which the submitted form data will be bound.

Individual fields are mapped using the _th:field=”*{name}”_ attribute, where the _name_ is the matching property of the object.

For the _Student_ class, we can create an input form:
    
    
    <form action="#" th:action="@{/saveStudent}" th:object="${student}" method="post">
        <table border="1">
            <tr>
                <td><label th:text="#{msg.id}" /></td>
                <td><input type="number" th:field="*{id}" /></td>
            </tr>
            <tr>
                <td><label th:text="#{msg.name}" /></td>
                <td><input type="text" th:field="*{name}" /></td>
            </tr>
            <tr>
                <td><input type="submit" value="Submit" /></td>
            </tr>
        </table>
    </form>

In the above code, _/saveStudent_ is the form action URL and a _student_ is the object that holds the form data submitted.

The _saveStudent_ method handles the form submission:
    
    
    @RequestMapping(value = "/saveStudent", method = RequestMethod.POST)
    public String saveStudent(Model model, @ModelAttribute("student") Student student) {
        // logic to process input data
    }

The _@RequestMapping_ annotation maps the controller method with the URL provided in the form. The annotated method _saveStudent()_ performs the required processing for the submitted form. Finally, the _@ModelAttribute_ annotation binds the form fields to the _student_ object.

## **8\. Displaying Validation Errors**

We can use the _#fields.hasErrors()_ function to check if a field has any validation errors. And we use the _#fields.errors()_ function to display errors for a particular field. The field name is the input parameter for both these functions.

Let’s take a look at the HTML code to iterate and display the errors for each of the fields in the form:
    
    
    <ul>
        <li th:each="err : ${#fields.errors('id')}" th:text="${err}" />
        <li th:each="err : ${#fields.errors('name')}" th:text="${err}" />
    </ul>

Instead of field name, the above functions accept the wild card character _*_ or the constant _all_ to indicate all fields. We used the _th:each_ attribute to iterate the multiple errors that may be present for each of the fields.

Here’s the previous HTML code rewritten using the wildcard _*_ :
    
    
    <ul>
        <li th:each="err : ${#fields.errors('*')}" th:text="${err}" />
    </ul>

And here we’re using the constant _all_ :
    
    
    <ul>
        <li th:each="err : ${#fields.errors('all')}" th:text="${err}" />
    </ul>

Similarly, we can display global errors in Spring using the _global_ constant.

Here’s the HTML code to display global errors:
    
    
    <ul>
        <li th:each="err : ${#fields.errors('global')}" th:text="${err}" />
    </ul>

Also, we can use the _th:errors_ attribute to display error messages.

The previous code to display errors in the form can be rewritten using _th:errors_ attribute:
    
    
    <ul>
        <li th:errors="*{id}" />
        <li th:errors="*{name}" />
    </ul>

## **9\. Using Conversions**

We use the double bracket syntax _{{}}_ to format data for display. This makes use of the _formatters_ configured for that type of field in the _conversionService_ bean of the context file.

Let’s see how to format the name field in the _Student_ class:
    
    
    <tr th:each="student: ${students}">
        <td th:text="${{student.name}}" />
    </tr>

The above code uses the _NameFormatter_ class, configured by overriding the _addFormatters()_ method from the _WebMvcConfigurer_ interface.

For this purpose, our _@Configuration_ class overrides the _WebMvcConfigurerAdapter_ class:
    
    
    @Configuration
    public class WebMVCConfig extends WebMvcConfigurerAdapter {
        // ...
        @Override
        @Description("Custom Conversion Service")
        public void addFormatters(FormatterRegistry registry) {
            registry.addFormatter(new NameFormatter());
        }
    }

The _NameFormatter_ class implements the Spring _Formatter_ interface.

We can also use the _#conversions_ utility to convert objects for display. The syntax for the utility function is _#conversions.convert(Object, Class)_ where _Object_ is converted to _Class_ type.

Here’s how to display _student_ object _percentage_ field with the fractional part removed:
    
    
    <tr th:each="student: ${students}">
        <td th:text="${#conversions.convert(student.percentage, 'Integer')}" />
    </tr>

## **10\. Conclusion**

In this article, we’ve seen how to integrate and use Thymeleaf in a Spring MVC application.

We have also seen examples of how to display fields, accept input, display validation errors, and convert data for display.
