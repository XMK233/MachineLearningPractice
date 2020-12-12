Sys.setlocale("LC_ALL","Chinese")
#Load RMS package
library(rms)
data <- read.csv('D:\\Users\\XMK1\\Desktop\\data clean\\elasticsearch\\result.csv') 
dir.create('D:\\Users\\XMK1\\Desktop\\analysis result\\elasticsearch')

names(data)<-c("module", "contributor", "author", "commentor"
               , "integrator" , "churn", "entropy", "size", "jjj" # 
               , "jnj", "njj", "nnj"
               , "jjn", "jnn", "njn", "nnn"
               , "top_iso", "top_rso", "top_tco", "status")
#data = data[,-1]
env_vars = c('contributor', 'author', 'commentor'
             ,'integrator', 'churn', 'entropy', 'size', 'jjj' #
             , 'jnj', 'njj', 'nnj'
             , 'jjn', 'jnn', 'njn', 'nnn'
             , 'top_iso', 'top_rso', 'top_tco')
dd <- datadist(data[,c(env_vars,'status')])
options(datadist = "dd")
##############################
#MC1_1
##############################
#Calculate spearman's correlation between independent variables
vcobj = varclus(~ contributor + author + commentor
                + integrator + churn + entropy + size + jjj#
                + jnj + njj + nnj
                + jjn + jnn + njn + nnn
                + top_iso + top_rso + top_tco,
                data = data, 
                similarity = "spearman",
                trans = "abs"
)
#Plot hierarchical clusters and the spearman's correlation threshold of 0.7
pdf(file="D:\\Users\\XMK1\\Desktop\\analysis result\\elasticsearch\\correlation.pdf", width = 11, height = 8.5)
plot(vcobj)
thresh = 0.7
abline (h = 1 - thresh, col = "red", lty = 2)
dev.off()

#############################

plot(vcobj)
thresh = 0.7
abline (h = 1 - thresh, col = "red", lty = 2)
#Remove the highly correlated variable from the hierarchical clusters 
#repeat this procedure if necessary