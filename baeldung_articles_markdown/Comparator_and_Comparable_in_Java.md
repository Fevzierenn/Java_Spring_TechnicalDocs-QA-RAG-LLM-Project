# Comparator and Comparable in Java

## **1\. Introduction**

Comparisons in Java are quite easy, until they’re not.

When working with custom types, or trying to compare objects that aren’t directly comparable, we need to make use of a comparison strategy. We can build one simply by making use of the _Comparator_ or _Comparable_ interfaces.

## **2\. Setting Up the Example**

Let’s use an example of a football team, where we want to line up the players by their rankings.

We’ll start by creating a simple _Player_ class:
    
    
    public class Player {
        private int ranking;
        private String name;
        private int age;
        
        // constructor, getters, setters  
    }

Next, we’ll create a _PlayerSorter_ class to create our collection, and attempt to sort it using _Collections.sort_ :
    
    
    public static void main(String[] args) {
        List<Player> footballTeam = new ArrayList<>();
        Player player1 = new Player(59, "John", 20);
        Player player2 = new Player(67, "Roger", 22);
        Player player3 = new Player(45, "Steven", 24);
        footballTeam.add(player1);
        footballTeam.add(player2);
        footballTeam.add(player3);
    
        System.out.println("Before Sorting : " + footballTeam);
        Collections.sort(footballTeam);
        System.out.println("After Sorting : " + footballTeam);
    }
    

As expected, this results in a compile-time error:
    
    
    The method sort(List<T>) in the type Collections 
      is not applicable for the arguments (ArrayList<Player>)

Now let’s try to understand what we did wrong here.

## **3._Comparable_**

As the name suggests, **_Comparable_ is an interface defining a strategy of comparing an object with other objects of the same type. This is called the class’s “natural ordering.”**

In order to be able to sort, we must define our _Player_ object as comparable by implementing the _Comparable_ interface:
    
    
    public class Player implements Comparable<Player> {
    
        // same as before
    
        @Override
        public int compareTo(Player otherPlayer) {
            return Integer.compare(getRanking(), otherPlayer.getRanking());
        }
    
    }
    

**The sorting order is decided by the return value of the _compareTo()_** **method.** The  _[Integer.compare(x, y)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/Integer.html#compare\(int,int\))_ returns -1 if  _x_ is less than  _y_ , 0 if they’re equal, and 1 otherwise.

The method returns a number indicating whether the object being compared is less than, equal to, or greater than the object being passed as an argument.

Now when we run our _PlayerSorter_ , we can see our _Players_ sorted by their ranking:
    
    
    Before Sorting : [John, Roger, Steven]
    After Sorting : [Steven, John, Roger]

Now that we have a clear understanding of natural ordering with _Comparable_ , let’s see **how we can use other types of ordering in a more flexible manner** than by directly implementing an interface.

## **4._Comparator_**

**The _Comparator_ interface defines a _compare(arg1, arg2)_ method** with two arguments that represent compared objects, and works similarly to the _Comparable.compareTo()_ method.

### **4.1. Creating _Comparators_**

To create a _Comparator,_ we have to implement the _Comparator_ interface.

For our first example, we’ll create a _Comparator_ to use the _ranking_ attribute of _Player_ to sort the players:
    
    
    public class PlayerRankingComparator implements Comparator<Player> {
    
        @Override
        public int compare(Player firstPlayer, Player secondPlayer) {
           return Integer.compare(firstPlayer.getRanking(), secondPlayer.getRanking());
        }
    
    }

Similarly, we can create a _Comparator_ to use the _age_ attribute of _Player_ to sort the players:
    
    
    public class PlayerAgeComparator implements Comparator<Player> {
    
        @Override
        public int compare(Player firstPlayer, Player secondPlayer) {
           return Integer.compare(firstPlayer.getAge(), secondPlayer.getAge());
        }
    
    }

### **4.2._Comparators_ in Action**

To demonstrate the concept, let’s modify our _PlayerSorter_ by introducing a second argument to the _Collections.sort_ method _,_ which is actually the instance of _Comparator_ we want to use.

**Using this approach, we can override the natural ordering** :
    
    
    PlayerRankingComparator playerComparator = new PlayerRankingComparator();
    Collections.sort(footballTeam, playerComparator);
    

Now let’s run our _PlayerRankingSorter to_ see the result:
    
    
    Before Sorting : [John, Roger, Steven]
    After Sorting by ranking : [Steven, John, Roger]

If we want a different sorting order, we only need to change the _Comparator_ we’re using:
    
    
    PlayerAgeComparator playerComparator = new PlayerAgeComparator();
    Collections.sort(footballTeam, playerComparator);

Now when we run our _PlayerAgeSorter_ , we can see a different sort order by _age:_
    
    
    Before Sorting : [John, Roger, Steven]
    After Sorting by age : [Roger, John, Steven]

### **4.3. Java 8 _Comparators_**

Java 8 provides new ways of defining _Comparators_ by using lambda expressions, and the _comparing()_ static factory method.

Let’s see a quick example of how to use a lambda expression to create a _Comparator_ :
    
    
    Comparator byRanking = 
      (Player player1, Player player2) -> Integer.compare(player1.getRanking(), player2.getRanking());

The _Comparator.comparing_ method takes a method calculating the property that will be used for comparing items, and returns a matching _Comparator_ instance:
    
    
    Comparator<Player> byRanking = Comparator
      .comparing(Player::getRanking);
    Comparator<Player> byAge = Comparator
      .comparing(Player::getAge);

To explore the Java 8 functionality in-depth, check out our [Java 8 Comparator.comparing](/java-8-comparator-comparing) guide.

## **5._Comparator_ vs _Comparable_**

**The _Comparable_ interface is a good choice to use for defining the default ordering, **or in other words, if it’s the main way of comparing objects.

So why use a _Comparator_ if we already have _Comparable_?

There are several reasons why:

  * Sometimes we can’t modify the source code of the class whose objects we want to sort, thus making the use of _Comparable_ impossible
  * Using _Comparators_ allows us to avoid adding additional code to our domain classes
  * We can define multiple different comparison strategies, which isn’t possible when using _Comparable_



## 6\. Avoiding the Subtraction Trick

Over the course of this tutorial, we’ve used the _Integer.compare()_ method to compare two integers. However, one might argue that we should use this clever one-liner instead:
    
    
    Comparator<Player> comparator = (p1, p2) -> p1.getRanking() - p2.getRanking();

**Although it’s much more concise than other solutions, it can be a victim of integer overflows in Java** :
    
    
    Player player1 = new Player(59, "John", Integer.MAX_VALUE);
    Player player2 = new Player(67, "Roger", -1);
    
    List<Player> players = Arrays.asList(player1, player2);
    players.sort(comparator);

Since -1 is much less than the  _Integer.MAX_VALUE_ , “Roger” should come before “John” in the sorted collection. **However, due to integer overflow, the _“Integer.MAX_VALUE – (-1)”_ will be less than zero**. So based on the _Comparator/Comparable_ contract, the  _Integer.MAX_VALUE_ is less than -1, which is obviously incorrect.

Therefore, despite what we expected, “John” comes before “Roger” in the sorted collection:
    
    
    assertEquals("John", players.get(0).getName());
    assertEquals("Roger", players.get(1).getName());

## **7\. Conclusion**

In this article, we explored the _Comparable_ and _Comparator_ interfaces, and discussed the differences between them.

To understand more advanced topics of sorting, check out our other articles, such as [Java 8 Comparator](/java-8-comparator-comparing), and [Java 8 Comparison with Lambdas](/java-8-sort-lambda).
