####################
#MA1
####################
val <- validate(fit, B=1000)
AUC = 0.5 + val[1,1]/2
AUC_optimism_reduced = (0.5 + val[1,5]/2)
AUC_optimism = AUC - AUC_optimism_reduced
print(c("AUC"=AUC,"AUC_optimism"=AUC_optimism))
write.csv(c("AUC"=AUC,"AUC_optimism"=AUC_optimism),file="D:\\Users\\XMK1\\Desktop\\analysis result\\elasticsearch\\AUC.csv",quote=F,row.names = T)

####################
#MA2
####################
explantory_power = anova(fit,test='Chisq')
print(explantory_power)
pdf(file="D:\\Users\\XMK1\\Desktop\\analysis result\\elasticsearch\\chi2_and_pValue.pdf", width = 11, height = 8.5)
plot(explantory_power)
dev.off()
plot(explantory_power)
write.csv(explantory_power,file="D:\\Users\\XMK1\\Desktop\\analysis result\\elasticsearch\\explanatory_power.csv",quote=F,row.names = T)
file.create("D:\\Users\\XMK1\\Desktop\\analysis result\\elasticsearch\\chi.txt") 
####################
#MA3
####################
patial_effect = summary(fit)#partial effect
print(patial_effect)
write.csv(patial_effect,file="D:\\Users\\XMK1\\Desktop\\analysis result\\elasticsearch\\partial_effect.csv",quote=F,row.names = T)
file.create("D:\\Users\\XMK1\\Desktop\\analysis result\\elasticsearch\\odds.txt") 

# predict <- Predict(fit,p5,fun=function(x)exp(x))
# plot(predict, ylab='Odds')
# plot(predict, ylab='Odds')