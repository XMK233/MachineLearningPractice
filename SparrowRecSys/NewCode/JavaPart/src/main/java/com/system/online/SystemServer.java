package com.system.online;

import java.net.InetSocketAddress;
import java.net.URI;
import java.net.URL;

import com.system.online.datamanager.DataManager;
import com.system.online.service.*;
import org.eclipse.jetty.server.Server;
import org.eclipse.jetty.servlet.DefaultServlet;
import org.eclipse.jetty.servlet.ServletContextHandler;
import org.eclipse.jetty.servlet.ServletHolder;
import org.eclipse.jetty.util.resource.Resource;
import java.net.InetSocketAddress;
import java.net.URI;
import java.net.URL;

public class SystemServer {

    public static void main(String[] args) throws Exception {
        new SystemServer().run();
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
        DataManager.getInstance().loadData(webRootUri.getPath() + "sampledata/movies.csv",
                webRootUri.getPath() + "sampledata/links.csv",webRootUri.getPath() + "sampledata/ratings.csv",
                webRootUri.getPath() + "modeldata/item2vecEmb.csv", // "modeldata/img2vecEmb.csv", //"modeldata/DeepWalkEmb.csv", //"modeldata/item2vecEmb.csv",
                webRootUri.getPath() + "modeldata/userEmb.csv",
                "img2vecEmb", //"i2vEmb",
                "uEmb");

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
