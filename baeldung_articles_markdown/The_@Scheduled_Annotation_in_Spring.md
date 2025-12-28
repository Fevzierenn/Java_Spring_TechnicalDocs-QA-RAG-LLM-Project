# The @Scheduled Annotation in Spring

## **1\. Overview**

In this tutorial, we’ll illustrate how **the Spring _@Scheduled_ annotation **can be used to configure and schedule tasks.

The simple rules that we need to follow to annotate a method with _@Scheduled_ are:

  * the method should typically have a void return type (if not, the returned value will be ignored)
  * the method should not expect any parameters



## **2\. Enable Support for Scheduling**

To enable support for scheduling tasks and the _@Scheduled_ annotation in Spring, we can use the Java enable-style annotation:
    
    
    @Configuration
    @EnableScheduling
    public class SpringConfig {
        ...
    }

Conversely, we can do the same in XML:
    
    
    <task:annotation-driven>

## **3\. Schedule a Task at Fixed Delay**

Let’s start by configuring a task to run after a fixed delay:
    
    
    @Scheduled(fixedDelay = 1000)
    public void scheduleFixedDelayTask() {
        System.out.println(
          "Fixed delay task - " + System.currentTimeMillis() / 1000);
    }

In this case, the duration between the end of the last execution and the start of the next execution is fixed. The task always waits until the previous one is finished.

This option should be used when it’s mandatory that the previous execution is completed before running again.

## **4\. Schedule a Task at a Fixed Rate**

Let’s now execute a task at a fixed interval of time:
    
    
    @Scheduled(fixedRate = 1000)
    public void scheduleFixedRateTask() {
        System.out.println(
          "Fixed rate task - " + System.currentTimeMillis() / 1000);
    }

This option should be used when each execution of the task is independent.

Note that scheduled tasks don’t run in parallel by default. So even if we used _fixedRate_ , the next task won’t be invoked until the previous one is done.

**If we want to support parallel behavior in scheduled tasks, we need to add the _@Async_ annotation:**
    
    
    @EnableAsync
    public class ScheduledFixedRateExample {
        @Async
        @Scheduled(fixedRate = 1000)
        public void scheduleFixedRateTaskAsync() throws InterruptedException {
            System.out.println(
              "Fixed rate task async - " + System.currentTimeMillis() / 1000);
            Thread.sleep(2000);
        }
    
    }

Now this asynchronous task will be invoked each second, even if the previous task isn’t done.

## 5\. Fixed Rate vs Fixed Delay

We can run a scheduled task using Spring’s _@Scheduled_ annotation, but based on the properties _fixedDelay_ and  _fixedRate,_ the nature of execution changes.

**The _fixedDelay_ property makes sure that there is a delay of _n_ millisecond between the finish time of an execution of a task and the start time of the next execution of the task. **

This property is specifically useful when we need to make sure that only one instance of the task runs all the time. For dependent jobs, it is quite helpful.

**The _fixedRate_ property runs the scheduled task at every  _n_ millisecond.** It doesn’t check for any previous executions of the task.

This is useful when all executions of the task are independent. If we don’t expect to exceed the size of the memory and the thread pool, _fixedRate_ should be quite handy.

Although, if the incoming tasks do not finish quickly, it’s possible they end up with “Out of Memory exception”.

## **6\. Schedule a Task With Initial Delay**

Next, let’s schedule a task with a delay (in milliseconds):
    
    
    @Scheduled(fixedDelay = 1000, initialDelay = 1000)
    public void scheduleFixedRateWithInitialDelayTask() {
     
        long now = System.currentTimeMillis() / 1000;
        System.out.println(
          "Fixed rate task with one second initial delay - " + now);
    }

Note how we’re using both _fixedDelay_ as well as _initialDelay_ in this example. The task will be executed the first time after the _initialDelay_ value, and it will continue to be executed according to the _fixedDelay_.

This option is convenient when the task has a setup that needs to be completed.

## **7\. Schedule a Task Using Cron Expressions**

Sometimes delays and rates are not enough, and we need the flexibility of a cron expression to control the schedule of our tasks:
    
    
    @Scheduled(cron = "0 15 10 15 * ?")
    public void scheduleTaskUsingCronExpression() {
     
        long now = System.currentTimeMillis() / 1000;
        System.out.println(
          "schedule tasks using cron jobs - " + now);
    }

Note that in this example, we’re scheduling a task to be executed at 10:15 AM on the 15th day of every month.

By default, Spring will use the server’s local time zone for the cron expression. However, **we can use the _zone_ attribute to change this timezone**:
    
    
    @Scheduled(cron = "0 15 10 15 * ?", zone = "Europe/Paris")

With this configuration, Spring will schedule the annotated method to run at 10:15 AM on the 15th day of every month in Paris time.

## **8\. Parameterizing the Schedule**

