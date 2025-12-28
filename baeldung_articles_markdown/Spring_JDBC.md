# Spring JDBC

## **1\. Overview**

In this tutorial, we’ll go through practical use cases of the Spring JDBC module.

All the classes in Spring JDBC are divided into four separate packages:

  * **_core_** — the core functionality of JDBC. Some of the important classes under this package include _JdbcTemplate_ ,_SimpleJdbcInsert_ , _SimpleJdbcCall,_ and _NamedParameterJdbcTemplate_
  * **_datasource_** — utility classes to access a data source. It also has various data source implementations for testing JDBC code outside the Jakarta EE container
  * **_object_** — DB access in an object-oriented manner. It allows running queries and returning the results as a business object. It also maps the query results between the columns and properties of business objects
  * **_support_** — support classes for classes under _core_ and _object_ packages, e.g., provides the _SQLException_ translation functionality  




## **2\. Maven Dependencies**

Let’s add the [_spring-boot-starter-jdbc_](https://mvnrepository.com/artifact/org.springframework.boot/spring-boot-starter-jdbc) and _[mysql-connector-j](https://mvnrepository.com/artifact/com.mysql/mysql-connector-j)_ to the _pom.xml_ :
    
    
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-jdbc</artifactId>
        <version>3.3.5</version>
    </dependency>
    <dependency>
        <groupId>com.mysql</groupId>
        <artifactId>mysql-connector-j</artifactId>
        <version>9.1.0</version>
    </dependency>
    

Also, let’s add the _[h2](https://mvnrepository.com/artifact/com.h2database/h2)_ dependency to the _pom.xml_ :
    
    
    <dependency>
        <groupId>com.h2database</groupId>
        <artifactId>h2</artifactId>
        <version>2.3.232</version>
        <scope>test</scope>
    </dependency>

The [H2 database](/spring-boot-h2-database) is an embedded database for fast prototyping.

## 3\. Configuration

There are two main approaches to configuring data sources in Spring: using properties files or using Java-based configuration.

### 3.1. MySQL Configuration

To configure the data source, let’s modify our _application.properties_ :
    
    
    spring.datasource.url=jdbc:mysql://localhost:3306/springjdbc
    spring.datasource.username=guest_user
    spring.datasource.password=guest_password
    spring.jpa.properties.hibernate.dialect=org.hibernate.dialect.MySQLDialect

Here, we configure the connection details to a MySQL database. We can now use it for database operations.

Notably, we can also configure the data source as a bean:
    
    
    @Configuration
    @ComponentScan("com.baeldung.jdbc")
    public class SpringJdbcConfig {
        @Bean
        public DataSource mysqlDataSource() {
            DriverManagerDataSource dataSource = new DriverManagerDataSource();
            dataSource.setDriverClassName("com.mysql.jdbc.Driver");
            dataSource.setUrl("jdbc:mysql://localhost:3306/springjdbc");
            dataSource.setUsername("guest_user");
            dataSource.setPassword("guest_password");
    
            return dataSource;
        }
    }

However, we should _prefer the application.properties_ file configuration because it separates the configuration from the code.

### 3.2. H2 Database Configuration

Alternatively, we can also make good use of an embedded database for development or testing. In that case, we can define the H2 database connection details in our _application.properties_ file:
    
    
    spring.datasource.url=jdbc:h2:mem:testdb
    spring.datasource.driverClassName=org.h2.Driver
    spring.datasource.username=sa
    spring.datasource.password=password
    spring.datasource.schema=classpath:jdbc/schema.sql
    spring.datasource.data=classpath:jdbc/test-data.sql

Alternatively, here’s a quick configuration that creates an instance of H2 embedded database and pre-populates it with simple SQL scripts as a bean:
    
    
    @Bean
    public DataSource dataSource() {
        return new EmbeddedDatabaseBuilder()
          .setType(EmbeddedDatabaseType.H2)
          .addScript("classpath:jdbc/schema.sql")
          .addScript("classpath:jdbc/test-data.sql").build();
    }

We can use this configuration if we don’t want to define it in the _application.properties_ file. However, configuring our data source in the _application.properties_ is generally preferred.

Notably, we can use [Spring profiles](/spring-profiles) to manage multiple configurations in a project.

## **4\. The _JdbcTemplate_ and Running Queries**

Let’s explore the basic usage of the _JdbcTemplate_.

### **4.1. Basic Queries**

The JDBC template is the main API through which we’ll access most of the functionality that we’re interested in:

  * creation and closing of connections
  * running statements and stored procedure calls
  * iterating over the _ResultSet_ and returning results



First, let’s start with a simple example to see what the _JdbcTemplate_ can do:
    
    
    int result = jdbcTemplate.queryForObject(
        "SELECT COUNT(*) FROM EMPLOYEE", Integer.class);
    

And here’s a simple INSERT:
    
    
    public int addEmplyee(int id) {
        return jdbcTemplate.update(
          "INSERT INTO EMPLOYEE VALUES (?, ?, ?, ?)", id, "Bill", "Gates", "USA");
    }

Notice the standard syntax of providing parameters using the _?_ character.

Next, let’s look at an alternative to this syntax.

### **4.2. Queries With Named Parameters**

To get **support for named parameters** , let’s use the other JDBC template provided by the framework — the _NamedParameterJdbcTemplate_.

It wraps the _JbdcTemplate_ and provides an alternative to the traditional syntax using ? to specify parameters.

Under the hood, it substitutes the named parameters to JDBC _?_ placeholder and delegates to the wrapped _JDCTemplate_ to run the queries:
    
    
    SqlParameterSource namedParameters = new MapSqlParameterSource().addValue("id", 1);
    return namedParameterJdbcTemplate.queryForObject(
      "SELECT FIRST_NAME FROM EMPLOYEE WHERE ID = :id", namedParameters, String.class);

Notice how we are using the _MapSqlParameterSource_ to provide the values for the named parameters.

Let’s look at using properties from a bean to determine the named parameters:
    
    
    Employee employee = new Employee();
    employee.setFirstName("James");
    
    String SELECT_BY_ID = "SELECT COUNT(*) FROM EMPLOYEE WHERE FIRST_NAME = :firstName";
    
    SqlParameterSource namedParameters = new BeanPropertySqlParameterSource(employee);
    return namedParameterJdbcTemplate.queryForObject(
      SELECT_BY_ID, namedParameters, Integer.class);

Note how we’re now using the _BeanPropertySqlParameterSource_ implementations instead of manually specifying the named parameters like before.

### **4.3. Mapping Query Results to Java Object**

Another very useful feature is the ability to map query results to Java objects by implementing the _RowMapper_ interface.

For example, for every row returned by the query, Spring uses the row mapper to populate the java bean:
    
    
    public class EmployeeRowMapper implements RowMapper<Employee> {
        @Override
        public Employee mapRow(ResultSet rs, int rowNum) throws SQLException {
            Employee employee = new Employee();
    
            employee.setId(rs.getInt("ID"));
            employee.setFirstName(rs.getString("FIRST_NAME"));
            employee.setLastName(rs.getString("LAST_NAME"));
            employee.setAddress(rs.getString("ADDRESS"));
    
            return employee;
        }
    }

Subsequently, we can now pass the row mapper to the query API and get fully populated Java objects:
    
    
    String query = "SELECT * FROM EMPLOYEE WHERE ID = ?";
    Employee employee = jdbcTemplate.queryForObject(query, new EmployeeRowMapper(), id);

## **5\. Exception Translation**

Spring comes with its own data exception hierarchy out of the box — with _DataAccessException_ as the root exception — and it translates all underlying raw exceptions to it.

So, we keep our sanity by not handling low-level persistence exceptions. We also benefit from the fact that Spring wraps the low-level exceptions in _DataAccessException_ or one of its sub-classes.

This also keeps the exception-handling mechanism independent of the underlying database we are using.

Besides the default _SQLErrorCodeSQLExceptionTranslator_ , we can also implement  _it ourselves_.

Here’s a quick example of a custom implementation — customizing the error message when there is a duplicate key violation, which results in [error code 23505](https://www.h2database.com/javadoc/org/h2/api/ErrorCode.html#c23505) when using H2:
    
    
    public class CustomSQLErrorCodeTranslator extends SQLErrorCodeSQLExceptionTranslator {
        @Override
        protected DataAccessException
          customTranslate(String task, String sql, SQLException sqlException) {
            if (sqlException.getErrorCode() == 23505) {
              return new DuplicateKeyException(
                "Custom Exception translator - Integrity constraint violation.", sqlException);
            }
            return null;
        }
    }

To use this custom exception translator, we need to pass it to the _JdbcTemplate_ by calling _setExceptionTranslator()_ method:
    
    
    CustomSQLErrorCodeTranslator customSQLErrorCodeTranslator = 
      new CustomSQLErrorCodeTranslator();
    jdbcTemplate.setExceptionTranslator(customSQLErrorCodeTranslator);

## **6\. JDBC Operations Using _SimpleJdbc_ Classes**

_SimpleJdbc_ classes provide an easy way to configure and run SQL statements. These classes use database metadata to build basic queries. So, _SimpleJdbcInsert_ and _SimpleJdbcCall_ classes provide an easier way to run insert and stored procedure calls.

### **6.1._SimpleJdbcInsert_**

Let’s take a look at running simple insert statements with minimal configuration.

**The INSERT statement is generated based on the configuration of _SimpleJdbcInsert_.** We need only provide the table, column, and value names.

First, let’s create a  _SimpleJdbcInsert_ :
    
    
    SimpleJdbcInsert simpleJdbcInsert = 
      new SimpleJdbcInsert(dataSource).withTableName("EMPLOYEE");

Next, let’s provide the column names and values and run the operation:
    
    
    public int addEmplyee(Employee emp) {
        Map<String, Object> parameters = new HashMap<String, Object>();
        parameters.put("ID", emp.getId());
        parameters.put("FIRST_NAME", emp.getFirstName());
        parameters.put("LAST_NAME", emp.getLastName());
        parameters.put("ADDRESS", emp.getAddress());
    
        return simpleJdbcInsert.execute(parameters);
    }

Further, we can use the _executeAndReturnKey()_ API to allow the **database to generate the primary key**. We’ll also need to configure the actual auto-generated column:
    
    
    SimpleJdbcInsert simpleJdbcInsert = new SimpleJdbcInsert(dataSource)
      .withTableName("EMPLOYEE")
      .usingGeneratedKeyColumns("ID");
    
    Number id = simpleJdbcInsert.executeAndReturnKey(parameters);
    System.out.println("Generated id - " + id.longValue());

Finally, we can pass in this data using the _BeanPropertySqlParameterSource_ and _MapSqlParameterSource_.

### **6.2. Stored Procedures With _SimpleJdbcCall_**

Let’s also take a look at running stored procedures.

We’ll make use of the _SimpleJdbcCall_ abstraction:
    
    
    SimpleJdbcCall simpleJdbcCall = new SimpleJdbcCall(dataSource).withProcedureName("READ_EMPLOYEE");
    
    
    
    public Employee getEmployeeUsingSimpleJdbcCall(int id) {
        SqlParameterSource in = new MapSqlParameterSource().addValue("in_id", id);
        Map<String, Object> out = simpleJdbcCall.execute(in);
    
        Employee emp = new Employee();
        emp.setFirstName((String) out.get("FIRST_NAME"));
        emp.setLastName((String) out.get("LAST_NAME"));
    
        return emp;
    }

## **7\. Batch Operations**

Another simple use case is batching multiple operations together.

### **7.1. Basic Batch Operations Using _JdbcTemplate_**

Using _JdbcTemplate_ ,_Batch Operations_ can be run via the _batchUpdate()_ API.

The interesting part here is the concise but highly useful _BatchPreparedStatementSetter_ implementation:
    
    
    public int[] batchUpdateUsingJdbcTemplate(List<Employee> employees) {
        return jdbcTemplate.batchUpdate("INSERT INTO EMPLOYEE VALUES (?, ?, ?, ?)",
            new BatchPreparedStatementSetter() {
                @Override
                public void setValues(PreparedStatement ps, int i) throws SQLException {
                    ps.setInt(1, employees.get(i).getId());
                    ps.setString(2, employees.get(i).getFirstName());
                    ps.setString(3, employees.get(i).getLastName());
                    ps.setString(4, employees.get(i).getAddress();
                }
                @Override
                public int getBatchSize() {
                    return 50;
                }
            });
    }

### **7.2. Batch Operations Using _NamedParameterJdbcTemplate_**

We also have the option of batching operations with the _NamedParameterJdbcTemplate_ – _batchUpdate()_ API.

This API is simpler than the previous one. So, there’s no need to implement any extra interfaces to set the parameters, as it has an internal prepared statement setter to set the parameter values.

Instead, the parameter values can be passed to the _batchUpdate()_ method as an array of _SqlParameterSource_.
    
    
    SqlParameterSource[] batch = SqlParameterSourceUtils.createBatch(employees.toArray());
    int[] updateCounts = namedParameterJdbcTemplate.batchUpdate(
      "INSERT INTO EMPLOYEE VALUES (:id, :firstName, :lastName, :address)", batch);
    return updateCounts;

## **8\. Conclusion**

In this article, we looked at the JDBC abstraction in the Spring Framework. We covered the various capabilities provided by Spring JDBC with practical examples.

We also looked into how we can quickly get started with Spring JDBC using a Spring Boot JDBC starter.
