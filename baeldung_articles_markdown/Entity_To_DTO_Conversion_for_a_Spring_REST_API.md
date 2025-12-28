# Entity To DTO Conversion for a Spring REST API

## **1\. Overview**

In this tutorial, we’ll handle the conversions that need to happen **between the internal entities of a Spring application and the external[DTOs](/java-dto-pattern)** (Data Transfer Objects) that are published back to the client.

## **2\. Model Mapper**

Let’s start by introducing the main library that we’re going to use to perform this entity-DTO conversion, _[ModelMapper](http://modelmapper.org/getting-started/)_.

We will need this dependency in the _pom.xml_ :
    
    
    <dependency>
        <groupId>org.modelmapper</groupId>
        <artifactId>modelmapper</artifactId>
        <version>3.2.0</version>
    </dependency>

To check if there’s any newer version of this library, [go here](https://mvnrepository.com/artifact/org.modelmapper/modelmapper).

Then we’ll define the _ModelMapper_ bean in our Spring configuration:
    
    
    @Bean
    public ModelMapper modelMapper() {
        return new ModelMapper();
    }

## **3\. The DTO**

Next let’s introduce the DTO side of this two-sided problem, _Post_ DTO:
    
    
    public class PostDto {
        private static final SimpleDateFormat dateFormat
          = new SimpleDateFormat("yyyy-MM-dd HH:mm");
    
        private Long id;
    
        private String title;
    
        private String url;
    
        private String date;
    
        private UserDto user;
    
        public Date getSubmissionDateConverted(String timezone) throws ParseException {
            dateFormat.setTimeZone(TimeZone.getTimeZone(timezone));
            return dateFormat.parse(this.date);
        }
    
        public void setSubmissionDate(Date date, String timezone) {
            dateFormat.setTimeZone(TimeZone.getTimeZone(timezone));
            this.date = dateFormat.format(date);
        }
    
        // standard getters and setters
    }
    

Note that the two custom date related methods handle the date conversion back and forth between the client and the server:

  * _getSubmissionDateConverted()_ method converts date _String_ into a _Date_ in the server’s timezone to use it in the persisting _Post_ entity
  * _setSubmissionDate()_ method is to set DTO’s date to _Post_ ‘s _Date_ in current user timezone



## **4\. The Service Layer**

Now let’s look at a service level operation, which will obviously work with the Entity (not the DTO):
    
    
    public List<Post> getPostsList(
      int page, int size, String sortDir, String sort) {
     
        PageRequest pageReq
         = PageRequest.of(page, size, Sort.Direction.fromString(sortDir), sort);
     
        Page<Post> posts = postRepository
          .findByUser(userService.getCurrentUser(), pageReq);
        return posts.getContent();
    }

We’re going to have a look at the layer above service next, the controller layer. This is where the conversion will actually happen.

## **5\. The Controller Layer**

Next let’s examine a standard controller implementation, exposing the simple REST API for the _Post_ resource.

We’re going to show here a few simple CRUD operations: create, update, get one, and get all. Given that the operations are pretty straightforward, **we are especially interested in the Entity-DTO conversion aspects** :
    
    
    @Controller
    class PostRestController {
    
        @Autowired
        private IPostService postService;
    
        @Autowired
        private IUserService userService;
    
        @Autowired
        private ModelMapper modelMapper;
    
        @GetMapping
        @ResponseBody
        public List<PostDto> getPosts(...) {
            //...
            List<Post> posts = postService.getPostsList(page, size, sortDir, sort);
            return posts.stream()
              .map(this::convertToDto)
              .collect(Collectors.toList());
        }
    
        @PostMapping
        @ResponseStatus(HttpStatus.CREATED)
        @ResponseBody
        public PostDto createPost(@RequestBody PostDto postDto) {
            Post post = convertToEntity(postDto);
            Post postCreated = postService.createPost(post));
            return convertToDto(postCreated);
        }
    
        @GetMapping(value = "/{id}")
        @ResponseBody
        public PostDto getPost(@PathVariable("id") Long id) {
            return convertToDto(postService.getPostById(id));
        }
    
        @PutMapping(value = "/{id}")
        @ResponseStatus(HttpStatus.OK)
        public void updatePost(@PathVariable("id") Long id, @RequestBody PostDto postDto) {
            if(!Objects.equals(id, postDto.getId())){
                throw new IllegalArgumentException("IDs don't match");
            }
            Post post = convertToEntity(postDto);
            postService.updatePost(post);
        }
    }

Here is **our conversion from _Post_ entity to _PostDto_ :**
    
    
    private PostDto convertToDto(Post post) {
        PostDto postDto = modelMapper.map(post, PostDto.class);
        postDto.setSubmissionDate(post.getSubmissionDate(), 
            userService.getCurrentUser().getPreference().getTimezone());
        return postDto;
    }

Here is the conversion **from DTO to an entity** :
    
    
    private Post convertToEntity(PostDto postDto) throws ParseException {
        Post post = modelMapper.map(postDto, Post.class);
        post.setSubmissionDate(postDto.getSubmissionDateConverted(
          userService.getCurrentUser().getPreference().getTimezone()));
     
        if (postDto.getId() != null) {
            Post oldPost = postService.getPostById(postDto.getId());
            post.setRedditID(oldPost.getRedditID());
            post.setSent(oldPost.isSent());
        }
        return post;
    }

So as we can see, with the help of the model mapper, **the conversion logic is quick and simple.** We’re using the _map_ API of the mapper, and getting the data converted without writing a single line of conversion logic.

## **6\. Unit Testing**

Finally, let’s do a very simple test to make sure the conversions between the entity and the DTO work well:
    
    
    public class PostDtoUnitTest {
    
        private ModelMapper modelMapper = new ModelMapper();
    
        @Test
        public void whenConvertPostEntityToPostDto_thenCorrect() {
            Post post = new Post();
            post.setId(1L);
            post.setTitle(randomAlphabetic(6));
            post.setUrl("www.test.com");
    
            PostDto postDto = modelMapper.map(post, PostDto.class);
            assertEquals(post.getId(), postDto.getId());
            assertEquals(post.getTitle(), postDto.getTitle());
            assertEquals(post.getUrl(), postDto.getUrl());
        }
    
        @Test
        public void whenConvertPostDtoToPostEntity_thenCorrect() {
            PostDto postDto = new PostDto();
            postDto.setId(1L);
            postDto.setTitle(randomAlphabetic(6));
            postDto.setUrl("www.test.com");
    
            Post post = modelMapper.map(postDto, Post.class);
            assertEquals(postDto.getId(), post.getId());
            assertEquals(postDto.getTitle(), post.getTitle());
            assertEquals(postDto.getUrl(), post.getUrl());
        }
    }

## **7\. Conclusion**

In this article, we detailed **simplifying the conversion from Entity to DTO, and from DTO to Entity in a Spring REST API** , by using the model mapper library instead of writing these conversions by hand.