Hardcoding these schedules is simple, but we usually need to be able to control the schedule without re-compiling and re-deploying the entire app.

We’ll make use of Spring Expressions to externalize the configuration of the tasks, and we’ll store these in properties files.

A _fixedDelay_ task:
    
    
    @Scheduled(fixedDelayString = "${fixedDelay.in.milliseconds}")

A _fixedRate_ task:
    
    
    @Scheduled(fixedRateString = "${fixedRate.in.milliseconds}")

A _cron_ expression based task:
    
    
    @Scheduled(cron = "${cron.expression}")

## **9\. Configuring Scheduled Tasks Using XML**

Spring also provides an XML way of configuring the scheduled tasks. Here is the XML configuration to set these up:
    
    
    <!-- Configure the scheduler -->
    <task:scheduler id="myScheduler" pool-size="10" />
    
    <!-- Configure parameters -->
    <task:scheduled-tasks scheduler="myScheduler">
        <task:scheduled ref="beanA" method="methodA" 
          fixed-delay="5000" initial-delay="1000" />
        <task:scheduled ref="beanB" method="methodB" 
          fixed-rate="5000" />
        <task:scheduled ref="beanC" method="methodC" 
          cron="*/5 * * * * MON-FRI" />
    </task:scheduled-tasks>

## 10\. Setting Delay or Rate Dynamically at Runtime

Normally, all the properties of the _@Scheduled_ annotation are resolved and initialized only once at Spring context startup.

Therefore, **changing the _fixedDelay_ or _fixedRate_ values at runtime isn’t possible when we use _@Scheduled_ annotation in Spring**.

However, there is a workaround. **Using Spring’s _SchedulingConfigurer_ provides a more customizable way to give us the opportunity of setting the delay or rate dynamically**.

Let’s create a Spring configuration, _DynamicSchedulingConfig_ , and implement the _SchedulingConfigurer_ interface:
    
    
    @Configuration
    @EnableScheduling
    public class DynamicSchedulingConfig implements SchedulingConfigurer {
    
        @Autowired
        private TickService tickService;
    
        @Bean
        public Executor taskExecutor() {
            return Executors.newSingleThreadScheduledExecutor();
        }
    
        @Override
        public void configureTasks(ScheduledTaskRegistrar taskRegistrar) {
            taskRegistrar.setScheduler(taskExecutor());
            taskRegistrar.addTriggerTask(
              new Runnable() {
                  @Override
                  public void run() {
                      tickService.tick();
                  }
              },
              new Trigger() {
                  @Override
                  public Date nextExecutionTime(TriggerContext context) {
                      Optional<Date> lastCompletionTime =
                        Optional.ofNullable(context.lastCompletionTime());
                      Instant nextExecutionTime =
                        lastCompletionTime.orElseGet(Date::new).toInstant()
                          .plusMillis(tickService.getDelay());
                      return Date.from(nextExecutionTime);
                  }
              }
            );
        }
    
    }

As we notice, with the help of the _ScheduledTaskRegistrar#addTriggerTask_ method, we can add a _Runnable_ task and a _Trigger_ implementation to recalculate the _nextExecutionTime_ after the end of each execution.

Additionally, we annotate our _DynamicSchedulingConfig_ with _@EnableScheduling_ to make the scheduling work.

As a result, we scheduled the _TickService#tick_ method to run it after each amount of delay, which is determined dynamically at runtime by the _getDelay_ method.

## 11\. Running Tasks in Parallel

By default, **Spring uses a local single-threaded scheduler to run the tasks**. As a result, even if we have multiple _@Scheduled_ methods, they each need to wait for the thread to complete executing a previous task.

If our tasks are truly independent, it’s more convenient to run them in parallel. For that, we need to provide a [_TaskScheduler_](/spring-task-scheduler) that better suits our needs:
    
    
    @Bean
    public TaskScheduler  taskScheduler() {
        ThreadPoolTaskScheduler threadPoolTaskScheduler = new ThreadPoolTaskScheduler();
        threadPoolTaskScheduler.setPoolSize(5);
        threadPoolTaskScheduler.setThreadNamePrefix("ThreadPoolTaskScheduler");
        return threadPoolTaskScheduler;
    }

In the above example, we configured the _TaskScheduler_ with a pool size of five, but keep in mind that the actual configuration should be fine-tuned to one’s specific needs.

### 11.1. Using Spring Boot

If we use Spring Boot, we can make use of an even more convenient approach to increase the scheduler’s pool size.

It’s simply enough to set the _spring.task.scheduling.pool.size_ property:  
`spring.task.scheduling.pool.size=5`

## **12\. Conclusion**

In this article, we discussed the way to **configure and use the _@Scheduled_ annotation**.

We covered the process to enable scheduling, and various ways of configuring scheduling task patterns. We also showed a workaround to configure the delay and rate dynamically.
