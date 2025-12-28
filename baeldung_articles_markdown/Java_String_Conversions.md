# Java String Conversions

## **1\. Overview**

In this quick article, we’ll explore some simple conversions of _String_ objects to different data types supported in Java.

## **2\. Converting _String_ to _int_ or _Integer_**

If we need to convert a _String_ to primitive _int_ or _Integer_ wrapper type, we can use either the _parseInt()_ or _valueOf()_ APIs to get the corresponding _int_ or _Integer_ return value:
    
    
    @Test
    public void whenConvertedToInt_thenCorrect() {
        String beforeConvStr = "1";
        int afterConvInt = 1;
    
        assertEquals(Integer.parseInt(beforeConvStr), afterConvInt);
    }
    
    @Test
    public void whenConvertedToInteger_thenCorrect() {
        String beforeConvStr = "12";
        Integer afterConvInteger = 12;
    
        assertEquals(Integer.valueOf(beforeConvStr).equals(afterConvInteger), true);
    }

## **3\. Converting _String_ to _long_ or _Long_**

If we need to convert a _String_ to primitive _long_ or _Long_ wrapper type, we can use _parseLong()_ or _valueOf()_ respectively:
    
    
    @Test
    public void whenConvertedTolong_thenCorrect() {
        String beforeConvStr = "12345";
        long afterConvLongPrimitive = 12345;
    
        assertEquals(Long.parseLong(beforeConvStr), afterConvLongPrimitive);
    }
    
    @Test
    public void whenConvertedToLong_thenCorrect() {
        String beforeConvStr = "14567";
        Long afterConvLong = 14567l;
    
        assertEquals(Long.valueOf(beforeConvStr).equals(afterConvLong), true);
    }

## **4\. Converting _String_ to _double_ or _Double_**

If we need to convert a _String_ to primitive _double_ or _Double_ wrapper type, we can use _parseDouble()_ or _valueOf()_ respectively:
    
    
    @Test
    public void whenConvertedTodouble_thenCorrect() {
        String beforeConvStr = "1.4";
        double afterConvDoublePrimitive = 1.4;
    
        assertEquals(Double.parseDouble(beforeConvStr), afterConvDoublePrimitive, 0.0);
    }
    
    @Test
    public void whenConvertedToDouble_thenCorrect() {
        String beforeConvStr = "145.67";
        double afterConvDouble = 145.67d;
    
        assertEquals(Double.valueOf(beforeConvStr).equals(afterConvDouble), true);
    }

## **5\. Converting _String_ to _ByteArray_**

In order to convert a _String_ to a byte array, _getBytes()_ encodes the _String_ into a sequence of bytes using the platform’s default charset, storing the result into a new byte array.

The behavior of _getBytes()_ is unspecified when the passed _String_ cannot be encoded using the default charset. As per the java [documentation](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/String.html), the [java.nio.charset.CharsetEncoder](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/nio/charset/CharsetEncoder.html) class should be used when more control over the encoding process is required:
    
    
    @Test
    public void whenConvertedToByteArr_thenCorrect() {
        String beforeConvStr = "abc";
        byte[] afterConvByteArr = new byte[] { 'a', 'b', 'c' };
    
        assertEquals(Arrays.equals(beforeConvStr.getBytes(), afterConvByteArr), true);
    }

## **6\. Converting _String_ to _CharArray_**

In order to convert a _String_ to a _CharArray_ instance, we can simply use _toCharArray()_ :
    
    
    @Test
    public void whenConvertedToCharArr_thenCorrect() {
        String beforeConvStr = "hello";
        char[] afterConvCharArr = { 'h', 'e', 'l', 'l', 'o' };
    
        assertEquals(Arrays.equals(beforeConvStr.toCharArray(), afterConvCharArr), true);
    }

## **7\. Converting _String_ to _boolean_ or _Boolean_**

To convert a _String_ instance to primitive _boolean_ or _Boolean_ wrapper type, we can use _parseBoolean()_ or _valueOf()_ APIs respectively:
    
    
    @Test
    public void whenConvertedToboolean_thenCorrect() {
        String beforeConvStr = "true";
        boolean afterConvBooleanPrimitive = true;
    
        assertEquals(Boolean.parseBoolean(beforeConvStr), afterConvBooleanPrimitive);
    }
    
    @Test
    public void whenConvertedToBoolean_thenCorrect() {
        String beforeConvStr = "true";
        Boolean afterConvBoolean = true;
    
        assertEquals(Boolean.valueOf(beforeConvStr), afterConvBoolean);
    }

## **8\. Converting _String_ to _Date_ or _LocalDateTime_**

Java 6 provides the _java.util.Date_ datatype for representing dates. Java 8 introduced new APIs for _Date_ and _Time_ to address the shortcomings of the older _java.util.Date_ and _java.util.Calendar_.

You can read [this](/java-8-date-time-intro) article for more details.

### **8.1. Converting _String_ to _java.util.Date_**

In order to convert _String_ objects to _Date_ objects, we need to first construct a _SimpleDateFormat_ object by passing the pattern describing the date and time format.

For example, a possible value for pattern could be “MM-dd-yyyy” or “yyyy-MM-dd”. Next, we need to invoke _parse_ method passing the _String_.

The _String_ passed as an argument should be in the same format as the pattern. Otherwise, a _ParseException_ will be thrown at runtime:
    
    
    @Test
    public void whenConvertedToDate_thenCorrect() throws ParseException {
        String beforeConvStr = "15/10/2013";
        int afterConvCalendarDay = 15;
        int afterConvCalendarMonth = 9;
        int afterConvCalendarYear = 2013;
        SimpleDateFormat formatter = new SimpleDateFormat("dd/M/yyyy");
        Date afterConvDate = formatter.parse(beforeConvStr);
        Calendar calendar = new GregorianCalendar();
        calendar.setTime(afterConvDate);
    
        assertEquals(calendar.get(Calendar.DAY_OF_MONTH), afterConvCalendarDay);
        assertEquals(calendar.get(Calendar.MONTH), afterConvCalendarMonth);
        assertEquals(calendar.get(Calendar.YEAR), afterConvCalendarYear);
    }

### **8.2. Converting _String_ to _java.time.LocalDateTime_**

_LocalDateTime_ is an immutable date-time object that represents a time, often viewed as year-month-day-hour-minute-second.

In order to convert String objects to _LocalDateTime_ objects, we can simply use the _parse_ API:
    
    
    @Test
    public void whenConvertedToLocalDateTime_thenCorrect() {
        String str = "2007-12-03T10:15:30";
        int afterConvCalendarDay = 03;
        Month afterConvCalendarMonth = Month.DECEMBER;
        int afterConvCalendarYear = 2007;
        LocalDateTime afterConvDate 
          = new UseLocalDateTime().getLocalDateTimeUsingParseMethod(str);
    
        assertEquals(afterConvDate.getDayOfMonth(), afterConvCalendarDay);
        assertEquals(afterConvDate.getMonth(), afterConvCalendarMonth);
        assertEquals(afterConvDate.getYear(), afterConvCalendarYear);
    }

The _String_ must represent a valid time according to [java.time.format.DateTimeFormatter.ISO_LOCAL_DATE_TIME](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/time/format/DateTimeFormatter.html#ISO_LOCAL_DATE_TIME). Otherwise, a _ParseException_ will be thrown at runtime.

For example ‘ _2011-12-03_ ‘ represents a valid string format having 4 digits for the year, 2 digits for the month for a year and 2 digits for the day of the month.

## **9\. Conclusion**

In this quick tutorial, we have covered different utility methods for converting S _tring_ objects to different data types supported in java.
