package com.system.online;

import java.lang.reflect.Array;
import java.net.InetSocketAddress;
import java.net.URI;
import java.net.URL;

import com.system.online.datamanager.DataManager;
import com.system.online.recprocess.RecForYouProcess;
import com.system.online.service.*;
import org.apache.flink.api.java.DataSet;
import org.apache.spark.sql.*;
import org.eclipse.jetty.server.Server;
import org.eclipse.jetty.servlet.DefaultServlet;
import org.eclipse.jetty.servlet.ServletContextHandler;
import org.eclipse.jetty.servlet.ServletHolder;
import org.eclipse.jetty.util.resource.Resource;
import java.net.InetSocketAddress;
import java.net.URI;
import java.net.URL;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Date;
import java.util.Map;

import com.system.online.scalaFeatureEngineering.*;
import org.json.JSONArray;
import org.json.JSONObject;

import java.util.List;

import org.apache.spark.SparkConf;
import org.apache.spark.api.java.JavaSparkContext;
import org.apache.spark.sql.RowFactory;
import org.apache.spark.api.java.JavaRDD;

import static com.system.online.util.HttpClient.asyncSinglePostRequest;
///////////////////////////////////////////
import com.system.online.datamanager.RedisClient;
import redis.clients.jedis.Jedis;
import java.io.Serializable;


class RatingTmp implements Serializable {
    private String userId;
    private String movieId;
    private String rating;
    private String timestamp;
    public RatingTmp(String userId, String movieId, String rating, String timestamp){
        this.userId = userId;
        this.movieId = movieId;
        this.rating = rating;
        this.timestamp = timestamp;
    }
}

class MovieTmp implements Serializable {
    private String movieId;
    private String title;
    private String genres;
    public MovieTmp(String movieId, String title, String genres){
        this.movieId = movieId;
        this.title = title;
        this.genres = genres;
    }
}

public class SystemServer {
    // https://timepasstechies.com/create-spark-dataframe-java-list/ 不会出错, 但是没用.

    public static void callDeepFMTFServing_easy(String userId, String movieId, SparkSession spark, SQLContext sqc){
        Jedis redisClient = RedisClient.getInstance();
        int haveRecord = 0;
        for (String key : redisClient.keys("rating-user_" + userId + "-*")){
            String mid = key.split("-")[2].split("_")[1];
            // System.out.println(mid);
            if (mid.equals(movieId)){
                haveRecord = 1;
            }
            String rating =  redisClient.hget(key, "rating");
            String timestamp =  redisClient.hget(key, "timestamp");
        }
    }
    public static void main(String[] args) throws Exception {
        new SystemServer().run();
        //////////////////////////////////////////
//        SparkSession spark = SparkSession.builder().master("local").appName("featureEngineering").getOrCreate();
//        SparkConf conf = new SparkConf().setAppName("SparkSample").setMaster("local[*]");
//        JavaSparkContext jsc = new JavaSparkContext(conf);
//        SQLContext sqc = new SQLContext(jsc);
//        SystemServer.callDeepFMTFServing_easy("1", "567", spark, sqc);
    }

    //recsys server port number
    private static final int DEFAULT_PORT = 6010;

    public void run() throws Exception{

        int port = DEFAULT_PORT;

        // 这句话干什么的? 有点多余, 要不先给它注释掉.
//        try {
//            port = Integer.parseInt(System.getenv("PORT"));
//        } catch (NumberFormatException ignored) {}

        //set ip and port number
//        InetSocketAddress inetAddress = new InetSocketAddress("0.0.0.0", port);
//        Server server = new Server(inetAddress);
        InetSocketAddress inetAddress = new InetSocketAddress("localhost", port);
        Server server = new Server(inetAddress);

        //get index.html path
        URL webRootLocation = this.getClass().getResource("/webroot/index.html");
        if (webRootLocation == null)
        {
            throw new IllegalStateException("Unable to determine webroot URL location");
        }

        //set index.html as the root page
        URI webRootUri = URI.create(webRootLocation.toURI().toASCIIString().replaceFirst("/index.html$","/"));
        System.out.printf("Web Root URI: %s%n", webRootUri.getPath());

        //load all the data to DataManager
        DataManager.getInstance().loadData(
                webRootUri.getPath() + "sampledata/movies.csv",
                webRootUri.getPath() + "sampledata/links.csv",
                webRootUri.getPath() + "sampledata/ratings.csv",
                webRootUri.getPath() + "modeldata/PosterFeatureVector.csv", //"modeldata/PosterFeatureVector.csv", // "modeldata/img2vecEmb.csv", //"modeldata/DeepWalkEmb.csv", //"modeldata/item2vecEmb.csv", //"modeldata/item2vecEmb_xmk.csv",
                webRootUri.getPath() + "modeldata/userEmb_xmk.csv",
                "img2vecEmb", //"i2vEmb",
                "uEmb"
        );

        //create server context
        ServletContextHandler context = new ServletContextHandler();
        context.setContextPath("/");
        context.setBaseResource(Resource.newResource(webRootUri));
        context.setWelcomeFiles(new String[] { "index.html" });
        context.getMimeTypes().addMimeMapping("txt","text/plain;charset=utf-8");

        //bind services with different servlets
        context.addServlet(DefaultServlet.class,"/");
        // add API: getMovie, to get movie-related data.
        context.addServlet(new ServletHolder(new MovieService()), "/getmovie");
        // add API: getUser, to get user-related data
        context.addServlet(new ServletHolder(new UserService()), "/getuser");
        // add API: getSimilarMovie, to get similar movies recommendation
        context.addServlet(new ServletHolder(new SimilarMovieService()), "/getsimilarmovie");
        // add new API to get recommended movies in different types.
        context.addServlet(new ServletHolder(new RecommendationService()), "/getrecommendation");
        // add new API to get a recommendataion for you.
        context.addServlet(new ServletHolder(new RecForYouService()), "/getrecforyou");

        //set url handler. Set Jetty environmental handler
        server.setHandler(context);
        System.out.println("Recommendation system Server has started....You can use it now");

        //start Jetty Server
        server.start();
        server.join();
    }
}
