# Java toString() Method

## 1\. Overview

Every class in Java is a child of the _Object_ class either directly or indirectly. And since the  _Object_ class contains a  _toString()_ method, we can call _toString()_ on any instance and get its string representation.

In this tutorial, we’ll look at the**default behavior of _toString()_ and learn how to change its behavior.**

## 2\. Default Behavior

Whenever we print an object reference, it invokes the _toString()_ method internally. So, if we don’t define a  _toString()_ method in our class, then _Object#__toString()_ is invoked.

_Object’s_  _toString()_ method is pretty generic:
    
    
    public String toString() {
        return getClass().getName()+"@"+Integer.toHexString(hashCode());
    }

To see how this works, let’s create a  _Customer_ object that we’ll use throughout our tutorial:
    
    
    public class Customer {
        private String firstName;
        private String lastName;
        // standard getters and setters. No toString() implementation
    }

Now, if we try to print our _C_ _ustomer_ object,  _Object_ #_toString()_ will be called, and the output will be similar to:
    
    
    com.baeldung.tostring.Customer@6d06d69c

## 3\. Overriding Default Behavior

Looking at the above output, we can see that it doesn’t give us much information about the contents of our  _Customer_ object. **Generally, we aren’t interested in knowing the hashcode of an object, but rather the contents of our object’s attributes.**

By overriding the default behavior of the _toString()_ method, we can make the output of the method call more meaningful.

Now, let’s look at a few different scenarios using objects to see how we can override this default behavior.

## 4\. Primitive Types and _Strings_

Our  _Customer_ object has both  _String_ and primitive attributes. We need to override the  _toString()_ method to achieve a more meaningful output:
    
    
    public class CustomerPrimitiveToString extends Customer {
        private long balance;
    
        @Override
        public String toString() {
            return "Customer [balance=" + balance + ", getFirstName()=" + getFirstName()
              + ", getLastName()=" + getLastName() + "]";
        }
    }
    

Let’s see what we get when we call _toString()_ now:
    
    
    @Test
    public void givenPrimitive_whenToString_thenCustomerDetails() {
        CustomerPrimitiveToString customer = new CustomerPrimitiveToString();
        customer.setFirstName("Rajesh");
        customer.setLastName("Bhojwani");
        customer.setBalance(110);
        assertEquals("Customer [balance=110, getFirstName()=Rajesh, getLastName()=Bhojwani]", 
          customer.toString());
    }

## 5\. Complex Java Objects

Let’s now consider a scenario where our _Customer_ object also contains an _order_ attribute that is of type  _Order._ Our  _Order_ class has both  _String_ and primitive data type fields.

So, let’s override _toString()_ again:
    
    
    public class CustomerComplexObjectToString extends Customer {
        private Order order;
        //standard setters and getters
        
        @Override
        public String toString() {
            return "Customer [order=" + order + ", getFirstName()=" + getFirstName()
              + ", getLastName()=" + getLastName() + "]";
        }      
    }

**Since _order_ is a complex object _,_ if we just print our  _Customer_ object, without overriding the  _toString()_ method in our  _Order_ class, it will print _orders_ as  _Order@ <hashcode>. _**

To fix that let’s override  _toString()_ in _Order_ , too:
    
    
    public class Order {
        
        private String orderId;
        private String desc;
        private long value;
        private String status;
     
        @Override
        public String toString() {
            return "Order [orderId=" + orderId + ", desc=" + desc + ", value=" + value + "]";
        }
    }
    

Now, let’s see what happens when we call the  _toString()_ method on our _Customer_ object that contains an  _order_ attribute:
    
    
    @Test
    public void givenComplex_whenToString_thenCustomerDetails() {
        CustomerComplexObjectToString customer = new CustomerComplexObjectToString();    
        // .. set up customer as before
        Order order = new Order();
        order.setOrderId("A1111");
        order.setDesc("Game");
        order.setStatus("In-Shiping");
        customer.setOrders(order);
            
        assertEquals("Customer [order=Order [orderId=A1111, desc=Game, value=0], " +
          "getFirstName()=Rajesh, getLastName()=Bhojwani]", customer.toString());
    }

## 6\. Array of Objects

Next, let’s change our _Customer_ to have an array of  _Order_ s _._ If we just print our  _Customer_ object, without special handling for our  _orders_ object, it will print _orders_ as  _Order;@ <hashcode>_.

To fix that let’s use  _[Arrays.toString()](/java-array-to-string) _for the  _orders_ field:
    
    
    public class CustomerArrayToString  extends Customer {
        private Order[] orders;
    
        @Override
        public String toString() {
            return "Customer [orders=" + Arrays.toString(orders) 
              + ", getFirstName()=" + getFirstName()
              + ", getLastName()=" + getLastName() + "]";
        }    
    }
    

Let’s see the results of calling the above _toString()_ method:
    
    
    @Test
    public void givenArray_whenToString_thenCustomerDetails() {
        CustomerArrayToString customer = new CustomerArrayToString();
        // .. set up customer as before
        // .. set up order as before
        customer.setOrders(new Order[] { order });         
        
        assertEquals("Customer [orders=[Order [orderId=A1111, desc=Game, value=0]], " +
          "getFirstName()=Rajesh, getLastName()=Bhojwani]", customer.toString());
    }

## 7\. Wrappers, Collections, and _StringBuffers_

When an object is made up entirely of [wrappers](/java-wrapper-classes), [collections](/java-collections), or [_StringBuffer_ s](/java-collections), no custom _toString()_ implementation is required because these objects have already overridden the _toString()_ method with meaningful representations:
    
    
    public class CustomerWrapperCollectionToString extends Customer {
        private Integer score; // Wrapper class object
        private List<String> orders; // Collection object
        private StringBuffer fullname; // StringBuffer object
      
        @Override
        public String toString() {
            return "Customer [score=" + score + ", orders=" + orders + ", fullname=" + fullname
              + ", getFirstName()=" + getFirstName() + ", getLastName()=" + getLastName() + "]";
        }
    }
    

Let’s again see the results of calling  _toString()_ :
    
    
    @Test
    public void givenWrapperCollectionStrBuffer_whenToString_thenCustomerDetails() {
        CustomerWrapperCollectionToString customer = new CustomerWrapperCollectionToString();
        // .. set up customer as before
        // .. set up orders as before 
        customer.setOrders(new Order[] { order }); 
        
        StringBuffer fullname = new StringBuffer();
        fullname.append(customer.getLastName()+ ", " + customer.getFirstName());
        
        assertEquals("Customer [score=8, orders=[Book, Pen], fullname=Bhojwani, Rajesh, getFirstName()=Rajesh, "
          + "getLastName()=Bhojwani]", customer.toString());
    }

## 8\. Conclusion

In this article, we looked at creating our own implementations of the  _toString()_ method.
