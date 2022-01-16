# Topic-Modelling-on-Tweets-Mentioning-Elon-Musk
## Topic Modelling
Topic modelling is an unsupervised learning technique used to represent text documents with the help of several topics. It does not require predefined list of tags for documents, instead, it analyzes text data to determine cluster words(topics) for a set of documents.
Let's say you run a start up which provides B2C service to your customers. You want to know what your customers are talking about your service inorder to take informed decision. Instead of manually going through heaps of feedback, in an attempt to deduce which texts are talking about your topics of interest, you could analyze them with a topic modeling algorithm.


There are several methods for doing topic modelling, but here, we will use the Latent Dirichlet Allocation (LDA) algorithm, probably the most popular topic modelling approach.
Latent Dirichlet Allocation (LDA)

## LDA
To understand the LDA algorithm, let's look at this example.
Suppose you have the following documents. 
Image by AuthorLDA would discover latent topics that these sentences contain. Given these sentences, LDA might produce something like:

<img src="https://user-images.githubusercontent.com/65237445/149661922-c0effb32-f8ea-4181-ba4a-1cb0e7292358.png" width="500" height = "300">

Document 1 and 2: 100% Topic A <br/>
Document 3 and 4: 100% Topic B <br/>
Document 5: 50% Topic A, 50% Topic B <br/>

where Topic A: 30% Apple, 10% orange, 10% milk, 10% pie, 10% market …. (One would interpret topic A to be about food) <br/> 
and Topic B: 30% market, 10% stationary, 10% bought, …….(One would interpret topic B to be about food) <br/>
Thus, LDA represents documents as a mixture of topics and every topic as a mixture of words.
