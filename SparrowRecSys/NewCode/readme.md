# 2021年2月11日

牛年快乐，新春大吉。

So I have to admit that this project is built on some other people's implementation. And what I have done is to understand what they have done and redo it on my own settings.

What I have practiced is divided into following parts: 

## Embedding

In this part, we try to do the embedding for the movie IDs (and user IDs). 

The Jupyter notebooks or code scripts are saved in `SparrowRecSys/NewCode/PythonPart/Embedding/OtherMethods`. While the embedding results are recommended to be put in `SparrowRecSys/NewCode/PythonPart/Embedding/OtherMethods/preprocessedData`

I mainly tried the following methods:

* **Item2Vec**. 
  * In file `FE-Item2Vec.ipynb`. 
  * The basic logic of the Item2Vec here is  that you order the movies that a user watches by rating timestamp as a sentence, i.e., each user has a movie "sentence". All the sentences are used to do **Word2Vec** embedding. 
  * In this notebook, you can also find the implementation of embedding users: summing up the movie IDs watched by a user as his/her embedding vector. 
* **DeepWalk + Word2Vec**. 
  * In file ``FE-DeepWalk_Item2Vec.ipynb``. 
  * Use the **DeepWalk** to generate the sequence, unlike what has been done in Item2Vec which regard the rating sequence as sentences. The so-called DeepWalk is described as follows. But to be noted that I used some other people's opensource implementation.  
    * You look into the rate time sequence again. For a user, if he watches movie A before movie B, then you draw a graph by adding a new edge like A --> B. Then you go through all of the movies and rating sequence, to build the whole graph. 
    * With the while graph built, you start random walking, starting from a random point. After several steps (e.g., 10 steps. The number of steps is a hyper-parameter), you generate a new sequence. Then you repeat the walking for several times (e.g., 10000 times. This is another hyper-parameter), you generate a lot of new sequences. 
    * Use the new sequences to do Word2Vec embedding. 
* **Deep image feature vector models + movie posters**. 
  * In file `FE-ImageEmbedding.ipynb` . 
  * Find the posters of each movie, and then use deep image classification networks (you can find a lot on TensorFlow Hub or PyTorch Hub) to extract the feature vector as embedding. In code I used EfficientNet, while any other nets can all work. 
* **(Unverified method)** Deep image feature vector models + movie posters + item2vec. 
  * In file `FE-ImageEmbedding_MultiLabel.ipynb` . 
  * The basic idea is that: based on Item2Vec principle, this method adds a process that do the embedding between image's feature vector extracted by deep learning models and skip-gram label data.  
  * How did I do? 
    * Just like Item2Vec, but the difference is that the "item" is not a traditional item but the image feature vectors. 
    * And build a new network structure, it can be done. 

## Feature engineering

Mainly contains 2 parts. The first part is in `SparrowRecSys\NewCode\PythonPart\Data2Redis`. In this part, notebook is used to upload the data into Redis. The second part is in `SparrowRecSys\NewCode\PythonPart\FeatureEngineering\newCode`. In this part, we can generate user and movie related features for deep learning recommendation model training. 

* `1-csv2redis.ipynb` in the first part. This part is very easy, just put the movies.csv and ratings.csv into redis for later usage. We can just pass this step. But I'd like to practice the Redis usage, so I do so. 
* `FeatureEngineering.ipynb` in the second part. This part mainly uses the PySpark to do feature calculation. It is also a good chance for us to learn how to do feature calculation with Spark APIs (which is pretty unfamiliar for you). After all, Spark seems to be more main-stream in feature calculation. 

## Model fitting

In this part, there are a lot of models can be used. But my main focus is DeepFM. Find the models training notebooks in `SparrowRecSys\NewCode\PythonPart\ModelTraining`. The model training notebooks can generate TF2 SavedModels. 

* DeepFM
  * About DeepFM algorithm itself, please refer to the corresponding papers or tutorials. What can be easily explained here is that in DeepFM, there are 2 parts which are deep part (generalization ability is good) and FM part (can be regarded as the substitution of the wide part in Wide&Deep network. FM part is here to learn the feature interactions). 
  * DeepFM code is in `DeepFM-Test.ipynb`. In this code, there are some cells that can plot the Keras models. To be noted that you will have to install some libraries in advance. But in fact I found that the Keras-generated plot is hard to read, so I use the draw.io to redraw the plot `DeepFMArchitecture.drawio` which is clearer to understand. 

* NeuralCF-Test
  * This is another model widely used for recommendation system. CF means collaborative filtering, which is a traditional recommendation algorithm. And the Neural means that the CF is updated with deep learning techniques. 
  * This method is in `NeuralCF-Test.ipynb`. 
  * This algorithm has a unique trait comparing with DeepFM one. NeuralCF algorithm in the code only needs the input of user IDs and movie IDs, which will be super easy for doing inference. You can imagine that when you want to learn whether a user will like a movie he never watched before, and you decide to use DeepFM, some of the user-movie-related features have to be calculated from the scratch, which takes time. But if you use neuralCF instead, you don't need to calculate those features, because just the user ID and new movie ID will be enough. 

