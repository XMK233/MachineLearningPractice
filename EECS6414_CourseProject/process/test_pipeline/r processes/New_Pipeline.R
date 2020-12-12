#library(randomForest)
library(rms)
data <- read.csv('kernel_competition_author.csv')# , stringsAsFactors=FALSE
# print(
# 
#         #"cmp_tier unique: ", 
#     unique(data["cmp_tier"])
# )
# print(
# 
#         #"scpt_tier unique: ", 
#         unique(data["scpt_tier"])
# 
# )
# print(
# 
#         #"dsc_tier unique: ", 
#         unique(data["dsc_tier"])
# 
# )
# data[data=="novice"] <- 1
# data[data=="contributor"] <- 2
# data[data=="expert"] <- 3
# data[data=="master"] <- 4
# data[data=="grandmaster"] <- 5

col_name <- names(data)
env_vars <- col_name
reject_vars <- c("kernel_datasets", # because they are all 1, so we can only get NaN. 
                 "kernel", "author", "competition", "organization" # unnecessary variables. 
                 )
env_vars <- env_vars[!(env_vars %in% reject_vars)]
# for (env in env_vars){
#    print(paste(env, "+"))
# }

vcobj = varclus(~ 
                kernel_versions +
                forks +
                comments +
                views +
                size +
                competition_discussion +
                competitors +
                competition_kernels +
                author_competitions +
                cmp_tier +
                author_kernels +
                scpt_tier +
                author_discussions +
                dsc_tier +
                author_followers +
                author_following,
                
                data = data, 
                
                similarity = "spearman",
                
                trans = "abs"
)

pdf(file="correlation.pdf", width = 11, height = 8.5)
plot(vcobj)
thresh = 0.8
abline (h = 1 - thresh, col = "red", lty = 2)
dev.off()

plot(vcobj)
thresh = 0.8
abline (h = 1 - thresh, col = "red", lty = 2)

# reject variables that closely related to each other. For now, we don't do this thing. 
reject_vars <- c()
env_vars <- env_vars[!(env_vars %in% reject_vars)]
data_lean = data[env_vars]




