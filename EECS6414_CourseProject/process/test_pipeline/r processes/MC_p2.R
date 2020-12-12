################
#MC1_2
################################
reject_vars <- c(
  'top_tco', #'top_rso', 
  'top_iso', 'contributor', 'commentor', 'author', 'churn', 'nnn' #, 'integrator'
)#
env_vars <- env_vars[!(env_vars %in% reject_vars)]

red <- redun(~., data[,env_vars], nk=0)
redun_vars <- red$Out
env_vars <- env_vars[!(env_vars %in% redun_vars)]

data1 = data[, c(env_vars, c("status"))]

sink("D:\\Users\\XMK1\\Desktop\\analysis result\\elasticsearch\\Documents.txt")
cat(c("-------------7 kinds of data in total-----------------\n\n"))
cat(c("1. correlated variables: ", reject_vars))
cat("\n\n")
cat(c("2. redundant variables: ", redun_vars))


# documents_txt <- file("D:\\Users\\XMK1\\Desktop\\Documents.txt", "w")
# write(c(reject_vars, c("\n"), redun_vars), documents_txt)
# close(documents_txt)

####################
#MC2
####################
budgetted_DF = floor(min(nrow(data1[data1$status == "True",]), nrow(data1[data1$status == "False",]) )/10)#change the /15 to /10
cat("\n\n")
cat(c("3. budgeted_DF: ", budgetted_DF))
cat("\n\n")
cat(c("4. allocation of degree of freedom: "))
cat("\n\n")
cat("5, 6, 7 are as follow: \n")
sink()

sp <- spearman2(formula(paste("status" ," ~ ",paste0(env_vars, collapse=" + "))), data= data1, p=2)
pdf(file="D:\\Users\\XMK1\\Desktop\\analysis result\\elasticsearch\\rou2.pdf", 
    width = 11, height = 8.5)
plot(sp)
dev.off()
plot(sp)

####################
#MC3_1
####################
cat(c("remaining variables: \n"))
for (i in env_vars){
  cat(c(i, "+ \n"))
}