## Business logic

This part is mainly implemented with Java. So you can see how Java can be used in recommended system. How widely it can be used. 

The code is mainly under `SparrowRecSys/NewCode/JavaPart/src/main/java/`. From file `src\main\java\com\system\online\SystemServer.java` , you go to a folder `src\main\java\com\system\online\service` and find corresponding service files. From service files you go one step further to process files in folder `src\main\java\com\system\online\recprocess` . 

You will have to run the file `src\main\java\com\system\online\SystemServer.java` to start the website service first. 

The most important business logic consists of 2 parts: recommending for movies and recommending for users. 

* In the first part **recommended for movies**, users will see what movies are similar to the current movie. In a movie page, for example, those recommended movies will be put in areas like "similar movies". 

  * The service file is `service/SimilarMovieService.java`. And in `recprocess/SimilarMovieProcess.java` , the main logic of finding most related movies can be found.
  * The main process of finding a limited number of similar movies is described as following: 
    * Roughly filter some similar movies, like getting all of the movies that share same genres with target movie (the movie that similar movies are found for). This step will find a lot of candidate movies. 
    * Then use the similarity (e.g., cosine similarity) between embeddings of candidate movies and target movie to filter again, to get a limited number of similar movies. 
  * IF you want to use new embedding results to do similar movie recommendation, you have to change some code in the `SimilarMovieService.java` to load the embedding results you want. The code looks like `DataManager.getInstance().loadData(<parameters>);`. 
  * The URL should be `http://localhost:6010/getsimilarmovie?movieId=300&size=16&model=emb`, to get similar movie recommendations for movie No. `300`, and `16` recommendations will be provided. As for the `model=emb` part, it means that how the similarity of movies will be calculated and when set like this, the similarity of embedding will be the similarity indicator. You can also use some other similarity criteria like [local sensitive hashing](https://en.wikipedia.org/wiki/Locality-sensitive_hashing). 

* In the second part **recommended for users**, users will be recommended some movies based on features related to themselves and movies. The recommended movies are like "The movie you may like". 

  * The service file is `service\RecForYouService.java`, the process file is `recprocess/RecForYouProcess.java`.  

  * The main recommendation process is described as follow:

    * Roughly filter some similar movies as candidate movies. 
    * Calculate the features of target user (the users that movies are recommended for) and one candidate movie. If the user didn't watch the movie before, then the features may need to be calculated from the scratch. For example, some features are calculated based on timestamp like blablabla feature means before watching this movie, the watcher (or user) did what or was like what. So when trying to predict whether a user will like a movie or not, an imagination timestamp will be generated, generally speaking it should be the timestamp now, which means we pretend that he or she will watch the movie now, and before watch this movie, he did what or was what. So that's the basic logic of generating features for a user and a candidate movie that he or she never watched before. 
      * To be noted that the new feature calculation logic for DeepFM models are written in Scala in file `src\main\java\DeepFMFeatureEng.scala`, but I currently don't find a way to make it run in Java settings. So currently the DeepFM model doesn't work at all. 
    * Send the calculated features to a served ML model and get the predictions back. The predictions will be the indicator of how much a user like a candidate movie. 
    * And the candidate movies that have the highest prediction value will be recommended to the user.   

  * In `RecForYouProcess.java` file, you will find `public static List<Movie> ranker(User user, List<Movie> candidates, String model)`, in this function, you can add new recommendation models in the `switch` part. Currently it only has `neuralcf` as a deep learning-based recommendation method. 

  * In order to make the this recommendation work, the trained DL models should be served. 

    * The trained and saved deep learning-based models is recommended to be put under `src\main\resources\webroot\modeldata` this folder, for the convenience of management. 

    * Run docker commands:

      * `docker pull tensorflow/serving` if you never download this docker image before. 

      * ```
        docker run -t --rm -p 8501:8501 
        -v "/mnt/d/MachineLearningPractice/SparrowRecSys/NewCode/JavaPart/src/main/resources/webroot/modeldata/neuralcf:/models/recmodel" 
        -e MODEL_NAME=recmodel tensorflow/serving &
        ```

      * Mind that the previous docker command needs the docker service to be run in advance. 

  * The URL of getting the movie recommendation is like this `http://localhost:6010/getrecforyou?id=678&size=32&model=emb` .  The id number is the user ID, and `model` should be set as the DL model you served. If you keep using `emb`, it will be general embedding-based recommendation, rather than DL-based. The implemented DL model should be `neuralcf`. 



## # 2020年1月8日

The `JavaPart_bak.zip` is a back-up file. If you change something and cannot reverse the changes, you'd better turn to this zip file to restore your changes. 