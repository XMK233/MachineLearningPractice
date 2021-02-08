## script version of 1-xxx.ipynb
import csv
import redis

r = redis.StrictRedis(host='localhost', port=6379) # , db=1, password='123456'

movieFilePath = r"D:/MachineLearningPractice/SparrowRecSys/NewCode/JavaPart/src/main/resources/webroot/sampledata/movies.csv"
ratingFilePath = r"D:/MachineLearningPractice/SparrowRecSys/NewCode/JavaPart/src/main/resources/webroot/sampledata/ratings.csv"

with open(movieFilePath, 'rt', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        movieId = row['movieId']
        title = row['title']
        genres = row["genres"]
#         r.delete(f"movie_{movieId}")
        r.set(
            "movie-{}".format(movieId), str({"title": title, "genres": genres})
        ) ## 字典转为str存储

with open(ratingFilePath, 'rt', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        userId = row['userId']
        movieId = row['movieId']
        rating = row['rating']
        timestamp = row["timestamp"]
        r.set(
            "rating-user_{}-movie_{}".format(userId, movieId), str({"rating": rating, "timestamp": timestamp}) 
        ) ## 字典转为str存储
## 大概要两三分钟的时间, 我等了一下, 然后中途吃了点东西, 回来又等了一会, 才完事儿. 