library(caret)
library(randomForest)
library(dplyr)

rev_loggy_df <- read.csv(file = "Heng_JIT_hadoop.csv",header=FALSE, sep=",")
names(rev_loggy_df) <- c("rev","log_num","log_den","avg_log_len","avg_log_level","avg_log_var",
                          "sloc", "codechurn_hist","class_num", "method_num", "catch_num", "throws_num",
                          "if_num", "else_num", "for_num", "while_num", "commit_type", "log_modified")

rev_loggy_df$log_modified = as.factor(rev_loggy_df$log_modified)


inTrain <- c(1:50)
training <- rev_loggy_df[inTrain, ]
testing <- rev_loggy_df[c(51), ]
# up_train <- upSample(x=training[, -ncol(training)], y = training$log_modified)
rf <- randomForest(log_modified ~. -rev, data=training)
pred <- predict(rf, testing)#,type="prob")
testing$log_modified


table(observed = testing[,"log_modified"], predicted = pred)
a = c()
for (i in 50:nrow(rev_loggy_df)-1) {
  # print (i)
  b <- predict_use_history(rev_loggy_df, c(1:i), c(i+1))
  a <- c(a,b)
}
a = as.factor(a)
summary(a)

write.csv(a, file="test")

heng_rev_loggy_df$log_modified <- as.factor(heng_rev_loggy_df$log_modified)
a <- predict_use_history(heng_rev_loggy_df, c(1:50), c(51))

predict_use_history = function(dataf, inTrain, test) {
  training <- dataf[inTrain, ]
  testing <- dataf[test, ]
  rf <- randomForest(log_modified ~. -rev, data=training)
  pred <- predict(rf, testing)
  if (pred =="true")
    return (1)
  else
    return (0)
  #print(pred)
  # if (pred == testing$log_modified && pred == "TRUE") {
  #   return ("TP");
  # } 
  # if (pred == testing$log_modified && pred == "FALSE") {
  #   return ("TN");
  # }
  # if (pred != testing$log_modified && pred == "TRUE") {
  #   return ("FP");
  # }
  # if (pred != testing$log_modified && pred == "FALSE") {
  #   return ("FN");
  # }
}

0.5 * sum(a == "TP") / (sum(a == "TP") + sum(a == "FN")) + 0.5 * (sum(a == "TN") / (sum(a == "FP") + sum(a == "TN")))

heng_rev_loggy_df <- read.csv(file="Hadoop.csv", header=TRUE, sep=",")
heng_rev_loggy_df$log_modified <- heng_rev_loggy_df$log_modified > 0
heng_rev_loggy_df$log_modified = as.factor(heng_rev_loggy_df$log_modified)

a = c()
for (i in (nrow(heng_rev_loggy_df)-50): 2) {
  # print (i)
  b <- predict_heng_use_history(heng_rev_loggy_df, c(i:nrow(heng_rev_loggy_df)), c(i-1))
  a <- c(a,b)
}
a = as.factor(a)
summary(a)

predict_heng_use_history = function(dataf, inTrain, test) {
  training <- dataf[inTrain, ]
  testing <- dataf[test, ]
  rf <- randomForest(log_modified ~. -revision -log_churn -log_added -log_deleted, data=training)
  pred <- predict(rf, testing)
  # if (pred =="true")
  #   return (1)
  # else
  #   return (0)
  print(test)
  if (pred == testing$log_modified && pred == "TRUE") {
    return ("TP");
  }
  if (pred == testing$log_modified && pred == "FALSE") {
    return ("TN");
  }
  if (pred != testing$log_modified && pred == "TRUE") {
    return ("FP");
  }
  if (pred != testing$log_modified && pred == "FALSE") {
    return ("FN");
  }
}

# inTrain <- c(1:as.integer(nrow(heng_rev_loggy_df) * 0.9))
# training <- heng_rev_loggy_df[inTrain, ]
# testing <- heng_rev_loggy_df[-inTrain, ]
# # up_train <- upSample(x=training[, -ncol(training)], y = training$log_modified)
# rf <- randomForest(log_modified ~. -revision -log_churn -log_added -log_deleted, data=training)
# pred <- predict(rf, testing)#,type="prob")
# table(observed = testing[,"log_modified"], predicted = pred)
