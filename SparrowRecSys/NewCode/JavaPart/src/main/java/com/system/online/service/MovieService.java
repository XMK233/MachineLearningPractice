package com.system.online.service;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.system.online.datamanager.DataManager;
import com.system.online.datamanager.Movie;

import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;

/**
 * MovieService, return information of a specific movie
 */

public class MovieService extends HttpServlet {
    protected void doGet(HttpServletRequest request,
                         HttpServletResponse response) throws IOException {
        try {
            response.setContentType("application/json");
            response.setStatus(HttpServletResponse.SC_OK);
            response.setCharacterEncoding("UTF-8");
            response.setHeader("Access-Control-Allow-Origin", "*");

            //get movie id via url parameter
            // URL is like this: http://localhost:6010/getmovie?id=798
            String movieId = request.getParameter("id");

            //get movie object from DataManager
            // DataManager is a singleton.
            Movie movie = DataManager.getInstance().getMovieById(Integer.parseInt(movieId));
            System.out.println(movie);

            //convert movie object to json format and return
            if (movie != null) {
                // change the movie object into json object.
                ObjectMapper mapper = new ObjectMapper();
                String jsonMovie = mapper.writeValueAsString(movie);
                //return the json object.
                response.getWriter().println(jsonMovie);
            }else {
                response.getWriter().println("");
            }

        } catch (Exception e) {
            e.printStackTrace();
            response.getWriter().println("");
        }
    }
}
