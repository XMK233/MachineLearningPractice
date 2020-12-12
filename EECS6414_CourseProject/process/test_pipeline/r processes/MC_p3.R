####################
#MC3_3
####################
fit <- lrm(status ~ 
             rcs(integrator, 5) + 
             entropy + 
             size + 
             rcs(jjj, 3) + 
             rcs(jnj, 5) + 
             rcs(njj, 5) + 
             rcs(nnj, 5) + 
             jjn + 
             jnn + 
             njn + 
             top_rso
           ,
           data=data1, x=T, y=T)
cat("Don't forget to record the 4th kind of data\n")
